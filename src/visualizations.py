import plotly.express as px
import plotly.graph_objects as go

def create_platform_comparison_chart(df, workload, metric):
    """
    Create a bar chart comparing platforms for a specific metric
    
    Args:
        df (pandas.DataFrame): DataFrame containing benchmark data
        workload (str): The workload to filter by
        metric (str): The metric to compare (e.g., "Execution Time (min)")
        
    Returns:
        plotly.graph_objects.Figure: The plotly figure object
    """
    filtered_df = df[df["Workload"] == workload]
    
    # For execution time and cost, lower is better
    if metric in ["Execution Time (min)", "Cost ($)"]:
        best_provider = filtered_df.loc[filtered_df[metric].idxmin()]["Provider"]
        # The chart will be sorted in ascending order
        filtered_df = filtered_df.sort_values(by=metric)
        color_scale = "Bluered_r"  # Reversed so blue (better) is for lower values
    else:
        # For throughput, higher is better
        best_provider = filtered_df.loc[filtered_df[metric].idxmax()]["Provider"]
        # The chart will be sorted in descending order
        filtered_df = filtered_df.sort_values(by=metric, ascending=False)
        color_scale = "Bluered"  # Blue (better) is for higher values
    
    # Create a discrete color map that highlights the best provider
    colors = ["#0066cc" if provider == best_provider else "#ff66b2" 
              for provider in filtered_df["Provider"]]
    
    # Create the bar chart
    fig = px.bar(
        filtered_df,
        x="Provider",
        y=metric,
        color="Provider",
        color_discrete_sequence=colors,
        title=f"{metric} Comparison for {workload}"
    )
    
    # Update layout for retro gaming style with light pink theme
    fig.update_layout(
        font_family="Space Mono, monospace",
        font_color="#0a0a20",
        title_font_family="VT323, monospace",
        title_font_color="#0066cc",
        title_font_size=24,
        plot_bgcolor="#ffe6f2",
        paper_bgcolor="#ffe6f2",
        xaxis=dict(
            title_font_family="Space Mono, monospace",
            title_font_color="#0a0a20",
            tickfont_family="Space Mono, monospace",
            tickfont_color="#0a0a20",
            gridcolor="#ffb3d9",
            gridwidth=0.5,
            zeroline=False
        ),
        yaxis=dict(
            title_font_family="Space Mono, monospace",
            title_font_color="#0a0a20",
            tickfont_family="Space Mono, monospace",
            tickfont_color="#0a0a20",
            gridcolor="#ffb3d9",
            gridwidth=0.5,
            zeroline=False
        ),
        showlegend=False
    )
    
    # Add pixel-style border
    fig.update_layout(
        shapes=[
            dict(
                type="rect",
                xref="paper",
                yref="paper",
                x0=0,
                y0=0,
                x1=1,
                y1=1,
                line=dict(
                    color="#ff66b2",
                    width=3,
                )
            )
        ]
    )
    
    # Add text labels on top of bars
    fig.update_traces(
        texttemplate='%{y}', 
        textposition='outside',
        textfont=dict(
            family="VT323, monospace",
            size=18,
            color="#0066cc"
        )
    )
    
    return fig

