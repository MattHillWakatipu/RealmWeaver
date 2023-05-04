import os

import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

query = "test"

completion = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "user", "content": query}
  ]
)

response = completion.choices[0].message.content

print(f'Query: {query}')
print(f'Response: {response}')
