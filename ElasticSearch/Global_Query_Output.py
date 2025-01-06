import time
import psutil
import numpy as np
from elasticsearch import Elasticsearch
from concurrent.futures import ThreadPoolExecutor

# Initialize Elasticsearch connection
es = Elasticsearch('https://localhost:9200', basic_auth=('elastic', 'uRmY*oulxBA8+N4m_4nW'), verify_certs=False)

# Define function for a single user's requests
def execute_requests(user_id, num_requests):
    local_response_times = []
    for _ in range(num_requests):
        # Step 1: Query to fetch top_content from regional_trends
        step1_start = time.time()
        response_1 = es.search(index="regional_trends", body={
            "query": {
                "bool": {
                    "filter": {
                        "terms": {
                            "region": ["Asia", "South America", "North America", "Europe"]
                        }
                    }
                }
            },
            "sort": [
                {"engagement_metrics.total_views": {"order": "desc"}},
                {"engagement_metrics.total_likes": {"order": "desc"}}
            ],
            "size": 5,
            "_source": ["top_content"]
        })
        step1_end = time.time()
        local_response_times.append((step1_end - step1_start) * 1000)  # Convert to milliseconds

        # Extract top_content titles
        top_content_titles = [hit["_source"]["top_content"] for hit in response_1["hits"]["hits"]]

        # Step 2: Query content_v2 using the top_content titles
        step2_start = time.time()
        es.search(index="content_v2", body={
            "query": {
                "terms": {
                    "title": top_content_titles
                }
            },
            "_source": [
                "content_id",
                "title",
                "description",
                "type",
                "genre",
                "metadata.duration",
                "metadata.actors",
                "metadata.release_date"
            ]
        })
        
        step2_end = time.time()
        local_response_times.append((step2_end - step2_start) * 1000)  # Convert to milliseconds
    return local_response_times

# Configuration for users and requests
total_users = 20
requests_per_user = 10  # 20 users x 10 requests each = 200 total requests
total_requests = total_users * requests_per_user

# Record initial CPU and memory utilization
cpu_before = psutil.cpu_percent(interval=1)
memory_before = psutil.virtual_memory().percent

# Start measuring performance
response_times = []
start_time = time.time()

# Use ThreadPoolExecutor to simulate concurrent users
with ThreadPoolExecutor(max_workers=total_users) as executor:
    futures = [
        executor.submit(execute_requests, user_id, requests_per_user)
        for user_id in range(total_users)
    ]
    for future in futures:
        response_times.extend(future.result())

end_time = time.time()

# Calculate metrics
total_execution_time = (end_time - start_time) * 1000  # Convert to milliseconds
throughput = total_requests / total_execution_time * 1000  # Requests per second, convert time to seconds
average_response_time = np.mean(response_times)
min_response_time = np.min(response_times)
max_response_time = np.max(response_times)
std_deviation = np.std(response_times)

# Record CPU and memory utilization after execution
cpu_after = psutil.cpu_percent(interval=1)
memory_after = psutil.virtual_memory().percent
cpu_utilization_increase = cpu_after - cpu_before
memory_utilization_increase = memory_after - memory_before

# Print metrics in milliseconds
print(f"Total Execution Time: {total_execution_time:.2f} ms")
print(f"Throughput: {throughput:.2f} requests per second")
print(f"Average Response Time: {average_response_time:.2f} ms")
print(f"Minimum Response Time: {min_response_time:.2f} ms")
print(f"Maximum Response Time: {max_response_time:.2f} ms")
print(f"Response Time Standard Deviation: {std_deviation:.2f} ms")
print(f"CPU Utilization Increase: {cpu_utilization_increase:.2f}%")
print(f"Memory Utilization Increase: {memory_utilization_increase:.2f}%")
