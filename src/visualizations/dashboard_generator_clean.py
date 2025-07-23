"""
Enhanced Interactive Dashboard Generator
Creates advanced interactive dashboards from table data with sophisticated visualization capabilities.
"""
import logging
from typing import Dict, Any, List, Optional
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import json
from datetime import datetime

logger = logging.getLogger(__name__)

class DashboardGenerator:
    """Enhanced dashboard generator with advanced capabilities."""
    
    def __init__(self):
        self.default_colors = px.colors.qualitative.Set3
        
    async def create_interactive_dashboard(self, table_data: Dict[str, Any], suggestions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create interactive dashboard from table data and suggestions."""
        try:
            # Convert table data to DataFrame
            if 'data' in table_data:
                df = pd.DataFrame(table_data['data'])
            else:
                df = pd.DataFrame(table_data)
            
            if df.empty:
                return {"error": "No data available for dashboard generation"}
            
            # Create charts based on suggestions
            charts = []
            for suggestion in suggestions[:5]:  # Limit to 5 charts
                chart = self._create_chart_from_suggestion(df, suggestion)
                if chart and 'error' not in chart:
                    charts.append(chart)
            
            # Create dashboard structure
            dashboard = {
                'title': table_data.get('title', 'Interactive Dashboard'),
                'charts': charts,
                'layout': 'grid',
                'created_at': datetime.now().isoformat(),
                'data_summary': {
                    'rows': len(df),
                    'columns': len(df.columns),
                    'column_names': list(df.columns)
                }
            }
            
            return dashboard
            
        except Exception as e:
            logger.error(f"Error creating dashboard: {str(e)}")
            return {"error": str(e)}
    
    def _create_chart_from_suggestion(self, df: pd.DataFrame, suggestion: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create chart from visualization suggestion."""
        try:
            chart_type = suggestion.get('type', 'bar')
            
            if chart_type == 'bar':
                return self._create_bar_chart(df, suggestion)
            elif chart_type == 'line':
                return self._create_line_chart(df, suggestion)
            elif chart_type == 'scatter':
                return self._create_scatter_plot(df, suggestion)
            elif chart_type == 'pie':
                return self._create_pie_chart(df, suggestion)
            else:
                return self._create_bar_chart(df, suggestion)
                
        except Exception as e:
            logger.error(f"Error creating chart: {str(e)}")
            return None
    
    def _create_bar_chart(self, df: pd.DataFrame, config: Dict[str, Any]) -> Dict[str, Any]:
        """Create bar chart."""
        try:
            # Use first two columns if not specified
            columns = list(df.columns)
            x_col = config.get('x_column', columns[0] if columns else None)
            y_col = config.get('y_column', columns[1] if len(columns) > 1 else columns[0] if columns else None)
            
            if not x_col or not y_col:
                return {"error": "No suitable columns for bar chart"}
            
            fig = px.bar(df, x=x_col, y=y_col, title=config.get('title', 'Bar Chart'))
            
            return {
                'type': 'bar',
                'config': fig.to_dict(),
                'title': config.get('title', 'Bar Chart'),
                'description': f"Bar chart showing {y_col} by {x_col}"
            }
            
        except Exception as e:
            return {"error": f"Error creating bar chart: {str(e)}"}
    
    def _create_line_chart(self, df: pd.DataFrame, config: Dict[str, Any]) -> Dict[str, Any]:
        """Create line chart."""
        try:
            columns = list(df.columns)
            x_col = config.get('x_column', columns[0] if columns else None)
            y_col = config.get('y_column', columns[1] if len(columns) > 1 else columns[0] if columns else None)
            
            if not x_col or not y_col:
                return {"error": "No suitable columns for line chart"}
            
            fig = px.line(df, x=x_col, y=y_col, title=config.get('title', 'Line Chart'))
            
            return {
                'type': 'line',
                'config': fig.to_dict(),
                'title': config.get('title', 'Line Chart'),
                'description': f"Line chart showing {y_col} over {x_col}"
            }
            
        except Exception as e:
            return {"error": f"Error creating line chart: {str(e)}"}
    
    def _create_scatter_plot(self, df: pd.DataFrame, config: Dict[str, Any]) -> Dict[str, Any]:
        """Create scatter plot."""
        try:
            columns = list(df.columns)
            x_col = config.get('x_column', columns[0] if columns else None)
            y_col = config.get('y_column', columns[1] if len(columns) > 1 else columns[0] if columns else None)
            
            if not x_col or not y_col:
                return {"error": "No suitable columns for scatter plot"}
            
            fig = px.scatter(df, x=x_col, y=y_col, title=config.get('title', 'Scatter Plot'))
            
            return {
                'type': 'scatter',
                'config': fig.to_dict(),
                'title': config.get('title', 'Scatter Plot'),
                'description': f"Scatter plot of {y_col} vs {x_col}"
            }
            
        except Exception as e:
            return {"error": f"Error creating scatter plot: {str(e)}"}
    
    def _create_pie_chart(self, df: pd.DataFrame, config: Dict[str, Any]) -> Dict[str, Any]:
        """Create pie chart."""
        try:
            columns = list(df.columns)
            names_col = config.get('names_column', columns[0] if columns else None)
            values_col = config.get('values_column', columns[1] if len(columns) > 1 else columns[0] if columns else None)
            
            if not names_col or not values_col:
                return {"error": "No suitable columns for pie chart"}
            
            fig = px.pie(df, names=names_col, values=values_col, title=config.get('title', 'Pie Chart'))
            
            return {
                'type': 'pie',
                'config': fig.to_dict(),
                'title': config.get('title', 'Pie Chart'),
                'description': f"Pie chart showing distribution of {values_col}"
            }
            
        except Exception as e:
            return {"error": f"Error creating pie chart: {str(e)}"}
