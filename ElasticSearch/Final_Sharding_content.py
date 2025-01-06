from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import json
from datetime import datetime

# Step 1: Initialize Elasticsearch Client
es = Elasticsearch('https://localhost:9200', basic_auth=('elastic', 'uRmY*oulxBA8+N4m_4nW'), verify_certs=False)

# Step 2: Define Index Settings and Mappings
index_name = "content_v2"

index_settings = {
    "settings": {
        "number_of_shards": 3,  # Shard into 3
        "number_of_replicas": 1
    },
    "mappings": {
        "properties": {
            "content_id": {
                "type": "keyword"
            },
            "title": {
                "type": "text"
            },
            "description": {
                "type": "text"
            },
            "type": {
                "type": "keyword"
            },
            "genre": {
                "type": "keyword"  # Genre for sharding
            },
            "metadata": {
                "properties": {
                    "duration": {"type": "keyword"},
                    "actors": {"type": "text"},
                    "release_date": {"type": "date"}
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
json_file_path = r"C:\Users\vicky\OneDrive\Desktop\ASU\Coursework\CSE 512\Project\DDS_Project.content.json"  # Replace with the correct path to your JSON file

with open(json_file_path, "r") as file:
    content_data = json.load(file)

# Step 4: Define Routing Logic
def get_routing_key(genre):
    routing_map = {
        "Drama": "0",
        "Comedy": "1",
        "Sci-Fi": "2",
        "Romance": "3",
        "Thriller": "3"
    }
    return routing_map.get(genre, "0")  # Default to shard 0 if genre is unknown

# Step 5: Prepare Documents for Bulk Upload
def generate_documents(data):
    for item in data:
        item_id = item["_id"]["$oid"]

        # Parse release_date from MongoDB $date format
        release_date = item["metadata"]["release_date"]["$date"]
        try:
            # Convert MongoDB $date format to ISO 8601 format
            parsed_date = datetime.strptime(release_date, "%Y-%m-%dT%H:%M:%S.%fZ")
        except ValueError:
            # Fallback if milliseconds are not present
            parsed_date = datetime.strptime(release_date, "%Y-%m-%dT%H:%M:%SZ")

        yield {
            "_index": "content",
            "_id": item_id,
            "_source": {
                "content_id": item["content_id"],
                "title": item["title"],
                "description": item["description"],
                "type": item["type"],
                "genre": item["genre"],
                "metadata": {
                    "duration": item["metadata"]["duration"],
                    "actors": item["metadata"]["actors"],
                    "release_date": parsed_date.isoformat()  # Convert back to ISO 8601
                }
            },
            "routing": get_routing_key(item["genre"])  # Custom routing
        }

# Step 6: Bulk Upload Data
try:
    success, errors = bulk(es, generate_documents(content_data), raise_on_error=False)
    print(f"Indexed {success} documents successfully.")
    if errors:
        print("Errors:")
        for error in errors:
            print(error)
except Exception as e:
    print(f"Error during bulk upload: {e}")

