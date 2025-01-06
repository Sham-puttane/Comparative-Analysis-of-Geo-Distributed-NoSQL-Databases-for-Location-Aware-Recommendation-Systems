from elasticsearch import Elasticsearch

es = Elasticsearch('https://localhost:9200', basic_auth=('elastic', 'uRmY*oulxBA8+N4m_4nW'), verify_certs=False)

# Step 1: Query to fetch top_content from regional_trends
response_1 = es.search(index="regional_trends", body={
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
    "size": 10,  # Retrieve top 10 documents
    "_source": [
        "top_content", 
        "engagement_metrics.total_likes", 
        "engagement_metrics.total_views", 
        "region"
    ]
})

# Print the results
for hit in response_1["hits"]["hits"]:
    print(hit["_source"])
