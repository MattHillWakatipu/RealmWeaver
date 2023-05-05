import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

query = "Assign a Category to this worldbuilding text: eg.(Cities, People, Magic, etc)\n" \
        "As the threads of political intrigue tighten around the peoples of Aotearoa, and the powers of magic whirl in a storm of potential and desire, the future of this extraordinary realm rests in the hands of the brave heroes who dare to keep the world from descending into chaos. In this place of wonder and mystery, elemental magic is not only a force to be wielded, but also a story to be told and a legacy waiting to be unveiled."

completion = openai.ChatCompletion.create(
  model="gpt-4",
  messages=[
    {"role": "user", "content": query}
  ]
)

response = completion.choices[0].message.content

print(f'Query: {query}')
print(f'Response: {response}')
