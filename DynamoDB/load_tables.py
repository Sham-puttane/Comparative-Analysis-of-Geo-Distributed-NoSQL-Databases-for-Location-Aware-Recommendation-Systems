import json
import boto3
from decouple import config
from botocore.exceptions import ClientError
from decimal import Decimal
from concurrent.futures import ThreadPoolExecutor
import time

# Initialize region mappings
regions = {
    "North America": "us-east-1",
    "South America": "sa-east-1",
    "Europe": "eu-central-1",
    "Asia": "ap-south-1"
}


def initialize_dynamodb(region_name):
    """Initialize DynamoDB resource for a specific region."""
    return boto3.resource(
        'dynamodb',
        region_name=region_name,
        aws_access_key_id=config('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY')
    )


def load_json_data(file_path):
    """Load data from a JSON file."""
    try:
        with open(file_path, 'r') as file:
            data = json.load(file, parse_float=Decimal)
            print(f"Data loaded from {file_path}. Total records: {len(data)}")
            return data
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return []
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {file_path}: {e}")
        return []


def preprocess_data(raw_data, table_name):
    """Preprocess data for a given table."""
    processed_data = []
    for record in raw_data:
        try:
            if table_name == "Users":
                # Remove '_id'
                record.pop('_id', None)
            elif table_name == "RegionalTrends":
                # Move '_id.$oid' to 'regional_trends_id' and remove '_id'
                if '_id' in record and '$oid' in record['_id']:
                    record['regional_trends_id'] = record['_id']['$oid']
                    del record['_id']
            elif table_name == "Content":
                # Remove '_id'
                record.pop('_id', None)
            elif table_name == "InteractionHistory":
                # Move '_id.$oid' to 'interaction_history_id' and remove '_id'
                if '_id' in record and '$oid' in record['_id']:
                    record['interaction_history_id'] = record['_id']['$oid']
                    del record['_id']
            processed_data.append(record)
        except Exception as e:
            print(f"Error processing record: {record}. Error: {e}")
    return processed_data


def batch_write_to_table(dynamodb, table_name, data):
    """Batch write data into a DynamoDB table."""
    table = dynamodb.Table(table_name)
    try:
        with table.batch_writer() as batch:
            for record in data:
                batch.put_item(Item=record)
        print(f"Batch data loaded successfully into {table_name} in region {dynamodb.meta.client.meta.region_name}. Total records: {len(data)}")
    except ClientError as e:
        print(f"ClientError: {e.response['Error']['Message']} while batch writing to {table_name} in region {dynamodb.meta.client.meta.region_name}")
    except Exception as e:
        print(f"Unexpected error while batch writing to {table_name} in region {dynamodb.meta.client.meta.region_name}: {e}")


def chunk_data(data, chunk_size=25):
    """Split data into smaller chunks for batch writing."""
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]


def write_data_in_chunks(dynamodb, table_name, data):
    """Write data in chunks to handle large datasets efficiently."""
    for chunk in chunk_data(data):
        batch_write_to_table(dynamodb, table_name, chunk)


def distribute_data_across_regions(data, table_name, column_name):
    """Distribute data to respective regions based on the region column."""
    # Preprocess the data
    data = preprocess_data(data, table_name)

    # Distribute preprocessed data by region
    regional_data = {region: [] for region in regions.keys()}

    for record in data:
        record_region = record.get(column_name)
        if record_region in regional_data:
            regional_data[record_region].append(record)

    with ThreadPoolExecutor(max_workers=len(regions)) as executor:
        for region, region_data in regional_data.items():
            print(f"Region {region} has {len(region_data)} records for {table_name}")
            if region_data:  # Only process if there is data for this region
                dynamodb = initialize_dynamodb(regions[region])
                executor.submit(write_data_in_chunks, dynamodb, table_name, region_data)


def replicate_data_across_regions(data, table_name):
    """Replicate data to all regions."""
    # Preprocess the data
    data = preprocess_data(data, table_name)

    with ThreadPoolExecutor(max_workers=len(regions)) as executor:
        for region in regions.values():
            dynamodb = initialize_dynamodb(region)
            executor.submit(write_data_in_chunks, dynamodb, table_name, data)


def main():
    # File paths for JSON data
    files = {
        "Users": "users.json",
        "RegionalTrends": "regional_trends.json",
        "Content": "content.json",
        "InteractionHistory": "interaction_history.json"
    }

    # Load and distribute Users table data
    users_data = load_json_data(files["Users"])
    distribute_data_across_regions(users_data, "Users", column_name="location")

    # Load and distribute RegionalTrends table data
    regional_trends_data = load_json_data(files["RegionalTrends"])
    distribute_data_across_regions(regional_trends_data, "RegionalTrends", column_name="region")

    # Load and replicate Content table data
    content_data = load_json_data(files["Content"])
    replicate_data_across_regions(content_data, "Content")

    # Load and replicate InteractionHistory table data
    interaction_history_data = load_json_data(files["InteractionHistory"])
    replicate_data_across_regions(interaction_history_data, "InteractionHistory")

    print("Data loading completed across regions.")


if __name__ == "__main__":
    try:
        print("Starting data loading process...")
        start_time = time.time()
        main()
        end_time = time.time()
        print(f"Data loading completed successfully! Total time: {end_time - start_time:.2f} seconds.")
    except ClientError as e:
        print(f"ClientError during data loading: {e.response['Error']['Message']}")
    except Exception as e:
        print(f"Unexpected error during data loading: {e}")
