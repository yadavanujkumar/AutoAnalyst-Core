# Contributing to AutoAnalyst-Core

Thank you for your interest in contributing to AutoAnalyst-Core! We welcome contributions from the community.

## 🌟 Ways to Contribute

- **Report bugs** and issues
- **Suggest new features** or enhancements
- **Improve documentation**
- **Submit code improvements**
- **Add new data sources** or visualization types
- **Enhance the NL query engine**

## 🚀 Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/AutoAnalyst-Core.git
   cd AutoAnalyst-Core
   ```
3. **Create a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 🔧 Development Workflow

1. **Create a new branch** for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**:
   - Follow the existing code style
   - Add docstrings to functions
   - Include type hints where appropriate
   - Test your changes locally

3. **Test your changes**:
   ```bash
   # Run the application
   streamlit run app.py
   
   # Test individual modules
   python3 -c "from modules.data_ingestion import DataIngestion; ..."
   ```

4. **Commit your changes**:
   ```bash
   git add .
   git commit -m "Add feature: your feature description"
   ```

5. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request** on GitHub

## 📝 Code Style Guidelines

### Python Code
- Follow [PEP 8](https://pep8.org/) style guide
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Include type hints for function parameters and return values

### Example:
```python
def process_data(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Process the specified column in the DataFrame.
    
    Args:
        df: Input DataFrame
        column: Name of the column to process
        
    Returns:
        Processed DataFrame
    """
    # Implementation
    pass
```

### Documentation
- Use clear, concise language
- Include examples where appropriate
- Update README.md if adding new features

## 🏗️ Project Structure

```
AutoAnalyst-Core/
├── app.py                      # Main Streamlit application
├── modules/                    # Core modules
│   ├── data_ingestion.py      # Data loading
│   ├── data_validation.py     # Data validation
│   ├── data_cleaning.py       # Data cleaning
│   ├── feature_engineering.py # Feature engineering
│   ├── visualization.py       # Visualizations
│   └── nl_query_engine.py     # NL queries
├── utils/                      # Utility scripts
└── data/                       # Sample data
```

## 🎯 Areas for Contribution

### High Priority
- [ ] Add support for more data sources (PostgreSQL, MongoDB, APIs)
- [ ] Implement data export to multiple formats
- [ ] Add more advanced statistical tests
- [ ] Enhance NL query capabilities
- [ ] Add unit tests for all modules

### Medium Priority
- [ ] Add data anonymization features
- [ ] Implement custom feature engineering rules
- [ ] Add report generation (PDF/HTML)
- [ ] Create more visualization types
- [ ] Add data lineage tracking

### Low Priority
- [ ] Add theme customization
- [ ] Implement data versioning
- [ ] Add collaboration features
- [ ] Create CLI interface

## 🐛 Reporting Bugs

When reporting bugs, please include:

1. **Description**: Clear description of the bug
2. **Steps to reproduce**: Step-by-step instructions
3. **Expected behavior**: What should happen
4. **Actual behavior**: What actually happens
5. **Environment**:
   - OS (Windows/Mac/Linux)
   - Python version
   - Package versions
6. **Screenshots**: If applicable
7. **Error messages**: Full error traceback

## 💡 Suggesting Features

When suggesting features, please include:

1. **Use case**: Why this feature is needed
2. **Description**: Clear description of the feature
3. **Mockups**: Visual examples if applicable
4. **Alternatives**: Other solutions you've considered

## ✅ Pull Request Guidelines

- **Keep PRs focused**: One feature or bug fix per PR
- **Write clear descriptions**: Explain what and why
- **Update documentation**: If adding/changing features
- **Test thoroughly**: Ensure your changes work
- **Follow code style**: Match existing code style
- **Be responsive**: Address review feedback promptly

## 🧪 Testing

Currently, AutoAnalyst-Core uses manual testing. We welcome contributions to add automated tests!

### Manual Testing Checklist
- [ ] Data ingestion works for CSV, Excel, JSON
- [ ] Validation detects issues correctly
- [ ] Cleaning operations work as expected
- [ ] Feature engineering creates valid features
- [ ] Visualizations render correctly
- [ ] NL queries execute successfully (if API key set)

## 📜 License

By contributing to AutoAnalyst-Core, you agree that your contributions will be licensed under the same license as the project.

## 🤝 Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Assume good intentions

## 💬 Questions?

If you have questions about contributing:
- Open an issue with the "question" label
- Check existing issues and discussions

## 🙏 Thank You!

Your contributions help make AutoAnalyst-Core better for everyone!
