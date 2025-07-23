"""
Data Extractor Module
Extracts and analyzes data patterns from Confluence content for visualization opportunities.
"""

import pandas as pd
import numpy as np
import re
from typing import Dict, List, Any, Optional, Tuple
from bs4 import BeautifulSoup, Tag
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class DataAnalyzer:
    """Analyzes data patterns and suggests appropriate visualizations."""
    
    def __init__(self):
        self.date_patterns = [
            r'\d{4}-\d{2}-\d{2}',  # YYYY-MM-DD
            r'\d{2}/\d{2}/\d{4}',  # MM/DD/YYYY
            r'\d{2}-\d{2}-\d{4}',  # MM-DD-YYYY
            r'\d{1,2}/\d{1,2}/\d{4}',  # M/D/YYYY
        ]
    
    def analyze_data_structure(self, data: List[List[Any]]) -> Dict[str, Any]:
        """Analyze the structure and patterns in table data."""
        if not data or len(data) < 2:
            return {'valid': False, 'reason': 'Insufficient data'}
        
        headers = data[0]
        rows = data[1:]
        
        analysis = {
            'valid': True,
            'num_rows': len(rows),
            'num_columns': len(headers),
            'headers': headers,
            'column_types': {},
            'has_time_series': False,
            'has_categories': False,
            'has_numeric_data': False,
            'has_correlations': False,
            'time_columns': [],
            'category_columns': [],
            'numeric_columns': [],
            'correlated_columns': [],
            'data_quality': {},
            'visualization_potential': 'high'
        }
        
        # Analyze each column
        for i, header in enumerate(headers):
            column_data = [row[i] if i < len(row) else None for row in rows]
            column_analysis = self._analyze_column(header, column_data)
            analysis['column_types'][header] = column_analysis
            
            # Categorize columns
            if column_analysis['type'] == 'datetime':
                analysis['has_time_series'] = True
                analysis['time_columns'].append(header)
            elif column_analysis['type'] == 'numeric':
                analysis['has_numeric_data'] = True
                analysis['numeric_columns'].append(header)
            elif column_analysis['type'] == 'categorical':
                analysis['has_categories'] = True
                analysis['category_columns'].append(header)
        
        # Check for correlations between numeric columns
        if len(analysis['numeric_columns']) >= 2:
            analysis['has_correlations'] = True
            analysis['correlated_columns'] = analysis['numeric_columns']
        
        # Assess visualization potential
        analysis['visualization_potential'] = self._assess_visualization_potential(analysis)
        
        return analysis
    
    def _analyze_column(self, header: str, data: List[Any]) -> Dict[str, Any]:
        """Analyze individual column data patterns."""
        non_null_data = [item for item in data if item is not None and str(item).strip()]
        
        if not non_null_data:
            return {'type': 'empty', 'completeness': 0}
        
        completeness = len(non_null_data) / len(data)
        
        # Check for datetime patterns
        if self._is_datetime_column(non_null_data):
            return {
                'type': 'datetime',
                'completeness': completeness,
                'format': self._detect_datetime_format(non_null_data[0])
            }
        
        # Check for numeric patterns
        if self._is_numeric_column(non_null_data):
            numeric_values = [self._extract_numeric(item) for item in non_null_data]
            return {
                'type': 'numeric',
                'completeness': completeness,
                'min': min(numeric_values),
                'max': max(numeric_values),
                'mean': sum(numeric_values) / len(numeric_values),
                'range': max(numeric_values) - min(numeric_values)
            }
        
        # Check for categorical patterns
        unique_values = set(str(item).lower() for item in non_null_data)
        if len(unique_values) <= len(non_null_data) * 0.7:  # 70% uniqueness threshold
            return {
                'type': 'categorical',
                'completeness': completeness,
                'unique_count': len(unique_values),
                'categories': list(unique_values)[:10]  # Top 10 categories
            }
        
        # Default to text
        return {
            'type': 'text',
            'completeness': completeness,
            'avg_length': sum(len(str(item)) for item in non_null_data) / len(non_null_data)
        }
    
    def _is_datetime_column(self, data: List[Any]) -> bool:
        """Check if column contains datetime data."""
        sample_size = min(5, len(data))
        datetime_count = 0
        
        for item in data[:sample_size]:
            item_str = str(item).strip()
            for pattern in self.date_patterns:
                if re.match(pattern, item_str):
                    datetime_count += 1
                    break
        
        return datetime_count >= sample_size * 0.8  # 80% threshold
    
    def _is_numeric_column(self, data: List[Any]) -> bool:
        """Check if column contains numeric data."""
        sample_size = min(10, len(data))
        numeric_count = 0
        
        for item in data[:sample_size]:
            if self._is_numeric(item):
                numeric_count += 1
        
        return numeric_count >= sample_size * 0.8  # 80% threshold
    
    def _is_numeric(self, value: Any) -> bool:
        """Check if a single value is numeric."""
        if value is None:
            return False
        
        # Remove common formatting
        clean_value = str(value).replace(',', '').replace('$', '').replace('%', '').strip()
        
        try:
            float(clean_value)
            return True
        except ValueError:
            return False
    
    def _extract_numeric(self, value: Any) -> float:
        """Extract numeric value from formatted string."""
        clean_value = str(value).replace(',', '').replace('$', '').replace('%', '').strip()
        return float(clean_value)
    
    def _detect_datetime_format(self, sample: Any) -> str:
        """Detect the datetime format used."""
        sample_str = str(sample).strip()
        
        for pattern in self.date_patterns:
            if re.match(pattern, sample_str):
                if '-' in sample_str and len(sample_str.split('-')[0]) == 4:
                    return 'YYYY-MM-DD'
                elif '/' in sample_str:
                    return 'MM/DD/YYYY'
                elif '-' in sample_str:
                    return 'MM-DD-YYYY'
        
        return 'unknown'
    
    def _assess_visualization_potential(self, analysis: Dict[str, Any]) -> str:
        """Assess the visualization potential of the data."""
        score = 0
        
        # Time series data is highly visualizable
        if analysis['has_time_series'] and analysis['has_numeric_data']:
            score += 3
        
        # Categorical data with numeric values
        if analysis['has_categories'] and analysis['has_numeric_data']:
            score += 2
        
        # Multiple numeric columns for correlations
        if len(analysis['numeric_columns']) >= 2:
            score += 2
        
        # Sufficient data volume
        if analysis['num_rows'] >= 5:
            score += 1
        
        # Data completeness
        avg_completeness = sum(
            col_info.get('completeness', 0) 
            for col_info in analysis['column_types'].values()
        ) / len(analysis['column_types'])
        
        if avg_completeness >= 0.8:
            score += 1
        
        if score >= 5:
            return 'high'
        elif score >= 3:
            return 'medium'
        else:
            return 'low'


