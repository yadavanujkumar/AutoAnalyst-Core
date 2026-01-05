"""
Visualization Module
Generates dynamic, interactive charts using Plotly
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from typing import Optional, List, Dict, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataVisualizer:
    """Handles automated data visualization"""
    
    def __init__(self):
        self.color_palette = px.colors.qualitative.Set2
        
    def create_distribution_plot(self, df: pd.DataFrame, column: str, title: Optional[str] = None) -> go.Figure:
        """
        Create a distribution plot for a numeric column
        """
        if title is None:
            title = f"Distribution of {column}"
        
        if pd.api.types.is_numeric_dtype(df[column]):
            fig = px.histogram(
                df, 
                x=column, 
                title=title,
                nbins=30,
                marginal="box"
            )
            fig.update_layout(
                xaxis_title=column,
                yaxis_title="Count",
                hovermode='x unified'
            )
        else:
            # For categorical data, show value counts
            value_counts = df[column].value_counts().head(20)
            fig = px.bar(
                x=value_counts.index,
                y=value_counts.values,
                title=title,
                labels={'x': column, 'y': 'Count'}
            )
        
        return fig
    
    def create_scatter_plot(self, df: pd.DataFrame, x: str, y: str, 
                          color: Optional[str] = None, size: Optional[str] = None,
                          title: Optional[str] = None) -> go.Figure:
        """
        Create an interactive scatter plot
        """
        if title is None:
            title = f"{y} vs {x}"
        
        fig = px.scatter(
            df,
            x=x,
            y=y,
            color=color,
            size=size,
            title=title,
            hover_data=df.columns.tolist()
        )
        
        fig.update_layout(
            xaxis_title=x,
            yaxis_title=y,
            hovermode='closest'
        )
        
        return fig
    
    def create_correlation_heatmap(self, df: pd.DataFrame, title: Optional[str] = None) -> go.Figure:
        """
        Create a correlation heatmap for numeric columns
        """
        if title is None:
            title = "Correlation Heatmap"
        
        # Select only numeric columns
        numeric_df = df.select_dtypes(include=[np.number])
        
        if numeric_df.empty:
            logger.warning("No numeric columns found for correlation heatmap")
            return None
        
        # Calculate correlation matrix
        corr_matrix = numeric_df.corr()
        
        fig = px.imshow(
            corr_matrix,
            title=title,
            labels=dict(color="Correlation"),
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            color_continuous_scale="RdBu_r",
            aspect="auto"
        )
        
        fig.update_layout(
            xaxis_title="Features",
            yaxis_title="Features"
        )
        
        return fig
    
    def create_time_series_plot(self, df: pd.DataFrame, date_column: str, 
                               value_column: str, title: Optional[str] = None) -> go.Figure:
        """
        Create a time series plot
        """
        if title is None:
            title = f"{value_column} Over Time"
        
        # Sort by date
        df_sorted = df.sort_values(by=date_column)
        
        fig = px.line(
            df_sorted,
            x=date_column,
            y=value_column,
            title=title,
            markers=True
        )
        
        fig.update_layout(
            xaxis_title=date_column,
            yaxis_title=value_column,
            hovermode='x unified'
        )
        
        return fig
    
    def create_box_plot(self, df: pd.DataFrame, column: str, 
                       group_by: Optional[str] = None, title: Optional[str] = None) -> go.Figure:
        """
        Create a box plot to show distribution and outliers
        """
        if title is None:
            title = f"Box Plot of {column}"
            if group_by:
                title += f" by {group_by}"
        
        if group_by:
            fig = px.box(
                df,
                x=group_by,
                y=column,
                title=title,
                color=group_by
            )
        else:
            fig = px.box(
                df,
                y=column,
                title=title
            )
        
        fig.update_layout(
            yaxis_title=column,
            hovermode='closest'
        )
        
        return fig
    
    def create_summary_dashboard(self, df: pd.DataFrame) -> List[go.Figure]:
        """
        Create a comprehensive dashboard with multiple visualizations
        """
        figures = []
        
        # Get numeric and categorical columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        datetime_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
        
        # Create distribution plots for first few numeric columns
        for col in numeric_cols[:3]:
            fig = self.create_distribution_plot(df, col)
            figures.append(fig)
        
        # Create correlation heatmap if we have numeric columns
        if len(numeric_cols) > 1:
            fig = self.create_correlation_heatmap(df)
            if fig:
                figures.append(fig)
        
        # Create bar charts for categorical columns
        for col in categorical_cols[:2]:
            fig = self.create_distribution_plot(df, col)
            figures.append(fig)
        
        # Create scatter plots for numeric column pairs
        if len(numeric_cols) >= 2:
            fig = self.create_scatter_plot(df, numeric_cols[0], numeric_cols[1])
            figures.append(fig)
        
        # Create time series if we have datetime columns
        if datetime_cols and numeric_cols:
            fig = self.create_time_series_plot(df, datetime_cols[0], numeric_cols[0])
            figures.append(fig)
        
        logger.info(f"Created {len(figures)} visualizations for dashboard")
        return figures
    
    def create_grouped_bar_chart(self, df: pd.DataFrame, x: str, y: str, 
                                color: str, title: Optional[str] = None) -> go.Figure:
        """
        Create a grouped bar chart
        """
        if title is None:
            title = f"{y} by {x} and {color}"
        
        fig = px.bar(
            df,
            x=x,
            y=y,
            color=color,
            title=title,
            barmode='group'
        )
        
        fig.update_layout(
            xaxis_title=x,
            yaxis_title=y,
            hovermode='x unified'
        )
        
        return fig
