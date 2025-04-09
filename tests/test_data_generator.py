import unittest
import pandas as pd
import sys
import os

# Add the parent directory to the path so we can import the src modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_generator import generate_sample_data, load_hardware_configs

class TestDataGenerator(unittest.TestCase):
    
    def test_generate_sample_data(self):
        """Test that the data generator produces correctly structured data"""
        df = generate_sample_data()
        
        # Check that the dataframe has the expected columns
        expected_columns = [
            "Provider", "Workload", "Execution Time (min)", "Cost ($)", 
            "Throughput", "Throughput Unit", "GPU Utilization (%)", 
            "Memory Usage (%)", "Cost-Performance Ratio"
        ]
        for col in expected_columns:
            self.assertIn(col, df.columns)
        
        # Check that we have the expected number of rows
        # 4 providers x 3 workloads = 12 rows
        self.assertEqual(len(df), 12)
        
        # Check that providers are as expected
        expected_providers = ["FlexAI", "AWS", "GCP", "Azure"]
        self.assertEqual(set(df["Provider"].unique()), set(expected_providers))
        
        # Check that workloads are as expected
        expected_workloads = [
            "LLM Fine-Tuning (Llama 3 8B)",
            "Batch Inference (Stable Diffusion XL)",
            "CV Model Training (ResNet-50)"
        ]
        self.assertEqual(set(df["Workload"].unique()), set(expected_workloads))
        
        # Check that numeric columns have sensible values
        self.assertTrue(all(df["Execution Time (min)"] > 0))
        self.assertTrue(all(df["Cost ($)"] > 0))
        self.assertTrue(all(df["Throughput"] > 0))
        self.assertTrue(all(df["GPU Utilization (%)"] >= 0) and all(df["GPU Utilization (%)"] <= 100))
        self.assertTrue(all(df["Memory Usage (%)"] >= 0) and all(df["Memory Usage (%)"] <= 100))
    
    def test_load_hardware_configs(self):
        """Test loading hardware configurations"""
        # Test with non-existent file to get default configs
        configs = load_hardware_configs("nonexistent_file.json")
        
        # Check that we have configs for all providers
        expected_providers = ["AWS", "GCP", "Azure", "FlexAI"]
        for provider in expected_providers:
            self.assertIn(provider, configs)
            
            # Check that each provider has GPUs and Instance_Types
            self.assertIn("GPUs", configs[provider])
            self.assertIn("Instance_Types", configs[provider])
            
            # Check that GPUs and Instance_Types are non-empty lists
            self.assertTrue(len(configs[provider]["GPUs"]) > 0)
            self.assertTrue(len(configs[provider]["Instance_Types"]) > 0)

if __name__ == "__main__":
    unittest.main()