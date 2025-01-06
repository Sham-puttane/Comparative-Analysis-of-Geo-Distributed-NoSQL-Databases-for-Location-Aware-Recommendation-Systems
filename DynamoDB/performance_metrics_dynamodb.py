import boto3
from boto3.dynamodb.conditions import Key
from botocore.config import Config
from collections import defaultdict
import time
import statistics
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
import psutil
from typing import List, Dict, Any
from decouple import config


class DynamoDBPerformanceAnalyzer:
    def __init__(self):
        """
        Initialize the performance analyzer for DynamoDB with a larger connection pool.
        """
        self.regions = {
            "us-east-1": "North America",
            "sa-east-1": "South America",
            "eu-central-1": "Europe",
            "ap-south-1": "Asia"
        }

        # Configure connection pool
        self.config = Config(
            retries={"max_attempts": 10, "mode": "standard"},  # Retry settings
            max_pool_connections=100  # Increase connection pool size
        )

        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s | %(levelname)-8s | %(message)s",
            filename="dynamodb_performance.log",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        self.logger = logging.getLogger(__name__)

        # Initialize DynamoDB resources once per region
        self.dynamodb_resources = {
            region: boto3.resource("dynamodb", region_name=region, config=self.config, aws_access_key_id=config('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY'))
            for region in self.regions.keys()
        }

    def initialize_dynamodb(self, region_name: str):
        """Get the pre-initialized DynamoDB resource for a region."""
        return self.dynamodb_resources[region_name]

    def scan_table(self, table_name: str, dynamodb):
        """
        Scan a DynamoDB table and retrieve all items.
        """
        table = dynamodb.Table(table_name)
        try:
            response = table.scan()
            return response.get("Items", [])
        except Exception as e:
            self.logger.error(f"Error scanning {table_name}: {e}")
            return []

    def measure_query_performance(
        self, table_name: str, query_func, query_name: str, num_requests: int, concurrent_users: int
    ) -> Dict[str, float]:
        """
        Measure the performance of a query function.

        Args:
            table_name (str): DynamoDB table name
            query_func (callable): Function to execute the query
            query_name (str): Name of the query
            num_requests (int): Number of requests to simulate
            concurrent_users (int): Number of concurrent users

        Returns:
            dict: Performance metrics
        """
        response_times: List[float] = []

        def execute_query():
            """Execute a single query and track response time."""
            start_time = time.perf_counter()
            query_func()
            response_time = (time.perf_counter() - start_time) * 1000  # Convert to ms
            response_times.append(response_time)

        # Initial system stats
        initial_cpu = psutil.cpu_percent()
        initial_memory = psutil.virtual_memory().percent

        # Execute queries concurrently
        start_time = time.perf_counter()
        with ThreadPoolExecutor(max_workers=concurrent_users) as executor:
            futures = [executor.submit(execute_query) for _ in range(num_requests)]
            list(as_completed(futures))  # Wait for all futures
        total_execution_time = (time.perf_counter() - start_time) * 1000  # in ms

        # Calculate metrics
        metrics = {
            "total_execution_time_ms": total_execution_time,
            "throughput_queries_per_sec": num_requests / (total_execution_time / 1000),
            "avg_response_time_ms": statistics.mean(response_times),
            "min_response_time_ms": min(response_times),
            "max_response_time_ms": max(response_times),
            "response_time_std_dev_ms": statistics.stdev(response_times)
            if len(response_times) > 1
            else 0,
            "cpu_utilization_increase": psutil.cpu_percent() - initial_cpu,
            "memory_utilization_increase": psutil.virtual_memory().percent - initial_memory,
        }

        # Log performance metrics
        self._log_performance_metrics(query_name, metrics)
        return metrics
    
    def _log_performance_metrics(self, query_name: str, metrics: Dict[str, float]):
        """
        Log performance metrics with detailed, human-readable format.
        
        Args:
            query_name (str): Name of the query being analyzed
            metrics (dict): Performance metrics to log
        """
        self.logger.info(f"\n{'='*50}")
        self.logger.info(f"Performance Metrics for: {query_name}")
        self.logger.info(f"{'='*50}")
        
        log_format = [
            ("Total Execution Time", "total_execution_time_ms", "ms"),
            ("Throughput", "throughput_queries_per_sec", "queries/sec"),
            ("Average Response Time", "avg_response_time_ms", "ms"),
            ("Minimum Response Time", "min_response_time_ms", "ms"),
            ("Maximum Response Time", "max_response_time_ms", "ms"),
            ("Response Time Std Deviation", "response_time_std_dev_ms", "ms"),
            ("CPU Utilization Increase", "cpu_utilization_increase", "%"),
            ("Memory Utilization Increase", "memory_utilization_increase", "%")
        ]
        
        for description, key, unit in log_format:
            self.logger.info(f"{description:<30}: {metrics[key]:.2f} {unit}")
        
        self.logger.info(f"{'='*50}\n")

    def regional_query(self, dynamodb, region):
        """
        Perform the regional query in region.
        """
        table_name = "RegionalTrends"
        items = self.scan_table(table_name, dynamodb)

        # Filter and sort items for region
        asia_items = [item for item in items if item.get("region") == region]
        sorted_items = sorted(
            asia_items,
            key=lambda x: (
                -int(x["engagement_metrics"]["total_views"]),
                -int(x["engagement_metrics"]["total_likes"]),
            ),
        )

        return sorted_items[:10]  # Limit to top 10

    def global_query(self):
        """
        Perform the global query across all regions.
        """
        table_name = "RegionalTrends"
        all_items = []

        # Scan tables in all regions
        for region, _ in self.regions.items():
            dynamodb = self.initialize_dynamodb(region)
            items = self.scan_table(table_name, dynamodb)
            all_items.extend(items)

        # Aggregate by top_content
        aggregated = defaultdict(int)
        for item in all_items:
            top_content = item.get("top_content")
            total_views = int(item["engagement_metrics"]["total_views"])
            if top_content:
                aggregated[top_content] += total_views

        # Sort by total_views and return top 5
        sorted_aggregated = sorted(aggregated.items(), key=lambda x: -x[1])
        return sorted_aggregated[:5]

    def execute_queries(self):
        """
        Execute both regional and global queries and measure their performance.
        """
        # Regional Query in Asia
        self.logger.info("Executing Regional Query (Asia)...")
        asia_dynamodb = self.initialize_dynamodb("ap-south-1")
        regional_metrics = self.measure_query_performance(
            table_name="RegionalTrends",
            query_func=lambda: self.regional_query(asia_dynamodb, region='Asia'),
            query_name="Asia Regional Query",
            num_requests=200,
            concurrent_users=20,
        )
        self.logger.info(f"Regional Query Metrics: {regional_metrics}")
        
        # Regional Query in North America
        self.logger.info("Executing Regional Query (North America)...")
        north_america_dynamodb = self.initialize_dynamodb("us-east-1")
        regional_metrics = self.measure_query_performance(
            table_name="RegionalTrends",
            query_func=lambda: self.regional_query(north_america_dynamodb, region='North America'),
            query_name="North America Regional Query",
            num_requests=200,
            concurrent_users=20,
        )
        self.logger.info(f"Regional Query Metrics: {regional_metrics}")
        
        # Regional Query in South America
        self.logger.info("Executing Regional Query (Asia)...")
        south_america_dynamodb = self.initialize_dynamodb("sa-east-1")
        regional_metrics = self.measure_query_performance(
            table_name="RegionalTrends",
            query_func=lambda: self.regional_query(south_america_dynamodb, region='South America'),
            query_name="South America Regional Query",
            num_requests=200,
            concurrent_users=20,
        )
        self.logger.info(f"Regional Query Metrics: {regional_metrics}")
        
        # Regional Query in Europe
        self.logger.info("Executing Regional Query (Asia)...")
        europe_dynamodb = self.initialize_dynamodb("eu-central-1")
        regional_metrics = self.measure_query_performance(
            table_name="RegionalTrends",
            query_func=lambda: self.regional_query(europe_dynamodb, region='Europe'),
            query_name="Europe Regional Query",
            num_requests=200,
            concurrent_users=20,
        )
        self.logger.info(f"Regional Query Metrics: {regional_metrics}")

        # Global Query
        self.logger.info("Executing Global Query (All Regions)...")
        global_metrics = self.measure_query_performance(
            table_name="RegionalTrends",
            query_func=self.global_query,
            query_name="Global Content Query",
            num_requests=1000,
            concurrent_users=100,
        )
        self.logger.info(f"Global Query Metrics: {global_metrics}")


# Main Script
def main():
    analyzer = DynamoDBPerformanceAnalyzer()
    analyzer.execute_queries()


if __name__ == "__main__":
    main()
