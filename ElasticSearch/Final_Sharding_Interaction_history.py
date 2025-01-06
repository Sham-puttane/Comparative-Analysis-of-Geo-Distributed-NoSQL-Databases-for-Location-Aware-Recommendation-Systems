from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import json
import hashlib

# Step 1: Initialize Elasticsearch Client
es = Elasticsearch('https://localhost:9200', basic_auth=('elastic', 'uRmY*oulxBA8+N4m_4nW'), verify_certs=False)

# Step 2: Define Index Settings and Mappings
index_name = "interaction_history"

index_settings = {
    "settings": {
        "number_of_shards": 4,  # Shard into 4
        "number_of_replicas": 1
    },
    "mappings": {
        "properties": {
            "user_id": {"type": "keyword"},
            "content_id": {"type": "keyword"},
            "interaction_type": {"type": "keyword"},
            "timestamp": {"type": "date"}  # Timestamp as ISO 8601
        }
    }
}

# Create the index if it doesn't exist
if not es.indices.exists(index=index_name):
    es.indices.create(index=index_name, body=index_settings)
    print(f"Index '{index_name}' created.")
else:
    print(f"Index '{index_name}' already exists.")

# Step 3: Load JSON Data
json_file_path = r"C:\Users\vicky\OneDrive\Desktop\ASU\Coursework\CSE 512\Project\DDS_Project.interaction_history.json"  # Replace with the correct path

with open(json_file_path, "r") as file:
    interaction_data = json.load(file)

# Step 4: Define Routing Logic (Hash-Based)
def get_routing_key(user_id):
    # Hash user_id and mod by 4 to determine the shard
    hash_value = int(hashlib.sha256(user_id.encode('utf-8')).hexdigest(), 16)
    return str(hash_value % 4)

# Step 5: Prepare Documents for Bulk Upload
def generate_documents(data):
    for item in data:
        item_id = item["_id"]["$oid"]
        routing_key = get_routing_key(item["user_id"])
        yield {
            "_index": index_name,
            "_id": item_id,
            "_source": {
                "user_id": item["user_id"],
                "content_id": item["content_id"],
                "interaction_type": item["interaction_type"],
                "timestamp": item["timestamp"]
            },
            "routing": routing_key  # Custom routing
        }

# Step 6: Bulk Upload Data
try:
    success, errors = bulk(es, generate_documents(interaction_data), raise_on_error=False)
    print(f"Indexed {success} documents successfully.")
    if errors:
        print("Errors:")
        for error in errors:
            print(error)
except Exception as e:
    print(f"Error during bulk upload: {e}")
