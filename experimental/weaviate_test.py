import os
import weaviate
from dotenv import load_dotenv

load_dotenv()

# Instantiate the client with the auth config
client = weaviate.Client(
    url='https://realm-weaver-f5qsqrbe.weaviate.network',
    auth_client_secret=weaviate.auth.AuthApiKey(api_key=os.getenv('WEAVIATE_API_KEY')),
    additional_headers={
        "X-OpenAI-Api-Key": os.getenv('openai_api_key')
    }
)

# class_obj = {
#     "class": "Question",
#     "vectorizer": "text2vec-openai"  # Or "text2vec-cohere" or "text2vec-huggingface"
# }
#
# client.schema.create_class(class_obj)

print(client.schema.get())
