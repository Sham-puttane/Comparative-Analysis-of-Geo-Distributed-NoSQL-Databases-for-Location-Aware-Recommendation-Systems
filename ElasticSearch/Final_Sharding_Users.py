from elasticsearch import Elasticsearch, helpers
import json


# Initialize the Elasticsearch client
es = Elasticsearch('https://localhost:9200', basic_auth=('elastic', 'uRmY*oulxBA8+N4m_4nW'), verify_certs=False)

# Define the index name
index_name = "users"

# Define the index settings and mappings
index_settings = {
    "settings": {
        "number_of_shards": 4,
        "number_of_replicas": 1
    },
    "mappings": {
        "properties": {
            "user_id": {
                "type": "keyword"
            },
            "name": {
                "type": "text",
                "fields": {
                    "raw": {
                        "type": "keyword"
                    }
                }
            },
            "location": {
                "type": "keyword"
            },
            "latitude": {
                "type": "float"
            },
            "longitude": {
                "type": "float"
            },
            "profile": {
                "properties": {
                    "age": {
                        "type": "integer"
                    },
                    "gender": {
                        "type": "keyword"
                    },
                    "interests": {
                        "type": "text",
                        "fields": {
                            "raw": {
                                "type": "keyword"
                            }
                        }
                    }
                }
            }
        }
    }
}

# Create the index with the specified settings and mappings (if it doesn't already exist)
if not es.indices.exists(index=index_name):
    es.indices.create(index=index_name, body=index_settings)
    print(f"Index '{index_name}' created successfully.")

# Load the JSON data from a file
def load_json_data(file_path):
    with open(file_path, "r") as file:
        return json.load(file)

# Define routing logic based on location to shard the data into 4 nodes
def get_routing_key(location):
    if location == "Asia":
        return "0"  # Shard 0
    elif location == "North America":
        return "1"  # Shard 1
    elif location == "South America":
        return "2"  # Shard 2
    elif location == "Europe":
        return "3"  # Shard 3
    else:
        return "0"  # Default shard if location doesn't match

# Function to generate the documents for the bulk upload
def generate_documents(users):
    for user in users:
        # Extract _id from the "$oid" field and ensure it's a simple value
        user_id = user.get("_id", {}).get("$oid")  # Extract the value of $oid
        if not user_id:
            raise ValueError(f"Missing or malformed '_id' for user: {user}")
        
        routing_key = get_routing_key(user["location"])
        yield {
            "_op_type": "index",
            "_index": index_name,
            "_id": user_id,  # Use the extracted _id value
            "_routing": routing_key,  # Custom routing to the correct shard
            "_source": {
                "user_id": user["user_id"],
                "name": user["name"],
                "location": user["location"],
                "latitude": user["latitude"],
                "longitude": user["longitude"],
                "profile": user["profile"]
            }
        }

# Load the JSON data (assuming the JSON file path is 'users_data.json')
file_path = r'C:\Users\vicky\OneDrive\Desktop\ASU\Coursework\CSE 512\Project\DDS_Project.users.json'
users_data = load_json_data(file_path)

# Bulk upload the documents to Elasticsearch
helpers.bulk(es, generate_documents(users_data))

print("Data uploaded successfully!")


