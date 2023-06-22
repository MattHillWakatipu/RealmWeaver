import json
import os
import weaviate
from dotenv import load_dotenv

load_dotenv()

# Instantiate the client with the auth config
client = weaviate.Client(
    url=os.getenv('WEAVIATE_URL'),
    auth_client_secret=weaviate.auth.AuthApiKey(api_key=os.getenv('WEAVIATE_API_KEY')),
    additional_headers={
        "X-OpenAI-Api-Key": os.getenv('openai_api_key')
    }
)

# # delete class "YourClassName" - THIS WILL DELETE ALL DATA IN THIS CLASS
# client.schema.delete_class("Question")  # Replace with your class name - e.g. "Question"

# ===== create schema =====
class_obj = {
    "class": "Lore",
    "vectorizer": "text2vec-openai"  # Or "text2vec-cohere" or "text2vec-huggingface"
}

client.schema.create_class(class_obj)

# ===== import data =====
# Load data and Configure a batch process
with open('world/test.json', mode='r', encoding='utf-8') as file, client.batch as batch:
    data = json.load(file)
    print(data)

    batch.batch_size = 100
    # Batch import all Questions
    for i, d in enumerate(data):
        print(f"importing question: {i + 1}")

        properties = {
            "lore": d["Lore"],
            "category": d["Category"],
        }

        client.batch.add_data_object(properties, "Lore")


print(client.query.aggregate('Lore').with_meta_count().do())


nearText = {"concepts": ["Magical Study"]}

result = (
    client.query
    .get("Lore", ["lore", "category"])
    .with_near_text(nearText)
    .with_limit(2)
    .do()
)

print(json.dumps(result, indent=4))
