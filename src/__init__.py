# Import main modules to make them available through the package
from .data_generator import generate_sample_data
from .visualizations import create_platform_comparison_chart, create_radar_chart
from .benchmark_simulator import simulate_benchmark_run
from .utils import format_currency, calculate_savings