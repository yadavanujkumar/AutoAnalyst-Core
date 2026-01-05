"""
AutoAnalyst-Core: Data Analytics & Intelligence Platform
Main Streamlit Application
"""

import streamlit as st
import pandas as pd
import os
import sys
from pathlib import Path

# Add modules to path
sys.path.append(str(Path(__file__).parent))

from modules.data_ingestion import DataIngestion
from modules.data_validation import DataValidator
from modules.data_cleaning import DataCleaner
from modules.feature_engineering import FeatureEngineer
from modules.visualization import DataVisualizer
from modules.nl_query_engine import NLQueryEngine

# Page configuration
st.set_page_config(
    page_title="AutoAnalyst-Core",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stAlert {
        margin-top: 1rem;
    }
    h1 {
        color: #1f77b4;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'df_original' not in st.session_state:
    st.session_state.df_original = None
if 'df_cleaned' not in st.session_state:
    st.session_state.df_cleaned = None
if 'metadata' not in st.session_state:
    st.session_state.metadata = None
if 'validation_results' not in st.session_state:
    st.session_state.validation_results = None
if 'cleaning_log' not in st.session_state:
    st.session_state.cleaning_log = []
if 'feature_log' not in st.session_state:
    st.session_state.feature_log = []


def main():
    """Main application function"""
    
    # Title and description
    st.title("📊 AutoAnalyst-Core")
    st.markdown("### End-to-End Data Analytics & Intelligence Platform")
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("🎯 Navigation")
        page = st.radio(
            "Select Module",
            [
                "📁 Data Ingestion",
                "✅ Data Validation",
                "🧹 Data Cleaning",
                "🔧 Feature Engineering",
                "📈 Visualization",
                "💬 Natural Language Query"
            ]
        )
        
        st.markdown("---")
        st.markdown("### About")
        st.info(
            "AutoAnalyst-Core is an automated data scientist platform that handles "
            "data ingestion, validation, cleaning, feature engineering, visualization, "
            "and natural language queries."
        )
    
    # Route to appropriate page
    if page == "📁 Data Ingestion":
        data_ingestion_page()
    elif page == "✅ Data Validation":
        data_validation_page()
    elif page == "🧹 Data Cleaning":
        data_cleaning_page()
    elif page == "🔧 Feature Engineering":
        feature_engineering_page()
    elif page == "📈 Visualization":
        visualization_page()
    elif page == "💬 Natural Language Query":
        nl_query_page()


def data_ingestion_page():
    """Data ingestion interface"""
    st.header("📁 Data Ingestion & Schema Detection")
    
    st.markdown("""
    Upload your data file in CSV, Excel, or JSON format. The system will automatically:
    - Detect the file format
    - Load the data
    - Analyze the schema
    """)
    
    # File upload
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=['csv', 'xlsx', 'xls', 'json'],
        help="Supported formats: CSV, Excel, JSON"
    )
    
    if uploaded_file is not None:
        try:
            # Save uploaded file temporarily
            temp_path = f"/tmp/{uploaded_file.name}"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Ingest data
            with st.spinner("Loading data..."):
                ingestion = DataIngestion()
                df, metadata = ingestion.ingest_data(temp_path)
                
                st.session_state.df_original = df
                st.session_state.metadata = metadata
            
            st.success(f"✅ Successfully loaded {metadata['rows']} rows and {metadata['columns']} columns!")
            
            # Display metadata
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Rows", metadata['rows'])
            with col2:
                st.metric("Total Columns", metadata['columns'])
            with col3:
                st.metric("Format", metadata['format'])
            
            # Display schema
            st.subheader("📋 Schema Information")
            schema = ingestion.detect_schema(df)
            
            schema_df = pd.DataFrame([
                {
                    'Column': col,
                    'Data Type': info['dtype'],
                    'Null Count': info['null_count'],
                    'Null %': f"{info['null_percentage']:.2f}%",
                    'Unique Values': info['unique_count'],
                    'Sample Values': str(info['sample_values'][:3])
                }
                for col, info in schema['columns'].items()
            ])
            
            st.dataframe(schema_df, use_container_width=True)
            
            # Display data preview
            st.subheader("👀 Data Preview")
            st.dataframe(df.head(10), use_container_width=True)
            
            # Download options
            st.subheader("💾 Download Data")
            col1, col2 = st.columns(2)
            with col1:
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download as CSV",
                    data=csv,
                    file_name="data.csv",
                    mime="text/csv"
                )
            with col2:
                # Note: Excel download requires openpyxl
                st.download_button(
                    label="Download as JSON",
                    data=df.to_json(orient='records'),
                    file_name="data.json",
                    mime="application/json"
                )
            
        except Exception as e:
            st.error(f"Error loading data: {str(e)}")


