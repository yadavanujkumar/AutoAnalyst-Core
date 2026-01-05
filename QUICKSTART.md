# Quick Start Guide

## 🚀 Getting Started with AutoAnalyst-Core

### Option 1: Automatic Setup (Recommended)

#### Linux/Mac:
```bash
chmod +x setup.sh
./setup.sh
```

#### Windows:
```powershell
.\setup.ps1
```

The setup script will:
- Create a virtual environment
- Install all dependencies
- Generate sample data
- Create `.env` file

### Option 2: Manual Setup

#### 1. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

#### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 3. Configure Environment (Optional for NL Query)
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

#### 4. Generate Sample Data
```bash
python3 utils/generate_sample_data.py
```

### 🎯 Running the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

### 📊 Using AutoAnalyst-Core

#### 1. Data Ingestion
- Click "📁 Data Ingestion" in the sidebar
- Upload your CSV, Excel, or JSON file
- View schema and data preview

#### 2. Data Validation
- Click "✅ Data Validation"
- Run validation to check data quality
- Review warnings and issues

#### 3. Data Cleaning
- Click "🧹 Data Cleaning"
- Configure cleaning options
- Clean your data and download results

#### 4. Feature Engineering
- Click "🔧 Feature Engineering"
- Generate new features automatically
- View feature engineering log

#### 5. Visualization
- Click "📈 Visualization"
- Create various chart types:
  - Distribution plots
  - Scatter plots
  - Correlation heatmaps
  - Time series
  - Box plots
- Generate auto-dashboard

#### 6. Natural Language Queries
- Click "💬 Natural Language Query"
- Ask questions in plain English
- View results and visualizations

### 💡 Example Queries

Try these natural language queries:

- "What is the average sales by region?"
- "Show me the top 10 products by quantity"
- "What were the total sales in December?"
- "Which region has the highest satisfaction score?"
- "Show me customers older than 50 years"

### 📁 Sample Data

The platform comes with sample sales data (`sample_sales_data.csv`) containing:
- Date (transaction date)
- Region (North, South, East, West)
- Product (Product A-E)
- Sales (revenue amount)
- Quantity (units sold)
- Customer Age
- Satisfaction Score (1-5 scale)

### 🔧 Troubleshooting

#### Module not found errors
```bash
pip install -r requirements.txt --upgrade
```

#### Streamlit not starting
```bash
streamlit --version
streamlit cache clear
streamlit run app.py
```

#### OpenAI API errors
- Make sure `.env` file exists with valid `OPENAI_API_KEY`
- Check your OpenAI account has credits
- Verify API key format (starts with `sk-`)

### 🎓 Next Steps

1. **Explore the sample data** to understand the platform capabilities
2. **Upload your own data** in CSV, Excel, or JSON format
3. **Try different visualizations** to gain insights
4. **Use natural language queries** to ask questions about your data
5. **Export cleaned and featured data** for further analysis

### 📚 Documentation

For detailed module documentation, see:
- [Data Ingestion Module](modules/data_ingestion.py)
- [Data Validation Module](modules/data_validation.py)
- [Data Cleaning Module](modules/data_cleaning.py)
- [Feature Engineering Module](modules/feature_engineering.py)
- [Visualization Module](modules/visualization.py)
- [NL Query Engine](modules/nl_query_engine.py)

### 🤝 Need Help?

- Check the [README.md](README.md) for detailed information
- Open an issue on GitHub
- Review the inline code documentation

### 🎉 Happy Analyzing!
