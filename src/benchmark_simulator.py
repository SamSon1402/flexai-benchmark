import time
import random
import streamlit as st

def simulate_benchmark_run():
    """
    Simulate a benchmark run with a progress bar and status updates
    
    Returns:
        bool: True if the benchmark completed successfully
    """
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    phases = [
        "Initializing benchmark environment...",
        "Preparing workload configurations...",
        "Deploying infrastructure...",
        "Running benchmark workloads...",
        "Collecting performance metrics...",
        "Calculating cost data...",
        "Compiling results..."
    ]
    
    for i, phase in enumerate(phases):
        status_text.text(phase)
        progress_value = (i + 1) / len(phases)
        progress_bar.progress(progress_value)
        time.sleep(0.5)  # Simulate processing time
    
    status_text.text("Benchmark completed successfully!")
    time.sleep(0.5)
    return True

def calculate_workload_cost(provider, workload_type, duration_minutes, instance_type=None):
    """
    Calculate the cost of running a workload based on provider pricing
    
    Args:
        provider (str): Cloud provider name
        workload_type (str): Type of workload
        duration_minutes (float): Duration in minutes
        instance_type (str, optional): Instance type
        
    Returns:
        float: Estimated cost in dollars
    """
    # Sample pricing data (per hour)
    hourly_rates = {
        "AWS": {
            "NVIDIA A100": 3.60,
            "NVIDIA T4": 0.95,
            "NVIDIA V100": 3.06
        },
        "GCP": {
            "NVIDIA A100": 3.35,
            "NVIDIA T4": 0.89,
            "NVIDIA L4": 1.35
        },
        "Azure": {
            "NVIDIA A100": 3.67,
            "NVIDIA T4": 0.99,
            "NVIDIA K80": 0.71
        },
        "FlexAI": {
            "NVIDIA A100": 2.89,
            "NVIDIA H100": 5.76,
            "NVIDIA T4": 0.76
        }
    }
    
    # Default to A100 if instance_type is not provided
    gpu_type = instance_type if instance_type else "NVIDIA A100"
    
    # Get the hourly rate
    hourly_rate = hourly_rates.get(provider, {}).get(gpu_type, 0)
    
    # Apply workload-specific multipliers
    if "LLM" in workload_type:
        multiplier = 1.2  # LLM fine-tuning is more expensive
    elif "Inference" in workload_type:
        multiplier = 0.8  # Inference might be cheaper
    else:
        multiplier = 1.0  # Default
    
    # Calculate cost
    cost = (duration_minutes / 60) * hourly_rate * multiplier
    
    # Add randomness to make it realistic
    cost *= random.uniform(0.95, 1.05)
    
    return round(cost, 2)