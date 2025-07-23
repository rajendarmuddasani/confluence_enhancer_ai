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
                if chart:
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
        
        fig = px.line(
            df, 
            x=x_col, 
            y=y_col,
            title=config.get('title', f'{y_col} Trend Over {x_col}'),
            hover_data=config.get('hover_data', []),
            color_discrete_sequence=self.default_colors
        )
        
        # Enhanced styling
        fig.update_layout(
            hovermode='x unified',
            showlegend=True,
            height=400,
            template='plotly_white',
            title_x=0.5,
            xaxis=dict(showgrid=True, gridwidth=1, gridcolor='LightPink'),
            yaxis=dict(showgrid=True, gridwidth=1, gridcolor='LightPink')
        )
        
        # Add interactivity
        fig.update_traces(
            mode='lines+markers',
            line=dict(width=3),
            marker=dict(size=6, line=dict(width=2, color='DarkSlateGrey'))
        )
        
        return {
            'type': 'line_chart',
            'config': fig.to_json(),
            'description': config.get('description', f"Interactive line chart showing {y_col} trends over {x_col}"),
            'interactivity': ['zoom', 'pan', 'hover', 'legend_toggle', 'selection'],
            'chart_id': config.get('chart_id', f'line_chart_{x_col}_{y_col}')
        }
    
    def _create_bar_chart(self, df: pd.DataFrame, config: Dict[str, Any]) -> Dict[str, Any]:
        """Create enhanced bar chart."""
        columns = config.get('columns', {})
        x_col = columns.get('x')
        y_col = columns.get('y')
        
        if not x_col or not y_col or x_col not in df.columns or y_col not in df.columns:
            return self._create_error_chart("Invalid column configuration for bar chart")
        
        # Handle multiple y columns for grouped bar chart
        y_columns = y_col if isinstance(y_col, list) else [y_col]
        
        if len(y_columns) > 1:
            # Create grouped bar chart
            fig = go.Figure()
            for i, y_column in enumerate(y_columns):
                fig.add_trace(go.Bar(
                    x=df[x_col],
                    y=df[y_column],
                    name=y_column,
                    marker_color=self.default_colors[i % len(self.default_colors)]
                ))
        else:
            fig = px.bar(
                df, 
                x=x_col, 
                y=y_columns[0],
                title=config.get('title', f'{y_columns[0]} by {x_col}'),
                color_discrete_sequence=self.default_colors
            )
        
        fig.update_layout(
            title=config.get('title', f'Comparison of {", ".join(y_columns)} by {x_col}'),
            xaxis_title=x_col,
            yaxis_title=", ".join(y_columns),
            hovermode='x unified',
            height=400,
            template='plotly_white',
            title_x=0.5
        )
        
        return {
            'type': 'bar_chart',
            'config': fig.to_json(),
            'description': config.get('description', f"Interactive bar chart comparing {', '.join(y_columns)} across {x_col}"),
            'interactivity': ['hover', 'click', 'selection', 'zoom'],
            'chart_id': config.get('chart_id', f'bar_chart_{x_col}_{y_columns[0]}')
        }
    
    def _create_scatter_plot(self, df: pd.DataFrame, config: Dict[str, Any]) -> Dict[str, Any]:
        """Create enhanced scatter plot."""
        columns = config.get('columns', {})
        x_col = columns.get('x')
        y_col = columns.get('y')
        color_col = columns.get('color')
        size_col = columns.get('size')
        
        if not x_col or not y_col:
            return self._create_error_chart("Invalid column configuration for scatter plot")
        
        fig = px.scatter(
            df,
            x=x_col,
            y=y_col,
            color=color_col if color_col and color_col in df.columns else None,
            size=size_col if size_col and size_col in df.columns else None,
            title=config.get('title', f'{y_col} vs {x_col} Correlation'),
            hover_data=config.get('hover_data', []),
            color_discrete_sequence=self.default_colors
        )
        
        fig.update_layout(
            hovermode='closest',
            height=400,
            template='plotly_white',
            title_x=0.5
        )
        
        # Add trendline if requested
        if config.get('trendline', False):
            fig.add_trace(go.Scatter(
                x=df[x_col],
                y=df[y_col],
                mode='lines',
                name='Trendline',
                line=dict(dash='dash', color='red')
            ))
        
        return {
            'type': 'scatter_plot',
            'config': fig.to_json(),
            'description': config.get('description', f"Scatter plot showing relationship between {x_col} and {y_col}"),
            'interactivity': ['zoom', 'pan', 'hover', 'selection', 'lasso'],
            'chart_id': config.get('chart_id', f'scatter_{x_col}_{y_col}')
        }


