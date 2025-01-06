from flask import Flask, render_template, jsonify
import pandas as pd
import plotly
import plotly.graph_objs as go
import json

app = Flask(__name__)

# Comprehensive performance data structure with full metrics
performance_data = {
    'MongoDB': {
        'Asia': {
            'Local': {
                'metrics': {
                    'total_execution_time': 704.64,
                    'throughput': 283.83,
                    'avg_response_time': 67.91,
                    'min_response_time': 23.71,
                    'max_response_time': 229.20,
                    'response_time_std_deviation': 40.51,
                    'cpu_utilization_increase': 70.70,
                    'memory_utilization_increase': 0.00
                },
                'recommendations': [
                    {
    'Content Title': 'Series west issue.',
    'Content Type': 'movie',
    'Total Views': 9951,
    'Total Likes': 3206
  },
  {
    'Content Title': 'Explain power experience perhaps.',
    'Content Type': 'movie',
    'Total Views': 9813,
    'Total Likes': 1412
  },
  {
    'Content Title': 'Just order reduce.',
    'Content Type': 'webseries',
    'Total Views': 9764,
    'Total Likes': 4649
  },
  {
    'Content Title': 'Music management expert.',
    'Content Type': 'movie',
    'Total Views': 9641,
    'Total Likes': 3475
  },
  {
    'Content Title': 'Myself film.',
    'Content Type': 'webseries',
    'Total Views': 9506,
    'Total Likes': 808
  },
  {
    'Content Title': 'Environmental owner.',
    'Content Type': 'documentary',
    'Total Views': 9296,
    'Total Likes': 4481
  },
  {
    'Content Title': 'Fall face along.',
    'Content Type': 'movie',
    'Total Views': 9270,
    'Total Likes': 4944
  },
  {
    'Content Title': 'Pick skin.',
    'Content Type': 'webseries',
    'Total Views': 9233,
    'Total Likes': 850
  },
  {
    'Content Title': 'Up physical.',
    'Content Type': 'movie',
    'Total Views': 9128,
    'Total Likes': 815
  },
  {
    'Content Title': 'Authority suddenly address too.',
    'Content Type': 'movie',
    'Total Views': 9116,
    'Total Likes': 2175
  }
                ]
            },
            'Global': {
                'metrics': {
                    'total_execution_time': 2236.44,
                    'throughput': 447.14,
                    'avg_response_time': 121.35,
                    'min_response_time': 5.48,
                    'max_response_time': 586.15,
                    'response_time_std_deviation': 114.07,
                    'cpu_utilization_increase':  -0.90,
                    'memory_utilization_increase': 0.10
                },
                'recommendations': [
                    {
    'Content Title': 'Rise beat central democratic.',
    'Content Type': 'webseries',
    'Total Views': 33744,
    'Total Likes': 14824
  },
  {
    'Content Title': 'Condition.',
    'Content Type': 'webseries',
    'Total Views': 33250,
    'Total Likes': 15218
  },
  {
    'Content Title': 'Fish that.',
    'Content Type': 'movie',
    'Total Views': 32268,
    'Total Likes': 9707
  },
  {
    'Content Title': 'Chance.',
    'Content Type': 'webseries',
    'Total Views': 31944,
    'Total Likes': 9094
  },
  {
    'Content Title': 'Family.',
    'Content Type': 'movie',
    'Total Views': 31873,
    'Total Likes': 4956
  }
                ]
            }
        },
        'Europe': {
            'Local': {
                'metrics': {
                    'total_execution_time': 577.03,
                    'throughput': 346.60,
                    'avg_response_time': 54.55,
                    'min_response_time': 22.68,
                    'max_response_time': 156.18,
                    'response_time_std_deviation': 26.19,
                    'cpu_utilization_increase': 61.40,
                    'memory_utilization_increase': 0.10
                },
                'recommendations': [
                    {
    'Content Title': 'Party TV conference.',
    'Content Type': 'documentary',
    'Total Views': 9986,
    'Total Likes': 3008
  },
  {
    'Content Title': 'Community ready.',
    'Content Type': 'documentary',
    'Total Views': 9963,
    'Total Likes': 2111
  },
  {
    'Content Title': 'Think instead.',
    'Content Type': 'webseries',
    'Total Views': 9918,
    'Total Likes': 1588
  },
  {
    'Content Title': 'Environmental owner.',
    'Content Type': 'documentary',
    'Total Views': 9890,
    'Total Likes': 2000
  },
  {
    'Content Title': 'Might local.',
    'Content Type': 'webseries',
    'Total Views': 9732,
    'Total Likes': 1489
  },
  {
    'Content Title': 'Authority suddenly address too.',
    'Content Type': 'movie',
    'Total Views': 9603,
    'Total Likes': 4065
  },
  {
    'Content Title': 'Chance.',
    'Content Type': 'webseries',
    'Total Views': 9593,
    'Total Likes': 2545
  },
  {
    'Content Title': 'Week control everything.',
    'Content Type': 'documentary',
    'Total Views': 9463,
    'Total Likes': 4167
  },
  {
    'Content Title': 'Least bank give.',
    'Content Type': 'documentary',
    'Total Views': 9338,
    'Total Likes': 2925
  },
  {
    'Content Title': 'Recently but check six.',
    'Content Type': 'webseries',
    'Total Views': 9301,
    'Total Likes': 4888
  }
                ]
            },
            'Global': {
                'metrics': {
                    'total_execution_time': 1949.38,
                    'throughput': 512.98,
                    'avg_response_time': 148.48,
                    'min_response_time': 11.75,
                    'max_response_time': 730.78,
                    'response_time_std_deviation': 153.41,
                    'cpu_utilization_increase': 90.70,
                    'memory_utilization_increase': 0.10
                },
                'recommendations': [
                    {
    'Content Title': 'Rise beat central democratic.',
    'Content Type': 'webseries',
    'Total Views': 33744,
    'Total Likes': 14824
  },
  {
    'Content Title': 'Condition.',
    'Content Type': 'webseries',
    'Total Views': 33250,
    'Total Likes': 15218
  },
  {
    'Content Title': 'Fish that.',
    'Content Type': 'movie',
    'Total Views': 32268,
    'Total Likes': 9707
  },
  {
    'Content Title': 'Chance.',
    'Content Type': 'webseries',
    'Total Views': 31944,
    'Total Likes': 9094
  },
  {
    'Content Title': 'Family.',
    'Content Type': 'movie',
    'Total Views': 31873,
    'Total Likes': 4956
  }
                ]
            }
        },
        'North America': {
            'Local': {
                'metrics': {
                    'total_execution_time': 583.57,
                    'throughput': 342.72,
                    'avg_response_time': 56.44,
                    'min_response_time': 12.58,
                    'max_response_time': 162.56,
                    'response_time_std_deviation': 26.24,
                    'cpu_utilization_increase': 48.70,
                    'memory_utilization_increase': 0.10
                },
                'recommendations': [
                    {
    'Content Title': 'Leader head.',
    'Content Type': 'documentary',
    'Total Views': 9962,
    'Total Likes': 4904
  },
  {
    'Content Title': 'Nation item.',
    'Content Type': 'documentary',
    'Total Views': 9951,
    'Total Likes': 1947
  },
  {
    'Content Title': 'Hundred shoulder might.',
    'Content Type': 'documentary',
    'Total Views': 9935,
    'Total Likes': 749
  },
  {
    'Content Title': 'Amount public.',
    'Content Type': 'webseries',
    'Total Views': 9771,
    'Total Likes': 2136
  },
  {
    'Content Title': 'Tough hear.',
    'Content Type': 'documentary',
    'Total Views': 9745,
    'Total Likes': 4604
  },
  {
    'Content Title': 'Wear mind.',
    'Content Type': 'webseries',
    'Total Views': 9669,
    'Total Likes': 1907
  },
  {
    'Content Title': 'World four decide a.',
    'Content Type': 'movie',
    'Total Views': 9646,
    'Total Likes': 2400
  },
  {
    'Content Title': 'Short price officer.',
    'Content Type': 'movie',
    'Total Views': 9521,
    'Total Likes': 2943
  },
  {
    'Content Title': 'Note right.',
    'Content Type': 'documentary',
    'Total Views': 9429,
    'Total Likes': 2636
  },
  {
    'Content Title': 'Rise beat central democratic.',
    'Content Type': 'webseries',
    'Total Views': 9324,
    'Total Likes': 2806
  }
                ]
            },
            'Global': {
                'metrics': {
                    'total_execution_time': 2450.97,
                    'throughput': 408.00,
                    'avg_response_time': 175.25,
                    'min_response_time': 14.73,
                    'max_response_time': 642.87,
                    'response_time_std_deviation': 114.69,
                    'cpu_utilization_increase': 95.60,
                    'memory_utilization_increase': 0.30
                },
                'recommendations': [
                    {
    'Content Title': 'Rise beat central democratic.',
    'Content Type': 'webseries',
    'Total Views': 33744,
    'Total Likes': 14824
  },
  {
    'Content Title': 'Condition.',
    'Content Type': 'webseries',
    'Total Views': 33250,
    'Total Likes': 15218
  },
  {
    'Content Title': 'Fish that.',
    'Content Type': 'movie',
    'Total Views': 32268,
    'Total Likes': 9707
  },
  {
    'Content Title': 'Chance.',
    'Content Type': 'webseries',
    'Total Views': 31944,
    'Total Likes': 9094
  },
  {
    'Content Title': 'Family.',
    'Content Type': 'movie',
    'Total Views': 31873,
    'Total Likes': 4956
  }
                ]
            }
        },
        'South America': {
            'Local': {
                'metrics': {
                    'total_execution_time': 673.04,
                    'throughput': 297.16,
                    'avg_response_time': 64.08,
                    'min_response_time': 20.70,
                    'max_response_time': 307.35,
                    'response_time_std_deviation': 41.34,
                    'cpu_utilization_increase': 86.90,
                    'memory_utilization_increase': 0.00
                },
                'recommendations': [
                    {
    'Content Title': 'Chance.',
    'Content Type': 'webseries',
    'Total Views': 9827,
    'Total Likes': 1359
  },
  {
    'Content Title': 'Firm skin often.',
    'Content Type': 'movie',
    'Total Views': 9794,
    'Total Likes': 4095
  },
  {
    'Content Title': 'Head first cost.',
    'Content Type': 'webseries',
    'Total Views': 9483,
    'Total Likes': 677
  },
  {
    'Content Title': 'Condition.',
    'Content Type': 'webseries',
    'Total Views': 9466,
    'Total Likes': 4483
  },
  {
    'Content Title': 'Deep different.',
    'Content Type': 'webseries',
    'Total Views': 9382,
    'Total Likes': 3849
  },
  {
    'Content Title': 'Term save apply.',
    'Content Type': 'movie',
    'Total Views': 9293,
    'Total Likes': 3751
  },
  {
    'Content Title': 'Final stuff.',
    'Content Type': 'movie',
    'Total Views': 9231,
    'Total Likes': 603
  },
  {
    'Content Title': 'Member rich network.',
    'Content Type': 'webseries',
    'Total Views': 9011,
    'Total Likes': 1033
  },
  {
    'Content Title': 'Reveal try determine.',
    'Content Type': 'movie',
    'Total Views': 8926,
    'Total Likes': 4365
  },
  {
    'Content Title': 'Interest beautiful value.',
    'Content Type': 'movie',
    'Total Views': 8812,
    'Total Likes': 2408
  }
                ]
            },
            'Global': {
                'metrics': {
                    'total_execution_time': 2042.63,
                    'throughput': 489.56,
                    'avg_response_time': 140.64,
                    'min_response_time': 5.31,
                    'max_response_time': 471.54,
                    'response_time_std_deviation': 153.41,
                    'cpu_utilization_increase': 87.80,
                    'memory_utilization_increase': 0.20
                },
                'recommendations': [
                    {
    'Content Title': 'Rise beat central democratic.',
    'Content Type': 'webseries',
    'Total Views': 33744,
    'Total Likes': 14824
  },
  {
    'Content Title': 'Condition.',
    'Content Type': 'webseries',
    'Total Views': 33250,
    'Total Likes': 15218
  },
  {
    'Content Title': 'Fish that.',
    'Content Type': 'movie',
    'Total Views': 32268,
    'Total Likes': 9707
  },
  {
    'Content Title': 'Chance.',
    'Content Type': 'webseries',
    'Total Views': 31944,
    'Total Likes': 9094
  },
  {
    'Content Title': 'Family.',
    'Content Type': 'movie',
    'Total Views': 31873,
    'Total Likes': 4956
  }
                ]
            }
        }
        
    },
    'DynamoDB': {'Asia': {
            'Local': {
                'metrics': {
                    'total_execution_time': 4670.14,
                    'throughput': 42.83,
                    'avg_response_time': 456.54,
                    'min_response_time': 269.48,
                    'max_response_time': 1696.84,
                    'response_time_std_deviation': 406.37,
                    'cpu_utilization_increase': 4.60 ,
                    'memory_utilization_increase': 0.10 
                },
                'recommendations': [
                    {
    'Content Title': 'Series west issue.',
    'Content Type': 'movie',
    'Total Views': 9951,
    'Total Likes': 3206
  },
  {
    'Content Title': 'Explain power experience perhaps.',
    'Content Type': 'movie',
    'Total Views': 9813,
    'Total Likes': 1412
  },
  {
    'Content Title': 'Just order reduce.',
    'Content Type': 'webseries',
    'Total Views': 9764,
    'Total Likes': 4649
  },
  {
    'Content Title': 'Music management expert.',
    'Content Type': 'movie',
    'Total Views': 9641,
    'Total Likes': 3475
  },
  {
    'Content Title': 'Myself film.',
    'Content Type': 'webseries',
    'Total Views': 9506,
    'Total Likes': 808
  },
  {
    'Content Title': 'Environmental owner.',
    'Content Type': 'documentary',
    'Total Views': 9296,
    'Total Likes': 4481
  },
  {
    'Content Title': 'Fall face along.',
    'Content Type': 'movie',
    'Total Views': 9270,
    'Total Likes': 4944
  },
  {
    'Content Title': 'Pick skin.',
    'Content Type': 'webseries',
    'Total Views': 9233,
    'Total Likes': 850
  },
  {
    'Content Title': 'Up physical.',
    'Content Type': 'movie',
    'Total Views': 9128,
    'Total Likes': 815
  },
  {
    'Content Title': 'Authority suddenly address too.',
    'Content Type': 'movie',
    'Total Views': 9116,
    'Total Likes': 2175
  }
                ]
            },
            'Global': {
                'metrics': {
                    'total_execution_time': 17351.12,
                    'throughput':  57.63 ,
                    'avg_response_time': 1327.17 ,
                    'min_response_time': 716.43,
                    'max_response_time': 11835.05,
                    'response_time_std_deviation': 935.47,
                    'cpu_utilization_increase':  16.10 ,
                    'memory_utilization_increase': 0.50
                },
                'recommendations': [
                    {
    'Content Title': 'Rise beat central democratic.',
    'Content Type': 'webseries',
    'Total Views': 33744,
    'Total Likes': 14824
  },
  {
    'Content Title': 'Condition.',
    'Content Type': 'webseries',
    'Total Views': 33250,
    'Total Likes': 15218
  },
  {
    'Content Title': 'Fish that.',
    'Content Type': 'movie',
    'Total Views': 32268,
    'Total Likes': 9707
  },
  {
    'Content Title': 'Chance.',
    'Content Type': 'webseries',
    'Total Views': 31944,
    'Total Likes': 9094
  },
  {
    'Content Title': 'Family.',
    'Content Type': 'movie',
    'Total Views': 31873,
    'Total Likes': 4956
  }
                ]
            }
        },
        'Europe': {
            'Local': {
                'metrics': {
                    'total_execution_time': 4763.36 ,
                    'throughput': 41.99,
                    'avg_response_time': 328.07,
                    'min_response_time': 155.57,
                    'max_response_time': 4754.75 ,
                    'response_time_std_deviation': 490.30 ,
                    'cpu_utilization_increase': 8.80 ,
                    'memory_utilization_increase':-0.90
                },
                'recommendations': [
                    {
    'Content Title': 'Party TV conference.',
    'Content Type': 'documentary',
    'Total Views': 9986,
    'Total Likes': 3008
  },
  {
    'Content Title': 'Community ready.',
    'Content Type': 'documentary',
    'Total Views': 9963,
    'Total Likes': 2111
  },
  {
    'Content Title': 'Think instead.',
    'Content Type': 'webseries',
    'Total Views': 9918,
    'Total Likes': 1588
  },
  {
    'Content Title': 'Environmental owner.',
    'Content Type': 'documentary',
    'Total Views': 9890,
    'Total Likes': 2000
  },
  {
    'Content Title': 'Might local.',
    'Content Type': 'webseries',
    'Total Views': 9732,
    'Total Likes': 1489
  },
  {
    'Content Title': 'Authority suddenly address too.',
    'Content Type': 'movie',
    'Total Views': 9603,
    'Total Likes': 4065
  },
  {
    'Content Title': 'Chance.',
    'Content Type': 'webseries',
    'Total Views': 9593,
    'Total Likes': 2545
  },
  {
    'Content Title': 'Week control everything.',
    'Content Type': 'documentary',
    'Total Views': 9463,
    'Total Likes': 4167
  },
  {
    'Content Title': 'Least bank give.',
    'Content Type': 'documentary',
    'Total Views': 9338,
    'Total Likes': 2925
  },
  {
    'Content Title': 'Recently but check six.',
    'Content Type': 'webseries',
    'Total Views': 9301,
    'Total Likes': 4888
  }
                ]
            },
            'Global': {
                'metrics': {
                    'total_execution_time': 17351.12,
                    'throughput':  57.63 ,
                    'avg_response_time': 1327.17 ,
                    'min_response_time': 716.43,
                    'max_response_time': 11835.05,
                    'response_time_std_deviation': 935.47,
                    'cpu_utilization_increase':  16.10 ,
                    'memory_utilization_increase': 0.50
                },
                'recommendations': [
                    {
    'Content Title': 'Rise beat central democratic.',
    'Content Type': 'webseries',
    'Total Views': 33744,
    'Total Likes': 14824
  },
  {
    'Content Title': 'Condition.',
    'Content Type': 'webseries',
    'Total Views': 33250,
    'Total Likes': 15218
  },
  {
    'Content Title': 'Fish that.',
    'Content Type': 'movie',
    'Total Views': 32268,
    'Total Likes': 9707
  },
  {
    'Content Title': 'Chance.',
    'Content Type': 'webseries',
    'Total Views': 31944,
    'Total Likes': 9094
  },
  {
    'Content Title': 'Family.',
    'Content Type': 'movie',
    'Total Views': 31873,
    'Total Likes': 4956
  }
                ]
            }
        },
        'North America': {
            'Local': {
                'metrics': {
                    'total_execution_time': 1356.61,
                    'throughput': 147.43 ,
                    'avg_response_time': 127.91 ,
                    'min_response_time': 73.29,
                    'max_response_time': 490.19,
                    'response_time_std_deviation': 110.01,
                    'cpu_utilization_increase': -64.00,
                    'memory_utilization_increase': 0.60
                },
                'recommendations': [
                    {
    'Content Title': 'Leader head.',
    'Content Type': 'documentary',
    'Total Views': 9962,
    'Total Likes': 4904
  },
  {
    'Content Title': 'Nation item.',
    'Content Type': 'documentary',
    'Total Views': 9951,
    'Total Likes': 1947
  },
  {
    'Content Title': 'Hundred shoulder might.',
    'Content Type': 'documentary',
    'Total Views': 9935,
    'Total Likes': 749
  },
  {
    'Content Title': 'Amount public.',
    'Content Type': 'webseries',
    'Total Views': 9771,
    'Total Likes': 2136
  },
  {
    'Content Title': 'Tough hear.',
    'Content Type': 'documentary',
    'Total Views': 9745,
    'Total Likes': 4604
  },
  {
    'Content Title': 'Wear mind.',
    'Content Type': 'webseries',
    'Total Views': 9669,
    'Total Likes': 1907
  },
  {
    'Content Title': 'World four decide a.',
    'Content Type': 'movie',
    'Total Views': 9646,
    'Total Likes': 2400
  },
  {
    'Content Title': 'Short price officer.',
    'Content Type': 'movie',
    'Total Views': 9521,
    'Total Likes': 2943
  },
  {
    'Content Title': 'Note right.',
    'Content Type': 'documentary',
    'Total Views': 9429,
    'Total Likes': 2636
  },
  {
    'Content Title': 'Rise beat central democratic.',
    'Content Type': 'webseries',
    'Total Views': 9324,
    'Total Likes': 2806
  }
                ]
            },
            'Global': {
                'metrics': {
                    'total_execution_time': 17351.12,
                    'throughput':  57.63 ,
                    'avg_response_time': 1327.17 ,
                    'min_response_time': 716.43,
                    'max_response_time': 11835.05,
                    'response_time_std_deviation': 935.47,
                    'cpu_utilization_increase':  16.10 ,
                    'memory_utilization_increase': 0.50
                },
                'recommendations': [
                    {
    'Content Title': 'Rise beat central democratic.',
    'Content Type': 'webseries',
    'Total Views': 33744,
    'Total Likes': 14824
  },
  {
    'Content Title': 'Condition.',
    'Content Type': 'webseries',
    'Total Views': 33250,
    'Total Likes': 15218
  },
  {
    'Content Title': 'Fish that.',
    'Content Type': 'movie',
    'Total Views': 32268,
    'Total Likes': 9707
  },
  {
    'Content Title': 'Chance.',
    'Content Type': 'webseries',
    'Total Views': 31944,
    'Total Likes': 9094
  },
  {
    'Content Title': 'Family.',
    'Content Type': 'movie',
    'Total Views': 31873,
    'Total Likes': 4956
  }
                ]
            }
        },
        'South America': {
            'Local': {
                'metrics': {
                    'total_execution_time': 673.04,
                    'throughput': 297.16,
                    'avg_response_time': 64.08,
                    'min_response_time': 20.70,
                    'max_response_time': 307.35,
                    'response_time_std_deviation': 41.34,
                    'cpu_utilization_increase': 86.90,
                    'memory_utilization_increase': 0.00
                },
                'recommendations': [
                    {
    'Content Title': 'Chance.',
    'Content Type': 'webseries',
    'Total Views': 9827,
    'Total Likes': 1359
  },
  {
    'Content Title': 'Firm skin often.',
    'Content Type': 'movie',
    'Total Views': 9794,
    'Total Likes': 4095
  },
  {
    'Content Title': 'Head first cost.',
    'Content Type': 'webseries',
    'Total Views': 9483,
    'Total Likes': 677
  },
  {
    'Content Title': 'Condition.',
    'Content Type': 'webseries',
    'Total Views': 9466,
    'Total Likes': 4483
  },
  {
    'Content Title': 'Deep different.',
    'Content Type': 'webseries',
    'Total Views': 9382,
    'Total Likes': 3849
  },
  {
    'Content Title': 'Term save apply.',
    'Content Type': 'movie',
    'Total Views': 9293,
    'Total Likes': 3751
  },
  {
    'Content Title': 'Final stuff.',
    'Content Type': 'movie',
    'Total Views': 9231,
    'Total Likes': 603
  },
  {
    'Content Title': 'Member rich network.',
    'Content Type': 'webseries',
    'Total Views': 9011,
    'Total Likes': 1033
  },
  {
    'Content Title': 'Reveal try determine.',
    'Content Type': 'movie',
    'Total Views': 8926,
    'Total Likes': 4365
  },
  {
    'Content Title': 'Interest beautiful value.',
    'Content Type': 'movie',
    'Total Views': 8812,
    'Total Likes': 2408
  }
                ]
            },
            'Global': {
                'metrics': {
                    'total_execution_time': 17351.12,
                    'throughput':  57.63 ,
                    'avg_response_time': 1327.17 ,
                    'min_response_time': 716.43,
                    'max_response_time': 11835.05,
                    'response_time_std_deviation': 935.47,
                    'cpu_utilization_increase':  16.10 ,
                    'memory_utilization_increase': 0.50
                },
                'recommendations': [
                    {
    'Content Title': 'Rise beat central democratic.',
    'Content Type': 'webseries',
    'Total Views': 33744,
    'Total Likes': 14824
  },
  {
    'Content Title': 'Condition.',
    'Content Type': 'webseries',
    'Total Views': 33250,
    'Total Likes': 15218
  },
  {
    'Content Title': 'Fish that.',
    'Content Type': 'movie',
    'Total Views': 32268,
    'Total Likes': 9707
  },
  {
    'Content Title': 'Chance.',
    'Content Type': 'webseries',
    'Total Views': 31944,
    'Total Likes': 9094
  },
  {
    'Content Title': 'Family.',
    'Content Type': 'movie',
    'Total Views': 31873,
    'Total Likes': 4956
  }
                ]
            }
        }},
    'ElasticSearch': {'Asia': {
            'Local': {
                'metrics': {
                    'total_execution_time': 884.39,
                    'throughput':  226.14,
                    'avg_response_time': 884.39,
                    'min_response_time': 884.39,
                    'max_response_time': 884.39,
                    'response_time_std_deviation': 0.0,
                    'cpu_utilization_increase':  7.20,
                    'memory_utilization_increase': -0.20
                },
                'recommendations': [
                    {
    'Content Title': 'Series west issue.',
    'Content Type': 'movie',
    'Total Views': 9951,
    'Total Likes': 3206
  },
  {
    'Content Title': 'Explain power experience perhaps.',
    'Content Type': 'movie',
    'Total Views': 9813,
    'Total Likes': 1412
  },
  {
    'Content Title': 'Just order reduce.',
    'Content Type': 'webseries',
    'Total Views': 9764,
    'Total Likes': 4649
  },
  {
    'Content Title': 'Music management expert.',
    'Content Type': 'movie',
    'Total Views': 9641,
    'Total Likes': 3475
  },
  {
    'Content Title': 'Myself film.',
    'Content Type': 'webseries',
    'Total Views': 9506,
    'Total Likes': 808
  },
  {
    'Content Title': 'Environmental owner.',
    'Content Type': 'documentary',
    'Total Views': 9296,
    'Total Likes': 4481
  },
  {
    'Content Title': 'Fall face along.',
    'Content Type': 'movie',
    'Total Views': 9270,
    'Total Likes': 4944
  },
  {
    'Content Title': 'Pick skin.',
    'Content Type': 'webseries',
    'Total Views': 9233,
    'Total Likes': 850
  },
  {
    'Content Title': 'Up physical.',
    'Content Type': 'movie',
    'Total Views': 9128,
    'Total Likes': 815
  },
  {
    'Content Title': 'Authority suddenly address too.',
    'Content Type': 'movie',
    'Total Views': 9116,
    'Total Likes': 2175
  }
                ]
            },
            'Global': {
                'metrics': {
                    'total_execution_time': 1604.27,
                    'throughput': 124.67,
                    'avg_response_time': 57.28,
                    'min_response_time': 9.10,
                    'max_response_time': 1233.34,
                    'response_time_std_deviation': 125.51,
                    'cpu_utilization_increase':  -1.40,
                    'memory_utilization_increase': 1.90
                },
                'recommendations': [
                    {
    'Content Title': 'Rise beat central democratic.',
    'Content Type': 'webseries',
    'Total Views': 33744,
    'Total Likes': 14824
  },
  {
    'Content Title': 'Condition.',
    'Content Type': 'webseries',
    'Total Views': 33250,
    'Total Likes': 15218
  },
  {
    'Content Title': 'Fish that.',
    'Content Type': 'movie',
    'Total Views': 32268,
    'Total Likes': 9707
  },
  {
    'Content Title': 'Chance.',
    'Content Type': 'webseries',
    'Total Views': 31944,
    'Total Likes': 9094
  },
  {
    'Content Title': 'Family.',
    'Content Type': 'movie',
    'Total Views': 31873,
    'Total Likes': 4956
  }
                ]
            }
        },
        'Europe': {
            'Local': {
                'metrics': {
                    'total_execution_time': 744.27,
                    'throughput': 268.72 ,
                    'avg_response_time': 744.27,
                    'min_response_time': 744.27,
                    'max_response_time': 744.27,
                    'response_time_std_deviation': 0.0,
                    'cpu_utilization_increase': -0.60,
                    'memory_utilization_increase': 0.90
                },
                'recommendations': [
                    {
    'Content Title': 'Party TV conference.',
    'Content Type': 'documentary',
    'Total Views': 9986,
    'Total Likes': 3008
  },
  {
    'Content Title': 'Community ready.',
    'Content Type': 'documentary',
    'Total Views': 9963,
    'Total Likes': 2111
  },
  {
    'Content Title': 'Think instead.',
    'Content Type': 'webseries',
    'Total Views': 9918,
    'Total Likes': 1588
  },
  {
    'Content Title': 'Environmental owner.',
    'Content Type': 'documentary',
    'Total Views': 9890,
    'Total Likes': 2000
  },
  {
    'Content Title': 'Might local.',
    'Content Type': 'webseries',
    'Total Views': 9732,
    'Total Likes': 1489
  },
  {
    'Content Title': 'Authority suddenly address too.',
    'Content Type': 'movie',
    'Total Views': 9603,
    'Total Likes': 4065
  },
  {
    'Content Title': 'Chance.',
    'Content Type': 'webseries',
    'Total Views': 9593,
    'Total Likes': 2545
  },
  {
    'Content Title': 'Week control everything.',
    'Content Type': 'documentary',
    'Total Views': 9463,
    'Total Likes': 4167
  },
  {
    'Content Title': 'Least bank give.',
    'Content Type': 'documentary',
    'Total Views': 9338,
    'Total Likes': 2925
  },
  {
    'Content Title': 'Recently but check six.',
    'Content Type': 'webseries',
    'Total Views': 9301,
    'Total Likes': 4888
  }
                ]
            },
            'Global': {
                'metrics': {
                    'total_execution_time': 1604.27,
                    'throughput': 124.67,
                    'avg_response_time': 57.28,
                    'min_response_time': 9.10,
                    'max_response_time': 1233.34,
                    'response_time_std_deviation': 125.51,
                    'cpu_utilization_increase':  -1.40,
                    'memory_utilization_increase': 1.90
                },
                'recommendations': [
                    {
    'Content Title': 'Rise beat central democratic.',
    'Content Type': 'webseries',
    'Total Views': 33744,
    'Total Likes': 14824
  },
  {
    'Content Title': 'Condition.',
    'Content Type': 'webseries',
    'Total Views': 33250,
    'Total Likes': 15218
  },
  {
    'Content Title': 'Fish that.',
    'Content Type': 'movie',
    'Total Views': 32268,
    'Total Likes': 9707
  },
  {
    'Content Title': 'Chance.',
    'Content Type': 'webseries',
    'Total Views': 31944,
    'Total Likes': 9094
  },
  {
    'Content Title': 'Family.',
    'Content Type': 'movie',
    'Total Views': 31873,
    'Total Likes': 4956
  }
                ]
            }
        },
        'North America': {
            'Local': {
                'metrics': {
                    'total_execution_time': 613.27,
                    'throughput': 326.12,
                    'avg_response_time': 613.27,
                    'min_response_time': 613.27,
                    'max_response_time': 613.27,
                    'response_time_std_deviation': 0.0,
                    'cpu_utilization_increase': 9.50,
                    'memory_utilization_increase': 1.40
                },
                'recommendations': [
                    {
    'Content Title': 'Leader head.',
    'Content Type': 'documentary',
    'Total Views': 9962,
    'Total Likes': 4904
  },
  {
    'Content Title': 'Nation item.',
    'Content Type': 'documentary',
    'Total Views': 9951,
    'Total Likes': 1947
  },
  {
    'Content Title': 'Hundred shoulder might.',
    'Content Type': 'documentary',
    'Total Views': 9935,
    'Total Likes': 749
  },
  {
    'Content Title': 'Amount public.',
    'Content Type': 'webseries',
    'Total Views': 9771,
    'Total Likes': 2136
  },
  {
    'Content Title': 'Tough hear.',
    'Content Type': 'documentary',
    'Total Views': 9745,
    'Total Likes': 4604
  },
  {
    'Content Title': 'Wear mind.',
    'Content Type': 'webseries',
    'Total Views': 9669,
    'Total Likes': 1907
  },
  {
    'Content Title': 'World four decide a.',
    'Content Type': 'movie',
    'Total Views': 9646,
    'Total Likes': 2400
  },
  {
    'Content Title': 'Short price officer.',
    'Content Type': 'movie',
    'Total Views': 9521,
    'Total Likes': 2943
  },
  {
    'Content Title': 'Note right.',
    'Content Type': 'documentary',
    'Total Views': 9429,
    'Total Likes': 2636
  },
  {
    'Content Title': 'Rise beat central democratic.',
    'Content Type': 'webseries',
    'Total Views': 9324,
    'Total Likes': 2806
  }
                ]
            },
            'Global': {
                'metrics': {
                    'total_execution_time': 1604.27,
                    'throughput': 124.67,
                    'avg_response_time': 57.28,
                    'min_response_time': 9.10,
                    'max_response_time': 1233.34,
                    'response_time_std_deviation': 125.51,
                    'cpu_utilization_increase':  -1.40,
                    'memory_utilization_increase': 1.90
                },
                'recommendations': [
                    {
    'Content Title': 'Rise beat central democratic.',
    'Content Type': 'webseries',
    'Total Views': 33744,
    'Total Likes': 14824
  },
  {
    'Content Title': 'Condition.',
    'Content Type': 'webseries',
    'Total Views': 33250,
    'Total Likes': 15218
  },
  {
    'Content Title': 'Fish that.',
    'Content Type': 'movie',
    'Total Views': 32268,
    'Total Likes': 9707
  },
  {
    'Content Title': 'Chance.',
    'Content Type': 'webseries',
    'Total Views': 31944,
    'Total Likes': 9094
  },
  {
    'Content Title': 'Family.',
    'Content Type': 'movie',
    'Total Views': 31873,
    'Total Likes': 4956
  }
                ]
            }
        },
        'South America': {
            'Local': {
                'metrics': {
                    'total_execution_time': 784.24,
                    'throughput': 255.02,
                    'avg_response_time': 784.24,
                    'min_response_time': 784.24,
                    'max_response_time': 784.24,
                    'response_time_std_deviation': 0.0,
                    'cpu_utilization_increase': 0.90,
                    'memory_utilization_increase': 0.80
                },
                'recommendations': [
                    {
    'Content Title': 'Chance.',
    'Content Type': 'webseries',
    'Total Views': 9827,
    'Total Likes': 1359
  },
  {
    'Content Title': 'Firm skin often.',
    'Content Type': 'movie',
    'Total Views': 9794,
    'Total Likes': 4095
  },
  {
    'Content Title': 'Head first cost.',
    'Content Type': 'webseries',
    'Total Views': 9483,
    'Total Likes': 677
  },
  {
    'Content Title': 'Condition.',
    'Content Type': 'webseries',
    'Total Views': 9466,
    'Total Likes': 4483
  },
  {
    'Content Title': 'Deep different.',
    'Content Type': 'webseries',
    'Total Views': 9382,
    'Total Likes': 3849
  },
  {
    'Content Title': 'Term save apply.',
    'Content Type': 'movie',
    'Total Views': 9293,
    'Total Likes': 3751
  },
  {
    'Content Title': 'Final stuff.',
    'Content Type': 'movie',
    'Total Views': 9231,
    'Total Likes': 603
  },
  {
    'Content Title': 'Member rich network.',
    'Content Type': 'webseries',
    'Total Views': 9011,
    'Total Likes': 1033
  },
  {
    'Content Title': 'Reveal try determine.',
    'Content Type': 'movie',
    'Total Views': 8926,
    'Total Likes': 4365
  },
  {
    'Content Title': 'Interest beautiful value.',
    'Content Type': 'movie',
    'Total Views': 8812,
    'Total Likes': 2408
  }
                ]
            },
            'Global': {
                'metrics': {
                    'total_execution_time': 1604.27,
                    'throughput': 124.67,
                    'avg_response_time': 57.28,
                    'min_response_time': 9.10,
                    'max_response_time': 1233.34,
                    'response_time_std_deviation': 125.51,
                    'cpu_utilization_increase':  -1.40,
                    'memory_utilization_increase': 1.90
                },
                'recommendations': [
                    {
    'Content Title': 'Rise beat central democratic.',
    'Content Type': 'webseries',
    'Total Views': 33744,
    'Total Likes': 14824
  },
  {
    'Content Title': 'Condition.',
    'Content Type': 'webseries',
    'Total Views': 33250,
    'Total Likes': 15218
  },
  {
    'Content Title': 'Fish that.',
    'Content Type': 'movie',
    'Total Views': 32268,
    'Total Likes': 9707
  },
  {
    'Content Title': 'Chance.',
    'Content Type': 'webseries',
    'Total Views': 31944,
    'Total Likes': 9094
  },
  {
    'Content Title': 'Family.',
    'Content Type': 'movie',
    'Total Views': 31873,
    'Total Likes': 4956
  }
                ]
            }
        }}
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/metrics/<database>/<region>/<query_type>')
def get_metrics(database, region, query_type):
    try:
        # Retrieve specific data
        data = performance_data.get(database, {}).get(region, {}).get(query_type, {})
        
        # Prepare data for comparative visualization
        metrics = data['metrics']
        
        # Create multiple visualizations
        # 1. Bar Chart for Key Performance Metrics
        fig_bar = go.Figure()
        
        # Add bars for key metrics
        metrics_to_compare = [
            'total_execution_time', 
            'throughput', 
            'avg_response_time', 
            'cpu_utilization_increase', 
            'memory_utilization_increase'
        ]
        
        colors = [
            'blue', 'green', 'red', 'purple', 'orange'
        ]
        
        for metric, color in zip(metrics_to_compare, colors):
            fig_bar.add_trace(go.Bar(
                x=[metric],
                y=[metrics[metric]],
                name=metric.replace('_', ' ').title(),
                marker_color=color
            ))
        
        fig_bar.update_layout(
            title=f'Performance Metrics - {database} ({region}) - {query_type} Query',
            xaxis_title='Metrics',
            yaxis_title='Value',
            height=400
        )
        
        # 2. Detailed Metrics Visualization
        fig_detailed = go.Figure(data=[
            go.Scatter(
                x=list(metrics.keys()),
                y=list(metrics.values()),
                mode='markers+text',
                text=list(metrics.values()),
                textposition='top center',
                marker=dict(
                    size=10,
                    color=list(range(len(metrics))),
                    colorscale='Viridis'
                )
            )
        ])
        
        fig_detailed.update_layout(
            title='Detailed Metrics Comparison',
            height=400
        )
        
        # Format recommendations
        formatted_recommendations = []
        for rec in data['recommendations']:
            rec_text = (f"Title: {rec['Content Title']} | "
                        f"Type: {rec['Content Type']} | "
                        f"Views: {rec['Total Views']} | "
                        f"Likes: {rec['Total Likes']}")
            formatted_recommendations.append(rec_text)
        
        return jsonify({
            'bar_chart': json.dumps(fig_bar, cls=plotly.utils.PlotlyJSONEncoder),
            'detailed_chart': json.dumps(fig_detailed, cls=plotly.utils.PlotlyJSONEncoder),
            'metrics': metrics,
            'recommendations': formatted_recommendations,
            'raw_recommendations': data['recommendations']
        })
    
    except Exception as e:
        return jsonify({
            'error': f'Error processing request: {str(e)}'
        }), 500

if __name__ == '__main__':
    app.run(debug=True)