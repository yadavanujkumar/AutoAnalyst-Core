"""
Generate sample data for testing AutoAnalyst-Core
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_sales_data(n_rows=1000):
    """Generate sample sales data"""
    
    np.random.seed(42)
    random.seed(42)
    
    # Generate dates
    start_date = datetime(2023, 1, 1)
    dates = [start_date + timedelta(days=i) for i in range(n_rows)]
    
    # Generate data
    regions = ['North', 'South', 'East', 'West']
    products = ['Product A', 'Product B', 'Product C', 'Product D', 'Product E']
    
    data = {
        'date': dates,
        'region': [random.choice(regions) for _ in range(n_rows)],
        'product': [random.choice(products) for _ in range(n_rows)],
        'sales': np.random.randint(100, 5000, n_rows),
        'quantity': np.random.randint(1, 100, n_rows),
        'customer_age': np.random.randint(18, 75, n_rows),
        'satisfaction_score': np.random.uniform(1, 5, n_rows).round(2)
    }
    
    df = pd.DataFrame(data)
    
    # Add some missing values
    missing_indices = np.random.choice(df.index, size=int(n_rows * 0.05), replace=False)
    df.loc[missing_indices, 'satisfaction_score'] = np.nan
    
    # Add some duplicates
    duplicate_rows = df.sample(n=10)
    df = pd.concat([df, duplicate_rows], ignore_index=True)
    
    # Add some outliers (negative ages)
    outlier_indices = np.random.choice(df.index, size=5, replace=False)
    df.loc[outlier_indices, 'customer_age'] = -np.random.randint(1, 50, 5)
    
    return df

if __name__ == "__main__":
    import os
    
    # Create data directory if it doesn't exist
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    # Generate and save sample data
    df = generate_sales_data()
    
    # Save as CSV
    csv_path = os.path.join(data_dir, 'sample_sales_data.csv')
    df.to_csv(csv_path, index=False)
    print(f"Generated sample_sales_data.csv with {len(df)} rows")
    
    # Save as Excel
    excel_path = os.path.join(data_dir, 'sample_sales_data.xlsx')
    df.to_excel(excel_path, index=False)
    print(f"Generated sample_sales_data.xlsx with {len(df)} rows")
    
    # Save as JSON
    json_path = os.path.join(data_dir, 'sample_sales_data.json')
    df.to_json(json_path, orient='records')
    print(f"Generated sample_sales_data.json with {len(df)} rows")