def create_radar_chart(df, workload):
    """
    Create a radar chart comparing all metrics across providers
    
    Args:
        df (pandas.DataFrame): DataFrame containing benchmark data
        workload (str): The workload to filter by
        
    Returns:
        plotly.graph_objects.Figure: The plotly figure object
    """
    filtered_df = df[df["Workload"] == workload]
    
    # Normalize the metrics for the radar chart
    metrics = ["Execution Time (min)", "Cost ($)", "Throughput", 
               "GPU Utilization (%)", "Memory Usage (%)"]
    
    # Create a copy to avoid modifying the original dataframe
    radar_df = filtered_df.copy()
    
    # For each metric, normalize to a 0-1 scale
    # For time and cost, lower is better, so we invert those
    for metric in metrics:
        if metric in ["Execution Time (min)", "Cost ($)"]:
            min_val = radar_df[metric].min()
            max_val = radar_df[metric].max()
            radar_df[f"{metric} (normalized)"] = 1 - ((radar_df[metric] - min_val) / (max_val - min_val) if max_val > min_val else 0)
        else:
            min_val = radar_df[metric].min()
            max_val = radar_df[metric].max()
            radar_df[f"{metric} (normalized)"] = (radar_df[metric] - min_val) / (max_val - min_val) if max_val > min_val else 0
    
    # Create the radar chart
    fig = go.Figure()
    
    colors = ["#0066cc", "#ff66b2", "#33cc33", "#cc6600"]
    
    for i, provider in enumerate(radar_df["Provider"]):
        provider_data = radar_df[radar_df["Provider"] == provider]
        
        fig.add_trace(go.Scatterpolar(
            r=[
                provider_data[f"Execution Time (min) (normalized)"].values[0],
                provider_data[f"Cost ($) (normalized)"].values[0],
                provider_data[f"Throughput (normalized)"].values[0],
                provider_data[f"GPU Utilization (%) (normalized)"].values[0],
                provider_data[f"Memory Usage (%) (normalized)"].values[0],
                provider_data[f"Execution Time (min) (normalized)"].values[0],  # Close the loop
            ],
            theta=[
                "Speed",
                "Cost",
                "Throughput",
                "GPU Utilization",
                "Memory Efficiency",
                "Speed"  # Close the loop
            ],
            name=provider,
            line=dict(color=colors[i], width=3),
            fill='toself',
            fillcolor='rgba(0, 102, 204, 0.2)' if i == 0 else 
                      'rgba(255, 102, 178, 0.2)' if i == 1 else
                      'rgba(51, 204, 51, 0.2)' if i == 2 else
                      'rgba(204, 102, 0, 0.2)'  # Proper rgba format
        ))
    
    # Update layout for light pink theme
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1],
                showticklabels=False,
                gridcolor="#ffb3d9",
                gridwidth=0.5
            ),
            angularaxis=dict(
                gridcolor="#ffb3d9",
                gridwidth=0.5
            ),
            bgcolor="#ffe6f2"
        ),
        font_family="Space Mono, monospace",
        font_color="#0a0a20",
        title=dict(
            text=f"Performance Radar for {workload}",
            font=dict(
                family="VT323, monospace",
                size=24,
                color="#0066cc"
            )
        ),
        paper_bgcolor="#ffe6f2",
        plot_bgcolor="#ffe6f2",
        showlegend=True,
        legend=dict(
            font=dict(
                family="Space Mono, monospace",
                size=12,
                color="#0a0a20"
            )
        )
    )
    
    # Add pixel-style border
    fig.update_layout(
        shapes=[
            dict(
                type="rect",
                xref="paper",
                yref="paper",
                x0=0,
                y0=0,
                x1=1,
                y1=1,
                line=dict(
                    color="#ff66b2",
                    width=3,
                )
            )
        ]
    )
    
    return fig

def create_leaderboard(df, workload, metric):
    """
    Create a leaderboard-style dataframe for platforms based on a metric
    
    Args:
        df (pandas.DataFrame): DataFrame containing benchmark data
        workload (str): The workload to filter by
        metric (str): The metric to rank by
        
    Returns:
        pandas.DataFrame: Sorted and ranked DataFrame
    """
    filtered_df = df[df["Workload"] == workload]
    
    # Determine sorting order based on metric
    ascending = True if metric in ["Execution Time (min)", "Cost ($)"] else False
    
    # Sort and rank
    sorted_df = filtered_df.sort_values(by=metric, ascending=ascending)
    sorted_df["Rank"] = range(1, len(sorted_df) + 1)
    
    # Select columns to display
    display_df = sorted_df[["Rank", "Provider", metric]]
    
    # Format for display
    display_df["Rank"] = display_df["Rank"].apply(lambda x: f"{x}")
    
    return display_df