"""
Test script for AutoAnalyst-Core
Tests all core modules and functionalities
"""

import sys
import pandas as pd
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from modules.data_ingestion import DataIngestion
from modules.data_validation import DataValidator
from modules.data_cleaning import DataCleaner
from modules.feature_engineering import FeatureEngineer
from modules.visualization import DataVisualizer
from modules.nl_query_engine import NLQueryEngine


def test_data_ingestion():
    """Test data ingestion module"""
    print("\n" + "="*60)
    print("Testing Data Ingestion Module")
    print("="*60)
    
    ingestion = DataIngestion()
    
    # Test CSV
    print("\n✓ Testing CSV ingestion...")
    df_csv, meta_csv = ingestion.ingest_data('data/sample_sales_data.csv')
    assert len(df_csv) > 0, "CSV data should not be empty"
    assert len(df_csv.columns) > 0, "CSV should have columns"
    print(f"  Loaded {len(df_csv)} rows, {len(df_csv.columns)} columns")
    
    # Test Excel
    print("\n✓ Testing Excel ingestion...")
    df_excel, meta_excel = ingestion.ingest_data('data/sample_sales_data.xlsx')
    assert len(df_excel) > 0, "Excel data should not be empty"
    print(f"  Loaded {len(df_excel)} rows, {len(df_excel.columns)} columns")
    
    # Test JSON
    print("\n✓ Testing JSON ingestion...")
    df_json, meta_json = ingestion.ingest_data('data/sample_sales_data.json')
    assert len(df_json) > 0, "JSON data should not be empty"
    print(f"  Loaded {len(df_json)} rows, {len(df_json.columns)} columns")
    
    # Test schema detection
    print("\n✓ Testing schema detection...")
    schema = ingestion.detect_schema(df_csv)
    assert 'columns' in schema, "Schema should have columns"
    assert 'summary' in schema, "Schema should have summary"
    print(f"  Detected {len(schema['columns'])} columns")
    
    print("\n✅ Data Ingestion Module: PASSED")
    return df_csv


def test_data_validation(df):
    """Test data validation module"""
    print("\n" + "="*60)
    print("Testing Data Validation Module")
    print("="*60)
    
    validator = DataValidator()
    
    # Test validation
    print("\n✓ Testing data validation...")
    results = validator.validate_data(df)
    assert 'warnings' in results, "Results should have warnings"
    assert 'issues' in results, "Results should have issues"
    print(f"  Found {len(results['warnings'])} warnings, {len(results['issues'])} issues")
    
    # Test missing values check
    print("\n✓ Testing missing values detection...")
    assert 'missing_values' in results
    print(f"  Missing values check: {'Found' if results['missing_values']['has_missing'] else 'None'}")
    
    # Test duplicates check
    print("\n✓ Testing duplicates detection...")
    assert 'duplicates' in results
    print(f"  Duplicate rows: {results['duplicates']['duplicate_count']}")
    
    # Test outliers check
    print("\n✓ Testing outliers detection...")
    assert 'outliers' in results
    print(f"  Columns with outliers: {len(results['outliers']['columns_with_outliers'])}")
    
    # Test validation report
    print("\n✓ Testing validation report generation...")
    report = validator.generate_validation_report(results)
    assert len(report) > 0, "Report should not be empty"
    print(f"  Generated report: {len(report)} characters")
    
    print("\n✅ Data Validation Module: PASSED")
    return results


def test_data_cleaning(df):
    """Test data cleaning module"""
    print("\n" + "="*60)
    print("Testing Data Cleaning Module")
    print("="*60)
    
    cleaner = DataCleaner()
    
    # Test auto cleaning
    print("\n✓ Testing auto cleaning...")
    df_clean = cleaner.auto_clean(df)
    assert len(df_clean) > 0, "Cleaned data should not be empty"
    print(f"  Rows: {len(df)} → {len(df_clean)}")
    
    # Test cleaning log
    print("\n✓ Testing cleaning log...")
    log = cleaner.get_cleaning_log()
    assert isinstance(log, list), "Log should be a list"
    print(f"  Operations performed: {len(log)}")
    for operation in log:
        print(f"    - {operation}")
    
    print("\n✅ Data Cleaning Module: PASSED")
    return df_clean


