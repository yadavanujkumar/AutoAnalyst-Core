"""
Data Cleaning Module
Implements auto-cleaning pipelines for data preprocessing
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
import re
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataCleaner:
    """Handles automated data cleaning operations"""
    
    def __init__(self):
        self.cleaning_log = []
        
    def auto_clean(self, df: pd.DataFrame, config: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
        """
        Automatically clean the DataFrame
        
        Args:
            df: Input DataFrame
            config: Optional configuration for cleaning operations
            
        Returns:
            Cleaned DataFrame
        """
        df_clean = df.copy()
        
        if config is None:
            config = {
                'remove_duplicates': True,
                'handle_missing': True,
                'normalize_text': True,
                'fix_dtypes': True
            }
        
        # Remove duplicates
        if config.get('remove_duplicates', True):
            df_clean = self.remove_duplicates(df_clean)
        
        # Handle missing values
        if config.get('handle_missing', True):
            df_clean = self.handle_missing_values(df_clean)
        
        # Normalize text columns
        if config.get('normalize_text', True):
            df_clean = self.normalize_text(df_clean)
        
        # Fix data types
        if config.get('fix_dtypes', True):
            df_clean = self.fix_data_types(df_clean)
        
        logger.info(f"Cleaning complete. Applied {len(self.cleaning_log)} operations")
        return df_clean
    
    def remove_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        """Remove duplicate rows"""
        initial_rows = len(df)
        df_clean = df.drop_duplicates()
        removed = initial_rows - len(df_clean)
        
        if removed > 0:
            self.cleaning_log.append(f"Removed {removed} duplicate rows")
            logger.info(f"Removed {removed} duplicate rows")
        
        return df_clean
    
    def handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Intelligently handle missing values based on column type
        """
        df_clean = df.copy()
        
        for col in df_clean.columns:
            if df_clean[col].isnull().any():
                # Numeric columns: impute with median
                if pd.api.types.is_numeric_dtype(df_clean[col]):
                    median_val = df_clean[col].median()
                    df_clean[col].fillna(median_val, inplace=True)
                    self.cleaning_log.append(f"Imputed missing values in '{col}' with median: {median_val}")
                
                # Categorical columns: impute with mode
                elif pd.api.types.is_object_dtype(df_clean[col]) or pd.api.types.is_categorical_dtype(df_clean[col]):
                    mode_val = df_clean[col].mode()
                    if len(mode_val) > 0:
                        df_clean[col].fillna(mode_val[0], inplace=True)
                        self.cleaning_log.append(f"Imputed missing values in '{col}' with mode: {mode_val[0]}")
                    else:
                        df_clean[col].fillna('Unknown', inplace=True)
                        self.cleaning_log.append(f"Imputed missing values in '{col}' with 'Unknown'")
                
                # DateTime columns: forward fill
                elif pd.api.types.is_datetime64_any_dtype(df_clean[col]):
                    df_clean[col].fillna(method='ffill', inplace=True)
                    self.cleaning_log.append(f"Forward filled missing values in '{col}'")
        
        return df_clean
    
    def normalize_text(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Normalize text columns (trim whitespace, standardize case)
        """
        df_clean = df.copy()
        
        for col in df_clean.columns:
            if pd.api.types.is_object_dtype(df_clean[col]):
                # Remove leading/trailing whitespace
                df_clean[col] = df_clean[col].apply(
                    lambda x: x.strip() if isinstance(x, str) else x
                )
                
                # Remove extra spaces
                df_clean[col] = df_clean[col].apply(
                    lambda x: re.sub(r'\s+', ' ', x) if isinstance(x, str) else x
                )
                
                self.cleaning_log.append(f"Normalized text in '{col}'")
        
        return df_clean
    
    def fix_data_types(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Attempt to convert columns to appropriate data types
        """
        df_clean = df.copy()
        
        for col in df_clean.columns:
            # Try to convert to datetime if column name suggests it's a date
            if any(keyword in col.lower() for keyword in ['date', 'time', 'datetime', 'timestamp']):
                try:
                    df_clean[col] = pd.to_datetime(df_clean[col], errors='coerce')
                    self.cleaning_log.append(f"Converted '{col}' to datetime")
                except Exception as e:
                    logger.warning(f"Could not convert '{col}' to datetime: {str(e)}")
            
            # Try to convert to numeric if values look numeric
            elif pd.api.types.is_object_dtype(df_clean[col]):
                try:
                    # Check if the column contains mostly numeric values
                    sample = df_clean[col].dropna().head(100)
                    if sample.str.match(r'^-?\d+\.?\d*$').sum() / len(sample) > 0.8:
                        df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
                        self.cleaning_log.append(f"Converted '{col}' to numeric")
                except Exception as e:
                    logger.warning(f"Could not convert '{col}' to numeric: {str(e)}")
        
        return df_clean
    
    def get_cleaning_log(self) -> List[str]:
        """Return the log of cleaning operations performed"""
        return self.cleaning_log
