from faker import Faker
from random import choice, randint, uniform, sample
from datetime import datetime
import randomtimestamp
from pymongo import MongoClient


client = MongoClient("mongodb://localhost:27017/")
db = client["DDS_Project"]
# Define collections
users_collection = db["users"]
content_collection = db["content"]
interaction_history_collection = db["interaction_history"]
recommendations_collection = db["recommendations"]
regional_trends_collection = db["regional_trends"]

fake = Faker()

# Regions for geo-distribution
regions = ["North America", "Europe", "Asia", "South America"]

# Sample data fields for content and interactions
content_types = ["movie", "webseries", "documentary"]
genres = ["Sci-Fi", "Romance", "Thriller", "Comedy", "Drama"]
tags = ["action", "adventure", "mystery", "fantasy", "horror"]
interaction_types = ["view", "like", "share"]

def generate_users(n):
    users = []
    for _ in range(n):
        user = {
            "user_id": fake.uuid4(),
            "name": fake.name(),
            "location": choice(regions),
            "latitude": round(uniform(-90.0, 90.0), 6),
            "longitude": round(uniform(-180.0, 180.0), 6),
            "profile": {
                "age": randint(18, 70),
                "gender": choice(["male", "female", "other"]),
                "interests": sample(genres, 3)
            }
        }
        users.append(user)
    return users

def generate_content(n):
    content_list = []
    for _ in range(n):
        content = {
            "content_id": fake.uuid4(),
            "title": fake.sentence(nb_words=3),
            "description": fake.paragraph(),
            "type": choice(content_types),
            "genre": choice(genres),
            "tags": sample(tags, 3),
            "metadata": {
                "duration": f"{randint(60, 180)} mins",
                "actors": [fake.name() for _ in range(3)],
                "release_date": fake.date_this_decade()
            }
        }
        content_list.append(content)
    return content_list

def generate_interaction_history(users, content_list, n):
    interaction_history = []
    for _ in range(n):
        interaction = {
            "user_id": choice(users)["user_id"],
            "content_id": choice(content_list)["content_id"],
            "interaction_type": choice(interaction_types),
            "timestamp": randomtimestamp.random_date(start=datetime(2022, 1, 1), end=datetime(2024, 12, 31)).isoformat()
        }
        interaction_history.append(interaction)
    return interaction_history

def generate_recommendations(users, content_list, n):
    recommendations = []
    for _ in range(n):
        recommendation = {
            "user_id": choice(users)["user_id"],
            "content_id": choice(content_list)["content_id"],
            "score": round(uniform(0.5, 5.0), 2),  # Relevance score out of 5
            "reason": choice(["Based on your interests", "Trending in your location", "Similar to content you've watched"]),
            "timestamp": datetime.now().isoformat()
        }
        recommendations.append(recommendation)
    return recommendations

def generate_regional_trends(content_list):
    regional_trends = []
    for region in regions:
        trend = {
            "region": region,
            "top_content": choice(content_list)["title"],
            "trending_content": sample([c["title"] for c in content_list], 2),
            "engagement_metrics": {
                "total_views": randint(1000, 10000),
                "total_likes": randint(500, 5000),
                "total_shares": randint(100, 1000)
            }
        }
        regional_trends.append(trend)
    return regional_trends
from datetime import date, datetime

def convert_dates(data):
    if isinstance(data, list):
        return [convert_dates(item) for item in data]
    elif isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, date) and not isinstance(value, datetime):
                data[key] = datetime.combine(value, datetime.min.time())
            elif isinstance(value, (dict, list)):
                data[key] = convert_dates(value)
    return data

# Insert data into collections
def insert_data(users,content_list,interaction_history,recommendations,regional_trends):
    # Clear collections first (optional, to avoid duplicates if rerunning)
    users_collection.delete_many({})
    content_collection.delete_many({})
    interaction_history_collection.delete_many({})
    recommendations_collection.delete_many({})
    regional_trends_collection.delete_many({})

    # Insert each dataset into the relevant collection
    users_collection.insert_many(users)
    content_collection.insert_many(content_list)
    interaction_history_collection.insert_many(interaction_history)
    recommendations_collection.insert_many(recommendations)
    regional_trends_collection.insert_many(regional_trends)

    print("Data inserted successfully.")

num_users = 10000         # Increased from 1000 to simulate a larger user base
num_content = 2000        # Increased from 500 to add more content variety
num_interactions = 50000  # Increased from 2000 to reflect frequent user interactions
num_recommendations = 20000 # Increased from 1500 to test recommendations at scale

# Generate data
users = generate_users(num_users)
content_list = generate_content(num_content)
interaction_history = generate_interaction_history(users, content_list, num_interactions)
recommendations = generate_recommendations(users, content_list, num_recommendations)
regional_trends = generate_regional_trends(content_list)

# Convert dates in each dataset
users = convert_dates(users)
content_list = convert_dates(content_list)
interaction_history = convert_dates(interaction_history)
recommendations = convert_dates(recommendations)
regional_trends = convert_dates(regional_trends)

print("Sample Users:", users[:2])
print("Sample Content:", content_list[:2])
print("Sample Interaction History:", interaction_history[:2])
print("Sample Recommendations:", recommendations[:2])
print("Sample Regional Trends:", regional_trends[:2])

# Run the insertion function
insert_data(users,content_list,interaction_history,recommendations,regional_trends)
