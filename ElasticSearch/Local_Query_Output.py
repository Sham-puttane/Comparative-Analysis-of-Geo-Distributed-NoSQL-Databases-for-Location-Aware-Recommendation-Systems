import time
import psutil
import numpy as np
from elasticsearch import Elasticsearch

# Initialize Elasticsearch client
es = Elasticsearch('https://localhost:9200', basic_auth=('elastic', 'uRmY*oulxBA8+N4m_4nW'), verify_certs=False)

# Function to get current CPU and Memory usage
def get_system_usage():
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent
    return cpu, memory

# Function to execute bulk search and measure response time
def execute_bulk_search(num_requests):
    # Prepare bulk search body
    body = []
    for _ in range(num_requests):
        # Metadata part (empty for now, it can contain index or other parameters)
        body.append({})
        # Query part
        body.append({
            "query": {
                "bool": {
                    "filter": {
                        "terms": {
                            "region": ["Europe"]
                        }
                    }
                }
            },
            "sort": [
                {"engagement_metrics.total_views": {"order": "desc"}},
                {"engagement_metrics.total_likes": {"order": "desc"}}
            ],
            "_source": [
                "top_content", 
                "engagement_metrics.total_likes", 
                "engagement_metrics.total_views", 
                "region"
            ],
            "size": 10  # Size should be part of the query, not metadata
        })
    
    # Execute bulk search request
    start_time = time.time()
    response = es.msearch(body=body)  # Perform the bulk search
    end_time = time.time()

    return (end_time - start_time) * 1000  # Return total response time in milliseconds

# Collecting performance metrics over 200 requests with 20 users
response_times = []
cpu_before, memory_before = get_system_usage()  # Get initial system usage

# Perform bulk search (e.g., 10 queries in one request)
num_requests_per_batch = 175
total_requests = 200
for i in range(total_requests // num_requests_per_batch):
    response_time = execute_bulk_search(num_requests_per_batch)  # Execute a bulk search
    response_times.append(response_time)

cpu_after, memory_after = get_system_usage()  # Get system usage after requests

# Calculate performance metrics
total_execution_time = sum(response_times)
throughput = total_requests / (total_execution_time / 1000)  # Requests per second (convert total execution time to seconds)
average_response_time = np.mean(response_times)
min_response_time = np.min(response_times)
max_response_time = np.max(response_times)
std_deviation = np.std(response_times)

# Calculate CPU and memory utilization increase
cpu_utilization_increase = cpu_after - cpu_before
memory_utilization_increase = memory_after - memory_before

# Print the performance metrics in milliseconds
print(f"Total Execution Time: {total_execution_time:.2f} ms")
print(f"Throughput: {throughput:.2f} requests per second")
print(f"Average Response Time: {average_response_time:.2f} ms")
print(f"Minimum Response Time: {min_response_time:.2f} ms")
print(f"Maximum Response Time: {max_response_time:.2f} ms")
print(f"Response Time Standard Deviation: {std_deviation:.2f} ms")
print(f"CPU Utilization Increase: {cpu_utilization_increase:.2f}%")
print(f"Memory Utilization Increase: {memory_utilization_increase:.2f}%")
