def format_currency(amount, precision=2, currency="$"):
    """
    Format a number as currency
    
    Args:
        amount (float): The amount to format
        precision (int): Decimal precision
        currency (str): Currency symbol
        
    Returns:
        str: Formatted currency string
    """
    return f"{currency}{amount:.{precision}f}"

def calculate_savings(base_cost, comparison_cost):
    """
    Calculate savings and percentage
    
    Args:
        base_cost (float): The reference cost (usually FlexAI)
        comparison_cost (float): The cost to compare against
        
    Returns:
        tuple: (absolute savings, percentage savings)
    """
    savings = comparison_cost - base_cost
    if comparison_cost > 0:
        savings_pct = (savings / comparison_cost) * 100
    else:
        savings_pct = 0
    
    return savings, savings_pct

def get_winner(data_df, workload, metrics):
    """
    Determine the winner across multiple metrics
    
    Args:
        data_df (pandas.DataFrame): DataFrame with benchmark data
        workload (str): The workload to filter by
        metrics (list): List of metrics to consider
        
    Returns:
        str: Name of the winning provider
    """
    filtered_df = data_df[data_df["Workload"] == workload]
    
    # Initialize points dictionary
    rankings = {}
    
    for metric in metrics:
        # Determine if lower is better
        ascending = True if metric in ["Execution Time (min)", "Cost ($)"] else False
        
        # Get sorted providers
        sorted_providers = filtered_df.sort_values(by=metric, ascending=ascending)["Provider"].tolist()
        
        # Assign points (reverse order)
        for i, provider in enumerate(sorted_providers):
            if provider not in rankings:
                rankings[provider] = 0
            
            # Add points (reverse order)
            rankings[provider] += len(sorted_providers) - i
    
    # Determine the winner
    winner = max(rankings.items(), key=lambda x: x[1])[0]
    
    return winner, rankings

def get_resource_price_table():
    """
    Get a pricing table for different resources
    
    Returns:
        pandas.DataFrame: DataFrame with pricing information
    """
    import pandas as pd
    
    # Sample pricing data
    pricing_data = [
        {"Provider": "AWS", "GPU": "NVIDIA A100", "Hourly Rate": 3.60, "Monthly Rate": 2592.00},
        {"Provider": "AWS", "GPU": "NVIDIA T4", "Hourly Rate": 0.95, "Monthly Rate": 684.00},
        {"Provider": "AWS", "GPU": "NVIDIA V100", "Hourly Rate": 3.06, "Monthly Rate": 2203.20},
        {"Provider": "GCP", "GPU": "NVIDIA A100", "Hourly Rate": 3.35, "Monthly Rate": 2412.00},
        {"Provider": "GCP", "GPU": "NVIDIA T4", "Hourly Rate": 0.89, "Monthly Rate": 640.80},
        {"Provider": "GCP", "GPU": "NVIDIA L4", "Hourly Rate": 1.35, "Monthly Rate": 972.00},
        {"Provider": "Azure", "GPU": "NVIDIA A100", "Hourly Rate": 3.67, "Monthly Rate": 2642.40},
        {"Provider": "Azure", "GPU": "NVIDIA T4", "Hourly Rate": 0.99, "Monthly Rate": 712.80},
        {"Provider": "Azure", "GPU": "NVIDIA K80", "Hourly Rate": 0.71, "Monthly Rate": 511.20},
        {"Provider": "FlexAI", "GPU": "NVIDIA A100", "Hourly Rate": 2.89, "Monthly Rate": 2080.80},
        {"Provider": "FlexAI", "GPU": "NVIDIA H100", "Hourly Rate": 5.76, "Monthly Rate": 4147.20},
        {"Provider": "FlexAI", "GPU": "NVIDIA T4", "Hourly Rate": 0.76, "Monthly Rate": 547.20}
    ]
    
    return pd.DataFrame(pricing_data)