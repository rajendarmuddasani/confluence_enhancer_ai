"""
Chart and plot generation
"""
import logging
from typing import Dict, Any, List, Optional
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

from ..models.visualization_model import VisualizationType, ChartConfig, VisualizationModel


logger = logging.getLogger(__name__)


class ChartGenerator:
    """Generate various types of charts and plots"""
    
    def __init__(self):
        self.default_colors = px.colors.qualitative.Set3
        self.chart_types = {
            VisualizationType.LINE_CHART: self.create_line_chart,
            VisualizationType.BAR_CHART: self.create_bar_chart,
            VisualizationType.SCATTER_PLOT: self.create_scatter_plot,
            VisualizationType.PIE_CHART: self.create_pie_chart,
            VisualizationType.HISTOGRAM: self.create_histogram,
            VisualizationType.HEATMAP: self.create_heatmap,
            VisualizationType.BOX_PLOT: self.create_box_plot
        }
    
    def generate_chart(self, chart_type: VisualizationType, data: pd.DataFrame, config: ChartConfig) -> Optional[VisualizationModel]:
        """Generate chart based on type and configuration"""
        try:
            logger.info(f"Generating {chart_type} chart")
            
            if chart_type not in self.chart_types:
                logger.error(f"Unsupported chart type: {chart_type}")
                return None
            
            chart_func = self.chart_types[chart_type]
            fig = chart_func(data, config)
            
            if fig is None:
                return None
            
            return VisualizationModel(
                visualization_id=f"chart_{chart_type}_{hash(str(config))}",
                title=config.title or f"{chart_type.replace('_', ' ').title()} Chart",
                type=chart_type,
                config=fig.to_json(),
                description=config.description or f"Generated {chart_type} visualization",
                interactive=True
            )
            
        except Exception as e:
            logger.error(f"Error generating chart: {e}")
            return None
    
    def create_line_chart(self, data: pd.DataFrame, config: ChartConfig) -> Optional[go.Figure]:
        """Create interactive line chart"""
        try:
            if not config.x_axis or not config.y_axis:
                logger.error("Line chart requires x_axis and y_axis configuration")
                return None
            
            if config.x_axis not in data.columns or config.y_axis not in data.columns:
                logger.error(f"Columns {config.x_axis} or {config.y_axis} not found in data")
                return None
            
            fig = px.line(
                data,
                x=config.x_axis,
                y=config.y_axis,
                title=config.title or f"{config.y_axis} over {config.x_axis}",
                color=config.color_column,
                hover_data=config.hover_columns or []
            )
            
            fig.update_layout(
                hovermode='x unified',
                showlegend=True,
                height=config.height or 400,
                width=config.width,
                xaxis_title=config.x_axis_title or config.x_axis,
                yaxis_title=config.y_axis_title or config.y_axis
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating line chart: {e}")
            return None
    
    def create_bar_chart(self, data: pd.DataFrame, config: ChartConfig) -> Optional[go.Figure]:
        """Create interactive bar chart"""
        try:
            if not config.x_axis or not config.y_axis:
                logger.error("Bar chart requires x_axis and y_axis configuration")
                return None
            
            if config.x_axis not in data.columns or config.y_axis not in data.columns:
                logger.error(f"Columns {config.x_axis} or {config.y_axis} not found in data")
                return None
            
            fig = px.bar(
                data,
                x=config.x_axis,
                y=config.y_axis,
                title=config.title or f"{config.y_axis} by {config.x_axis}",
                color=config.color_column,
                hover_data=config.hover_columns or []
            )
            
            fig.update_layout(
                showlegend=True,
                height=config.height or 400,
                width=config.width,
                xaxis_title=config.x_axis_title or config.x_axis,
                yaxis_title=config.y_axis_title or config.y_axis
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating bar chart: {e}")
            return None
    
    def create_scatter_plot(self, data: pd.DataFrame, config: ChartConfig) -> Optional[go.Figure]:
        """Create interactive scatter plot"""
        try:
            if not config.x_axis or not config.y_axis:
                logger.error("Scatter plot requires x_axis and y_axis configuration")
                return None
            
            if config.x_axis not in data.columns or config.y_axis not in data.columns:
                logger.error(f"Columns {config.x_axis} or {config.y_axis} not found in data")
                return None
            
            fig = px.scatter(
                data,
                x=config.x_axis,
                y=config.y_axis,
                title=config.title or f"{config.y_axis} vs {config.x_axis}",
                color=config.color_column,
                size=config.size_column,
                hover_data=config.hover_columns or []
            )
            
            fig.update_layout(
                height=config.height or 400,
                width=config.width,
                xaxis_title=config.x_axis_title or config.x_axis,
                yaxis_title=config.y_axis_title or config.y_axis
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating scatter plot: {e}")
            return None
    
    def create_pie_chart(self, data: pd.DataFrame, config: ChartConfig) -> Optional[go.Figure]:
        """Create interactive pie chart"""
        try:
            if not config.values_column or not config.names_column:
                logger.error("Pie chart requires values_column and names_column configuration")
                return None
            
            if config.values_column not in data.columns or config.names_column not in data.columns:
                logger.error(f"Columns {config.values_column} or {config.names_column} not found in data")
                return None
            
            fig = px.pie(
                data,
                values=config.values_column,
                names=config.names_column,
                title=config.title or f"Distribution of {config.values_column}"
            )
            
            fig.update_layout(
                height=config.height or 400,
                width=config.width
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating pie chart: {e}")
            return None
    
    def create_histogram(self, data: pd.DataFrame, config: ChartConfig) -> Optional[go.Figure]:
        """Create interactive histogram"""
        try:
            if not config.x_axis:
                logger.error("Histogram requires x_axis configuration")
                return None
            
            if config.x_axis not in data.columns:
                logger.error(f"Column {config.x_axis} not found in data")
                return None
            
            fig = px.histogram(
                data,
                x=config.x_axis,
                title=config.title or f"Distribution of {config.x_axis}",
                color=config.color_column,
                nbins=config.bins or 30
            )
            
            fig.update_layout(
                height=config.height or 400,
                width=config.width,
                xaxis_title=config.x_axis_title or config.x_axis,
                yaxis_title="Count"
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating histogram: {e}")
            return None
    
    def create_heatmap(self, data: pd.DataFrame, config: ChartConfig) -> Optional[go.Figure]:
        """Create interactive heatmap"""
        try:
            # For correlation heatmap
            if config.heatmap_type == 'correlation':
                numeric_cols = data.select_dtypes(include=[np.number]).columns
                if len(numeric_cols) < 2:
                    logger.error("Not enough numeric columns for correlation heatmap")
                    return None
                
                corr_matrix = data[numeric_cols].corr()
                
                fig = px.imshow(
                    corr_matrix,
                    title=config.title or "Correlation Heatmap",
                    color_continuous_scale='RdBu_r',
                    aspect='auto'
                )
                
            # For value heatmap
            elif config.x_axis and config.y_axis and config.values_column:
                if not all(col in data.columns for col in [config.x_axis, config.y_axis, config.values_column]):
                    logger.error("Required columns not found for value heatmap")
                    return None
                
                pivot_data = data.pivot_table(
                    values=config.values_column,
                    index=config.y_axis,
                    columns=config.x_axis,
                    aggfunc='mean'
                )
                
                fig = px.imshow(
                    pivot_data,
                    title=config.title or f"Heatmap of {config.values_column}",
                    aspect='auto'
                )
            else:
                logger.error("Insufficient configuration for heatmap")
                return None
            
            fig.update_layout(
                height=config.height or 400,
                width=config.width
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating heatmap: {e}")
            return None
    
    def create_box_plot(self, data: pd.DataFrame, config: ChartConfig) -> Optional[go.Figure]:
        """Create interactive box plot"""
        try:
            if not config.y_axis:
                logger.error("Box plot requires y_axis configuration")
                return None
            
            if config.y_axis not in data.columns:
                logger.error(f"Column {config.y_axis} not found in data")
                return None
            
            fig = px.box(
                data,
                x=config.x_axis,
                y=config.y_axis,
                title=config.title or f"Box Plot of {config.y_axis}",
                color=config.color_column
            )
            
            fig.update_layout(
                height=config.height or 400,
                width=config.width,
                xaxis_title=config.x_axis_title or config.x_axis or "Category",
                yaxis_title=config.y_axis_title or config.y_axis
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating box plot: {e}")
            return None
    
    def create_time_series_chart(self, data: pd.DataFrame, config: ChartConfig) -> Optional[go.Figure]:
        """Create specialized time series chart"""
        try:
            if not config.x_axis or not config.y_axis:
                logger.error("Time series chart requires x_axis and y_axis configuration")
                return None
            
            # Ensure x_axis is datetime
            if data[config.x_axis].dtype != 'datetime64[ns]':
                try:
                    data[config.x_axis] = pd.to_datetime(data[config.x_axis])
                except:
                    logger.error(f"Cannot convert {config.x_axis} to datetime")
                    return None
            
            fig = px.line(
                data,
                x=config.x_axis,
                y=config.y_axis,
                title=config.title or f"Time Series: {config.y_axis}",
                color=config.color_column
            )
            
            # Add time series specific features
            fig.update_layout(
                xaxis=dict(
                    rangeselector=dict(
                        buttons=list([
                            dict(count=1, label="1m", step="month", stepmode="backward"),
                            dict(count=6, label="6m", step="month", stepmode="backward"),
                            dict(count=1, label="1y", step="year", stepmode="backward"),
                            dict(step="all")
                        ])
                    ),
                    rangeslider=dict(visible=True),
                    type="date"
                ),
                height=config.height or 500,
                width=config.width
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating time series chart: {e}")
            return None
    
    def create_multi_axis_chart(self, data: pd.DataFrame, config: ChartConfig) -> Optional[go.Figure]:
        """Create chart with multiple y-axes"""
        try:
            if not config.x_axis or not config.y_axis or not config.secondary_y_axis:
                logger.error("Multi-axis chart requires x_axis, y_axis, and secondary_y_axis")
                return None
            
            # Create subplots with secondary y-axis
            from plotly.subplots import make_subplots
            
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            
            # Add primary trace
            fig.add_trace(
                go.Scatter(
                    x=data[config.x_axis],
                    y=data[config.y_axis],
                    name=config.y_axis,
                    mode='lines+markers'
                ),
                secondary_y=False
            )
            
            # Add secondary trace
            fig.add_trace(
                go.Scatter(
                    x=data[config.x_axis],
                    y=data[config.secondary_y_axis],
                    name=config.secondary_y_axis,
                    mode='lines+markers'
                ),
                secondary_y=True
            )
            
            # Update layout
            fig.update_layout(
                title=config.title or "Multi-Axis Chart",
                height=config.height or 400,
                width=config.width
            )
            
            # Update axis labels
            fig.update_yaxes(title_text=config.y_axis, secondary_y=False)
            fig.update_yaxes(title_text=config.secondary_y_axis, secondary_y=True)
            fig.update_xaxes(title_text=config.x_axis)
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating multi-axis chart: {e}")
            return None
