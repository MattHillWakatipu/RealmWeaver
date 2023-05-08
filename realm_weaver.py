import os
import openai
import weaviate
from dotenv import load_dotenv

COMPLETION_MODEL = 'gpt-4'
EMBEDDING_MODEL = 'text-embedding-ada-002'


def fetch_related(user_string):
    """
    Fetch N-nearest lore snippets to the input user string

    :param user_string:     The user's input string.
    :return:                A string containing the related context for the N-nearest lore snippets in Weaviate.
    """
    query = 'In one sentence provide a category of background knowledge ' \
            'that would be beneficial for the following worldbuilding query:\n' \
            + user_string

    completion = openai.ChatCompletion.create(
        model=COMPLETION_MODEL,
        messages=[
            {"role": "user", "content": query}
        ]
    )

    concepts = completion.choices[0].message.content

    print(f'concepts: {concepts}')

    near_text = {'concepts': concepts}

    response = (
        weaviate_client.query
        .get('Lore', ['lore', 'category'])
        .with_near_text(near_text)
        .with_limit(2)
        .do()
    )

    result = 'Context:\n'

    # Extract information from response
    result += response['data']['Get']['Lore'][0]['lore'] + '\n'
    result += response['data']['Get']['Lore'][1]['lore']

    return result


def store_response(response):
    """
    Store the Model's response in the Weaviate Cluster.

    :param response:    The Model response to store.
    :return:            None.
    """
    formatted = format_response(response)

    print(f'formatted: {formatted}')

    with weaviate_client.batch as batch:
        batch.add_data_object(formatted, 'Lore')


def format_response(lore):
    """
    Format a Lore object, assigns a category for the lore with GPT-4.

    :param lore:    The input lore snipppet.
    :return:        A lore snippet formatted as a dictionary, ready to be saved to Weaviate.
    """
    query = 'Assign a Category to this Worldbuilding text: eg.(Cities, Regions, Culture etc.)\n' + lore

    completion = openai.ChatCompletion.create(
        model=COMPLETION_MODEL,
        messages=[
            {"role": "user", "content": query}
        ]
    )

    category = completion.choices[0].message.content

    formatted = {"category": category,
                 "lore": lore}

    return formatted


def main():
    user_string = 'create an important historical event for me.'

    header = 'Background:\n' \
             'I am doing some worldbuilding for a fantasy novel.\n' \
             'The setting is inspired by New Zealand, featuring elemental magic and political intrigue.\n' \
             '************\n'

    instructions = 'Instructions:\n' \
                   f'In one paragraph {user_string}\n' \
                   '************\n'

    context = fetch_related(user_string)

    query = header + instructions + context

    completion = openai.ChatCompletion.create(
        model=COMPLETION_MODEL,
        messages=[
            {"role": "user", "content": query}
        ]
    )

    response = completion.choices[0].message.content

    print(f'Query: {query}')
    print(f'Response: {response}')

    store_response(response)


def create_weaviate_client():
    """
    Create a Weaviate client.

    :return:    The Weaviate client.
    """
    return weaviate.Client(
        url='https://realm-weaver-f5qsqrbe.weaviate.network',
        auth_client_secret=weaviate.auth.AuthApiKey(api_key=os.getenv('WEAVIATE_API_KEY')),
        additional_headers={
            'X-OpenAI-Api-Key': os.getenv('OPENAI_API_KEY')
        }
    )


if __name__ == '__main__':
    load_dotenv()
    openai.api_key = os.getenv('OPENAI_API_KEY')

    # FIXME Socket not closing for whatever reason, doesn't seem to matter if this is global or within a function.
    #  Doesn't occur in weaviate_test.py, could be because that is a script with no function calls but not sure.
    #  Doesn't seem very critical anyway as this will only be done once.
    weaviate_client = create_weaviate_client()

    main()
