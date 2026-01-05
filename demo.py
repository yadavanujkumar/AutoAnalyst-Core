"""
Demo Script for AutoAnalyst-Core
Demonstrates the complete workflow of the platform
"""

import pandas as pd
from pathlib import Path

from modules.data_ingestion import DataIngestion
from modules.data_validation import DataValidator
from modules.data_cleaning import DataCleaner
from modules.feature_engineering import FeatureEngineer
from modules.visualization import DataVisualizer


def print_header(text):
    """Print a formatted header"""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70 + "\n")


def demo_workflow():
    """Demonstrate the complete AutoAnalyst-Core workflow"""
    
    print_header("🚀 AutoAnalyst-Core Demo")
    
    # Step 1: Data Ingestion
    print_header("📁 Step 1: Data Ingestion")
    
    ingestion = DataIngestion()
    print("Loading sample sales data...")
    df, metadata = ingestion.ingest_data('data/sample_sales_data.csv')
    
    print(f"\n✅ Successfully loaded data:")
    print(f"   - Rows: {metadata['rows']}")
    print(f"   - Columns: {metadata['columns']}")
    print(f"   - Format: {metadata['format']}")
    
    print("\n📋 Column Information:")
    schema = ingestion.detect_schema(df)
    for col, info in list(schema['columns'].items())[:5]:
        print(f"   - {col}: {info['dtype']} ({info['unique_count']} unique values)")
    
    print("\n👀 Data Preview:")
    print(df.head(3).to_string(index=False))
    
    # Step 2: Data Validation
    print_header("✅ Step 2: Data Validation")
    
    validator = DataValidator()
    print("Running data validation checks...")
    validation_results = validator.validate_data(df)
    
    print(f"\n📊 Validation Summary:")
    print(f"   - Total Rows: {validation_results['total_rows']}")
    print(f"   - Total Columns: {validation_results['total_columns']}")
    print(f"   - Issues Found: {len(validation_results['issues'])}")
    print(f"   - Warnings: {len(validation_results['warnings'])}")
    
    if validation_results['warnings']:
        print("\n⚠️ Warnings:")
        for warning in validation_results['warnings']:
            print(f"   • {warning}")
    
    if validation_results['missing_values']['has_missing']:
        print("\n📉 Missing Values Detected:")
        for col, details in validation_results['missing_values']['details'].items():
            print(f"   • {col}: {details['count']} missing ({details['percentage']:.1f}%)")
    
    if validation_results['duplicates']['has_duplicates']:
        print(f"\n🔄 Duplicate Rows: {validation_results['duplicates']['duplicate_count']}")
    
    # Step 3: Data Cleaning
    print_header("🧹 Step 3: Data Cleaning")
    
    cleaner = DataCleaner()
    print("Applying automated cleaning operations...")
    df_cleaned = cleaner.auto_clean(df)
    
    print(f"\n✅ Cleaning Complete:")
    print(f"   - Original Rows: {len(df)}")
    print(f"   - Cleaned Rows: {len(df_cleaned)}")
    print(f"   - Rows Removed: {len(df) - len(df_cleaned)}")
    
    print("\n📝 Operations Performed:")
    for operation in cleaner.get_cleaning_log():
        print(f"   • {operation}")
    
    # Step 4: Feature Engineering
    print_header("🔧 Step 4: Feature Engineering")
    
    engineer = FeatureEngineer()
    print("Generating new features automatically...")
    df_featured = engineer.auto_engineer_features(df_cleaned)
    
    print(f"\n✅ Feature Engineering Complete:")
    print(f"   - Original Features: {len(df_cleaned.columns)}")
    print(f"   - New Features: {len(df_featured.columns) - len(df_cleaned.columns)}")
    print(f"   - Total Features: {len(df_featured.columns)}")
    
    print("\n🆕 New Features Created:")
    feature_log = engineer.get_feature_log()
    for i, feature in enumerate(feature_log[:10], 1):
        print(f"   {i}. {feature}")
    if len(feature_log) > 10:
        print(f"   ... and {len(feature_log) - 10} more")
    
    # Step 5: Basic Statistics
    print_header("📊 Step 5: Statistical Summary")
    
    print("Numeric Column Statistics:")
    numeric_stats = df_featured.select_dtypes(include=['number']).describe()
    print(numeric_stats.to_string())
    
    # Step 6: Visualization
    print_header("📈 Step 6: Visualization")
    
    visualizer = DataVisualizer()
    print("Creating visualizations...")
    
    # Create various visualizations
    numeric_cols = df_featured.select_dtypes(include=['number']).columns.tolist()
    
    if len(numeric_cols) >= 2:
        print(f"\n✅ Available Visualizations:")
        print(f"   • Distribution plots for {len(numeric_cols)} numeric columns")
        print(f"   • Scatter plots for column pairs")
        print(f"   • Correlation heatmap")
        print(f"   • Box plots for outlier analysis")
        print(f"   • Time series analysis (if date columns exist)")
        
        # Generate dashboard
        figures = visualizer.create_summary_dashboard(df_featured)
        print(f"\n📊 Auto-generated dashboard with {len(figures)} visualizations")
    
    # Step 7: Summary
    print_header("🎉 Workflow Complete!")
    
    print("Summary of Results:")
    print(f"   ✓ Ingested {metadata['rows']} rows from {metadata['format']} format")
    print(f"   ✓ Validated data and found {len(validation_results['warnings'])} warnings")
    print(f"   ✓ Cleaned data, removing {len(df) - len(df_cleaned)} problematic rows")
    print(f"   ✓ Created {len(df_featured.columns) - len(df.columns)} new features")
    print(f"   ✓ Generated {len(figures) if 'figures' in locals() else 0} visualizations")
    
    print("\n💾 Saving results...")
    output_path = 'data/demo_output_cleaned_featured.csv'
    df_featured.to_csv(output_path, index=False)
    print(f"   Saved to: {output_path}")
    
    print_header("🚀 Next Steps")
    
    print("To explore the full interactive platform:")
    print("\n   1. Run: streamlit run app.py")
    print("   2. Upload your own data (CSV, Excel, JSON)")
    print("   3. Use natural language queries to analyze your data")
    print("   4. Create custom visualizations")
    print("   5. Export cleaned and featured data")
    
    print("\n" + "="*70)
    print("  Thank you for using AutoAnalyst-Core! 📊")
    print("="*70 + "\n")


if __name__ == "__main__":
    try:
        demo_workflow()
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