class DataExtractor:
    """Main class for extracting and preparing data for visualization."""
    
    def __init__(self):
        self.analyzer = DataAnalyzer()
    
    def extract_table_data(self, table_element: Tag) -> Dict[str, Any]:
        """Extract structured data from HTML table element."""
        try:
            headers = []
            rows = []
            
            # Extract headers
            header_row = table_element.find('tr')
            if header_row:
                headers = [th.get_text().strip() for th in header_row.find_all(['th', 'td'])]
            
            # Extract data rows
            for row in table_element.find_all('tr')[1:]:  # Skip header row
                cells = [td.get_text().strip() for td in row.find_all(['td', 'th'])]
                if cells:  # Only add non-empty rows
                    rows.append(cells)
            
            if not headers or not rows:
                return {'valid': False, 'reason': 'No valid data found'}
            
            # Create structured data
            table_data = [headers] + rows
            
            # Analyze the data
            analysis = self.analyzer.analyze_data_structure(table_data)
            
            return {
                'valid': True,
                'headers': headers,
                'rows': rows,
                'data': table_data,
                'analysis': analysis,
                'visualization_suggestions': self._generate_visualization_suggestions(analysis)
            }
            
        except Exception as e:
            logger.error(f"Error extracting table data: {str(e)}")
            return {'valid': False, 'reason': f'Extraction error: {str(e)}'}
    
    def _generate_visualization_suggestions(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate visualization suggestions based on data analysis."""
        suggestions = []
        
        if not analysis.get('valid', False):
            return suggestions
        
        # Time series visualizations
        if analysis['has_time_series'] and analysis['has_numeric_data']:
            suggestions.append({
                'type': 'line_chart',
                'priority': 'high',
                'reason': 'Time series data detected - ideal for trend analysis',
                'columns': {
                    'x': analysis['time_columns'][0] if analysis['time_columns'] else None,
                    'y': analysis['numeric_columns'][0] if analysis['numeric_columns'] else None
                },
                'description': 'Interactive line chart showing trends over time'
            })
        
        # Categorical visualizations
        if analysis['has_categories'] and analysis['has_numeric_data']:
            suggestions.append({
                'type': 'bar_chart',
                'priority': 'high',
                'reason': 'Categorical data with numeric values - perfect for comparisons',
                'columns': {
                    'x': analysis['category_columns'][0] if analysis['category_columns'] else None,
                    'y': analysis['numeric_columns'][0] if analysis['numeric_columns'] else None
                },
                'description': 'Bar chart comparing values across categories'
            })
        
        # Correlation visualizations
        if len(analysis['numeric_columns']) >= 2:
            suggestions.append({
                'type': 'scatter_plot',
                'priority': 'medium',
                'reason': 'Multiple numeric columns - useful for correlation analysis',
                'columns': {
                    'x': analysis['numeric_columns'][0],
                    'y': analysis['numeric_columns'][1]
                },
                'description': 'Scatter plot showing relationship between variables'
            })
        
        # Distribution visualizations
        if analysis['has_numeric_data']:
            suggestions.append({
                'type': 'histogram',
                'priority': 'medium',
                'reason': 'Numeric data available - show distribution patterns',
                'columns': {
                    'x': analysis['numeric_columns'][0] if analysis['numeric_columns'] else None
                },
                'description': 'Histogram showing data distribution'
            })
        
        # Heatmap for correlation matrix
        if len(analysis['numeric_columns']) >= 3:
            suggestions.append({
                'type': 'heatmap',
                'priority': 'medium',
                'reason': 'Multiple numeric columns - correlation heatmap reveals patterns',
                'columns': {
                    'data': analysis['numeric_columns']
                },
                'description': 'Correlation heatmap showing relationships between all numeric variables'
            })
        
        return suggestions
    
    def extract_list_data(self, list_elements: List[Tag]) -> Dict[str, Any]:
        """Extract data from HTML list elements for potential visualization."""
        try:
            structured_data = []
            
            for list_elem in list_elements:
                items = []
                for li in list_elem.find_all('li'):
                    text = li.get_text().strip()
                    if text:
                        items.append(text)
                
                if items:
                    structured_data.append({
                        'type': 'list',
                        'items': items,
                        'count': len(items)
                    })
            
            if not structured_data:
                return {'valid': False, 'reason': 'No valid list data found'}
            
            return {
                'valid': True,
                'lists': structured_data,
                'visualization_suggestions': self._generate_list_visualizations(structured_data)
            }
            
        except Exception as e:
            logger.error(f"Error extracting list data: {str(e)}")
            return {'valid': False, 'reason': f'Extraction error: {str(e)}'}
    
    def _generate_list_visualizations(self, list_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate visualization suggestions for list data."""
        suggestions = []
        
        for list_item in list_data:
            items = list_item['items']
            
            # Check if items contain numeric patterns (for metrics/KPIs)
            numeric_items = []
            for item in items:
                # Look for pattern: "Label: Number" or "Label - Number"
                match = re.search(r'(.+?)[:|-]\s*(\d+(?:\.\d+)?)', item)
                if match:
                    label, value = match.groups()
                    numeric_items.append({'label': label.strip(), 'value': float(value)})
            
            if len(numeric_items) >= 2:
                suggestions.append({
                    'type': 'bar_chart',
                    'priority': 'medium',
                    'reason': 'List contains numeric values - can be visualized as chart',
                    'data': numeric_items,
                    'description': 'Bar chart from list data showing comparative values'
                })
        
        return suggestions
