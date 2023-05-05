import os
import openai
import weaviate
from dotenv import load_dotenv

COMPLETION_MODEL = 'gpt-4'
EMBEDDING_MODEL = 'text-embedding-ada-002'


def fetch_related():
    # TODO make this dynamic
    near_text = {'concepts': ['Cities']}

    # with weaviate_client.query as query:

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
    formatted = format_response(response)

    print(f'formatted: {formatted}')

    with weaviate_client.batch as batch:
        batch.add_data_object(formatted, 'Lore')


def format_response(lore):
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
    header = 'Background:\n' \
             'I am doing some worldbuilding for a fantasy novel.\n' \
             'The setting is inspired by New Zealand, featuring elemental magic and political intrigue.\n' \
             '************\n'

    input = 'Instructions:\n' \
            'In one paragraph create a political leader for me.\n' \
            '************\n'

    context = fetch_related()

    query = header + input + context

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
    return weaviate.Client(
        url='https://realm-weaver-f5qsqrbe.weaviate.network',
        auth_client_secret=weaviate.auth.AuthApiKey(api_key=os.getenv('WEAVIATE_API_KEY')),
        additional_headers={
            'X-OpenAI-Api-Key': os.getenv('openai_api_key')
        }
    )


if __name__ == '__main__':
    load_dotenv()
    openai.api_key = os.getenv('OPENAI_API_KEY')

    # FIXME Socket not closing for whatever reason, doesn't seem to matter if this is global or within a function.
    #  Doesn't occur in weaviate_test.py, could be because that is a script with no function calls but not sure.
    #  Doesn't seem very critical anyway.
    weaviate_client = create_weaviate_client()

    main()
