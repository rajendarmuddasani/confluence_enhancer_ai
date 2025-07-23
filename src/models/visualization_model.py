"""
Data models for visualizations
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field
from enum import Enum


class VisualizationType(str, Enum):
    LINE_CHART = "line_chart"
    BAR_CHART = "bar_chart"
    SCATTER_PLOT = "scatter_plot"
    HEATMAP = "heatmap"
    PIE_CHART = "pie_chart"
    HISTOGRAM = "histogram"
    BOX_PLOT = "box_plot"
    DASHBOARD = "dashboard"
    FLOWCHART = "flowchart"
    NETWORK_DIAGRAM = "network_diagram"
    ARCHITECTURE_DIAGRAM = "architecture_diagram"


class ChartConfig(BaseModel):
    """Configuration for charts"""
    chart_type: VisualizationType
    title: str
    x_axis: Optional[str] = None
    y_axis: Optional[str] = None
    color_column: Optional[str] = None
    size_column: Optional[str] = None
    height: int = 400
    width: int = 600
    theme: str = "plotly_white"
    interactive: bool = True
    annotations: List[Dict[str, Any]] = Field(default_factory=list)


class VisualizationModel(BaseModel):
    """Model for visualization data"""
    viz_id: Optional[str] = None
    content_id: str
    viz_type: VisualizationType
    title: str
    description: str
    config: ChartConfig
    data: Dict[str, Any]
    code: Optional[str] = None  # For diagram code (Mermaid, GraphViz, etc.)
    format: Optional[str] = None  # 'mermaid', 'graphviz', 'plantuml'
    created_date: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class DashboardModel(BaseModel):
    """Model for interactive dashboards"""
    dashboard_id: Optional[str] = None
    content_id: str
    title: str
    description: str
    layout: Dict[str, Any]
    charts: List[VisualizationModel]
    filters: List[Dict[str, Any]] = Field(default_factory=list)
    interactions: Dict[str, Any] = Field(default_factory=dict)
    summary_stats: Dict[str, Any] = Field(default_factory=dict)
    created_date: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class DiagramNode(BaseModel):
    """Model for diagram nodes"""
    node_id: str
    label: str
    node_type: str
    shape: str = "rectangle"
    color: str = "#ffffff"
    position: Optional[Dict[str, float]] = None


class DiagramEdge(BaseModel):
    """Model for diagram edges"""
    edge_id: str
    from_node: str
    to_node: str
    label: Optional[str] = None
    edge_type: str = "directed"
    color: str = "#000000"


class DiagramModel(BaseModel):
    """Model for diagrams (flowcharts, network diagrams, etc.)"""
    diagram_id: Optional[str] = None
    content_id: str
    diagram_type: VisualizationType
    title: str
    description: str
    nodes: List[DiagramNode]
    edges: List[DiagramEdge]
    layout: str = "hierarchical"  # 'hierarchical', 'force', 'circular'
    code: Optional[str] = None  # Generated diagram code
    format: str = "mermaid"  # 'mermaid', 'graphviz', 'plantuml'
    created_date: Optional[datetime] = None
    
    class Config:
        from_attributes = True