def data_validation_page():
    """Data validation interface"""
    st.header("✅ Data Validation & Integrity Checks")
    
    if st.session_state.df_original is None:
        st.warning("⚠️ Please upload data in the Data Ingestion page first.")
        return
    
    df = st.session_state.df_original
    
    st.markdown("""
    Perform comprehensive data validation including:
    - Missing value detection
    - Duplicate row identification
    - Statistical outlier detection
    - Data type validation
    """)
    
    if st.button("Run Validation", type="primary"):
        with st.spinner("Validating data..."):
            validator = DataValidator()
            validation_results = validator.validate_data(df)
            st.session_state.validation_results = validation_results
        
        st.success("✅ Validation complete!")
        
        # Display summary metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Rows", validation_results['total_rows'])
        with col2:
            st.metric("Total Columns", validation_results['total_columns'])
        with col3:
            st.metric("Issues", len(validation_results['issues']))
        with col4:
            st.metric("Warnings", len(validation_results['warnings']))
        
        # Display warnings and issues
        if validation_results['warnings']:
            st.subheader("⚠️ Warnings")
            for warning in validation_results['warnings']:
                st.warning(warning)
        
        if validation_results['issues']:
            st.subheader("🚨 Issues")
            for issue in validation_results['issues']:
                st.error(issue)
        
        # Missing values details
        if validation_results['missing_values']['has_missing']:
            st.subheader("📊 Missing Values Analysis")
            missing_data = []
            for col, details in validation_results['missing_values']['details'].items():
                missing_data.append({
                    'Column': col,
                    'Missing Count': details['count'],
                    'Missing %': f"{details['percentage']:.2f}%"
                })
            st.dataframe(pd.DataFrame(missing_data), use_container_width=True)
        
        # Duplicates
        if validation_results['duplicates']['has_duplicates']:
            st.subheader("🔄 Duplicate Rows")
            st.info(f"Found {validation_results['duplicates']['duplicate_count']} duplicate rows "
                   f"({validation_results['duplicates']['percentage']:.2f}% of data)")
        
        # Outliers
        if validation_results['outliers']['columns_with_outliers']:
            st.subheader("📈 Outliers Detection")
            outlier_data = []
            for col, details in validation_results['outliers']['details'].items():
                outlier_data.append({
                    'Column': col,
                    'Outlier Count': details['count'],
                    'Outlier %': f"{details['percentage']:.2f}%",
                    'Lower Bound': f"{details['lower_bound']:.2f}",
                    'Upper Bound': f"{details['upper_bound']:.2f}"
                })
            st.dataframe(pd.DataFrame(outlier_data), use_container_width=True)
        
        # Display validation report
        with st.expander("📄 Full Validation Report"):
            report = validator.generate_validation_report(validation_results)
            st.text(report)


def data_cleaning_page():
    """Data cleaning interface"""
    st.header("🧹 Intelligent Data Cleaning")
    
    if st.session_state.df_original is None:
        st.warning("⚠️ Please upload data in the Data Ingestion page first.")
        return
    
    df = st.session_state.df_original
    
    st.markdown("""
    Automatically clean your data with:
    - Duplicate removal
    - Missing value imputation
    - Text normalization
    - Data type correction
    """)
    
    # Cleaning configuration
    st.subheader("⚙️ Cleaning Configuration")
    col1, col2 = st.columns(2)
    with col1:
        remove_duplicates = st.checkbox("Remove Duplicates", value=True)
        handle_missing = st.checkbox("Handle Missing Values", value=True)
    with col2:
        normalize_text = st.checkbox("Normalize Text", value=True)
        fix_dtypes = st.checkbox("Fix Data Types", value=True)
    
    if st.button("Clean Data", type="primary"):
        with st.spinner("Cleaning data..."):
            cleaner = DataCleaner()
            config = {
                'remove_duplicates': remove_duplicates,
                'handle_missing': handle_missing,
                'normalize_text': normalize_text,
                'fix_dtypes': fix_dtypes
            }
            df_cleaned = cleaner.auto_clean(df, config)
            st.session_state.df_cleaned = df_cleaned
            st.session_state.cleaning_log = cleaner.get_cleaning_log()
        
        st.success("✅ Data cleaning complete!")
        
        # Display metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Original Rows", len(df))
        with col2:
            st.metric("Cleaned Rows", len(df_cleaned))
        with col3:
            rows_removed = len(df) - len(df_cleaned)
            st.metric("Rows Removed", rows_removed)
        
        # Display cleaning log
        st.subheader("📝 Cleaning Operations Log")
        if st.session_state.cleaning_log:
            for log_entry in st.session_state.cleaning_log:
                st.info(log_entry)
        else:
            st.info("No cleaning operations performed.")
        
        # Display cleaned data preview
        st.subheader("👀 Cleaned Data Preview")
        st.dataframe(df_cleaned.head(10), use_container_width=True)
        
        # Download cleaned data
        st.subheader("💾 Download Cleaned Data")
        csv = df_cleaned.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Cleaned CSV",
            data=csv,
            file_name="cleaned_data.csv",
            mime="text/csv"
        )


