"""
Visualization engine for generating charts and interactive elements
"""
import logging
from typing import Dict, Any, List, Optional, Tuple
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import json
from datetime import datetime

from ..models.visualization_model import VisualizationModel, VisualizationType, ChartConfig
from ..models.content_model import TableData


logger = logging.getLogger(__name__)


class VisualizationEngine:
    """Generate visualizations from content data"""
    
    def __init__(self):
        self.chart_generators = {
            VisualizationType.LINE_CHART: self._create_line_chart,
            VisualizationType.BAR_CHART: self._create_bar_chart,
            VisualizationType.SCATTER_PLOT: self._create_scatter_plot,
            VisualizationType.PIE_CHART: self._create_pie_chart,
            VisualizationType.HISTOGRAM: self._create_histogram,
            VisualizationType.HEATMAP: self._create_heatmap,
            VisualizationType.BOX_PLOT: self._create_box_plot
        }
        
        self.color_schemes = {
            'default': px.colors.qualitative.Set3,
            'professional': px.colors.qualitative.Plotly,
            'vibrant': px.colors.qualitative.Bold,
            'pastel': px.colors.qualitative.Pastel
        }
    
    def analyze_visualization_opportunities(self, content_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Analyze content for visualization opportunities"""
        try:
            opportunities = []
            
            # Analyze tables for chart potential
            if 'tables' in content_data:
                for table in content_data['tables']:
                    table_opportunities = self._analyze_table_for_charts(table)
                    opportunities.extend(table_opportunities)
            
            # Analyze text for data patterns
            if 'raw_text' in content_data:
                text_opportunities = self._analyze_text_for_patterns(content_data['raw_text'])
                opportunities.extend(text_opportunities)
            
            # Analyze metrics and numbers
            metrics_opportunities = self._analyze_metrics_data(content_data)
            opportunities.extend(metrics_opportunities)
            
            return opportunities
            
        except Exception as e:
            logger.error(f"Failed to analyze visualization opportunities: {e}")
            return []
    
    def generate_visualizations(self, tables: List[TableData], suggestions: List[Dict[str, Any]]) -> List[VisualizationModel]:
        """Generate visualizations based on suggestions"""
        visualizations = []
        
        try:
            for suggestion in suggestions:
                table_data = self._find_table_by_id(tables, suggestion.get('table_id'))
                if table_data:
                    viz = self._create_visualization(table_data, suggestion)
                    if viz:
                        visualizations.append(viz)
            
            return visualizations
            
        except Exception as e:
            logger.error(f"Failed to generate visualizations: {e}")
            return []
    
    def _analyze_table_for_charts(self, table: TableData) -> List[Dict[str, Any]]:
        """Analyze a table for chart opportunities"""
        opportunities = []
        
        try:
            # Convert to DataFrame for analysis
            df = pd.DataFrame(table.rows, columns=table.headers)
            
            # Detect numeric columns
            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
            
            # Detect date/time columns
            date_cols = self._detect_date_columns(df)
            
            # Detect categorical columns
            categorical_cols = self._detect_categorical_columns(df)
            
            # Generate suggestions based on column types
            if date_cols and numeric_cols:
                opportunities.append({
                    'type': 'line_chart',
                    'table_id': table.table_id,
                    'reason': 'Time series data detected',
                    'x_column': date_cols[0],
                    'y_columns': numeric_cols,
                    'priority': 'high',
                    'confidence': 0.9
                })
            
            if categorical_cols and numeric_cols:
                opportunities.append({
                    'type': 'bar_chart',
                    'table_id': table.table_id,
                    'reason': 'Categorical data with numeric values',
                    'x_column': categorical_cols[0],
                    'y_columns': numeric_cols,
                    'priority': 'high',
                    'confidence': 0.8
                })
            
            if len(numeric_cols) >= 2:
                opportunities.append({
                    'type': 'scatter_plot',
                    'table_id': table.table_id,
                    'reason': 'Multiple numeric columns for correlation analysis',
                    'x_column': numeric_cols[0],
                    'y_columns': numeric_cols[1:2],
                    'priority': 'medium',
                    'confidence': 0.7
                })
            
            # Pie chart for categorical with small number of categories
            for cat_col in categorical_cols:
                if df[cat_col].nunique() <= 8:
                    opportunities.append({
                        'type': 'pie_chart',
                        'table_id': table.table_id,
                        'reason': f'Categorical distribution for {cat_col}',
                        'category_column': cat_col,
                        'value_column': numeric_cols[0] if numeric_cols else None,
                        'priority': 'medium',
                        'confidence': 0.6
                    })
            
            return opportunities
            
        except Exception as e:
            logger.error(f"Failed to analyze table for charts: {e}")
            return []
    
    def _analyze_text_for_patterns(self, text: str) -> List[Dict[str, Any]]:
        """Analyze text for data patterns that could be visualized"""
        opportunities = []
        
        # Look for percentage mentions
        import re
        
        percentage_pattern = r'(\d+(?:\.\d+)?)\s*%'
        percentages = re.findall(percentage_pattern, text)
        
        if len(percentages) >= 3:
            opportunities.append({
                'type': 'bar_chart',
                'reason': 'Multiple percentages found in text',
                'data': percentages,
                'priority': 'low',
                'confidence': 0.5
            })
        
        # Look for step-by-step processes
        step_pattern = r'(?:step|phase|stage)\s*\d+'
        steps = re.findall(step_pattern, text, re.IGNORECASE)
        
        if len(steps) >= 3:
            opportunities.append({
                'type': 'process_flow',
                'reason': 'Step-by-step process detected',
                'data': steps,
                'priority': 'medium',
                'confidence': 0.6
            })
        
        return opportunities
    
    def _analyze_metrics_data(self, content_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Analyze for metrics and KPI data"""
        opportunities = []
        
        # Look for metrics in analysis results
        if 'analysis_results' in content_data:
            analysis = content_data['analysis_results']
            
            if 'quality_score' in analysis:
                opportunities.append({
                    'type': 'gauge_chart',
                    'reason': 'Quality score metric detected',
                    'metric': 'quality_score',
                    'value': analysis['quality_score'],
                    'priority': 'medium',
                    'confidence': 0.8
                })
        
        return opportunities
    
    def _create_visualization(self, table_data: TableData, suggestion: Dict[str, Any]) -> Optional[VisualizationModel]:
        """Create a visualization based on suggestion"""
        try:
            viz_type = suggestion['type']
            
            if viz_type in self.chart_generators:
                chart_config, chart_data = self.chart_generators[viz_type](table_data, suggestion)
                
                visualization = VisualizationModel(
                    visualization_id=f"viz_{datetime.now().timestamp()}",
                    content_id=table_data.table_id,
                    visualization_type=VisualizationType(viz_type.upper()),
                    title=self._generate_chart_title(table_data, suggestion),
                    description=suggestion.get('reason', ''),
                    chart_config=chart_config,
                    data=chart_data,
                    created_at=datetime.now(),
                    metadata={'suggestion': suggestion}
                )
                
                return visualization
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to create visualization: {e}")
            return None
    
    def _create_line_chart(self, table_data: TableData, suggestion: Dict[str, Any]) -> Tuple[ChartConfig, Dict[str, Any]]:
        """Create line chart configuration"""
        
        df = pd.DataFrame(table_data.rows, columns=table_data.headers)
        
        x_col = suggestion['x_column']
        y_cols = suggestion['y_columns']
        
        fig = px.line(
            df,
            x=x_col,
            y=y_cols[0] if y_cols else None,
            title=f"{y_cols[0]} over {x_col}" if y_cols else "Line Chart"
        )
        
        fig.update_layout(
            height=400,
            showlegend=True,
            hovermode='x unified'
        )
        
        config = ChartConfig(
            chart_type="line",
            x_axis=x_col,
            y_axis=y_cols[0] if y_cols else "",
            color_scheme="default",
            interactive=True,
            responsive=True
        )
        
        return config, json.loads(fig.to_json())
    
    def _create_bar_chart(self, table_data: TableData, suggestion: Dict[str, Any]) -> Tuple[ChartConfig, Dict[str, Any]]:
        """Create bar chart configuration"""
        
        df = pd.DataFrame(table_data.rows, columns=table_data.headers)
        
        x_col = suggestion['x_column']
        y_cols = suggestion['y_columns']
        
        fig = px.bar(
            df,
            x=x_col,
            y=y_cols[0] if y_cols else None,
            title=f"{y_cols[0]} by {x_col}" if y_cols else "Bar Chart"
        )
        
        fig.update_layout(height=400)
        
        config = ChartConfig(
            chart_type="bar",
            x_axis=x_col,
            y_axis=y_cols[0] if y_cols else "",
            color_scheme="default",
            interactive=True,
            responsive=True
        )
        
        return config, json.loads(fig.to_json())
    
    def _create_scatter_plot(self, table_data: TableData, suggestion: Dict[str, Any]) -> Tuple[ChartConfig, Dict[str, Any]]:
        """Create scatter plot configuration"""
        
        df = pd.DataFrame(table_data.rows, columns=table_data.headers)
        
        x_col = suggestion['x_column']
        y_cols = suggestion['y_columns']
        
        fig = px.scatter(
            df,
            x=x_col,
            y=y_cols[0] if y_cols else None,
            title=f"{y_cols[0]} vs {x_col}" if y_cols else "Scatter Plot"
        )
        
        fig.update_layout(height=400)
        
        config = ChartConfig(
            chart_type="scatter",
            x_axis=x_col,
            y_axis=y_cols[0] if y_cols else "",
            color_scheme="default",
            interactive=True,
            responsive=True
        )
        
        return config, json.loads(fig.to_json())
    
    def _create_pie_chart(self, table_data: TableData, suggestion: Dict[str, Any]) -> Tuple[ChartConfig, Dict[str, Any]]:
        """Create pie chart configuration"""
        
        df = pd.DataFrame(table_data.rows, columns=table_data.headers)
        
        category_col = suggestion['category_column']
        value_col = suggestion.get('value_column')
        
        if value_col:
            fig = px.pie(df, names=category_col, values=value_col)
        else:
            # Count frequencies
            value_counts = df[category_col].value_counts()
            fig = px.pie(values=value_counts.values, names=value_counts.index)
        
        fig.update_layout(height=400)
        
        config = ChartConfig(
            chart_type="pie",
            x_axis=category_col,
            y_axis=value_col or "count",
            color_scheme="default",
            interactive=True,
            responsive=True
        )
        
        return config, json.loads(fig.to_json())
    
    def _create_histogram(self, table_data: TableData, suggestion: Dict[str, Any]) -> Tuple[ChartConfig, Dict[str, Any]]:
        """Create histogram configuration"""
        
        df = pd.DataFrame(table_data.rows, columns=table_data.headers)
        
        x_col = suggestion['x_column']
        
        fig = px.histogram(df, x=x_col, title=f"Distribution of {x_col}")
        fig.update_layout(height=400)
        
        config = ChartConfig(
            chart_type="histogram",
            x_axis=x_col,
            y_axis="count",
            color_scheme="default",
            interactive=True,
            responsive=True
        )
        
        return config, json.loads(fig.to_json())
    
    def _create_heatmap(self, table_data: TableData, suggestion: Dict[str, Any]) -> Tuple[ChartConfig, Dict[str, Any]]:
        """Create heatmap configuration"""
        
        df = pd.DataFrame(table_data.rows, columns=table_data.headers)
        
        # Calculate correlation matrix for numeric columns
        numeric_cols = df.select_dtypes(include=['number']).columns
        corr_matrix = df[numeric_cols].corr()
        
        fig = px.imshow(corr_matrix, title="Correlation Heatmap")
        fig.update_layout(height=400)
        
        config = ChartConfig(
            chart_type="heatmap",
            x_axis="variables",
            y_axis="variables",
            color_scheme="default",
            interactive=True,
            responsive=True
        )
        
        return config, json.loads(fig.to_json())
    
    def _create_box_plot(self, table_data: TableData, suggestion: Dict[str, Any]) -> Tuple[ChartConfig, Dict[str, Any]]:
        """Create box plot configuration"""
        
        df = pd.DataFrame(table_data.rows, columns=table_data.headers)
        
        y_col = suggestion['y_columns'][0] if suggestion['y_columns'] else None
        x_col = suggestion.get('x_column')
        
        if x_col:
            fig = px.box(df, x=x_col, y=y_col, title=f"Box Plot of {y_col} by {x_col}")
        else:
            fig = px.box(df, y=y_col, title=f"Box Plot of {y_col}")
        
        fig.update_layout(height=400)
        
        config = ChartConfig(
            chart_type="box",
            x_axis=x_col or "",
            y_axis=y_col or "",
            color_scheme="default",
            interactive=True,
            responsive=True
        )
        
        return config, json.loads(fig.to_json())
    
    def _detect_date_columns(self, df: pd.DataFrame) -> List[str]:
        """Detect date/time columns in DataFrame"""
        date_cols = []
        
        for col in df.columns:
            # Try to parse as datetime
            try:
                pd.to_datetime(df[col].dropna().head(10))
                date_cols.append(col)
            except:
                # Check for date-like column names
                if any(word in col.lower() for word in ['date', 'time', 'created', 'updated', 'timestamp']):
                    date_cols.append(col)
        
        return date_cols
    
    def _detect_categorical_columns(self, df: pd.DataFrame) -> List[str]:
        """Detect categorical columns in DataFrame"""
        categorical_cols = []
        
        for col in df.columns:
            if df[col].dtype == 'object' or df[col].nunique() / len(df) < 0.1:
                categorical_cols.append(col)
        
        return categorical_cols
    
    def _find_table_by_id(self, tables: List[TableData], table_id: str) -> Optional[TableData]:
        """Find table by ID"""
        for table in tables:
            if table.table_id == table_id:
                return table
        return None
    
    def _generate_chart_title(self, table_data: TableData, suggestion: Dict[str, Any]) -> str:
        """Generate appropriate chart title"""
        chart_type = suggestion['type'].replace('_', ' ').title()
        reason = suggestion.get('reason', '')
        
        if 'x_column' in suggestion and 'y_columns' in suggestion and suggestion['y_columns']:
            return f"{chart_type}: {suggestion['y_columns'][0]} vs {suggestion['x_column']}"
        elif reason:
            return f"{chart_type}: {reason}"
        else:
            return f"{chart_type} from {table_data.table_id}"
