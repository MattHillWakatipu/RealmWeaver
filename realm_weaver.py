import logging
import os
import openai
import weaviate
from dotenv import load_dotenv

COMPLETION_MODEL = 'gpt-3.5-turbo'
EMBEDDING_MODEL = 'text-embedding-ada-002'


def fetch_related(user_string, n=2):
    """
    Fetch N-nearest lore snippets to the input user string

    :param user_string:     The user's input string.
    :param n:               The number of lore snippets to add, defaults to 2.
    :return:                A string containing the related context for the N-nearest lore snippets in Weaviate.
    """
    # Construct a list of topics to enhance linking
    concepts = {'concepts': construct_background_prompt(user_string)}

    # Fetch related items from Weaviate
    logging.info(f'Fetching {n} closest related items from Weaviate...')
    response = (
        weaviate_client.query
        .get('Lore', ['lore', 'category'])
        .with_near_text(concepts)
        .with_limit(n)
        .do()
    )
    logging.info('Retrieved related content from Weaviate.')

    # Extract information from response and construct result
    result = 'Context:\n'
    for i in range(n):
        result += response['data']['Get']['Lore'][i]['lore'] + '\n'

    logging.debug(f'{n} closest items retrieved from Weaviate:\n{result}')
    return result


def construct_background_prompt(user_string):
    """
    TODO

    :param user_string: TODO
    :return: TODO
    """
    # TODO work out which one to use
    # query = 'In one sentence provide a category of background knowledge ' \
    #         'that would be beneficial for the following worldbuilding query:\n' \
    #         + user_string
    query = 'In one sentence construct a list of five or fewer topics ' \
            'that would be beneficial for the following worldbuilding query:\n' \
            + user_string

    logging.info('Constructing background information prompt...')
    completion = openai.ChatCompletion.create(
        model=COMPLETION_MODEL,
        messages=[
            {"role": "user", "content": query}
        ]
    )

    background_info = completion.choices[0].message.content
    logging.info(f'Background information prompt constructed.')
    logging.info(f'Prompt: {background_info}')
    return background_info


def store_response(response):
    """
    Store the Model's response in the Weaviate Cluster.

    :param response:    The Model response to store.
    :return:            None.
    """
    # TODO chunk response

    formatted = format_response(response)

    logging.info('Storing Lore object in Weaviate Cluster...')
    with weaviate_client.batch as batch:
        batch.add_data_object(formatted, 'Lore')
        logging.info('Successfully stored Lore object in Weaviate Cluster.')


def format_response(lore):
    """
    Format a Lore object, assigns a category for the lore with GPT-4.

    :param lore:    The input lore snippet.
    :return:        A lore snippet formatted as a dictionary, ready to be saved to Weaviate.
    """
    # Query to categorize the lore snippet
    # TODO adding more categories to examples could be beneficial
    query = 'Assign a Category to this Worldbuilding text: eg.(Cities, Regions, Culture etc.)\n' + lore

    # Query the model
    logging.info('Assigning a category to response...')
    completion = openai.ChatCompletion.create(
        model=COMPLETION_MODEL,
        messages=[
            {"role": "user", "content": query}
        ]
    )
    category = completion.choices[0].message.content
    logging.info('Category assigned to response.')
    logging.info(f'Category: {category}')

    # Formatted as a Dictionary to store
    formatted = {"category": category,
                 "lore": lore}
    logging.debug(f'formatted: {formatted}')

    return formatted


def main():
    # The worldbuilding header
    # TODO this should be defined somewhere during an initialisation process and should probably not change per project.
    header = 'Background:\n' \
             'I am doing some worldbuilding for a fantasy novel.\n' \
             'The setting is inspired by New Zealand, featuring elemental magic and political intrigue.\n' \
             '************\n'
    logging.debug(f'Worldbuilding header:\n{header}')

    # TODO dynamic input from user
    user_string = 'Create an important historical event for me.'
    logging.info(f'User input string: {user_string}')

    instructions = 'Instructions:\n' \
                   f'{user_string}\n' \
                   '************\n'

    # Get releated context based on the users input string
    context = fetch_related(user_string)

    # Construct the final query based on the Header, Instructions and Weaviate related context
    query = header + instructions + context
    logging.debug(f'Full query to GPT-4:\n')

    # Query the model
    logging.info('Querying GPT-4 with additional context from Weaviate...')
    completion = openai.ChatCompletion.create(
        model=COMPLETION_MODEL,
        messages=[
            {"role": "user", "content": query}
        ]
    )
    logging.info(f'Response received from GPT-4.')
    response = completion.choices[0].message.content

    # TODO Send response to user, and get user input of whether to save or not
    print(f'Response: {response}')

    # Store the response in Weaviate cluster
    store_response(response)


def create_weaviate_client():
    """
    Create a Weaviate client.

    :return:    The Weaviate client.
    """
    logging.info('Creating Weaviate client...')
    client = weaviate.Client(
        url=os.getenv('WEAVIATE_URL'),
        auth_client_secret=weaviate.auth.AuthApiKey(api_key=os.getenv('WEAVIATE_API_KEY')),
        additional_headers={
            'X-OpenAI-Api-Key': os.getenv('OPENAI_API_KEY')
        }
    )
    logging.info('Successfully created Weaviate client.')
    return client


if __name__ == '__main__':
    load_dotenv()
    openai.api_key = os.getenv('OPENAI_API_KEY')

    # Configure logging
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    # FIXME Socket not closing for whatever reason, doesn't seem to matter if this is global or within a function.
    #  Doesn't occur in weaviate_setup.py, could be because that is a script with no function calls but not sure.
    #  Doesn't seem very critical anyway as this will only be done once.
    weaviate_client = create_weaviate_client()

    main()
