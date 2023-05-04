import os
import openai
import weaviate
from dotenv import load_dotenv

openai.api_key = os.getenv('OPENAI_API_KEY')
weaviate_api_key = os.getenv('weaviate_api_key')
COMPLETIONS_MODEL = 'text-davinci-003'
EMBEDDING_MODEL = 'text-embedding-ada-002'


def fetch_related():
    pass


def store_response(response):
    pass


def main():
    input = "Create a City for me."

    context = fetch_related()

    query = input + context

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": query}
        ]
    )

    response = completion.choices[0].message.content

    print(f'Query: {query}')
    print(f'Response: {response}')

    store_response(response)


if __name__ == '__main__':
    load_dotenv()
    main()
