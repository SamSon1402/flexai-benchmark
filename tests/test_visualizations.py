import unittest
import pandas as pd
import sys
import os
import plotly.graph_objects as go

# Add the parent directory to the path so we can import the src modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.visualizations import create_platform_comparison_chart, create_radar_chart, create_leaderboard

class TestVisualizations(unittest.TestCase):
    
    def setUp(self):
        """Set up test data"""
        # Create a small test dataframe
        self.test_data = pd.DataFrame([
            {
                "Provider": "FlexAI", 
                "Workload": "Test Workload",
                "Execution Time (min)": 100,
                "Cost ($)": 20,
                "Throughput": 50,
                "Throughput Unit": "tokens/sec",
                "GPU Utilization (%)": 90,
                "Memory Usage (%)": 85
            },
            {
                "Provider": "AWS", 
                "Workload": "Test Workload",
                "Execution Time (min)": 120,
                "Cost ($)": 30,
                "Throughput": 40,
                "Throughput Unit": "tokens/sec",
                "GPU Utilization (%)": 80,
                "Memory Usage (%)": 75
            },
            {
                "Provider": "GCP", 
                "Workload": "Test Workload",
                "Execution Time (min)": 110,
                "Cost ($)": 25,
                "Throughput": 45,
                "Throughput Unit": "tokens/sec",
                "GPU Utilization (%)": 85,
                "Memory Usage (%)": 80
            },
            {
                "Provider": "Azure", 
                "Workload": "Test Workload",
                "Execution Time (min)": 130,
                "Cost ($)": 35,
                "Throughput": 35,
                "Throughput Unit": "tokens/sec",
                "GPU Utilization (%)": 75,
                "Memory Usage (%)": 70
            }
        ])
    
    def test_create_platform_comparison_chart(self):
        """Test creating a platform comparison chart"""
        # Test with execution time (lower is better)
        fig1 = create_platform_comparison_chart(self.test_data, "Test Workload", "Execution Time (min)")
        self.assertIsInstance(fig1, go.Figure)
        
        # Test with throughput (higher is better)
        fig2 = create_platform_comparison_chart(self.test_data, "Test Workload", "Throughput")
        self.assertIsInstance(fig2, go.Figure)
    
    def test_create_radar_chart(self):
        """Test creating a radar chart"""
        fig = create_radar_chart(self.test_data, "Test Workload")
        self.assertIsInstance(fig, go.Figure)
        
        # Check that we have the right number of traces (one per provider)
        self.assertEqual(len(fig.data), 4)
    
    def test_create_leaderboard(self):
        """Test creating a leaderboard"""
        # Test with execution time (lower is better)
        leaderboard1 = create_leaderboard(self.test_data, "Test Workload", "Execution Time (min)")
        self.assertIsInstance(leaderboard1, pd.DataFrame)
        self.assertEqual(len(leaderboard1), 4)
        
        # The first row should be the best provider (FlexAI for execution time)
        self.assertEqual(leaderboard1.iloc[0]["Provider"], "FlexAI")
        
        # Test with throughput (higher is better)
        leaderboard2 = create_leaderboard(self.test_data, "Test Workload", "Throughput")
        self.assertIsInstance(leaderboard2, pd.DataFrame)
        self.assertEqual(len(leaderboard2), 4)
        
        # The first row should be the best provider (FlexAI for throughput)
        self.assertEqual(leaderboard2.iloc[0]["Provider"], "FlexAI")

if __name__ == "__main__":
    unittest.main()