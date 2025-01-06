from elasticsearch import Elasticsearch

es = Elasticsearch('https://localhost:9200', basic_auth=('elastic', 'uRmY*oulxBA8+N4m_4nW'), verify_certs=False)

# Step 1: Query to fetch top_content from regional_trends
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

# Extract top_content titles
top_content_titles = [hit["_source"]["top_content"] for hit in response_1["hits"]["hits"]]

# Step 2: Query content_v2 using the top_content titles
response_2 = es.search(index="content_v2", body={
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

# Print the results
for hit in response_2["hits"]["hits"]:
    print(hit["_source"])