def feature_engineering_page():
    """Feature engineering interface"""
    st.header("🔧 Automated Feature Engineering")
    
    # Use cleaned data if available, otherwise use original
    if st.session_state.df_cleaned is not None:
        df = st.session_state.df_cleaned
        st.info("Using cleaned data for feature engineering")
    elif st.session_state.df_original is not None:
        df = st.session_state.df_original
        st.info("Using original data for feature engineering")
    else:
        st.warning("⚠️ Please upload data in the Data Ingestion page first.")
        return
    
    st.markdown("""
    Automatically generate new features:
    - Extract date components (year, month, day, etc.)
    - Create categorical bins for numeric data
    - Generate interaction features
    """)
    
    if st.button("Engineer Features", type="primary"):
        with st.spinner("Engineering features..."):
            engineer = FeatureEngineer()
            df_featured = engineer.auto_engineer_features(df)
            st.session_state.df_cleaned = df_featured
            st.session_state.feature_log = engineer.get_feature_log()
        
        st.success("✅ Feature engineering complete!")
        
        # Display metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Original Features", len(df.columns))
        with col2:
            st.metric("New Features", len(df_featured.columns))
        with col3:
            st.metric("Features Added", len(df_featured.columns) - len(df.columns))
        
        # Display feature log
        st.subheader("📝 Feature Engineering Log")
        if st.session_state.feature_log:
            for log_entry in st.session_state.feature_log:
                st.info(log_entry)
        else:
            st.info("No new features created.")
        
        # Display new features
        st.subheader("🆕 New Features")
        new_cols = [col for col in df_featured.columns if col not in df.columns]
        if new_cols:
            st.dataframe(df_featured[new_cols].head(10), use_container_width=True)
        
        # Display full data preview
        st.subheader("👀 Full Data Preview")
        st.dataframe(df_featured.head(10), use_container_width=True)


def visualization_page():
    """Visualization interface"""
    st.header("📈 Interactive Data Visualization")
    
    # Use cleaned data if available, otherwise use original
    if st.session_state.df_cleaned is not None:
        df = st.session_state.df_cleaned
    elif st.session_state.df_original is not None:
        df = st.session_state.df_original
    else:
        st.warning("⚠️ Please upload data in the Data Ingestion page first.")
        return
    
    visualizer = DataVisualizer()
    
    # Tabs for different visualization types
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Distribution", "🔵 Scatter Plot", "🔥 Heatmap", "📈 Time Series", "📦 Box Plot"
    ])
    
    with tab1:
        st.subheader("Distribution Analysis")
        column = st.selectbox("Select Column", df.columns.tolist(), key="dist_col")
        if st.button("Generate Distribution Plot", key="dist_btn"):
            fig = visualizer.create_distribution_plot(df, column)
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("Scatter Plot")
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        if len(numeric_cols) >= 2:
            col1, col2 = st.columns(2)
            with col1:
                x_col = st.selectbox("X-axis", numeric_cols, key="scatter_x")
            with col2:
                y_col = st.selectbox("Y-axis", numeric_cols, index=1 if len(numeric_cols) > 1 else 0, key="scatter_y")
            
            color_col = st.selectbox("Color by (optional)", ['None'] + df.columns.tolist(), key="scatter_color")
            color_col = None if color_col == 'None' else color_col
            
            if st.button("Generate Scatter Plot", key="scatter_btn"):
                fig = visualizer.create_scatter_plot(df, x_col, y_col, color=color_col)
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Need at least 2 numeric columns for scatter plot")
    
    with tab3:
        st.subheader("Correlation Heatmap")
        if st.button("Generate Heatmap", key="heatmap_btn"):
            fig = visualizer.create_correlation_heatmap(df)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("No numeric columns available for correlation heatmap")
    
    with tab4:
        st.subheader("Time Series Analysis")
        datetime_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        
        if datetime_cols and numeric_cols:
            col1, col2 = st.columns(2)
            with col1:
                date_col = st.selectbox("Date Column", datetime_cols, key="ts_date")
            with col2:
                value_col = st.selectbox("Value Column", numeric_cols, key="ts_value")
            
            if st.button("Generate Time Series", key="ts_btn"):
                fig = visualizer.create_time_series_plot(df, date_col, value_col)
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Need at least one datetime column and one numeric column for time series")
    
    with tab5:
        st.subheader("Box Plot")
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        if numeric_cols:
            column = st.selectbox("Select Column", numeric_cols, key="box_col")
            group_by = st.selectbox("Group by (optional)", ['None'] + df.columns.tolist(), key="box_group")
            group_by = None if group_by == 'None' else group_by
            
            if st.button("Generate Box Plot", key="box_btn"):
                fig = visualizer.create_box_plot(df, column, group_by=group_by)
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No numeric columns available for box plot")
    
    # Auto-generated dashboard
    st.markdown("---")
    st.subheader("🎨 Auto-Generated Dashboard")
    if st.button("Generate Complete Dashboard", type="primary"):
        with st.spinner("Generating visualizations..."):
            figures = visualizer.create_summary_dashboard(df)
        
        st.success(f"✅ Generated {len(figures)} visualizations!")
        
        for i, fig in enumerate(figures):
            st.plotly_chart(fig, use_container_width=True)


