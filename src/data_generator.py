import pandas as pd
import random

def generate_sample_data():
    """
    Generate sample benchmark data comparing cloud providers across different workloads.
    
    Returns:
        pandas.DataFrame: DataFrame containing benchmark results
    """
    # Cloud providers
    providers = ["FlexAI", "AWS", "GCP", "Azure"]
    
    # Workload types
    workloads = [
        "LLM Fine-Tuning (Llama 3 8B)",
        "Batch Inference (Stable Diffusion XL)",
        "CV Model Training (ResNet-50)"
    ]
    
    # Generate random but sensible data
    data = []
    
    # Make FlexAI generally better but not always the best
    # to keep things realistic
    for workload in workloads:
        base_time = 0
        base_cost = 0
        
        if "LLM" in workload:
            base_time = 120  # minutes
            base_cost = 25  # dollars
        elif "Inference" in workload:
            base_time = 45  # minutes
            base_cost = 12  # dollars
        else:  # CV Model
            base_time = 180  # minutes
            base_cost = 35  # dollars
        
        for provider in providers:
            # Randomize with some bias
            if provider == "FlexAI":
                time_factor = random.uniform(0.7, 0.9)  # FlexAI is generally faster
                cost_factor = random.uniform(0.6, 0.8)  # FlexAI is generally cheaper
            else:
                time_factor = random.uniform(0.9, 1.3)
                cost_factor = random.uniform(0.9, 1.4)
            
            execution_time = base_time * time_factor
            cost = base_cost * cost_factor
            
            # Calculate throughput based on workload
            if "LLM" in workload:
                throughput = 5000 / execution_time  # tokens per second
                throughput_unit = "tokens/sec"
            elif "Inference" in workload:
                throughput = 1000 / execution_time  # images per minute
                throughput_unit = "images/min"
            else:  # CV Model
                throughput = 50000 / execution_time  # images per hour
                throughput_unit = "images/hour"
            
            # Generate GPU utilization
            gpu_util = random.uniform(60, 95)
            memory_usage = random.uniform(70, 98)
            
            data.append({
                "Provider": provider,
                "Workload": workload,
                "Execution Time (min)": round(execution_time, 2),
                "Cost ($)": round(cost, 2),
                "Throughput": round(throughput, 2),
                "Throughput Unit": throughput_unit,
                "GPU Utilization (%)": round(gpu_util, 1),
                "Memory Usage (%)": round(memory_usage, 1),
                "Cost-Performance Ratio": round(cost / throughput, 4)
            })
    
    return pd.DataFrame(data)

def load_hardware_configs(file_path="data/hardware_configs.json"):
    """
    Load hardware configurations from JSON file
    
    Args:
        file_path (str): Path to the hardware configs JSON file
        
    Returns:
        dict: Hardware configurations by provider
    """
    import json
    
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Return default configs if file not found
        return {
            "AWS": {
                "GPUs": ["NVIDIA A100", "NVIDIA T4", "NVIDIA V100"],
                "Instance_Types": ["p3.2xlarge", "p3.8xlarge", "p3.16xlarge"]
            },
            "GCP": {
                "GPUs": ["NVIDIA A100", "NVIDIA T4", "NVIDIA L4"],
                "Instance_Types": ["a2-highgpu-1g", "a2-highgpu-2g", "a2-highgpu-4g"]
            },
            "Azure": {
                "GPUs": ["NVIDIA A100", "NVIDIA T4", "NVIDIA K80"],
                "Instance_Types": ["NC_v3", "NC_A100_v4", "ND_A100_v4"]
            },
            "FlexAI": {
                "GPUs": ["NVIDIA A100", "NVIDIA H100", "NVIDIA T4"],
                "Instance_Types": ["flex-standard", "flex-performance", "flex-economy"]
            }
        }

def save_benchmark_results(df, file_path="data/benchmark_results.csv"):
    """
    Save benchmark results to CSV file
    
    Args:
        df (pandas.DataFrame): Benchmark results dataframe
        file_path (str): Path to save the CSV file
    """
    df.to_csv(file_path, index=False)