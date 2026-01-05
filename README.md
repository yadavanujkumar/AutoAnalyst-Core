# AutoAnalyst-Core 📊

## End-to-End Data Analytics & Intelligence Platform

AutoAnalyst-Core is a comprehensive, automated data analytics platform that functions as an AI-powered data scientist. It handles the complete data analytics workflow from ingestion to insights, with natural language query capabilities.

## ✨ Features

### 🔄 Automated Ingestion & Validation
- **Auto-detect file formats**: Automatically identifies CSV, Excel, JSON, and SQL database formats
- **Schema detection**: Analyzes and reports column types, null values, and data statistics
- **Data integrity checks**: 
  - Detects negative values in age/price columns
  - Identifies missing and null values
  - Flags statistical outliers using IQR method
  - Validates data types and logical constraints

### 🧹 Intelligent Cleaning & Feature Engineering
- **Auto-cleaning pipelines**:
  - Imputes missing values (median for numeric, mode for categorical)
  - Removes duplicate rows
  - Normalizes text (trims whitespace, standardizes formatting)
  - Fixes data types automatically
- **Automatic feature generation**:
  - Extracts date components (year, month, day, day of week, quarter, hour)
  - Creates categorical bins for numerical data
  - Generates interaction features and ratios

### 📊 Interactive Visualization Dashboard
- **Dynamic charts** powered by Plotly:
  - Distribution plots (histograms with box plots)
  - Scatter plots with color/size encoding
  - Correlation heatmaps
  - Time series analysis
  - Box plots for outlier visualization
  - Grouped bar charts
- **Auto-generated dashboard**: Creates comprehensive multi-chart dashboards automatically
- **Interactive features**: Hover details, zoom, pan, and drill-down capabilities

### 💬 Natural Language Query Engine
- **LLM-powered interface** using OpenAI GPT:
  - Ask questions in plain English (e.g., "What were the average sales in December?")
  - Automatically translates to executable Pandas code
  - Returns results with appropriate visualizations
  - Query history tracking
  - Smart query suggestions based on your data

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yadavanujkumar/AutoAnalyst-Core.git
   cd AutoAnalyst-Core
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure OpenAI API (Optional, for NL Query features)**:
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

### Running the Application

1. **Start the Streamlit app**:
   ```bash
   streamlit run app.py
   ```

2. **Open your browser** to `http://localhost:8501`

3. **Upload your data** in the Data Ingestion page (CSV, Excel, or JSON)

4. **Explore the modules**:
   - ✅ Validate your data
   - 🧹 Clean your data
   - 🔧 Engineer new features
   - 📈 Create visualizations
   - 💬 Ask questions in natural language

## 📁 Project Structure

```
AutoAnalyst-Core/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
├── .gitignore                      # Git ignore rules
├── modules/                        # Core modules
│   ├── __init__.py
│   ├── data_ingestion.py          # Data loading and format detection
│   ├── data_validation.py         # Data quality checks
│   ├── data_cleaning.py           # Automated cleaning pipelines
│   ├── feature_engineering.py     # Feature generation
│   ├── visualization.py           # Plotly visualizations
│   └── nl_query_engine.py         # Natural language queries
├── utils/                          # Utility scripts
│   └── generate_sample_data.py    # Sample data generator
└── data/                           # Data directory (for samples)
```

## 💡 Usage Examples

### Data Ingestion
```python
from modules.data_ingestion import DataIngestion

ingestion = DataIngestion()
df, metadata = ingestion.ingest_data("data.csv")
schema = ingestion.detect_schema(df)
```

### Data Validation
```python
from modules.data_validation import DataValidator

validator = DataValidator()
validation_results = validator.validate_data(df)
report = validator.generate_validation_report(validation_results)
```

### Data Cleaning
```python
from modules.data_cleaning import DataCleaner

cleaner = DataCleaner()
df_cleaned = cleaner.auto_clean(df)
cleaning_log = cleaner.get_cleaning_log()
```

### Feature Engineering
```python
from modules.feature_engineering import FeatureEngineer

engineer = FeatureEngineer()
df_featured = engineer.auto_engineer_features(df)
feature_log = engineer.get_feature_log()
```

### Visualization
```python
from modules.visualization import DataVisualizer

visualizer = DataVisualizer()
fig = visualizer.create_scatter_plot(df, x='age', y='sales', color='region')
fig.show()
```

### Natural Language Queries
```python
from modules.nl_query_engine import NLQueryEngine

query_engine = NLQueryEngine(df)
result, explanation, error = query_engine.query("What is the average sales by region?")
```

## 🛠️ Tech Stack

- **Frontend**: Streamlit (UI framework)
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly (interactive charts)
- **NLP/LLM**: OpenAI API, LangChain
- **Database**: SQLAlchemy (for SQL support)
- **Excel Support**: openpyxl
- **ML/Stats**: scikit-learn

## 📊 Sample Data

Generate sample data for testing:

```bash
cd utils
python generate_sample_data.py
```

This creates sample sales data in CSV, Excel, and JSON formats in the `data/` directory.

## 🔐 Security & Privacy

- API keys are stored securely in `.env` files (not committed to git)
- Data is processed locally on your machine
- No data is sent to external services except OpenAI API for NL queries (if enabled)
- Generated code is executed in a safe environment with restricted builtins

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the terms specified in the LICENSE file.

## 🙏 Acknowledgments

- Built with Streamlit for rapid UI development
- Powered by OpenAI GPT for natural language understanding
- Uses Plotly for beautiful, interactive visualizations

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

**Made with ❤️ by the AutoAnalyst-Core Team**