def nl_query_page():
    """Natural language query interface"""
    st.header("💬 Natural Language Query Engine")
    
    # Use cleaned data if available, otherwise use original
    if st.session_state.df_cleaned is not None:
        df = st.session_state.df_cleaned
    elif st.session_state.df_original is not None:
        df = st.session_state.df_original
    else:
        st.warning("⚠️ Please upload data in the Data Ingestion page first.")
        return
    
    st.markdown("""
    Ask questions about your data in plain English! The AI will:
    - Translate your question to code
    - Execute the query
    - Return results with visualizations
    """)
    
    # Initialize query engine
    query_engine = NLQueryEngine(df)
    
    # Display suggestions
    st.subheader("💡 Suggested Questions")
    suggestions = query_engine.get_query_suggestions()
    
    cols = st.columns(2)
    for i, suggestion in enumerate(suggestions):
        with cols[i % 2]:
            if st.button(suggestion, key=f"suggestion_{i}"):
                st.session_state.current_query = suggestion
    
    # Query input
    st.subheader("❓ Ask a Question")
    
    query = st.text_input(
        "Enter your question:",
        value=st.session_state.get('current_query', ''),
        placeholder="e.g., What is the average sales by region?",
        key="nl_query_input"
    )
    
    if st.button("Submit Query", type="primary") and query:
        with st.spinner("Processing query..."):
            result_df, explanation, error = query_engine.query(query)
        
        if error:
            st.error(f"Error: {explanation}")
            
            if error == "API_KEY_MISSING":
                st.info("""
                🔑 **OpenAI API Key Required**
                
                To use the Natural Language Query feature:
                1. Create a `.env` file in the project root
                2. Add your OpenAI API key: `OPENAI_API_KEY=your_key_here`
                3. Restart the application
                
                Get your API key at: https://platform.openai.com/api-keys
                """)
        else:
            st.success("✅ Query executed successfully!")
            
            # Display explanation
            with st.expander("📝 Execution Details"):
                st.code(explanation)
            
            # Display results
            st.subheader("📊 Query Results")
            if result_df is not None:
                st.dataframe(result_df, use_container_width=True)
                
                # Auto-generate visualization if applicable
                if len(result_df) > 0:
                    st.subheader("📈 Visualization")
                    visualizer = DataVisualizer()
                    
                    # Try to create an appropriate visualization
                    numeric_cols = result_df.select_dtypes(include=['number']).columns.tolist()
                    if len(numeric_cols) > 0:
                        if len(result_df) <= 20:
                            # Bar chart for small results
                            fig = visualizer.create_distribution_plot(result_df, numeric_cols[0])
                            st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("No results returned")
    
    # Query history
    st.markdown("---")
    st.subheader("📜 Query History")
    history = query_engine.get_query_history()
    if history:
        for i, entry in enumerate(reversed(history[-5:])):  # Show last 5 queries
            with st.expander(f"Query {len(history) - i}: {entry['query']}", expanded=False):
                st.code(entry['code'])
                status = "✅ Success" if entry['success'] else "❌ Failed"
                st.markdown(f"**Status:** {status}")
    else:
        st.info("No query history yet")


if __name__ == "__main__":
    main()
