"""
Feature Engineering Module
Automatically generates new features from existing data
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FeatureEngineer:
    """Handles automated feature engineering"""
    
    def __init__(self):
        self.feature_log = []
        
    def auto_engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Automatically generate new features
        
        Args:
            df: Input DataFrame
            
        Returns:
            DataFrame with additional engineered features
        """
        df_featured = df.copy()
        
        # Extract date features
        df_featured = self.extract_date_features(df_featured)
        
        # Create categorical bins for numeric columns
        df_featured = self.create_numeric_bins(df_featured)
        
        # Create interaction features for numeric columns
        df_featured = self.create_interactions(df_featured)
        
        logger.info(f"Feature engineering complete. Created {len(self.feature_log)} new features")
        return df_featured
    
    def extract_date_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Extract features from datetime columns (year, month, day, day of week, etc.)
        """
        df_featured = df.copy()
        
        for col in df_featured.columns:
            if pd.api.types.is_datetime64_any_dtype(df_featured[col]):
                # Extract year
                df_featured[f'{col}_year'] = df_featured[col].dt.year
                self.feature_log.append(f"Extracted year from '{col}'")
                
                # Extract month
                df_featured[f'{col}_month'] = df_featured[col].dt.month
                self.feature_log.append(f"Extracted month from '{col}'")
                
                # Extract day
                df_featured[f'{col}_day'] = df_featured[col].dt.day
                self.feature_log.append(f"Extracted day from '{col}'")
                
                # Extract day of week
                df_featured[f'{col}_dayofweek'] = df_featured[col].dt.dayofweek
                self.feature_log.append(f"Extracted day of week from '{col}'")
                
                # Extract quarter
                df_featured[f'{col}_quarter'] = df_featured[col].dt.quarter
                self.feature_log.append(f"Extracted quarter from '{col}'")
                
                # Extract hour if time information is present
                if df_featured[col].dt.hour.nunique() > 1:
                    df_featured[f'{col}_hour'] = df_featured[col].dt.hour
                    self.feature_log.append(f"Extracted hour from '{col}'")
                
                logger.info(f"Extracted date features from '{col}'")
        
        return df_featured
    
    def create_numeric_bins(self, df: pd.DataFrame, n_bins: int = 5) -> pd.DataFrame:
        """
        Create categorical bins for numeric columns
        """
        df_featured = df.copy()
        
        numeric_columns = df_featured.select_dtypes(include=[np.number]).columns
        
        for col in numeric_columns:
            # Skip if column has too few unique values
            if df_featured[col].nunique() < n_bins:
                continue
            
            try:
                # Create bins using quantiles
                df_featured[f'{col}_bin'] = pd.qcut(
                    df_featured[col], 
                    q=n_bins, 
                    labels=[f'Q{i+1}' for i in range(n_bins)],
                    duplicates='drop'
                )
                self.feature_log.append(f"Created {n_bins} bins for '{col}'")
                logger.info(f"Created categorical bins for '{col}'")
            except Exception as e:
                logger.warning(f"Could not create bins for '{col}': {str(e)}")
        
        return df_featured
    
    def create_interactions(self, df: pd.DataFrame, max_interactions: int = 5) -> pd.DataFrame:
        """
        Create interaction features between numeric columns
        """
        df_featured = df.copy()
        
        numeric_columns = df_featured.select_dtypes(include=[np.number]).columns
        
        # Limit the number of interaction features
        if len(numeric_columns) > 2:
            interaction_count = 0
            
            # Create ratio features for related columns
            for i, col1 in enumerate(numeric_columns):
                if interaction_count >= max_interactions:
                    break
                    
                for col2 in numeric_columns[i+1:]:
                    if interaction_count >= max_interactions:
                        break
                    
                    # Avoid division by zero
                    if (df_featured[col2] != 0).all():
                        try:
                            df_featured[f'{col1}_per_{col2}'] = df_featured[col1] / df_featured[col2]
                            self.feature_log.append(f"Created ratio feature: {col1}/{col2}")
                            interaction_count += 1
                        except Exception as e:
                            logger.warning(f"Could not create ratio for {col1}/{col2}: {str(e)}")
        
        return df_featured
    
    def get_feature_log(self) -> List[str]:
        """Return the log of feature engineering operations performed"""
        return self.feature_log
