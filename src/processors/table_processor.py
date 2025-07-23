"""
Enhanced Table Processor Module
Advanced processing of HTML tables with data analysis and visualization suggestions.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from bs4 import BeautifulSoup, Tag
import logging
import re
from datetime import datetime

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
        unique_values = {str(item).lower() for item in non_null_data}
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


class TableProcessor:
    """Enhanced table processor with advanced analysis capabilities."""
    
    def __init__(self):
        self.data_analyzer = DataAnalyzer()
    
    def extract_and_analyze_tables(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """Extract tables and analyze data patterns for visualization opportunities."""
        tables = soup.find_all('table')
        processed_tables = []
        
        for i, table in enumerate(tables):
            try:
                table_data = self._extract_table_data(table)
                
                if table_data.get('valid', False):
                    # Enhanced analysis
                    enhanced_analysis = self._enhance_table_analysis(table_data)
                    table_data.update(enhanced_analysis)
                    
                    # Dashboard potential assessment
                    dashboard_potential = self._assess_dashboard_potential(table_data)
                    table_data['dashboard_potential'] = dashboard_potential
                    
                    processed_tables.append(table_data)
                    
            except Exception as e:
                logger.error(f"Error processing table {i}: {str(e)}")
                continue
        
        return processed_tables
        """Suggest appropriate visualizations for table data"""
        try:
            suggestions = []
            
            if not table.rows or not analysis.get('patterns'):
                return suggestions
            
            df = pd.DataFrame(table.rows, columns=table.headers)
            data_types = analysis.get('data_types', {})
            patterns = analysis.get('patterns', [])
            
            # Time series detection
            if 'time_series' in patterns:
                time_col = self._find_time_column(df, data_types)
                numeric_cols = self._find_numeric_columns(df, data_types)
                
                for numeric_col in numeric_cols:
                    suggestions.append({
                        'type': VisualizationType.LINE_CHART,
                        'title': f'{numeric_col} over Time',
                        'description': f'Time series visualization of {numeric_col}',
                        'config': {
                            'x_axis': time_col,
                            'y_axis': numeric_col,
                            'chart_type': VisualizationType.LINE_CHART
                        },
                        'priority': 'high'
                    })
            
            # Categorical data with numeric values
            if 'categorical_numeric' in patterns:
                categorical_cols = self._find_categorical_columns(df, data_types)
                numeric_cols = self._find_numeric_columns(df, data_types)
                
                for cat_col in categorical_cols:
                    for num_col in numeric_cols:
                        suggestions.append({
                            'type': VisualizationType.BAR_CHART,
                            'title': f'{num_col} by {cat_col}',
                            'description': f'Bar chart showing {num_col} distribution across {cat_col}',
                            'config': {
                                'x_axis': cat_col,
                                'y_axis': num_col,
                                'chart_type': VisualizationType.BAR_CHART
                            },
                            'priority': 'medium'
                        })
            
            # Correlation analysis
            if 'correlations' in patterns:
                numeric_cols = self._find_numeric_columns(df, data_types)
                
                if len(numeric_cols) >= 2:
                    suggestions.append({
                        'type': VisualizationType.SCATTER_PLOT,
                        'title': f'Correlation: {numeric_cols[0]} vs {numeric_cols[1]}',
                        'description': f'Scatter plot showing relationship between {numeric_cols[0]} and {numeric_cols[1]}',
                        'config': {
                            'x_axis': numeric_cols[0],
                            'y_axis': numeric_cols[1],
                            'chart_type': VisualizationType.SCATTER_PLOT
                        },
                        'priority': 'medium'
                    })
            
            # Distribution analysis
            if 'distributions' in patterns:
                numeric_cols = self._find_numeric_columns(df, data_types)
                
                for num_col in numeric_cols:
                    suggestions.append({
                        'type': VisualizationType.HISTOGRAM,
                        'title': f'Distribution of {num_col}',
                        'description': f'Histogram showing distribution of {num_col} values',
                        'config': {
                            'x_axis': num_col,
                            'chart_type': VisualizationType.HISTOGRAM
                        },
                        'priority': 'low'
                    })
            
            # Heatmap for correlation matrix
            numeric_cols = self._find_numeric_columns(df, data_types)
            if len(numeric_cols) >= 3:
                suggestions.append({
                    'type': VisualizationType.HEATMAP,
                    'title': 'Correlation Matrix',
                    'description': 'Heatmap showing correlations between numeric variables',
                    'config': {
                        'chart_type': VisualizationType.HEATMAP,
                        'columns': numeric_cols
                    },
                    'priority': 'low'
                })
            
            logger.info(f"Generated {len(suggestions)} visualization suggestions")
            return suggestions
            
        except Exception as e:
            logger.error(f"Error suggesting visualizations: {e}")
            return []
    
    def assess_dashboard_potential(self, table: TableData) -> Dict[str, Any]:
        """Assess whether table data is suitable for dashboard creation"""
        try:
            if not table.rows or len(table.rows) < 5:
                return {'suitable': False, 'reason': 'Insufficient data'}
            
            df = pd.DataFrame(table.rows, columns=table.headers)
            
            # Check for multiple data types
            data_types = self._analyze_data_types(df)
            has_numeric = any(dt in ['numeric', 'integer', 'float'] for dt in data_types.values())
            has_categorical = any(dt in ['categorical', 'text'] for dt in data_types.values())
            has_temporal = any(dt in ['date', 'datetime'] for dt in data_types.values())
            
            # Calculate suitability score
            score = 0
            features = []
            
            if has_numeric:
                score += 30
                features.append('numeric_data')
            
            if has_categorical:
                score += 20
                features.append('categorical_data')
            
            if has_temporal:
                score += 30
                features.append('temporal_data')
            
            if len(df.columns) >= 3:
                score += 15
                features.append('multiple_dimensions')
            
            if len(df) >= 20:
                score += 5
                features.append('sufficient_records')
            
            suitable = score >= 50
            
            return {
                'suitable': suitable,
                'score': score,
                'features': features,
                'reason': f'Dashboard suitability score: {score}/100'
            }
            
        except Exception as e:
            logger.error(f"Error assessing dashboard potential: {e}")
            return {'suitable': False, 'reason': 'Analysis error'}
    
    def create_dashboard_config(self, table: TableData, suggestions: List[Dict[str, Any]]) -> Optional[DashboardModel]:
        """Create dashboard configuration from table and suggestions"""
        try:
            if not suggestions:
                return None
            
            # Filter high and medium priority suggestions
            priority_suggestions = [s for s in suggestions if s.get('priority') in ['high', 'medium']]
            if not priority_suggestions:
                priority_suggestions = suggestions[:4]  # Take first 4 if no priorities
            
            # Create chart models
            charts = []
            for i, suggestion in enumerate(priority_suggestions[:6]):  # Limit to 6 charts
                chart_config = ChartConfig(
                    chart_type=suggestion['type'],
                    title=suggestion['title'],
                    x_axis=suggestion['config'].get('x_axis'),
                    y_axis=suggestion['config'].get('y_axis'),
                    height=400,
                    width=600
                )
                
                chart = VisualizationModel(
                    content_id=table.metadata.get('source_content_id', ''),
                    viz_type=suggestion['type'],
                    title=suggestion['title'],
                    description=suggestion['description'],
                    config=chart_config,
                    data={'table_id': table.table_id, 'suggestion_index': i}
                )
                charts.append(chart)
            
            # Create filters based on categorical columns
            df = pd.DataFrame(table.rows, columns=table.headers)
            data_types = self._analyze_data_types(df)
            categorical_cols = self._find_categorical_columns(df, data_types)
            
            filters = []
            for cat_col in categorical_cols[:3]:  # Limit to 3 filters
                unique_values = df[cat_col].unique().tolist()
                if len(unique_values) <= 20:  # Only create filter if manageable number of values
                    filters.append({
                        'name': cat_col,
                        'type': 'select',
                        'options': unique_values,
                        'default': 'all'
                    })
            
            # Create dashboard layout
            layout = {
                'type': 'grid',
                'columns': 2 if len(charts) > 1 else 1,
                'rows': (len(charts) + 1) // 2,
                'responsive': True
            }
            
            # Calculate summary statistics
            numeric_cols = self._find_numeric_columns(df, data_types)
            summary_stats = {}
            
            for col in numeric_cols:
                try:
                    col_data = pd.to_numeric(df[col], errors='coerce')
                    summary_stats[col] = {
                        'mean': float(col_data.mean()),
                        'median': float(col_data.median()),
                        'std': float(col_data.std()),
                        'min': float(col_data.min()),
                        'max': float(col_data.max())
                    }
                except:
                    pass
            
            dashboard = DashboardModel(
                content_id=table.metadata.get('source_content_id', ''),
                title=f"Dashboard for {table.table_id}",
                description=f"Interactive dashboard generated from table data with {len(table.rows)} records",
                layout=layout,
                charts=charts,
                filters=filters,
                interactions={'cross_filter': True, 'zoom': True, 'hover': True},
                summary_stats=summary_stats
            )
            
            return dashboard
            
        except Exception as e:
            logger.error(f"Error creating dashboard config: {e}")
            return None
    
    def _analyze_data_types(self, df: pd.DataFrame) -> Dict[str, str]:
        """Analyze data types of DataFrame columns"""
        data_types = {}
        
        for col in df.columns:
            col_data = df[col].dropna()
            
            if len(col_data) == 0:
                data_types[col] = 'empty'
                continue
            
            # Try to convert to numeric
            numeric_data = pd.to_numeric(col_data, errors='coerce')
            if not numeric_data.isna().all():
                if numeric_data.dtype == 'int64':
                    data_types[col] = 'integer'
                else:
                    data_types[col] = 'numeric'
                continue
            
            # Try to convert to datetime
            try:
                pd.to_datetime(col_data)
                data_types[col] = 'datetime'
                continue
            except:
                pass
            
            # Check if categorical (limited unique values)
            unique_ratio = len(col_data.unique()) / len(col_data)
            if unique_ratio < 0.5 and len(col_data.unique()) < 20:
                data_types[col] = 'categorical'
            else:
                data_types[col] = 'text'
        
        return data_types
    
    def _identify_data_patterns(self, df: pd.DataFrame) -> List[str]:
        """Identify patterns in the data"""
        patterns = []
        data_types = self._analyze_data_types(df)
        
        # Time series pattern
        if any(dt in ['datetime', 'date'] for dt in data_types.values()):
            patterns.append('time_series')
        
        # Categorical + Numeric pattern
        has_categorical = any(dt == 'categorical' for dt in data_types.values())
        has_numeric = any(dt in ['numeric', 'integer'] for dt in data_types.values())
        
        if has_categorical and has_numeric:
            patterns.append('categorical_numeric')
        
        # Multiple numeric columns for correlation
        numeric_cols = [col for col, dt in data_types.items() if dt in ['numeric', 'integer']]
        if len(numeric_cols) >= 2:
            patterns.append('correlations')
        
        # Distribution patterns
        if numeric_cols:
            patterns.append('distributions')
        
        return patterns
    
    def _check_data_quality(self, df: pd.DataFrame) -> List[str]:
        """Check for data quality issues"""
        issues = []
        
        # Check for missing values
        missing_pct = (df.isnull().sum() / len(df) * 100)
        for col, pct in missing_pct.items():
            if pct > 10:
                issues.append(f"High missing values in {col}: {pct:.1f}%")
        
        # Check for duplicate rows
        duplicates = df.duplicated().sum()
        if duplicates > 0:
            issues.append(f"Found {duplicates} duplicate rows")
        
        # Check for outliers in numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            outliers = df[(df[col] < Q1 - 1.5 * IQR) | (df[col] > Q3 + 1.5 * IQR)]
            
            if len(outliers) > 0:
                issues.append(f"Found {len(outliers)} outliers in {col}")
        
        return issues
    
    def _assess_visualization_potential(self, df: pd.DataFrame) -> str:
        """Assess the visualization potential of the data"""
        if len(df) < 3:
            return 'low'
        
        data_types = self._analyze_data_types(df)
        
        # High potential: time series, multiple numeric, categorical + numeric
        time_cols = sum(1 for dt in data_types.values() if dt in ['datetime', 'date'])
        numeric_cols = sum(1 for dt in data_types.values() if dt in ['numeric', 'integer'])
        categorical_cols = sum(1 for dt in data_types.values() if dt == 'categorical')
        
        score = 0
        if time_cols > 0:
            score += 30
        if numeric_cols >= 2:
            score += 25
        if categorical_cols > 0 and numeric_cols > 0:
            score += 20
        if len(df) >= 10:
            score += 15
        if len(df.columns) >= 3:
            score += 10
        
        if score >= 60:
            return 'high'
        elif score >= 30:
            return 'medium'
        else:
            return 'low'
    
    def _find_time_column(self, df: pd.DataFrame, data_types: Dict[str, str]) -> Optional[str]:
        """Find the time/date column"""
        for col, dtype in data_types.items():
            if dtype in ['datetime', 'date']:
                return col
        return None
    
    def _find_numeric_columns(self, df: pd.DataFrame, data_types: Dict[str, str]) -> List[str]:
        """Find numeric columns"""
        return [col for col, dtype in data_types.items() if dtype in ['numeric', 'integer']]
    
    def _find_categorical_columns(self, df: pd.DataFrame, data_types: Dict[str, str]) -> List[str]:
        """Find categorical columns"""
        return [col for col, dtype in data_types.items() if dtype == 'categorical']