class DashboardGenerator:
    """Enhanced dashboard generator with advanced layout and interactivity."""
    
    def __init__(self):
        self.chart_generator = ChartGenerator()
    
    def create_interactive_dashboard(self, table_data: Dict[str, Any], suggestions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create enhanced interactive dashboard from table data."""
        try:
            # Extract data
            headers = table_data.get('headers', [])
            rows = table_data.get('rows', [])
            
            if not headers or not rows:
                return self._create_error_dashboard("No valid data found")
            
            # Create DataFrame
            df = pd.DataFrame(rows, columns=headers)
            
            # Design dashboard layout
            dashboard_config = self._design_dashboard_layout(df, suggestions)
            
            dashboard = {
                'title': self._generate_dashboard_title(df),
                'layout': dashboard_config['layout'],
                'charts': [],
                'filters': dashboard_config['filters'],
                'interactions': dashboard_config['interactions'],
                'summary': self._generate_summary_stats(df),
                'kpi_cards': self._generate_kpi_cards(df),
                'metadata': {
                    'created_at': datetime.now().isoformat(),
                    'data_rows': len(rows),
                    'data_columns': len(headers),
                    'chart_count': len(suggestions)
                }
            }
            
            # Generate charts
            for i, suggestion in enumerate(suggestions):
                try:
                    # Add chart ID for tracking
                    suggestion['chart_id'] = f'chart_{i+1}'
                    chart = self.chart_generator.create_chart(df, suggestion)
                    
                    if chart and chart.get('type') != 'error':
                        dashboard['charts'].append(chart)
                        
                except Exception as e:
                    logger.error(f"Error creating chart {i+1}: {str(e)}")
                    continue
            
            # Add cross-chart interactions
            dashboard['cross_chart_interactions'] = self._setup_cross_chart_interactions(dashboard['charts'])
            
            return dashboard
            
        except Exception as e:
            logger.error(f"Error creating dashboard: {str(e)}")
            return self._create_error_dashboard(str(e))
            
            # Create filters
            filters = self._create_dashboard_filters(df)
            
            # Generate summary statistics
            summary_stats = self._generate_summary_statistics(df)
            
            # Create dashboard model
            dashboard = DashboardModel(
                content_id=table.metadata.get('source_content_id', ''),
                title=f"Interactive Dashboard - {table.table_id}",
                description=f"Dashboard generated from table with {len(table.rows)} records and {len(table.headers)} columns",
                layout=layout,
                charts=charts,
                filters=filters,
                interactions={
                    'cross_filter': True,
                    'zoom': True,
                    'hover': True,
                    'selection': True
                },
                summary_stats=summary_stats
            )
            
            logger.info(f"Successfully created dashboard with {len(charts)} charts")
            return dashboard
            
        except Exception as e:
            logger.error(f"Error creating dashboard: {e}")
            return None
    
    def _create_chart_from_suggestion(self, df: pd.DataFrame, suggestion: Dict[str, Any], chart_index: int) -> Optional[VisualizationModel]:
        """Create a chart visualization from suggestion"""
        try:
            chart_type = suggestion['type']
            config = suggestion.get('config', {})
            
            # Create chart config
            chart_config = ChartConfig(
                chart_type=chart_type,
                title=suggestion.get('title', f'Chart {chart_index + 1}'),
                x_axis=config.get('x_axis'),
                y_axis=config.get('y_axis'),
                color_column=config.get('color_column'),
                height=400,
                width=600,
                theme="plotly_white",
                interactive=True
            )
            
            # Generate chart data using appropriate generator
            chart_generator = self.chart_generators.get(chart_type)
            if not chart_generator:
                logger.warning(f"No generator found for chart type: {chart_type}")
                return None
            
            chart_data = chart_generator(df, chart_config)
            
            if not chart_data:
                logger.warning(f"Failed to generate chart data for: {chart_type}")
                return None
            
            # Create visualization model
            chart = VisualizationModel(
                content_id=chart_config.title.replace(' ', '_').lower(),
                viz_type=chart_type,
                title=chart_config.title,
                description=suggestion.get('description', f'{chart_type.value} visualization'),
                config=chart_config,
                data=chart_data
            )
            
            return chart
            
        except Exception as e:
            logger.error(f"Error creating chart from suggestion: {e}")
            return None
    
    def _create_line_chart(self, df: pd.DataFrame, config: ChartConfig) -> Optional[Dict[str, Any]]:
        """Create line chart"""
        try:
            x_col = config.x_axis
            y_col = config.y_axis
            
            if not x_col or not y_col or x_col not in df.columns or y_col not in df.columns:
                return None
            
            fig = px.line(
                df, 
                x=x_col, 
                y=y_col,
                title=config.title,
                color=config.color_column if config.color_column and config.color_column in df.columns else None,
                height=config.height,
                color_discrete_sequence=self.default_colors
            )
            
            fig.update_layout(
                xaxis_title=x_col,
                yaxis_title=y_col,
                hovermode='x unified',
                showlegend=True
            )
            
            return {
                'plotly_json': fig.to_json(),
                'chart_type': 'line',
                'data_summary': {
                    'x_column': x_col,
                    'y_column': y_col,
                    'data_points': len(df)
                }
            }
            
        except Exception as e:
            logger.error(f"Error creating line chart: {e}")
            return None
    
    def _create_bar_chart(self, df: pd.DataFrame, config: ChartConfig) -> Optional[Dict[str, Any]]:
        """Create bar chart"""
        try:
            x_col = config.x_axis
            y_col = config.y_axis
            
            if not x_col or not y_col or x_col not in df.columns or y_col not in df.columns:
                return None
            
            # Group data if needed
            grouped_df = df.groupby(x_col)[y_col].sum().reset_index()
            
            fig = px.bar(
                grouped_df,
                x=x_col,
                y=y_col,
                title=config.title,
                height=config.height,
                color_discrete_sequence=self.default_colors
            )
            
            fig.update_layout(
                xaxis_title=x_col,
                yaxis_title=y_col,
                showlegend=False
            )
            
            return {
                'plotly_json': fig.to_json(),
                'chart_type': 'bar',
                'data_summary': {
                    'x_column': x_col,
                    'y_column': y_col,
                    'categories': len(grouped_df)
                }
            }
            
        except Exception as e:
            logger.error(f"Error creating bar chart: {e}")
            return None
    
    def _create_scatter_plot(self, df: pd.DataFrame, config: ChartConfig) -> Optional[Dict[str, Any]]:
        """Create scatter plot"""
        try:
            x_col = config.x_axis
            y_col = config.y_axis
            
            if not x_col or not y_col or x_col not in df.columns or y_col not in df.columns:
                return None
            
            fig = px.scatter(
                df,
                x=x_col,
                y=y_col,
                title=config.title,
                color=config.color_column if config.color_column and config.color_column in df.columns else None,
                size=config.size_column if config.size_column and config.size_column in df.columns else None,
                height=config.height,
                color_discrete_sequence=self.default_colors
            )
            
            fig.update_layout(
                xaxis_title=x_col,
                yaxis_title=y_col
            )
            
            return {
                'plotly_json': fig.to_json(),
                'chart_type': 'scatter',
                'data_summary': {
                    'x_column': x_col,
                    'y_column': y_col,
                    'data_points': len(df)
                }
            }
            
        except Exception as e:
            logger.error(f"Error creating scatter plot: {e}")
            return None
    
    def _create_pie_chart(self, df: pd.DataFrame, config: ChartConfig) -> Optional[Dict[str, Any]]:
        """Create pie chart"""
        try:
            x_col = config.x_axis  # Category column
            y_col = config.y_axis  # Value column
            
            if not x_col or x_col not in df.columns:
                return None
            
            # Aggregate data
            if y_col and y_col in df.columns:
                pie_data = df.groupby(x_col)[y_col].sum().reset_index()
                values = pie_data[y_col]
            else:
                pie_data = df[x_col].value_counts().reset_index()
                pie_data.columns = [x_col, 'count']
                values = pie_data['count']
            
            fig = px.pie(
                pie_data,
                names=x_col,
                values=values.name,
                title=config.title,
                height=config.height,
                color_discrete_sequence=self.default_colors
            )
            
            return {
                'plotly_json': fig.to_json(),
                'chart_type': 'pie',
                'data_summary': {
                    'category_column': x_col,
                    'value_column': values.name,
                    'categories': len(pie_data)
                }
            }
            
        except Exception as e:
            logger.error(f"Error creating pie chart: {e}")
            return None
    
    def _create_histogram(self, df: pd.DataFrame, config: ChartConfig) -> Optional[Dict[str, Any]]:
        """Create histogram"""
        try:
            x_col = config.x_axis
            
            if not x_col or x_col not in df.columns:
                return None
            
            fig = px.histogram(
                df,
                x=x_col,
                title=config.title,
                height=config.height,
                color_discrete_sequence=self.default_colors
            )
            
            fig.update_layout(
                xaxis_title=x_col,
                yaxis_title='Frequency'
            )
            
            return {
                'plotly_json': fig.to_json(),
                'chart_type': 'histogram',
                'data_summary': {
                    'column': x_col,
                    'data_points': len(df)
                }
            }
            
        except Exception as e:
            logger.error(f"Error creating histogram: {e}")
            return None
    
    def _create_heatmap(self, df: pd.DataFrame, config: ChartConfig) -> Optional[Dict[str, Any]]:
        """Create correlation heatmap"""
        try:
            # Select numeric columns for correlation
            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
            
            if len(numeric_cols) < 2:
                return None
            
            correlation_matrix = df[numeric_cols].corr()
            
            fig = px.imshow(
                correlation_matrix,
                title=config.title,
                height=config.height,
                color_continuous_scale='RdBu_r',
                aspect='auto'
            )
            
            return {
                'plotly_json': fig.to_json(),
                'chart_type': 'heatmap',
                'data_summary': {
                    'columns': numeric_cols,
                    'correlation_matrix_size': f"{len(numeric_cols)}x{len(numeric_cols)}"
                }
            }
            
        except Exception as e:
            logger.error(f"Error creating heatmap: {e}")
            return None
    
    def _create_box_plot(self, df: pd.DataFrame, config: ChartConfig) -> Optional[Dict[str, Any]]:
        """Create box plot"""
        try:
            y_col = config.y_axis
            x_col = config.x_axis  # Optional grouping column
            
            if not y_col or y_col not in df.columns:
                return None
            
            fig = px.box(
                df,
                y=y_col,
                x=x_col if x_col and x_col in df.columns else None,
                title=config.title,
                height=config.height,
                color_discrete_sequence=self.default_colors
            )
            
            return {
                'plotly_json': fig.to_json(),
                'chart_type': 'box',
                'data_summary': {
                    'y_column': y_col,
                    'x_column': x_col,
                    'data_points': len(df)
                }
            }
            
        except Exception as e:
            logger.error(f"Error creating box plot: {e}")
            return None
    
    def _design_dashboard_layout(self, num_charts: int) -> Dict[str, Any]:
        """Design dashboard layout based on number of charts"""
        if num_charts == 1:
            return {'type': 'single', 'columns': 1, 'rows': 1}
        elif num_charts == 2:
            return {'type': 'grid', 'columns': 2, 'rows': 1}
        elif num_charts <= 4:
            return {'type': 'grid', 'columns': 2, 'rows': 2}
        elif num_charts <= 6:
            return {'type': 'grid', 'columns': 3, 'rows': 2}
        else:
            return {'type': 'grid', 'columns': 3, 'rows': 3}
    
    def _create_dashboard_filters(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Create interactive filters for dashboard"""
        filters = []
        
        # Create filters for categorical columns with reasonable number of unique values
        for col in df.columns:
            unique_values = df[col].dropna().unique()
            
            if len(unique_values) <= 20 and len(unique_values) > 1:
                filter_config = {
                    'name': col,
                    'type': 'multi_select',
                    'options': [{'label': str(val), 'value': str(val)} for val in sorted(unique_values)],
                    'default': [str(val) for val in unique_values],  # All selected by default
                    'label': col.replace('_', ' ').title()
                }
                filters.append(filter_config)
        
        return filters[:5]  # Limit to 5 filters to avoid clutter
    
    def _generate_summary_statistics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Generate summary statistics for the dashboard"""
        summary = {
            'total_records': len(df),
            'total_columns': len(df.columns),
            'column_types': {}
        }
        
        # Analyze column types
        for col in df.columns:
            if df[col].dtype in ['int64', 'float64']:
                summary['column_types'][col] = {
                    'type': 'numeric',
                    'mean': float(df[col].mean()) if not df[col].isna().all() else None,
                    'median': float(df[col].median()) if not df[col].isna().all() else None,
                    'std': float(df[col].std()) if not df[col].isna().all() else None,
                    'min': float(df[col].min()) if not df[col].isna().all() else None,
                    'max': float(df[col].max()) if not df[col].isna().all() else None
                }
            else:
                summary['column_types'][col] = {
                    'type': 'categorical',
                    'unique_values': int(df[col].nunique()),
                    'most_common': str(df[col].mode().iloc[0]) if not df[col].empty else None
                }
        
        return summary
