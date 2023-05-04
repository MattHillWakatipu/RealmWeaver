import os
import openai
import weaviate
from dotenv import load_dotenv

openai.api_key = os.getenv('OPENAI_API_KEY')
COMPLETION_MODEL = 'text-davinci-003'
EMBEDDING_MODEL = 'text-embedding-ada-002'


def fetch_related():
    # TODO make this dynamic
    near_text = {"concepts": ["Cities"]}

    response = (
        weaviate_client.query
        .get("Question", ["question", "answer", "category"])
        .with_near_text(near_text)
        .with_limit(2)
        .do()
    )

    result = '\n\n' \
             '************\n' \
             'Context:\n\n'

    # Extract information from response
    result += response['data']['Get']['Question'][0]['question'] + '\n\n'
    result += response['data']['Get']['Question'][1]['question']

    # print(json.dumps(response, indent=4))

    # print(result)
    return result


def store_response(response):
    pass


def main():
    input = "Create a City for me."

    context = fetch_related()

    query = input + context

    print(query)

    # completion = openai.ChatCompletion.create(
    #     model="gpt-3.5-turbo",
    #     messages=[
    #         {"role": "user", "content": query}
    #     ]
    # )
    #
    # response = completion.choices[0].message.content
    #
    # print(f'Query: {query}')
    # print(f'Response: {response}')
    #
    # store_response(response)


def create_weaviate_client():
    return weaviate.Client(
        url='https://realm-weaver-f5qsqrbe.weaviate.network',
        auth_client_secret=weaviate.auth.AuthApiKey(api_key=os.getenv('WEAVIATE_API_KEY')),
        additional_headers={
            "X-OpenAI-Api-Key": os.getenv('openai_api_key')
        }
    )


if __name__ == '__main__':
    load_dotenv()
    weaviate_client = create_weaviate_client()
    main()
