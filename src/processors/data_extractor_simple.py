"""
Enhanced Data Extraction and Analysis
Provides advanced data extraction capabilities with pattern analysis and visualization suggestions.
"""
import logging
import re
from typing import Dict, Any, List, Optional
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np

logger = logging.getLogger(__name__)

class DataExtractor:
    """Enhanced data extractor with advanced analysis capabilities."""
    
    def __init__(self):
        self.data_quality_threshold = 0.7
        self.pattern_matchers = self._initialize_pattern_matchers()
    
    def _initialize_pattern_matchers(self) -> Dict[str, Any]:
        """Initialize pattern matching rules for data analysis."""
        return {
            'time_series': [
                r'\b(?:date|time|timestamp|created|updated|modified)\b',
                r'\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\b',
                r'\d{4}[-/]\d{2}[-/]\d{2}',
                r'\d{2}[-/]\d{2}[-/]\d{4}'
            ],
            'performance_metrics': [
                r'\b(?:response|latency|throughput|rps|qps|cpu|memory|disk)\b',
                r'\b(?:ms|seconds|milliseconds|percentage|percent|%|mb|gb|kb)\b'
            ],
            'financial': [
                r'\$\d+',
                r'\b(?:cost|price|revenue|profit|budget|expense)\b',
                r'\b(?:usd|eur|gbp|currency)\b'
            ],
            'categorical': [
                r'\b(?:status|type|category|class|group|department)\b',
                r'\b(?:active|inactive|pending|completed|failed|success)\b'
            ]
        }
    
    async def extract_tables(self, html_content: str) -> List[Dict[str, Any]]:
        """Extract and analyze tables from HTML content."""
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            tables = soup.find_all('table')
            
            extracted_tables = []
            for i, table in enumerate(tables):
                table_data = self._parse_table_to_dict(table, f"table_{i}")
                if table_data and table_data.get('data'):
                    extracted_tables.append(table_data)
            
            logger.info(f"Extracted {len(extracted_tables)} tables from content")
            return extracted_tables
            
        except Exception as e:
            logger.error(f"Error extracting tables: {str(e)}")
            return []
    
    def _parse_table_to_dict(self, table_soup, table_id: str) -> Dict[str, Any]:
        """Parse HTML table to dictionary format."""
        try:
            # Extract headers
            headers = []
            header_row = table_soup.find('tr')
            if header_row:
                for th in header_row.find_all(['th', 'td']):
                    headers.append(th.get_text(strip=True))
            
            # Extract data rows
            rows = []
            for tr in table_soup.find_all('tr')[1:]:  # Skip header row
                row = []
                for td in tr.find_all(['td', 'th']):
                    row.append(td.get_text(strip=True))
                if row:
                    rows.append(row)
            
            # Create data dictionary
            if headers and rows:
                data = {}
                for i, header in enumerate(headers):
                    data[header] = [row[i] if i < len(row) else None for row in rows]
                
                return {
                    'id': table_id,
                    'headers': headers,
                    'data': data,
                    'row_count': len(rows),
                    'column_count': len(headers)
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Error parsing table: {str(e)}")
            return None
    
    async def analyze_data_structure(self, table_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze data structure and quality."""
        try:
            data = table_data.get('data', {})
            if not data:
                return {'data_quality': 'poor', 'analysis': 'No data available'}
            
            df = pd.DataFrame(data)
            
            # Analyze data types and patterns
            column_analysis = {}
            for col in df.columns:
                column_analysis[col] = self._analyze_column(df[col])
            
            # Calculate overall data quality
            quality_score = self._calculate_data_quality(df)
            
            # Detect data patterns
            patterns = self._detect_data_patterns(df)
            
            analysis = {
                'data_quality': 'high' if quality_score > 0.8 else 'medium' if quality_score > 0.6 else 'low',
                'quality_score': quality_score,
                'column_analysis': column_analysis,
                'patterns': patterns,
                'shape': {'rows': len(df), 'columns': len(df.columns)},
                'missing_data_percentage': (df.isnull().sum().sum() / df.size) * 100
            }
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing data structure: {str(e)}")
            return {'data_quality': 'poor', 'error': str(e)}
    
    def _analyze_column(self, column: pd.Series) -> Dict[str, Any]:
        """Analyze individual column characteristics."""
        try:
            # Detect data type
            if pd.api.types.is_numeric_dtype(column):
                data_type = 'numeric'
                stats = {
                    'mean': column.mean(),
                    'median': column.median(),
                    'std': column.std(),
                    'min': column.min(),
                    'max': column.max()
                }
            else:
                data_type = 'categorical'
                stats = {
                    'unique_values': column.nunique(),
                    'most_common': column.value_counts().index[0] if not column.empty else None,
                    'most_common_count': column.value_counts().iloc[0] if not column.empty else 0
                }
            
            return {
                'data_type': data_type,
                'non_null_count': column.count(),
                'null_count': column.isnull().sum(),
                'stats': stats
            }
            
        except Exception as e:
            return {'data_type': 'unknown', 'error': str(e)}
    
    def _calculate_data_quality(self, df: pd.DataFrame) -> float:
        """Calculate overall data quality score."""
        try:
            # Factors: completeness, consistency, validity
            completeness = 1 - (df.isnull().sum().sum() / df.size)
            
            # Simple consistency check (no duplicate rows)
            consistency = 1 - (df.duplicated().sum() / len(df)) if len(df) > 0 else 1
            
            # Overall quality score
            quality_score = (completeness + consistency) / 2
            return min(max(quality_score, 0), 1)
            
        except Exception:
            return 0.5
    
    def _detect_data_patterns(self, df: pd.DataFrame) -> List[str]:
        """Detect common data patterns in the dataset."""
        patterns = []
        
        try:
            # Check for time series data
            for col in df.columns:
                col_lower = col.lower()
                for pattern in self.pattern_matchers['time_series']:
                    if re.search(pattern, col_lower):
                        patterns.append('time_series')
                        break
            
            # Check for performance metrics
            for col in df.columns:
                col_lower = col.lower()
                for pattern in self.pattern_matchers['performance_metrics']:
                    if re.search(pattern, col_lower):
                        patterns.append('performance_metrics')
                        break
            
            # Check for financial data
            for col in df.columns:
                col_lower = col.lower()
                for pattern in self.pattern_matchers['financial']:
                    if re.search(pattern, col_lower):
                        patterns.append('financial')
                        break
            
            return list(set(patterns))  # Remove duplicates
            
        except Exception:
            return []
    
    async def suggest_visualizations(self, table_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Suggest appropriate visualizations for the data."""
        try:
            data = table_data.get('data', {})
            if not data:
                return []
            
            df = pd.DataFrame(data)
            suggestions = []
            
            # Analyze data to suggest appropriate charts
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
            
            # Bar chart suggestions
            if categorical_cols and numeric_cols:
                suggestions.append({
                    'type': 'bar',
                    'title': f'{numeric_cols[0]} by {categorical_cols[0]}',
                    'x_column': categorical_cols[0],
                    'y_column': numeric_cols[0],
                    'description': f'Bar chart showing {numeric_cols[0]} across different {categorical_cols[0]} values'
                })
            
            # Line chart for time series
            if len(numeric_cols) >= 2:
                suggestions.append({
                    'type': 'line',
                    'title': f'{numeric_cols[1]} over {numeric_cols[0]}',
                    'x_column': numeric_cols[0],
                    'y_column': numeric_cols[1],
                    'description': f'Line chart showing trend of {numeric_cols[1]} over {numeric_cols[0]}'
                })
            
            # Scatter plot for correlation
            if len(numeric_cols) >= 2:
                suggestions.append({
                    'type': 'scatter',
                    'title': f'{numeric_cols[0]} vs {numeric_cols[1]}',
                    'x_column': numeric_cols[0],
                    'y_column': numeric_cols[1],
                    'description': f'Scatter plot showing relationship between {numeric_cols[0]} and {numeric_cols[1]}'
                })
            
            # Pie chart for categorical distribution
            if categorical_cols and numeric_cols:
                suggestions.append({
                    'type': 'pie',
                    'title': f'Distribution of {numeric_cols[0]}',
                    'names_column': categorical_cols[0],
                    'values_column': numeric_cols[0],
                    'description': f'Pie chart showing distribution of {numeric_cols[0]} by {categorical_cols[0]}'
                })
            
            return suggestions
            
        except Exception as e:
            logger.error(f"Error suggesting visualizations: {str(e)}")
            return []
