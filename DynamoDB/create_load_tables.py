import boto3
from decouple import config  # For loading AWS credentials from environment variables
from botocore.exceptions import ClientError  # Import ClientError for error handling

# List of AWS regions
regions = ["us-east-1", "sa-east-1", "eu-central-1", "ap-south-1"]

def initialize_dynamodb(region_name):
    """Initialize DynamoDB resource for a specific region."""
    return boto3.resource(
        'dynamodb',
        region_name=region_name,
        aws_access_key_id=config('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY')
    )


def create_table_on_demand(dynamodb, table_name, partition_key, sort_key=None):
    """Creates a table with on-demand capacity."""
    key_schema = [{'AttributeName': partition_key, 'KeyType': 'HASH'}]
    attribute_definitions = [{'AttributeName': partition_key, 'AttributeType': 'S'}]
    if sort_key:
        key_schema.append({'AttributeName': sort_key, 'KeyType': 'RANGE'})
        attribute_definitions.append({'AttributeName': sort_key, 'AttributeType': 'S'})
    
    try:
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=key_schema,
            AttributeDefinitions=attribute_definitions,
            BillingMode='PAY_PER_REQUEST'  # On-demand capacity mode
        )
        print(f"Creating table {table_name} in On-Demand mode in region {dynamodb.meta.client.meta.region_name}...")
        table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
        print(f"Table {table_name} created successfully in region {dynamodb.meta.client.meta.region_name}!")
    except ClientError as e:
        print(f"ClientError: {e.response['Error']['Message']} for table {table_name} in region {dynamodb.meta.client.meta.region_name}")
    except Exception as e:
        print(f"Unexpected error while creating table {table_name} in region {dynamodb.meta.client.meta.region_name}: {e}")


def create_tables_on_demand(dynamodb):
    """Creates DynamoDB tables with on-demand capacity mode based on the schema."""
    # Create Users Table
    create_table_on_demand(
        dynamodb=dynamodb,
        table_name="Users",
        partition_key="location",  # Partitioned by location
        sort_key="user_id"  # Sort key for unique records
    )

    # Create Regional Trends Table
    create_table_on_demand(
        dynamodb=dynamodb,
        table_name="RegionalTrends",
        partition_key="region",  # Partitioned by region
        sort_key="regional_trends_id"  # Sort key for unique trends
    )

    # Create Content Table
    create_table_on_demand(
        dynamodb=dynamodb,
        table_name="Content",
        partition_key="genre",  # Partitioned by genre
        sort_key="content_id"  # Sort key for unique content
    )

    # Create Interaction History Table
    create_table_on_demand(
        dynamodb=dynamodb,
        table_name="InteractionHistory",
        partition_key="user_id",  # Partitioned by user
        sort_key="interaction_history_id"  # Sort key for unique interactions
    )


def enable_point_in_time_recovery(dynamodb, table_name):
    """Enable Point-in-Time Recovery (PITR) for fault tolerance."""
    try:
        dynamodb.meta.client.update_continuous_backups(
            TableName=table_name,
            PointInTimeRecoverySpecification={
                'PointInTimeRecoveryEnabled': True
            }
        )
        print(f"Point-in-Time Recovery enabled for {table_name} in region {dynamodb.meta.client.meta.region_name}.")
    except ClientError as e:
        print(f"ClientError: {e.response['Error']['Message']} while enabling PITR for {table_name} in region {dynamodb.meta.client.meta.region_name}")
    except Exception as e:
        print(f"Unexpected error while enabling PITR for {table_name} in region {dynamodb.meta.client.meta.region_name}: {e}")


def setup_fault_tolerance(dynamodb):
    """Setup fault tolerance for all tables."""
    tables = ["Users", "RegionalTrends", "Content", "InteractionHistory"]

    for table in tables:
        enable_point_in_time_recovery(dynamodb, table)


def main():
    # Iterate over each region and set up the tables
    for region in regions:
        print(f"Setting up DynamoDB in region {region}...")
        dynamodb = initialize_dynamodb(region)
        create_tables_on_demand(dynamodb)
        setup_fault_tolerance(dynamodb)
        print(f"DynamoDB setup completed in region {region}!")


if __name__ == "__main__":
    try:
        print("Starting DynamoDB On-Demand setup in multiple regions...")
        main()
        print("DynamoDB setup with On-Demand capacity mode completed in all regions!")
    except ClientError as e:
        print(f"ClientError during setup: {e.response['Error']['Message']}")
    except Exception as e:
        print(f"Unexpected error during setup: {e}")
