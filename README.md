# FlexAI Benchmarking Suite

![Image](https://github.com/user-attachments/assets/83ccef0f-9025-4ce5-a234-5445bc62376d)

![Image](https://github.com/user-attachments/assets/4b9ec90f-ea2d-4fab-a5e8-847f43e73174)

![Image](https://github.com/user-attachments/assets/c2f8add0-c8ff-4b15-b080-7306d34f1eb7)

![Image](https://github.com/user-attachments/assets/920e3fda-7f7c-4ec6-9c1b-b1b0cbdd202e)

A retro-styled interactive application for comparing AI workload performance and costs across cloud providers (FlexAI, AWS, GCP, Azure). This tool helps demonstrate the cost and performance advantages of FlexAI's Workload as a Service (WaaS) platform.

## 🎮 Features

- **Interactive Performance Comparison**: Visualize execution time, throughput, and resource utilization metrics across platforms
- **Detailed Cost Analysis**: Compare costs across providers and calculate potential savings
- **Performance Leaderboards**: See rankings across multiple performance dimensions
- **Customizable Workloads**: Compare different AI tasks (LLM fine-tuning, batch inference, CV model training)
- **Retro Gaming Aesthetic**: Engaging visual design with pixel-perfect UI elements and vibrant colors

## 📊 Business Value

- Demonstrate FlexAI's performance advantages with engaging, data-driven visualizations
- Help customers quantify potential cost savings when switching to FlexAI
- Support sales and marketing teams with compelling, interactive demonstrations
- Provide transparent, objective comparisons with major cloud providers

## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/flexai/benchmark-suite.git
cd flexai-benchmark

# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## 💻 Usage

```bash
# Run the Streamlit application
streamlit run app.py
```

Navigate to http://localhost:8501 in your browser to view the application.

### Basic Usage Instructions:

1. Select a workload type from the sidebar
2. Configure hardware options for each provider
3. Click "RUN BENCHMARK" to execute the simulation
4. Explore the results across the Performance, Cost, and Leaderboard tabs

## 📁 Project Structure

```
flexai-benchmark/
│
├── app.py                      # Main Streamlit application
├── requirements.txt            # Dependencies 
├── README.md                   # Project documentation
│
├── data/                       # Sample and generated data
│   ├── sample_benchmarks.csv   # Pre-generated benchmark results
│   └── hardware_configs.json   # Hardware configuration options
│
├── src/                        # Source code modules
│   ├── __init__.py
│   ├── data_generator.py       # Functions to generate sample data
│   ├── visualizations.py       # Chart creation functions
│   ├── benchmark_simulator.py  # Benchmark simulation logic
│   └── utils.py                # Helper functions
│
├── static/                     # Static assets
│   ├── css/
│   │   └── retro_style.css     # Custom CSS styles
│   └── images/
│       ├── logo.png            # FlexAI logo
│       └── favicon.ico         # Browser favicon
│
└── tests/                      # Unit tests
    ├── __init__.py
    ├── test_data_generator.py
    └── test_visualizations.py
```

## 🛠️ Technologies Used

- **Streamlit**: For the interactive web application
- **Plotly**: For interactive data visualizations
- **Pandas**: For data manipulation and analysis
- **Python**: Core programming language

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is proprietary and confidential. © 2025 FlexAI Inc. All rights reserved.

## 🙏 Acknowledgments

- Special thanks to the FlexAI Engineering team for providing performance metrics
- Retro gaming inspiration from classic arcade games of the 1980s
- Benchmark methodology based on industry standard practices

---

For questions or support, please contact Sameerm140299@gmail.com
