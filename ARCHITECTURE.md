# AutoAnalyst-Core Architecture

## 🏗️ System Architecture

AutoAnalyst-Core is designed as a modular, end-to-end data analytics platform with clear separation of concerns and extensibility.

## 📐 Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit Web Interface                  │
│                         (app.py)                            │
└─────────────────────────────────────────────────────────────┘
                              │
                              ├─────────────────┐
                              ▼                 ▼
┌──────────────────────────────────┐  ┌────────────────────┐
│      Core Processing Modules      │  │   Visualization    │
│                                   │  │      Engine        │
│  ┌────────────────────────────┐  │  │                    │
│  │   Data Ingestion           │  │  │  • Plotly Charts   │
│  │   - Format Detection       │  │  │  • Dashboards      │
│  │   - Schema Analysis        │  │  │  • Interactive     │
│  └────────────────────────────┘  │  │    Plots           │
│                                   │  └────────────────────┘
│  ┌────────────────────────────┐  │
│  │   Data Validation          │  │  ┌────────────────────┐
│  │   - Missing Values         │  │  │  NL Query Engine   │
│  │   - Duplicates             │  │  │                    │
│  │   - Outliers               │  │  │  • OpenAI API      │
│  │   - Type Checking          │  │  │  • Code Generation │
│  └────────────────────────────┘  │  │  • Safe Execution  │
│                                   │  └────────────────────┘
│  ┌────────────────────────────┐  │
│  │   Data Cleaning            │  │
│  │   - Imputation             │  │
│  │   - Deduplication          │  │
│  │   - Normalization          │  │
│  └────────────────────────────┘  │
│                                   │
│  ┌────────────────────────────┐  │
│  │   Feature Engineering      │  │
│  │   - Date Extraction        │  │
│  │   - Binning                │  │
│  │   - Interactions           │  │
│  └────────────────────────────┘  │
└──────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────┐
│           Data Storage              │
│   • CSV, Excel, JSON Support        │
│   • In-Memory Processing            │
│   • Export Capabilities             │
└─────────────────────────────────────┘
```

## 🔧 Component Details

### 1. Data Ingestion Module (`data_ingestion.py`)

**Purpose**: Load and analyze data from multiple sources

**Key Features**:
- Automatic format detection (CSV, Excel, JSON, SQL)
- Schema inference and analysis
- Metadata extraction

**Design Patterns**:
- Factory pattern for format-specific readers
- Strategy pattern for different data sources

**Dependencies**: `pandas`, `openpyxl`, `sqlalchemy`

### 2. Data Validation Module (`data_validation.py`)

**Purpose**: Ensure data quality and integrity

**Key Features**:
- Missing value detection
- Duplicate identification
- Statistical outlier detection (IQR method)
- Logical constraint validation

**Design Patterns**:
- Validator pattern for different validation rules
- Report generator for human-readable output

**Dependencies**: `pandas`, `numpy`

### 3. Data Cleaning Module (`data_cleaning.py`)

**Purpose**: Automatically clean and prepare data

**Key Features**:
- Intelligent missing value imputation
- Duplicate removal
- Text normalization
- Data type correction

**Design Patterns**:
- Pipeline pattern for sequential operations
- Strategy pattern for different imputation methods

**Dependencies**: `pandas`, `numpy`, `re`

### 4. Feature Engineering Module (`feature_engineering.py`)

**Purpose**: Generate new features from existing data

**Key Features**:
- Date component extraction
- Categorical binning
- Interaction features
- Automatic feature discovery

**Design Patterns**:
- Builder pattern for feature construction
- Template method for feature generation

**Dependencies**: `pandas`, `numpy`

### 5. Visualization Module (`visualization.py`)

**Purpose**: Create interactive visualizations

**Key Features**:
- Multiple chart types (scatter, heatmap, time-series, box)
- Auto-generated dashboards
- Interactive Plotly charts

**Design Patterns**:
- Factory pattern for different chart types
- Adapter pattern for data transformation

**Dependencies**: `plotly`, `pandas`, `numpy`

### 6. Natural Language Query Engine (`nl_query_engine.py`)

**Purpose**: Enable natural language data queries

**Key Features**:
- Text-to-code translation using LLMs
- Safe code execution
- Query history
- Auto-suggestions

**Design Patterns**:
- Interpreter pattern for query processing
- Sandbox pattern for safe execution
- Strategy pattern for different query types

**Dependencies**: `openai`, `pandas`, `dotenv`

### 7. Main Application (`app.py`)

**Purpose**: Unified web interface

**Key Features**:
- Multi-page navigation
- Session state management
- File upload/download
- Real-time processing

**Design Patterns**:
- MVC pattern (Streamlit provides View + Controller)
- Observer pattern for reactive updates
- Facade pattern for module integration

**Dependencies**: `streamlit`, all core modules

## 🔄 Data Flow

### Typical Workflow

1. **Upload**: User uploads data file
   ```
   File → DataIngestion → DataFrame + Metadata
   ```

2. **Validate**: Check data quality
   ```
   DataFrame → DataValidator → ValidationResults
   ```

3. **Clean**: Apply automated cleaning
   ```
   DataFrame → DataCleaner → CleanedDataFrame
   ```

4. **Engineer**: Generate features
   ```
   CleanedDataFrame → FeatureEngineer → FeaturedDataFrame
   ```

5. **Analyze**: Two paths:
   
   a. **Visualization**:
   ```
   FeaturedDataFrame → DataVisualizer → PlotlyFigures
   ```
   
   b. **NL Query**:
   ```
   Question → NLQueryEngine → Code → Result + Visualization
   ```

6. **Export**: Download processed data
   ```
   FeaturedDataFrame → CSV/JSON/Excel
   ```

## 🗃️ State Management

The application uses Streamlit's session state to maintain:

- `df_original`: Original uploaded DataFrame
- `df_cleaned`: Cleaned DataFrame
- `metadata`: File metadata
- `validation_results`: Validation outputs
- `cleaning_log`: List of cleaning operations
- `feature_log`: List of generated features

## 🔐 Security Considerations

### Data Privacy
- All processing happens locally
- No data is stored on servers (except temporary Streamlit cache)
- Data files are not committed to git

### API Security
- OpenAI API key stored in `.env` file (not in code)
- `.env` file excluded from git via `.gitignore`
- API key validation before use

### Code Execution Safety
- NL query code executes in restricted environment
- Limited builtins access
- No file system operations from generated code
- Timeout mechanisms (handled by pandas)

## 📊 Performance Considerations

### Memory Management
- Uses pandas for efficient in-memory processing
- Streams large files when possible
- Caching for repeated operations (Streamlit `@st.cache_data`)

### Scalability
- Designed for datasets up to millions of rows
- Optimized pandas operations
- Vectorized computations
- Minimal data copying

### Optimization Opportunities
1. Add support for Polars for faster processing
2. Implement chunked processing for very large files
3. Add database backend for persistent storage
4. Implement distributed processing (Dask/Ray)

## 🧩 Extensibility

### Adding New Data Sources

1. Extend `DataIngestion` class
2. Add format detection logic
3. Implement reader method
4. Update `ingest_data()` dispatcher

### Adding New Validations

1. Add method to `DataValidator`
2. Update `validate_data()` to call it
3. Add results to validation report

### Adding New Visualizations

1. Add method to `DataVisualizer`
2. Add UI controls in `app.py`
3. Handle edge cases (empty data, wrong types)

### Adding New Features

1. Add feature generation logic to `FeatureEngineer`
2. Update `auto_engineer_features()`
3. Add to feature log

## 🔮 Future Enhancements

### Planned Features
- [ ] Real-time data streaming support
- [ ] Advanced ML model integration
- [ ] Collaborative features (sharing analyses)
- [ ] Report generation (PDF/HTML)
- [ ] Data versioning and lineage
- [ ] Custom transformation pipelines
- [ ] API for programmatic access

### Integration Opportunities
- [ ] Cloud storage (S3, Azure Blob, GCS)
- [ ] Database connectors (PostgreSQL, MySQL, MongoDB)
- [ ] BI tool integrations (Tableau, Power BI)
- [ ] CI/CD pipeline integration
- [ ] Containerization (Docker)

## 📚 Technology Stack

| Category | Technology | Purpose |
|----------|-----------|---------|
| Frontend | Streamlit | Web UI framework |
| Data Processing | Pandas | DataFrame operations |
| Visualization | Plotly | Interactive charts |
| NLP/LLM | OpenAI API | Natural language queries |
| Data Formats | openpyxl | Excel support |
| Database | SQLAlchemy | SQL database support |
| ML/Stats | scikit-learn | Statistical operations |
| Configuration | python-dotenv | Environment variables |

## 🏆 Design Principles

1. **Modularity**: Each module has a single, well-defined responsibility
2. **Extensibility**: Easy to add new features without modifying core logic
3. **Usability**: Simple, intuitive interface for non-technical users
4. **Reliability**: Comprehensive error handling and validation
5. **Performance**: Efficient data processing for large datasets
6. **Security**: Safe execution and data privacy
7. **Documentation**: Clear code comments and user guides

## 📞 Support

For architecture questions or contribution guidelines, see:
- [CONTRIBUTING.md](CONTRIBUTING.md) - How to contribute
- [QUICKSTART.md](QUICKSTART.md) - Getting started guide
- [README.md](README.md) - Project overview

---

**Last Updated**: January 2026
**Version**: 1.0.0