def test_feature_engineering(df):
    """Test feature engineering module"""
    print("\n" + "="*60)
    print("Testing Feature Engineering Module")
    print("="*60)
    
    engineer = FeatureEngineer()
    
    # Test auto feature engineering
    print("\n✓ Testing auto feature engineering...")
    df_featured = engineer.auto_engineer_features(df)
    assert len(df_featured.columns) >= len(df.columns), "Should have more or equal columns"
    print(f"  Columns: {len(df.columns)} → {len(df_featured.columns)}")
    
    # Test feature log
    print("\n✓ Testing feature log...")
    log = engineer.get_feature_log()
    assert isinstance(log, list), "Log should be a list"
    print(f"  Features created: {len(log)}")
    
    print("\n✅ Feature Engineering Module: PASSED")
    return df_featured


def test_visualization(df):
    """Test visualization module"""
    print("\n" + "="*60)
    print("Testing Visualization Module")
    print("="*60)
    
    visualizer = DataVisualizer()
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    
    # Test distribution plot
    print("\n✓ Testing distribution plot...")
    if numeric_cols:
        fig = visualizer.create_distribution_plot(df, numeric_cols[0])
        assert fig is not None, "Figure should not be None"
        print(f"  Created distribution plot for '{numeric_cols[0]}'")
    
    # Test scatter plot
    print("\n✓ Testing scatter plot...")
    if len(numeric_cols) >= 2:
        fig = visualizer.create_scatter_plot(df, numeric_cols[0], numeric_cols[1])
        assert fig is not None, "Figure should not be None"
        print(f"  Created scatter plot: {numeric_cols[0]} vs {numeric_cols[1]}")
    
    # Test correlation heatmap
    print("\n✓ Testing correlation heatmap...")
    if len(numeric_cols) > 1:
        fig = visualizer.create_correlation_heatmap(df)
        assert fig is not None, "Figure should not be None"
        print(f"  Created correlation heatmap")
    
    # Test box plot
    print("\n✓ Testing box plot...")
    if numeric_cols:
        fig = visualizer.create_box_plot(df, numeric_cols[0])
        assert fig is not None, "Figure should not be None"
        print(f"  Created box plot for '{numeric_cols[0]}'")
    
    # Test dashboard
    print("\n✓ Testing summary dashboard...")
    figures = visualizer.create_summary_dashboard(df)
    assert len(figures) > 0, "Should create at least one figure"
    print(f"  Created {len(figures)} visualizations")
    
    print("\n✅ Visualization Module: PASSED")


def test_nl_query_engine(df):
    """Test natural language query engine"""
    print("\n" + "="*60)
    print("Testing Natural Language Query Engine")
    print("="*60)
    
    query_engine = NLQueryEngine(df)
    
    # Test initialization
    print("\n✓ Testing query engine initialization...")
    if query_engine.llm_available:
        print("  OpenAI API available")
    else:
        print("  OpenAI API not configured (optional)")
    
    # Test schema context
    print("\n✓ Testing schema context generation...")
    schema = query_engine.get_schema_context()
    assert len(schema) > 0, "Schema context should not be empty"
    print(f"  Schema context: {len(schema)} characters")
    
    # Test query suggestions
    print("\n✓ Testing query suggestions...")
    suggestions = query_engine.get_query_suggestions()
    assert len(suggestions) > 0, "Should have suggestions"
    print(f"  Generated {len(suggestions)} suggestions")
    for i, suggestion in enumerate(suggestions[:3], 1):
        print(f"    {i}. {suggestion}")
    
    print("\n✅ Natural Language Query Engine: PASSED")


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("AutoAnalyst-Core - Test Suite")
    print("="*60)
    
    try:
        # Test each module
        df = test_data_ingestion()
        validation_results = test_data_validation(df)
        df_clean = test_data_cleaning(df)
        df_featured = test_feature_engineering(df_clean)
        test_visualization(df_featured)
        test_nl_query_engine(df_featured)
        
        # Summary
        print("\n" + "="*60)
        print("✅ ALL TESTS PASSED!")
        print("="*60)
        print("\nAutoAnalyst-Core is working correctly.")
        print("Run 'streamlit run app.py' to start the application.")
        print("="*60)
        
        return True
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        return False
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
