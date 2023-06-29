import logging
import os
import openai
import weaviate
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter

COMPLETION_MODEL = 'gpt-4'
EMBEDDING_MODEL = 'text-embedding-ada-002'


def fetch_related(weaviate_client, user_string, n=4):
    """
    Fetch N-nearest lore snippets to the input user string

    :param weaviate_client:
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
    result = ''
    for i in range(n):
        result += '* ' + response['data']['Get']['Lore'][i]['lore'] + '\n'

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


def confirm_save():
    # FIXME this is real ugly and will break the web version
    user_input = input("Do you want to save? (Y/N): ")

    if user_input.lower() == "y" or user_input.lower() == 'yes':
        logging.info('Saving data...')
        return True
    elif user_input.lower() == "n" or user_input.lower() == 'no':
        return False
    else:
        logging.info('Invalid input.')
        return False


def store_response(weaviate_client, response):
    """
    Store the Model's response in the Weaviate Cluster.

    :param weaviate_client:
    :param response:    The Model response to store.
    :return:            None.
    """
    # Format the response
    formatted = format_response(response)

    # Store in Weaviate Cluster
    logging.info('Storing response in Weaviate Cluster...')
    with weaviate_client.batch as batch:
        batch.add_data_object(formatted, 'Lore')
        logging.info('Successfully stored response in Weaviate Cluster.')


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
    logging.info(f'Assigning a category to response...')
    completion = openai.ChatCompletion.create(
        model=COMPLETION_MODEL,
        messages=[
            {"role": "user", "content": query}
        ]
    )
    category = completion.choices[0].message.content
    logging.info(f'Category assigned to response.')
    logging.info(f'Category: {category}')

    # Formatted as a Dictionary to store
    formatted = {"category": category,
                 "lore": lore}
    logging.debug(f'formatted: {formatted}')

    return formatted


def main(user_string='Create an important historical event for me.'):
    load_dotenv()
    openai.api_key = os.getenv('OPENAI_API_KEY')

    # Configure logging
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    # FIXME Socket not closing for whatever reason, doesn't seem to matter if this is global or within a function.
    #  Doesn't occur in weaviate_setup.py, could be because that is a script with no function calls but not sure.
    #  Doesn't seem very critical anyway as this will only be done once.
    weaviate_client = create_weaviate_client()

    # The worldbuilding header
    # TODO this should be defined somewhere during an initialisation process and should probably not change per project.
    header = 'Background:\n' \
             'I am doing some worldbuilding for a fantasy novel.\n' \
             'The setting is inspired by New Zealand, featuring elemental magic and political intrigue.\n' \
             '************\n'
    logging.debug(f'Worldbuilding header:\n{header}')

    # TODO dynamic input from user

    logging.info(f'User input string: {user_string}')

    # Get related context based on the users input string
    context = 'Background:\n' \
              f'{fetch_related(weaviate_client, user_string)}' \
              f'************\n'

    instructions = 'Instructions:\n' \
                   'Using the background as either example or ' \
                   'by directly linking to it, complete the following instruction.\n' \
                   f'{user_string}\n' \
                   '************\n'

    # Construct the final query based on the Header, Instructions and Weaviate related context
    query = header + context + instructions
    logging.debug(f'Full query to GPT-4:\n{query}')

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

    if confirm_save():
        # Store the response in Weaviate cluster
        store_response(weaviate_client, response)

    return response


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
    main()
