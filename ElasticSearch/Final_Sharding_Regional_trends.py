from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import json

# Step 1: Initialize Elasticsearch Client
es = Elasticsearch('https://localhost:9200', basic_auth=('elastic', 'uRmY*oulxBA8+N4m_4nW'), verify_certs=False)

# Step 2: Define Index Settings and Mappings
index_name = "regional_trends"

index_settings = {
    "settings": {
        "number_of_shards": 4,  # Shard into 4 regions
        "number_of_replicas": 1
    },
    "mappings": {
        "properties": {
            "region": {
                "type": "keyword"  # Precise matching
            },
            "top_content": {
                "type": "text"
            },
            "engagement_metrics": {
                "properties": {
                    "total_views": {"type": "integer"},
                    "total_likes": {"type": "integer"},
                    "total_dislikes": {"type": "integer"}
                }
            }
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
# Make sure your JSON file is correctly formatted as per the given schema
json_file_path = r"C:\Users\vicky\OneDrive\Desktop\ASU\Coursework\CSE 512\Project\DDS_Project.regional_trends.json"  # Replace with the correct path to your JSON file

with open(json_file_path, "r") as file:
    regional_trends_data = json.load(file)

# Step 4: Define Routing Logic
def get_routing_key(region):
    routing_map = {
        "North America": "0",
        "Europe": "1",
        "Asia": "2",
        "South America": "3"
    }
    return routing_map.get(region, "0")  # Default to shard 0 if region is unknown

# Step 5: Prepare Documents for Bulk Upload
def generate_documents(data):
    for item in data:
        yield {
            "_index": index_name,
            "_id": item["_id"]["$oid"],  # Use `_id` as the document ID
            "_source": {
                "region": item["region"],
                "top_content": item["top_content"],
                "engagement_metrics": item["engagement_metrics"]
            },
            "routing": get_routing_key(item["region"])  # Custom routing
        }

# Step 6: Bulk Upload Data
try:
    bulk(es, generate_documents(regional_trends_data))
    print("Data uploaded successfully!")
except Exception as e:
    print(f"Error during bulk upload: {e}")


