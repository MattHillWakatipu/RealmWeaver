import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

query = '''
Instructions: Create an example of bio-engineered flora.

Background:  In 2073, Victoria University of Wellington has been transformed into a bleeding-edge citadel of higher learning, radiating with futurism amidst the atmospheric backdrop of New Zealand's rugged landscapes. Nestled between the Wellington Harbour's shimmering neon-lit waves and the rolling, raven-hued hills, the university has evolved into a nucleus of cutting-edge technology and cyberspace innovation. Classrooms have evolved into immersive virtual reality domains, while students navigate their campus experiences through sleek augmented reality lenses, which also project holographic renditions of the iconic university buildings into the night sky. A flourishing hub amidst the city's glittering cyberpunk skyline, the university has become a beacon of both academia and rebellion; a sanctuary for intellectuals and hackers alike. Dissonant notes of old tradition and new technology create a tension that fills the air with a palpable undercurrent of change and progress. Prominent kiwi symbols and neo-Maori aesthetics blend into this high-tech ambiance, adding a unique antipodean charm to the otherwise stark, high-tech universe. Striking a balance between ecological preservation and technological revolution, Victoria University is a mesmerizing melting pot of bioengineered flora, AI-driven facilities, and passionate, forward-thinking inhabitants armed with knowledge and digital tools.
'''
completion = openai.ChatCompletion.create(
  model="gpt-4",
  messages=[
    {"role": "user", "content": query}
  ]
)

response = completion.choices[0].message.content

print(f'Query: {query}')
print(f'Response: {response}')
