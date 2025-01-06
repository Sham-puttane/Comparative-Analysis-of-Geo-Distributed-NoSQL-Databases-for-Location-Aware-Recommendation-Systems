








import time
import statistics
import logging
from typing import List, Dict, Any
from pymongo import MongoClient
from concurrent.futures import ThreadPoolExecutor, as_completed
import psutil
import plotly.graph_objs as plt
import plotly.io as pio
import numpy as np

class EnhancedQueryPerformanceAnalyzer:
    def __init__(self, connection_string: str, database: str):
        """
        Initialize the performance analyzer with enhanced logging and visualization
        
        Args:
            connection_string (str): MongoDB connection string
            database (str): Database name
        """
        self.client = MongoClient(connection_string)
        self.db = self.client[database]
        
        # Configure enhanced logging
        logging.basicConfig(
            level=logging.INFO, 
            format='%(asctime)s | %(levelname)-8s | %(message)s',
            filename='query_performance_detailed.log',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        self.logger = logging.getLogger(__name__)

    def measure_query_performance(
        self, 
        collection: str, 
        pipeline: List[Dict[str, Any]], 
        query_name: str = "Default Query",
        num_requests: int = 100, 
        concurrent_users: int = 10
    ) -> Dict[str, float]:
        """
        Comprehensively measure query performance with millisecond-level precision
        
        Args:
            collection (str): Collection to query
            pipeline (list): MongoDB aggregation pipeline
            query_name (str): Name for identifying the specific query
            num_requests (int): Number of requests to simulate
            concurrent_users (int): Number of concurrent users
        
        Returns:
            dict: Detailed performance metrics
        """
        # Individual query response times
        response_times: List[float] = []
        query_results: List[Any] = []
        
        def execute_query():
            """Execute single query and track response time with high precision"""
            start_time = time.perf_counter()
            try:
                result = list(self.db[collection].aggregate(pipeline))
                response_time = (time.perf_counter() - start_time) * 1000  # Convert to milliseconds
                response_times.append(response_time)
                query_results.append(result)
                return result
            except Exception as e:
                self.logger.error(f"Query execution error for {query_name}: {e}")
                return None

        # Detailed logging of query parameters
        self.logger.info(f"Performance Test Started: {query_name}")
        self.logger.info(f"Collection: {collection}")
        self.logger.info(f"Concurrent Users: {concurrent_users}")
        self.logger.info(f"Total Requests: {num_requests}")
        self.logger.info(f"Pipeline: {pipeline}")

        # Track system resources before and during query
        initial_cpu = psutil.cpu_percent()
        initial_memory = psutil.virtual_memory().percent

        # Concurrent query execution
        start_time = time.perf_counter()
        with ThreadPoolExecutor(max_workers=concurrent_users) as executor:
            futures = [executor.submit(execute_query) for _ in range(num_requests)]
            list(as_completed(futures))  # Wait for all futures
        
        total_execution_time = (time.perf_counter() - start_time) * 1000  # milliseconds

        # Calculate performance metrics with millisecond precision
        metrics = {
            'total_execution_time_ms': total_execution_time,
            'throughput_queries_per_sec': num_requests / (total_execution_time / 1000),
            'avg_response_time_ms': statistics.mean(response_times),
            'min_response_time_ms': min(response_times),
            'max_response_time_ms': max(response_times),
            'response_time_std_dev_ms': statistics.stdev(response_times) if len(response_times) > 1 else 0,
            'cpu_utilization_increase': psutil.cpu_percent() - initial_cpu,
            'memory_utilization_increase': psutil.virtual_memory().percent - initial_memory,
            'total_requests': num_requests,
            'concurrent_users': concurrent_users
        }

        # Enhanced detailed logging
        self._log_performance_metrics(query_name, metrics)
        
        # Create interactive visualization
        #self._create_interactive_visualization(response_times, query_name)

        return metrics

    def _log_performance_metrics(self, query_name: str, metrics: Dict[str, float]):
        """
        Log performance metrics with detailed, human-readable format
        
        Args:
            query_name (str): Name of the query being analyzed
            metrics (dict): Performance metrics to log
        """
        self.logger.info(f"\n{'='*50}")
        self.logger.info(f"Performance Metrics for: {query_name}")
        self.logger.info(f"{'='*50}")
        
        # Format and log each metric with descriptive text
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

    def _create_interactive_visualization(self, response_times: List[float], query_name: str):
        """
        Create an interactive Plotly visualization of response times
        
        Args:
            response_times (list): List of response times in milliseconds
            query_name (str): Name of the query for plot title
        """
        # Calculate optimal number of bins using Sturges' rule
        num_bins = int(1 + 3.322 * np.log10(len(response_times)))
        
        # Create interactive histogram
        histogram = plt.Figure(data=[
            plt.Histogram(
                x=response_times, 
                nbinsx=num_bins,  # Use calculated number of bins 
                marker_color='skyblue', 
                marker_line_color='black',
                marker_line_width=1
            )
        ])
        
        # Customize layout
        histogram.update_layout(
            title=f'Response Time Distribution - {query_name}',
            xaxis_title='Response Time (milliseconds)',
            yaxis_title='Frequency',
            template='plotly_white'
        )

        # Create interactive box plot
        boxplot = plt.Figure(data=[
            plt.Box(
                y=response_times,
                marker_color='lightgreen',
                boxmean=True  # Shows the mean as a dashed line
            )
        ])
        
        boxplot.update_layout(
            title=f'Response Time Box Plot - {query_name}',
            yaxis_title='Response Time (milliseconds)',
            template='plotly_white'
        )

        # Save interactive plots
        pio.write_html(histogram, file=f'{query_name}_response_histogram.html')
        pio.write_html(boxplot, file=f'{query_name}_response_boxplot.html')
def main():
    # MongoDB connection and performance measurement
    analyzer = EnhancedQueryPerformanceAnalyzer(
        connection_string="mongodb://localhost:27015/", 
        database="DDS_Project"
    )

    # Regional query performance
    regional_pipeline = [
         { 
        "$match": { "region": "South America" }
    },
    {
        "$sort": {
            "engagement_metrics.total_views": -1,
            "engagement_metrics.total_likes": -1
        }
    },
    {
        "$lookup": {
            "from": "content",
            "localField": "top_content",
            "foreignField": "title",
            "as": "content_details"
        }
    },
    { 
        "$unwind": "$content_details"
    },
    {
        "$project": {
            "_id": 0,
            "Content Title": "$top_content",
            "Content Type": "$content_details.type",
            "Total Views": "$engagement_metrics.total_views",
            "Total Likes": "$engagement_metrics.total_likes"
        }
    },
    { 
        "$limit": 10
    }
    ]

    regional_metrics = analyzer.measure_query_performance(
        collection="regional_trends", 
        pipeline=regional_pipeline, 
        query_name="South America Regional Trends",
        num_requests=200, 
        concurrent_users=20
    )

    # Global query performance
    global_pipeline = [
        {"$group": {
            "_id": "$top_content",
            "total_views": {"$sum": "$engagement_metrics.total_views"}
        }},
        {"$sort": {"total_views": -1}},
        {"$limit": 5}
    ]

    global_metrics = analyzer.measure_query_performance(
        collection="regional_trends", 
        pipeline=global_pipeline, 
        query_name="Global Content Trends",
        num_requests=1000, 
        concurrent_users=100
    )

if __name__ == "__main__":
    main()























































































'''import time
from pymongo import MongoClient
from concurrent.futures import ThreadPoolExecutor

def measure_regional_query_performance(location, num_requests=100, concurrent_users=10):
    client = MongoClient("mongodb://localhost:27015/")
    db = client["DDS_Project"]

    # Define the regional query pipeline
    pipeline = [
        {"$match": {"region": location}},
        {"$sort": {
            "engagement_metrics.total_views": -1,
            "engagement_metrics.total_likes": -1
        }},
        {"$lookup": {
            "from": "content",
            "localField": "top_content",
            "foreignField": "title",
            "as": "content_details"
        }},
        {"$unwind": "$content_details"},
        {"$project": {
            "region": 1,
            "top_content": 1,
            "engagement_metrics": 1,
            "details": {
                "title": "$content_details.title",
                "genre": "$content_details.genre",
                "type": "$content_details.type",
                "metadata": "$content_details.metadata"
            }
        }},
        {"$limit": 10}
    ]

    # Measure response time for a single query
    start_time = time.time()
    db.regional_trends.aggregate(pipeline)
    response_time = time.time() - start_time
    print(f"Response Time for Regional Query (Location: {location}): {response_time:.4f} seconds")

    # Simulate concurrent queries to measure throughput
    def execute_query():
        db.regional_trends.aggregate(pipeline)

    start_time = time.time()
    with ThreadPoolExecutor(max_workers=concurrent_users) as executor:
        for _ in range(num_requests):
            executor.submit(execute_query)
    total_time = time.time() - start_time

    throughput = num_requests / total_time
    print(f"Throughput for Regional Query (Location: {location}): {throughput:.2f} queries/second")


def measure_global_query_performance(num_requests=100, concurrent_users=10):
    client = MongoClient("mongodb://localhost:27015/")
    db = client["DDS_Project"]

    # Define the global query pipeline
    pipeline = [
        {"$group": {
            "_id": "$top_content",
            "total_views": {"$sum": "$engagement_metrics.total_views"},
            "total_likes": {"$sum": "$engagement_metrics.total_likes"},
            "regions": {"$addToSet": "$region"}
        }},
        {"$match": {"regions.3": {"$exists": True}}},
        {"$sort": {"total_views": -1, "total_likes": -1}},
        {"$lookup": {
            "from": "content",
            "localField": "_id",
            "foreignField": "title",
            "as": "content_details"
        }},
        {"$unwind": "$content_details"},
        {"$project": {
            "content_title": "$_id",
            "total_views": 1,
            "total_likes": 1,
            "regions": 1,
            "details": {
                "genre": "$content_details.genre",
                "type": "$content_details.type",
                "metadata": "$content_details.metadata"
            }
        }},
        {"$limit": 5}
    ]

    # Measure response time for a single query
    start_time = time.time()
    db.regional_trends.aggregate(pipeline)
    response_time = time.time() - start_time
    print(f"Response Time for Global Query: {response_time:.4f} seconds")

    # Simulate concurrent queries to measure throughput
    def execute_query():
        db.regional_trends.aggregate(pipeline)

    start_time = time.time()
    with ThreadPoolExecutor(max_workers=concurrent_users) as executor:
        for _ in range(num_requests):
            executor.submit(execute_query)
    total_time = time.time() - start_time

    throughput = num_requests / total_time
    print(f"Throughput for Global Query: {throughput:.2f} queries/second")



# Measure performance for regional query
measure_regional_query_performance(location="Asia", num_requests=200, concurrent_users=20)

# Measure performance for global query
measure_global_query_performance(num_requests=1000, concurrent_users=100)'''
