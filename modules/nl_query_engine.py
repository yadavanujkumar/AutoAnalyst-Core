"""
Natural Language Query Engine
Integrates LLM for text-to-SQL/Pandas query conversion
"""

import pandas as pd
import os
from typing import Optional, Dict, Any, Tuple
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NLQueryEngine:
    """Handles natural language queries using LLM"""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.query_history = []
        
        # Initialize OpenAI client if API key is available
        if self.api_key and self.api_key.strip() and not self.api_key.startswith('your_'):
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=self.api_key)
                self.llm_available = True
                logger.info("OpenAI client initialized successfully")
            except Exception as e:
                logger.warning(f"Could not initialize OpenAI client: {str(e)}")
                self.llm_available = False
        else:
            logger.warning("OpenAI API key not configured. NL query features will be limited.")
            self.llm_available = False
    
    def get_schema_context(self) -> str:
        """
        Generate a schema description for the LLM
        """
        schema_info = []
        schema_info.append("Dataset Schema:")
        schema_info.append(f"Total rows: {len(self.df)}")
        schema_info.append(f"Total columns: {len(self.df.columns)}")
        schema_info.append("\nColumns:")
        
        for col in self.df.columns:
            dtype = str(self.df[col].dtype)
            sample_values = self.df[col].dropna().head(3).tolist()
            schema_info.append(f"  - {col} ({dtype}): Sample values: {sample_values}")
        
        return "\n".join(schema_info)
    
    def query(self, natural_language_query: str) -> Tuple[Optional[pd.DataFrame], str, Optional[str]]:
        """
        Process a natural language query and return results
        
        Args:
            natural_language_query: User's question in plain English
            
        Returns:
            Tuple of (result_dataframe, explanation, error_message)
        """
        if not self.llm_available:
            return None, "OpenAI API key not configured. Please set OPENAI_API_KEY in .env file.", "API_KEY_MISSING"
        
        try:
            # Create prompt for LLM
            schema_context = self.get_schema_context()
            
            system_prompt = """You are a data analyst assistant. Given a dataset schema and a natural language query,
generate Python pandas code to answer the question. Return ONLY the pandas code, no explanations.
The DataFrame is available as 'df'. Use pandas operations to filter, aggregate, and analyze the data.
Make sure the code is safe and doesn't modify the original DataFrame."""

            user_prompt = f"""{schema_context}

User Question: {natural_language_query}

Generate pandas code to answer this question. Return only the code, starting with 'result = '"""

            # Call OpenAI API
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1,
                max_tokens=500
            )
            
            # Extract generated code
            generated_code = response.choices[0].message.content.strip()
            
            # Clean up the code (remove markdown code blocks if present)
            if generated_code.startswith('```python'):
                generated_code = generated_code[len('```python'):].strip()
            if generated_code.startswith('```'):
                generated_code = generated_code[3:].strip()
            if generated_code.endswith('```'):
                generated_code = generated_code[:-3].strip()
            
            logger.info(f"Generated code: {generated_code}")
            
            # Execute the code safely
            result = self.execute_query_code(generated_code)
            
            # Store in history
            self.query_history.append({
                'query': natural_language_query,
                'code': generated_code,
                'success': result is not None
            })
            
            explanation = f"Executed query: {natural_language_query}\nGenerated code:\n{generated_code}"
            
            return result, explanation, None
            
        except Exception as e:
            error_msg = f"Error processing query: {str(e)}"
            logger.error(error_msg)
            return None, error_msg, str(e)
    
    def execute_query_code(self, code: str) -> Optional[pd.DataFrame]:
        """
        Safely execute generated pandas code in a restricted environment
        """
        try:
            # Validate that code doesn't contain dangerous operations
            dangerous_keywords = ['import', 'exec', 'eval', 'compile', '__', 'open', 'file', 'os', 'sys']
            if any(keyword in code for keyword in dangerous_keywords):
                logger.error("Generated code contains potentially dangerous operations")
                return None
            
            # Create a safe execution environment
            local_vars = {
                'df': self.df.copy(),
                'pd': pd,
                'result': None
            }
            
            # Execute the code with restricted builtins
            exec(code, {"__builtins__": {}}, local_vars)
            
            result = local_vars.get('result')
            
            # Convert result to DataFrame if it's not already
            if result is not None and not isinstance(result, pd.DataFrame):
                if isinstance(result, pd.Series):
                    result = result.to_frame()
                elif isinstance(result, (int, float, str)):
                    result = pd.DataFrame({'result': [result]})
                else:
                    result = pd.DataFrame(result)
            
            return result
            
        except Exception as e:
            logger.error(f"Error executing query code: {str(e)}")
            return None
    
    def get_query_suggestions(self) -> list:
        """
        Generate sample query suggestions based on the dataset
        """
        suggestions = []
        
        numeric_cols = self.df.select_dtypes(include=['number']).columns.tolist()
        categorical_cols = self.df.select_dtypes(include=['object', 'category']).columns.tolist()
        datetime_cols = self.df.select_dtypes(include=['datetime64']).columns.tolist()
        
        if numeric_cols:
            suggestions.append(f"What is the average {numeric_cols[0]}?")
            if len(numeric_cols) > 1:
                suggestions.append(f"Show me the correlation between {numeric_cols[0]} and {numeric_cols[1]}")
        
        if categorical_cols:
            suggestions.append(f"How many unique {categorical_cols[0]} are there?")
            if numeric_cols:
                suggestions.append(f"What is the total {numeric_cols[0]} by {categorical_cols[0]}?")
        
        if datetime_cols and numeric_cols:
            suggestions.append(f"What were the {numeric_cols[0]} trends over time?")
        
        suggestions.append("Show me the top 10 rows")
        suggestions.append("What are the summary statistics?")
        
        return suggestions
    
    def get_query_history(self) -> list:
        """Return the query history"""
        return self.query_history
