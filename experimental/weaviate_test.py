import json
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

# # ===== import data =====
# # Load data
# import requests
# url = 'https://raw.githubusercontent.com/weaviate-tutorials/quickstart/main/data/jeopardy_tiny.json'
# resp = requests.get(url)
# data = json.loads(resp.text)
#
# # Configure a batch process
# with client.batch as batch:
#     batch.batch_size = 100
#     # Batch import all Questions
#     for i, d in enumerate(data):
#         print(f"importing question: {i + 1}")
#
#         properties = {
#             "answer": d["Answer"],
#             "question": d["Question"],
#             "category": d["Category"],
#         }
#
#         client.batch.add_data_object(properties, "Question")

# print(client.query.aggregate('Question').with_meta_count().do())

nearText = {"concepts": ["biology"]}

result = (
    client.query
    .get("Question", ["question", "answer", "category"])
    .with_near_text(nearText)
    .with_limit(2)
    .do()
)

print(json.dumps(result, indent=4))
