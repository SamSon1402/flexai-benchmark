import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import random
import time
import base64

# Set page configuration
st.set_page_config(
    page_title="FlexAI Benchmarking Suite",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS for retro gaming aesthetic with light pink background
def load_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=VT323&family=Space+Mono:wght@400;700&display=swap');
        
        /* Main container styling */
        .main {
            background-color: #ffe6f2;
            color: #0a0a20;
        }
        
        /* Header styling */
        h1, h2, h3 {
            font-family: 'VT323', monospace;
            color: #0066cc;
            text-shadow: 2px 2px 0px #ff66b2;
            padding: 10px;
            border: 2px solid #ff66b2;
            background-color: #ffcce6;
        }
        
        /* Text styling */
        p, li {
            font-family: 'Space Mono', monospace;
            color: #0a0a20;
        }
        
        /* Button styling */
        .stButton button {
            font-family: 'VT323', monospace;
            background-color: #ff66b2;
            color: #ffffff;
            border: 2px solid #0066cc;
            box-shadow: 3px 3px 0px #0066cc;
        }
        
        /* Selectbox styling */
        .stSelectbox {
            font-family: 'Space Mono', monospace;
        }
        
        /* Card-like containers */
        .css-card {
            border: 2px solid #ff66b2;
            border-radius: 0px;
            padding: 20px;
            margin: 10px;
            background-color: #ffcce6;
            box-shadow: 4px 4px 0px #0066cc;
        }
        
        /* Metric styling */
        .metric-container {
            background-color: #ffcce6;
            border: 2px solid #ff66b2;
            padding: 15px;
            text-align: center;
            margin: 5px;
        }
        
        .metric-value {
            font-family: 'VT323', monospace;
            font-size: 32px;
            color: #0066cc;
        }
        
        .metric-label {
            font-family: 'Space Mono', monospace;
            font-size: 14px;
            color: #0a0a20;
        }
        
        /* Divider */
        hr {
            border: 1px dashed #ff66b2;
        }
        
        /* Table styling */
        .dataframe {
            font-family: 'Space Mono', monospace;
            border: 2px solid #ff66b2;
        }
        
        .dataframe th {
            background-color: #ff66b2;
            color: #ffffff;
            font-weight: bold;
            padding: 10px;
            text-align: center;
        }
        
        .dataframe td {
            padding: 8px;
            border: 1px solid #ff66b2;
            background-color: #ffe6f2;
        }
        
        /* Sidebar */
        .css-1d391kg, [data-testid="stSidebar"] {
            background-color: #ffcce6;
        }
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
        }
        
        .stTabs [data-baseweb="tab"] {
            font-family: 'VT323', monospace;
            background-color: #ffe6f2;
            border: 2px solid #ff66b2;
            border-radius: 0px;
            color: #0a0a20;
            padding: 10px 20px;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: #ff66b2;
            color: #ffffff;
        }
    </style>
    """, unsafe_allow_html=True)

load_css()

# Custom header with retro animation effect
def retro_header(text, level=1):
    if level == 1:
        st.markdown(f'<h1 class="retro-header">{text}</h1>', unsafe_allow_html=True)
    elif level == 2:
        st.markdown(f'<h2 class="retro-header">{text}</h2>', unsafe_allow_html=True)
    else:
        st.markdown(f'<h3 class="retro-header">{text}</h3>', unsafe_allow_html=True)

# Generate sample data
def generate_sample_data():
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

# Simulate a loading animation for benchmark execution
def simulate_benchmark_run():
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

# Create a pixel art style visualization for provider comparison
def create_platform_comparison_chart(df, workload, metric):
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

# Create a radar chart comparing all metrics
def create_radar_chart(df, workload):
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

# Create leaderboard-style table
def create_leaderboard(df, workload, metric):
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

# Main application
def main():
    # Sidebar
    st.sidebar.markdown("<h1 style='text-align: center; color: #0066cc;'>FLEXAI BENCHMARK</h1>", unsafe_allow_html=True)
    st.sidebar.markdown("<p style='text-align: center; color: #0a0a20;'>WORKLOAD CONFIGURATION</p>", unsafe_allow_html=True)
    
    # Add a pixelated logo or image
    st.sidebar.markdown("""
    <div style='text-align: center; margin-bottom: 20px;'>
        <div style='font-family: "VT323", monospace; font-size: 24px; color: #0066cc; margin-bottom: 10px;'>
        ▄▄▄▄▄▄▄▄▄▄▄▄▄<br/>
        █ FLEXAI VS █<br/>
        █ THE CLOUD █<br/>
        ▀▀▀▀▀▀▀▀▀▀▀▀▀<br/>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar controls
    selected_workload = st.sidebar.selectbox(
        "SELECT WORKLOAD:",
        [
            "LLM Fine-Tuning (Llama 3 8B)",
            "Batch Inference (Stable Diffusion XL)",
            "CV Model Training (ResNet-50)"
        ]
    )
    
    # Hardware configuration (for demonstration)
    st.sidebar.markdown("<p style='text-align: center; color: #0a0a20;'>HARDWARE CONFIGURATION</p>", unsafe_allow_html=True)
    
    gpu_options = {
        "AWS": ["NVIDIA A100", "NVIDIA T4", "NVIDIA V100"],
        "GCP": ["NVIDIA A100", "NVIDIA T4", "NVIDIA L4"],
        "Azure": ["NVIDIA A100", "NVIDIA T4", "NVIDIA K80"],
        "FlexAI": ["NVIDIA A100", "NVIDIA H100", "NVIDIA T4"]
    }
    
    # Hardware configuration for each provider
    for provider in gpu_options.keys():
        st.sidebar.selectbox(
            f"{provider} GPU:",
            gpu_options[provider],
            key=f"gpu_{provider}"
        )
    
    # Run benchmark button
    if st.sidebar.button("▶ RUN BENCHMARK"):
        with st.spinner("Executing benchmark..."):
            success = simulate_benchmark_run()
            if success:
                st.session_state.benchmark_run = True
                st.session_state.benchmark_data = generate_sample_data()
    
    # Credits
    st.sidebar.markdown("---")
    st.sidebar.markdown("<p style='text-align: center; color: #0a0a20;'>© 2025 FLEXAI BENCHMARKS</p>", unsafe_allow_html=True)
    
    # Main content
    retro_header("FlexAI vs Cloud Providers: Benchmark Suite")
    
    st.markdown("""
    <div class="css-card">
    <p>Compare performance and cost metrics for AI workloads across different cloud platforms. 
    Select a workload from the sidebar and run the benchmark to see the results.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state for benchmark data
    if 'benchmark_run' not in st.session_state:
        st.session_state.benchmark_run = False
    
    if 'benchmark_data' not in st.session_state:
        # Pre-generate some data for first load
        st.session_state.benchmark_data = generate_sample_data()
    
    # Display benchmark results
    if st.session_state.benchmark_run:
        # Tabs for different views
        tab1, tab2, tab3 = st.tabs(["📊 PERFORMANCE", "💰 COST", "🏆 LEADERBOARD"])
        
        with tab1:
            retro_header("Performance Metrics", level=2)
            
            # Performance metrics section
            col1, col2 = st.columns(2)
            
            with col1:
                fig1 = create_platform_comparison_chart(
                    st.session_state.benchmark_data, 
                    selected_workload, 
                    "Execution Time (min)"
                )
                st.plotly_chart(fig1, use_container_width=True)
            
            with col2:
                fig2 = create_platform_comparison_chart(
                    st.session_state.benchmark_data, 
                    selected_workload, 
                    "Throughput"
                )
                st.plotly_chart(fig2, use_container_width=True)
            
            # Radar chart for all metrics
            st.markdown("### Overall Performance Comparison")
            radar_fig = create_radar_chart(st.session_state.benchmark_data, selected_workload)
            st.plotly_chart(radar_fig, use_container_width=True)
            
            # Additional performance metrics
            filtered_data = st.session_state.benchmark_data[
                st.session_state.benchmark_data["Workload"] == selected_workload
            ]
            
            # Display gpu utilization and memory usage
            st.markdown("### Resource Utilization")
            col1, col2, col3, col4 = st.columns(4)
            
            for i, provider in enumerate(filtered_data["Provider"]):
                provider_data = filtered_data[filtered_data["Provider"] == provider]
                col = [col1, col2, col3, col4][i]
                
                with col:
                    st.markdown(f"""
                    <div class="metric-container">
                        <div class="metric-label">{provider} GPU Util.</div>
                        <div class="metric-value">{provider_data["GPU Utilization (%)"].values[0]}%</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    <div class="metric-container">
                        <div class="metric-label">{provider} Memory</div>
                        <div class="metric-value">{provider_data["Memory Usage (%)"].values[0]}%</div>
                    </div>
                    """, unsafe_allow_html=True)
        
        with tab2:
            retro_header("Cost Analysis", level=2)
            
            # Cost metrics section
            col1, col2 = st.columns(2)
            
            with col1:
                fig3 = create_platform_comparison_chart(
                    st.session_state.benchmark_data, 
                    selected_workload, 
                    "Cost ($)"
                )
                st.plotly_chart(fig3, use_container_width=True)
            
            # Calculate cost efficiency metrics
            filtered_data = st.session_state.benchmark_data[
                st.session_state.benchmark_data["Workload"] == selected_workload
            ]
            
            # Add cost efficiency calculation
            filtered_data["Cost per Hour ($)"] = filtered_data["Cost ($)"] / (filtered_data["Execution Time (min)"] / 60)
            
            with col2:
                # Create bar chart for cost per hour
                fig4 = px.bar(
                    filtered_data.sort_values(by="Cost per Hour ($)"),
                    x="Provider", 
                    y="Cost per Hour ($)",
                    color="Provider",
                    color_discrete_sequence=["#0066cc", "#ff66b2", "#33cc33", "#cc6600"],
                    title="Hourly Cost Comparison"
                )
                
                # Update layout for retro gaming style with light pink theme
                fig4.update_layout(
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
                    ),
                    yaxis=dict(
                        title_font_family="Space Mono, monospace",
                        title_font_color="#0a0a20",
                        tickfont_family="Space Mono, monospace",
                        tickfont_color="#0a0a20",
                        gridcolor="#ffb3d9",
                        gridwidth=0.5,
                    ),
                    showlegend=False
                )
                
                # Add text labels on top of bars
                fig4.update_traces(
                    texttemplate='$%{y:.2f}', 
                    textposition='outside',
                    textfont=dict(
                        family="VT323, monospace",
                        size=18,
                        color="#0066cc"
                    )
                )
                
                st.plotly_chart(fig4, use_container_width=True)
            
            # Cost savings calculation
            st.markdown("### Estimated Cost Savings with FlexAI")
            
            flexai_cost = filtered_data[filtered_data["Provider"] == "FlexAI"]["Cost ($)"].values[0]
            
            col1, col2, col3 = st.columns(3)
            
            for i, provider in enumerate(["AWS", "GCP", "Azure"]):
                provider_data = filtered_data[filtered_data["Provider"] == provider]
                provider_cost = provider_data["Cost ($)"].values[0]
                savings = provider_cost - flexai_cost
                savings_pct = (savings / provider_cost) * 100
                
                col = [col1, col2, col3][i]
                
                with col:
                    st.markdown(f"""
                    <div class="metric-container">
                        <div class="metric-label">vs {provider}</div>
                        <div class="metric-value">${savings:.2f}</div>
                        <div class="metric-label">({savings_pct:.1f}% savings)</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Cost comparison table
            st.markdown("### Detailed Cost Breakdown")
            cost_table = filtered_data[["Provider", "Cost ($)", "Execution Time (min)"]]
            cost_table["Cost per Minute"] = cost_table["Cost ($)"] / cost_table["Execution Time (min)"]
            cost_table = cost_table.sort_values(by="Cost per Minute")
            
            # Format the table
            formatted_table = cost_table.copy()
            formatted_table["Cost ($)"] = formatted_table["Cost ($)"].map("${:.2f}".format)
            formatted_table["Cost per Minute"] = formatted_table["Cost per Minute"].map("${:.4f}".format)
            formatted_table = formatted_table.rename(columns={
                "Provider": "CLOUD PROVIDER",
                "Cost ($)": "TOTAL COST",
                "Execution Time (min)": "RUNTIME (MIN)",
                "Cost per Minute": "COST PER MINUTE"
            })
            
            st.table(formatted_table)
            
        with tab3:
            retro_header("Performance Leaderboard", level=2)
            
            # Create leaderboards for different metrics
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 🚀 Speed Champions")
                time_leaderboard = create_leaderboard(
                    st.session_state.benchmark_data,
                    selected_workload,
                    "Execution Time (min)"
                )
                time_leaderboard = time_leaderboard.rename(columns={
                    "Rank": "RANK",
                    "Provider": "PROVIDER",
                    "Execution Time (min)": "TIME (MIN)"
                })
                st.table(time_leaderboard)
                
                st.markdown("### 💡 Throughput Champions")
                throughput_leaderboard = create_leaderboard(
                    st.session_state.benchmark_data,
                    selected_workload,
                    "Throughput"
                )
                throughput_unit = st.session_state.benchmark_data[
                    st.session_state.benchmark_data["Workload"] == selected_workload
                ]["Throughput Unit"].iloc[0]
                throughput_leaderboard = throughput_leaderboard.rename(columns={
                    "Rank": "RANK",
                    "Provider": "PROVIDER",
                    "Throughput": f"THROUGHPUT ({throughput_unit})"
                })
                st.table(throughput_leaderboard)
            
            with col2:
                st.markdown("### 💰 Cost Champions")
                cost_leaderboard = create_leaderboard(
                    st.session_state.benchmark_data,
                    selected_workload,
                    "Cost ($)"
                )
                cost_leaderboard = cost_leaderboard.rename(columns={
                    "Rank": "RANK",
                    "Provider": "PROVIDER",
                    "Cost ($)": "COST ($)"
                })
                st.table(cost_leaderboard)
                
                # Calculate and display cost-performance ratio
                st.markdown("### 🏅 Cost-Performance Champions")
                
                # Create cost-performance DataFrame
                filtered_data = st.session_state.benchmark_data[
                    st.session_state.benchmark_data["Workload"] == selected_workload
                ]
                
                if "Cost-Performance Ratio" not in filtered_data.columns:
                    filtered_data["Cost-Performance Ratio"] = filtered_data["Cost ($)"] / filtered_data["Throughput"]
                
                cp_leaderboard = create_leaderboard(
                    filtered_data,
                    selected_workload,
                    "Cost-Performance Ratio"
                )
                cp_leaderboard = cp_leaderboard.rename(columns={
                    "Rank": "RANK",
                    "Provider": "PROVIDER",
                    "Cost-Performance Ratio": "COST/PERFORMANCE"
                })
                st.table(cp_leaderboard)
            
            # Overall winner determination
            st.markdown("### 👑 OVERALL CHAMPION")
            
            # Count first places across all metrics
            filtered_data = st.session_state.benchmark_data[
                st.session_state.benchmark_data["Workload"] == selected_workload
            ]
            
            # Get rankings for each metric
            metrics = ["Execution Time (min)", "Cost ($)", "Throughput", "GPU Utilization (%)", "Memory Usage (%)"]
            rankings = {}
            
            for metric in metrics:
                # Determine if lower is better
                ascending = True if metric in ["Execution Time (min)", "Cost ($)"] else False
                
                # Get sorted providers
                sorted_providers = filtered_data.sort_values(by=metric, ascending=ascending)["Provider"].tolist()
                
                # Assign points (4 for 1st, 3 for 2nd, etc.)
                for i, provider in enumerate(sorted_providers):
                    if provider not in rankings:
                        rankings[provider] = 0
                    
                    # Add points (reverse order)
                    rankings[provider] += len(sorted_providers) - i
            
            # Determine the winner
            winner = max(rankings.items(), key=lambda x: x[1])[0]
            
            # Create a points table
            points_data = []
            for provider, points in rankings.items():
                points_data.append({
                    "Provider": provider,
                    "Points": points
                })
            
            points_df = pd.DataFrame(points_data).sort_values(by="Points", ascending=False)
            points_df["Rank"] = range(1, len(points_df) + 1)
            points_df = points_df[["Rank", "Provider", "Points"]]
            
            # Display the winner
            st.markdown(f"""
            <div style="text-align: center; margin: 20px 0;">
                <div style="font-family: 'VT323', monospace; font-size: 36px; color: #0066cc;">
                    👑 {winner} 👑
                </div>
                <div style="font-family: 'Space Mono', monospace; font-size: 18px; color: #0a0a20;">
                    BENCHMARK CHAMPION
                </div>
                <div style="font-family: 'Space Mono', monospace; font-size: 14px; color: #0a0a20; margin-top: 10px;">
                    with {rankings[winner]} total points
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Display the points table
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                points_df = points_df.rename(columns={
                    "Rank": "POSITION",
                    "Provider": "PROVIDER",
                    "Points": "TOTAL POINTS"
                })
                st.table(points_df)
    else:
        # Initial state - no benchmark run yet
        st.markdown("""
        <div style="text-align: center; margin: 50px 0;">
            <div style="font-family: 'VT323', monospace; font-size: 24px; color: #0066cc;">
                SELECT A WORKLOAD AND CLICK "RUN BENCHMARK" TO BEGIN
            </div>
            <div style="font-family: 'Space Mono', monospace; font-size: 16px; color: #0a0a20; margin-top: 10px;">
                The benchmark will compare FlexAI against AWS, GCP, and Azure
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Display sample screenshots of what the benchmark will show
        st.markdown("""
        <div class="css-card">
            <h3 style="font-family: 'VT323', monospace; color: #0066cc;">ABOUT THIS BENCHMARK</h3>
            <p>This interactive demonstration compares the performance and cost of running AI workloads across different cloud platforms:</p>
            <ul>
                <li>⚡ <strong>Performance metrics</strong>: Execution time, throughput, GPU utilization</li>
                <li>💰 <strong>Cost analysis</strong>: Total cost, cost per hour, estimated savings</li>
                <li>🏆 <strong>Rankings</strong>: See how each platform performs across different metrics</li>
            </ul>
            <p>Choose your workload scenario from the sidebar and run the benchmark to see detailed comparisons!</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()