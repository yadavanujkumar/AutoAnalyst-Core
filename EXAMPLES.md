# AutoAnalyst-Core Usage Examples

This document provides practical examples of using AutoAnalyst-Core modules programmatically.

## Table of Contents
1. [Basic Usage](#basic-usage)
2. [Data Ingestion Examples](#data-ingestion-examples)
3. [Data Validation Examples](#data-validation-examples)
4. [Data Cleaning Examples](#data-cleaning-examples)
5. [Feature Engineering Examples](#feature-engineering-examples)
6. [Visualization Examples](#visualization-examples)
7. [NL Query Examples](#nl-query-examples)
8. [Complete Pipeline Example](#complete-pipeline-example)

## Basic Usage

### Installation and Setup

```bash
# Install dependencies
pip install -r requirements.txt

# For NL query features, set up OpenAI API key
echo "OPENAI_API_KEY=your_key_here" > .env
```

### Quick Start

```python
from modules.data_ingestion import DataIngestion

# Load data
ingestion = DataIngestion()
df, metadata = ingestion.ingest_data('your_data.csv')
print(f"Loaded {metadata['rows']} rows")
```

## Data Ingestion Examples

### Example 1: Load CSV File

```python
from modules.data_ingestion import DataIngestion

ingestion = DataIngestion()
df, metadata = ingestion.ingest_data('data/sales.csv')

print(f"Format: {metadata['format']}")
print(f"Rows: {metadata['rows']}")
print(f"Columns: {metadata['columns']}")
```

### Example 2: Load Excel with Specific Sheet

```python
# Load specific sheet
df, metadata = ingestion.ingest_data(
    'data/report.xlsx',
    sheet_name='Q1 Sales'
)
```

### Example 3: Load JSON with Nested Structure

```python
# Load JSON (will be flattened automatically)
df, metadata = ingestion.ingest_data('data/users.json')
```

### Example 4: Analyze Schema

```python
schema = ingestion.detect_schema(df)

for col, info in schema['columns'].items():
    print(f"{col}:")
    print(f"  Type: {info['dtype']}")
    print(f"  Nulls: {info['null_percentage']:.1f}%")
    print(f"  Unique: {info['unique_count']}")
```

## Data Validation Examples

### Example 1: Comprehensive Validation

```python
from modules.data_validation import DataValidator

validator = DataValidator()
results = validator.validate_data(df)

# Check for issues
if results['issues']:
    print("❌ Issues found:")
    for issue in results['issues']:
        print(f"  - {issue}")

# Check for warnings
if results['warnings']:
    print("⚠️ Warnings:")
    for warning in results['warnings']:
        print(f"  - {warning}")
```

### Example 2: Check Missing Values

```python
missing_info = results['missing_values']

if missing_info['has_missing']:
    print(f"Total missing: {missing_info['total_missing']}")
    for col, details in missing_info['details'].items():
        print(f"{col}: {details['percentage']:.1f}% missing")
```

### Example 3: Detect Outliers

```python
outliers = results['outliers']

for col in outliers['columns_with_outliers']:
    details = outliers['details'][col]
    print(f"{col}:")
    print(f"  Outliers: {details['count']} ({details['percentage']:.1f}%)")
    print(f"  Range: [{details['lower_bound']:.2f}, {details['upper_bound']:.2f}]")
```

### Example 4: Generate Report

```python
report = validator.generate_validation_report(results)
print(report)

# Save report to file
with open('validation_report.txt', 'w') as f:
    f.write(report)
```

## Data Cleaning Examples

### Example 1: Auto Clean with Default Settings

```python
from modules.data_cleaning import DataCleaner

cleaner = DataCleaner()
df_clean = cleaner.auto_clean(df)

print(f"Rows before: {len(df)}")
print(f"Rows after: {len(df_clean)}")
print("\nOperations:")
for op in cleaner.get_cleaning_log():
    print(f"  - {op}")
```

### Example 2: Custom Cleaning Configuration

```python
config = {
    'remove_duplicates': True,
    'handle_missing': True,
    'normalize_text': False,  # Don't normalize
    'fix_dtypes': True
}

df_clean = cleaner.auto_clean(df, config)
```

### Example 3: Selective Cleaning

```python
# Only remove duplicates
df_no_dupes = cleaner.remove_duplicates(df)

# Only handle missing values
df_no_missing = cleaner.handle_missing_values(df)

# Only normalize text
df_normalized = cleaner.normalize_text(df)
```

## Feature Engineering Examples

### Example 1: Auto Generate All Features

```python
from modules.feature_engineering import FeatureEngineer

engineer = FeatureEngineer()
df_featured = engineer.auto_engineer_features(df)

print(f"Original columns: {len(df.columns)}")
print(f"New columns: {len(df_featured.columns)}")
print("\nNew features:")
for feature in engineer.get_feature_log():
    print(f"  - {feature}")
```

### Example 2: Date Feature Extraction

```python
# Extract features from date columns
df_with_dates = engineer.extract_date_features(df)

# You'll get: year, month, day, day_of_week, quarter, hour
```

### Example 3: Create Bins

```python
# Create categorical bins for numeric columns
df_binned = engineer.create_numeric_bins(df, n_bins=5)

# Check new binned columns
binned_cols = [col for col in df_binned.columns if col.endswith('_bin')]
print(f"Binned columns: {binned_cols}")
```

### Example 4: Custom Feature Engineering

```python
# After auto-engineering, add your own features
df_featured['price_per_unit'] = df_featured['price'] / df_featured['quantity']
df_featured['discount_rate'] = (df_featured['original_price'] - df_featured['price']) / df_featured['original_price']
```

## Visualization Examples

### Example 1: Create Distribution Plot

```python
from modules.visualization import DataVisualizer

visualizer = DataVisualizer()

# Numeric distribution
fig = visualizer.create_distribution_plot(df, 'sales')
fig.show()

# Categorical distribution
fig = visualizer.create_distribution_plot(df, 'category')
fig.show()
```

### Example 2: Create Scatter Plot

```python
# Simple scatter
fig = visualizer.create_scatter_plot(df, x='age', y='income')
fig.show()

# Scatter with color and size
fig = visualizer.create_scatter_plot(
    df, 
    x='age', 
    y='income',
    color='region',
    size='purchases'
)
fig.show()
```

### Example 3: Correlation Heatmap

```python
fig = visualizer.create_correlation_heatmap(df)
fig.show()

# Save to file
fig.write_html('correlation_heatmap.html')
```

### Example 4: Time Series

```python
fig = visualizer.create_time_series_plot(
    df,
    date_column='date',
    value_column='sales'
)
fig.show()
```

### Example 5: Box Plot

```python
# Single column
fig = visualizer.create_box_plot(df, 'price')
fig.show()

# Grouped by category
fig = visualizer.create_box_plot(df, 'price', group_by='category')
fig.show()
```

### Example 6: Auto-Dashboard

```python
# Generate multiple visualizations at once
figures = visualizer.create_summary_dashboard(df)

# Display all
for i, fig in enumerate(figures, 1):
    print(f"Visualization {i}")
    fig.show()

# Save all to HTML
for i, fig in enumerate(figures, 1):
    fig.write_html(f'dashboard_chart_{i}.html')
```

## NL Query Examples

### Example 1: Basic Query

```python
from modules.nl_query_engine import NLQueryEngine

query_engine = NLQueryEngine(df)

# Ask a question
result, explanation, error = query_engine.query(
    "What is the average sales by region?"
)

if error:
    print(f"Error: {error}")
else:
    print(explanation)
    print(result)
```

### Example 2: Complex Query

```python
# More complex analysis
result, explanation, error = query_engine.query(
    "Show me the top 5 products by total revenue in December 2023"
)

if not error:
    print(result)
```

### Example 3: Get Query Suggestions

```python
# Get suggestions based on your data
suggestions = query_engine.get_query_suggestions()

print("Try these queries:")
for i, suggestion in enumerate(suggestions, 1):
    print(f"{i}. {suggestion}")
```

### Example 4: Query History

```python
# View previous queries
history = query_engine.get_query_history()

for entry in history:
    print(f"Query: {entry['query']}")
    print(f"Code: {entry['code']}")
    print(f"Success: {entry['success']}")
    print("-" * 50)
```

## Complete Pipeline Example

### Example: End-to-End Analysis

```python
from modules.data_ingestion import DataIngestion
from modules.data_validation import DataValidator
from modules.data_cleaning import DataCleaner
from modules.feature_engineering import FeatureEngineer
from modules.visualization import DataVisualizer
from modules.nl_query_engine import NLQueryEngine

# 1. Ingest
print("Step 1: Ingesting data...")
ingestion = DataIngestion()
df, metadata = ingestion.ingest_data('data/sales.csv')
print(f"✓ Loaded {metadata['rows']} rows")

# 2. Validate
print("\nStep 2: Validating data...")
validator = DataValidator()
validation = validator.validate_data(df)
print(f"✓ Found {len(validation['warnings'])} warnings")

# 3. Clean
print("\nStep 3: Cleaning data...")
cleaner = DataCleaner()
df_clean = cleaner.auto_clean(df)
print(f"✓ Cleaned: {len(df)} → {len(df_clean)} rows")

# 4. Engineer Features
print("\nStep 4: Engineering features...")
engineer = FeatureEngineer()
df_featured = engineer.auto_engineer_features(df_clean)
print(f"✓ Features: {len(df_clean.columns)} → {len(df_featured.columns)}")

# 5. Visualize
print("\nStep 5: Creating visualizations...")
visualizer = DataVisualizer()
figures = visualizer.create_summary_dashboard(df_featured)
print(f"✓ Created {len(figures)} visualizations")

# 6. Query
print("\nStep 6: Natural language query...")
query_engine = NLQueryEngine(df_featured)
result, explanation, error = query_engine.query(
    "What is the average sales by region?"
)
if not error:
    print("✓ Query executed successfully")
    print(result)

# 7. Export
print("\nStep 7: Exporting results...")
df_featured.to_csv('output_processed.csv', index=False)
print("✓ Saved to output_processed.csv")

print("\n✅ Complete pipeline finished!")
```

### Example: Custom Pipeline

```python
# Build a custom pipeline for specific needs
def custom_analysis_pipeline(file_path, output_path):
    """Custom analysis pipeline with specific requirements"""
    
    # Load
    ingestion = DataIngestion()
    df, _ = ingestion.ingest_data(file_path)
    
    # Clean (no duplicate removal, keep all data)
    cleaner = DataCleaner()
    config = {
        'remove_duplicates': False,
        'handle_missing': True,
        'normalize_text': True,
        'fix_dtypes': True
    }
    df_clean = cleaner.auto_clean(df, config)
    
    # Add custom features
    engineer = FeatureEngineer()
    df_featured = engineer.auto_engineer_features(df_clean)
    
    # Add domain-specific features
    df_featured['profit_margin'] = (
        (df_featured['revenue'] - df_featured['cost']) / 
        df_featured['revenue'] * 100
    )
    
    # Save
    df_featured.to_csv(output_path, index=False)
    
    return df_featured

# Use it
result = custom_analysis_pipeline('input.csv', 'output.csv')
```

## Tips and Best Practices

1. **Always validate before cleaning**: Understand your data quality issues first
2. **Check cleaning logs**: Review what operations were performed
3. **Feature engineering**: Start with auto-generated features, then add custom ones
4. **Visualizations**: Use the dashboard for quick overview, then create specific plots
5. **NL queries**: Start with suggested queries to understand capabilities
6. **Error handling**: Always check for errors in validation and cleaning
7. **Export regularly**: Save intermediate results during analysis
8. **Memory management**: For large files, process in chunks if needed

## Common Patterns

### Pattern 1: Quick Analysis

```python
# For quick data exploration
ingestion = DataIngestion()
df, _ = ingestion.ingest_data('data.csv')
visualizer = DataVisualizer()
visualizer.create_summary_dashboard(df)
```

### Pattern 2: Production Pipeline

```python
# For production data processing
def process_data(input_file, output_file):
    ingestion = DataIngestion()
    df, _ = ingestion.ingest_data(input_file)
    
    cleaner = DataCleaner()
    df_clean = cleaner.auto_clean(df)
    
    engineer = FeatureEngineer()
    df_final = engineer.auto_engineer_features(df_clean)
    
    df_final.to_csv(output_file, index=False)
    return df_final
```

### Pattern 3: Interactive Analysis

```python
# For interactive Jupyter notebook analysis
from IPython.display import display

df, _ = DataIngestion().ingest_data('data.csv')
validation = DataValidator().validate_data(df)

# Display validation report
print(DataValidator().generate_validation_report(validation))

# Display visualizations
visualizer = DataVisualizer()
for fig in visualizer.create_summary_dashboard(df):
    fig.show()
```

---

For more examples and updates, check the [GitHub repository](https://github.com/yadavanujkumar/AutoAnalyst-Core).
