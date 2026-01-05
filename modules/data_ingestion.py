"""
Data Ingestion Module
Auto-detects file formats and loads data from multiple sources (CSV, Excel, JSON, SQL)
"""

import pandas as pd
import json
import os
from typing import Optional, Tuple, Dict, Any
from sqlalchemy import create_engine
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataIngestion:
    """Handles automated data ingestion from multiple file formats"""
    
    def __init__(self):
        self.supported_formats = ['.csv', '.xlsx', '.xls', '.json', '.db', '.sqlite']
        
    def auto_detect_format(self, file_path: str) -> str:
        """
        Auto-detect file format based on extension
        
        Args:
            file_path: Path to the data file
            
        Returns:
            str: Detected file format
        """
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()
        
        if ext not in self.supported_formats:
            raise ValueError(f"Unsupported file format: {ext}. Supported formats: {self.supported_formats}")
        
        logger.info(f"Detected file format: {ext}")
        return ext
    
    def ingest_data(self, file_path: str, **kwargs) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Ingest data from file and return DataFrame with metadata
        
        Args:
            file_path: Path to the data file
            **kwargs: Additional parameters for specific readers
            
        Returns:
            Tuple of (DataFrame, metadata dictionary)
        """
        file_format = self.auto_detect_format(file_path)
        metadata = {
            'file_path': file_path,
            'format': file_format,
            'success': False
        }
        
        try:
            if file_format == '.csv':
                df = pd.read_csv(file_path, **kwargs)
            elif file_format in ['.xlsx', '.xls']:
                df = pd.read_excel(file_path, **kwargs)
            elif file_format == '.json':
                df = pd.read_json(file_path, **kwargs)
            elif file_format in ['.db', '.sqlite']:
                # For SQL databases, need table name
                table_name = kwargs.get('table_name')
                if not table_name:
                    raise ValueError("table_name parameter required for SQL database files")
                engine = create_engine(f'sqlite:///{file_path}')
                df = pd.read_sql_table(table_name, engine)
            else:
                raise ValueError(f"Unsupported format: {file_format}")
            
            metadata['success'] = True
            metadata['rows'] = len(df)
            metadata['columns'] = len(df.columns)
            metadata['column_names'] = df.columns.tolist()
            metadata['dtypes'] = df.dtypes.to_dict()
            
            logger.info(f"Successfully ingested {len(df)} rows and {len(df.columns)} columns")
            return df, metadata
            
        except Exception as e:
            logger.error(f"Error ingesting data: {str(e)}")
            metadata['error'] = str(e)
            raise
    
    def detect_schema(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Detect and analyze schema of the DataFrame
        
        Args:
            df: Input DataFrame
            
        Returns:
            Dictionary containing schema information
        """
        schema = {
            'columns': {},
            'summary': {
                'total_columns': len(df.columns),
                'total_rows': len(df),
                'memory_usage': df.memory_usage(deep=True).sum()
            }
        }
        
        for col in df.columns:
            col_info = {
                'dtype': str(df[col].dtype),
                'null_count': int(df[col].isnull().sum()),
                'null_percentage': float(df[col].isnull().sum() / len(df) * 100),
                'unique_count': int(df[col].nunique()),
                'sample_values': df[col].dropna().head(3).tolist()
            }
            
            # Add statistics for numeric columns
            if pd.api.types.is_numeric_dtype(df[col]):
                col_info['statistics'] = {
                    'mean': float(df[col].mean()) if not df[col].isna().all() else None,
                    'median': float(df[col].median()) if not df[col].isna().all() else None,
                    'min': float(df[col].min()) if not df[col].isna().all() else None,
                    'max': float(df[col].max()) if not df[col].isna().all() else None,
                    'std': float(df[col].std()) if not df[col].isna().all() else None
                }
            
            schema['columns'][col] = col_info
        
        return schema
