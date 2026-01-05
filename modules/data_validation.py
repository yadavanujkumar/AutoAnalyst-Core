"""
Data Validation Module
Performs rigorous data integrity checks
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Tuple
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataValidator:
    """Handles data validation and integrity checks"""
    
    def __init__(self):
        self.validation_results = {}
        
    def validate_data(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Perform comprehensive data validation
        
        Args:
            df: Input DataFrame
            
        Returns:
            Dictionary containing validation results
        """
        results = {
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'issues': [],
            'warnings': [],
            'column_validations': {}
        }
        
        # Check for missing values
        missing_check = self.check_missing_values(df)
        results['missing_values'] = missing_check
        
        # Check for duplicates
        duplicate_check = self.check_duplicates(df)
        results['duplicates'] = duplicate_check
        
        # Check for outliers in numeric columns
        outlier_check = self.check_outliers(df)
        results['outliers'] = outlier_check
        
        # Check data types and logical constraints
        type_check = self.check_data_types(df)
        results['type_validation'] = type_check
        
        # Aggregate issues and warnings
        if missing_check['has_missing']:
            results['warnings'].append(f"Found missing values in {missing_check['columns_with_missing']} columns")
        
        if duplicate_check['duplicate_count'] > 0:
            results['warnings'].append(f"Found {duplicate_check['duplicate_count']} duplicate rows")
        
        if outlier_check['columns_with_outliers']:
            results['warnings'].append(f"Found outliers in {len(outlier_check['columns_with_outliers'])} columns")
        
        logger.info(f"Validation complete: {len(results['issues'])} issues, {len(results['warnings'])} warnings")
        return results
    
    def check_missing_values(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Check for missing values in DataFrame"""
        missing_info = {
            'has_missing': df.isnull().any().any(),
            'total_missing': int(df.isnull().sum().sum()),
            'columns_with_missing': int(df.isnull().any().sum()),
            'details': {}
        }
        
        for col in df.columns:
            if df[col].isnull().any():
                missing_info['details'][col] = {
                    'count': int(df[col].isnull().sum()),
                    'percentage': float(df[col].isnull().sum() / len(df) * 100)
                }
        
        return missing_info
    
    def check_duplicates(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Check for duplicate rows"""
        duplicates = df.duplicated()
        duplicate_info = {
            'has_duplicates': duplicates.any(),
            'duplicate_count': int(duplicates.sum()),
            'percentage': float(duplicates.sum() / len(df) * 100)
        }
        
        return duplicate_info
    
    def check_outliers(self, df: pd.DataFrame, iqr_multiplier: float = 1.5) -> Dict[str, Any]:
        """
        Check for statistical outliers using IQR method
        
        Args:
            df: Input DataFrame
            iqr_multiplier: Multiplier for IQR to determine outlier bounds (default: 1.5)
        """
        outlier_info = {
            'columns_with_outliers': [],
            'details': {}
        }
        
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_columns:
            # IQR method
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - iqr_multiplier * IQR
            upper_bound = Q3 + iqr_multiplier * IQR
            
            outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)][col]
            
            if len(outliers) > 0:
                outlier_info['columns_with_outliers'].append(col)
                outlier_info['details'][col] = {
                    'count': int(len(outliers)),
                    'percentage': float(len(outliers) / len(df) * 100),
                    'lower_bound': float(lower_bound),
                    'upper_bound': float(upper_bound),
                    'min_outlier': float(outliers.min()),
                    'max_outlier': float(outliers.max())
                }
        
        return outlier_info
    
    def check_data_types(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Validate data types and check for logical constraints
        """
        type_info = {
            'issues': [],
            'column_checks': {}
        }
        
        for col in df.columns:
            col_checks = {
                'dtype': str(df[col].dtype),
                'issues': []
            }
            
            # Check for negative values in age-like columns
            if 'age' in col.lower():
                if pd.api.types.is_numeric_dtype(df[col]):
                    negative_ages = df[df[col] < 0]
                    if len(negative_ages) > 0:
                        issue = f"Found {len(negative_ages)} negative values in '{col}' column"
                        col_checks['issues'].append(issue)
                        type_info['issues'].append(issue)
            
            # Check for future dates in date columns
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                future_dates = df[df[col] > pd.Timestamp.now()]
                if len(future_dates) > 0:
                    warning = f"Found {len(future_dates)} future dates in '{col}' column"
                    col_checks['issues'].append(warning)
            
            # Check for negative values in price/amount columns
            if any(keyword in col.lower() for keyword in ['price', 'amount', 'cost', 'salary']):
                if pd.api.types.is_numeric_dtype(df[col]):
                    negative_values = df[df[col] < 0]
                    if len(negative_values) > 0:
                        issue = f"Found {len(negative_values)} negative values in '{col}' column"
                        col_checks['issues'].append(issue)
                        type_info['issues'].append(issue)
            
            type_info['column_checks'][col] = col_checks
        
        return type_info
    
    def generate_validation_report(self, validation_results: Dict[str, Any]) -> str:
        """Generate a human-readable validation report"""
        report_lines = [
            "="*60,
            "DATA VALIDATION REPORT",
            "="*60,
            f"\nDataset Overview:",
            f"  Total Rows: {validation_results['total_rows']}",
            f"  Total Columns: {validation_results['total_columns']}",
            f"\nIssues Found: {len(validation_results['issues'])}",
            f"Warnings: {len(validation_results['warnings'])}",
        ]
        
        if validation_results['warnings']:
            report_lines.append("\nWarnings:")
            for warning in validation_results['warnings']:
                report_lines.append(f"  - {warning}")
        
        if validation_results['issues']:
            report_lines.append("\nIssues:")
            for issue in validation_results['issues']:
                report_lines.append(f"  - {issue}")
        
        report_lines.append("="*60)
        
        return "\n".join(report_lines)
