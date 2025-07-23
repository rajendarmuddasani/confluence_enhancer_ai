"""
Network and relationship diagrams
"""
import logging
from typing import Dict, Any, List, Optional, Tuple
import pandas as pd
import networkx as nx
import plotly.graph_objects as go
import plotly.express as px
from dataclasses import dataclass

from ..models.visualization_model import DiagramModel, DiagramNode, DiagramEdge


logger = logging.getLogger(__name__)


@dataclass
class NetworkNode:
    """Represents a node in a network"""
    id: str
    label: str
    size: float = 10.0
    color: str = "#1f77b4"
    shape: str = "circle"
    metadata: Dict[str, Any] = None


@dataclass
class NetworkEdge:
    """Represents an edge in a network"""
    source: str
    target: str
    weight: float = 1.0
    label: str = ""
    color: str = "#888888"
    metadata: Dict[str, Any] = None


class NetworkVisualizer:
    """Generate network and relationship diagrams"""
    
    def __init__(self):
        self.default_node_size = 20
        self.default_edge_width = 2
        self.layout_algorithms = {
            'spring': nx.spring_layout,
            'circular': nx.circular_layout,
            'random': nx.random_layout,
            'shell': nx.shell_layout,
            'kamada_kawai': nx.kamada_kawai_layout
        }
    
    def create_network_diagram(self, nodes: List[NetworkNode], edges: List[NetworkEdge], 
                             layout: str = 'spring', **kwargs) -> Optional[go.Figure]:
        """Create interactive network diagram"""
        try:
            logger.info(f"Creating network diagram with {len(nodes)} nodes and {len(edges)} edges")
            
            if not nodes:
                logger.error("No nodes provided for network diagram")
                return None
            
            # Create NetworkX graph
            G = nx.Graph()
            
            # Add nodes
            for node in nodes:
                G.add_node(node.id, label=node.label, size=node.size, 
                          color=node.color, shape=node.shape)
            
            # Add edges
            for edge in edges:
                if edge.source in G.nodes and edge.target in G.nodes:
                    G.add_edge(edge.source, edge.target, weight=edge.weight, 
                             label=edge.label, color=edge.color)
            
            # Calculate layout
            if layout in self.layout_algorithms:
                pos = self.layout_algorithms[layout](G)
            else:
                pos = nx.spring_layout(G)
            
            # Create Plotly traces
            edge_trace = self._create_edge_trace(G, pos, edges)
            node_trace = self._create_node_trace(G, pos, nodes)
            
            # Create figure
            fig = go.Figure(data=[edge_trace, node_trace],
                          layout=go.Layout(
                              title=kwargs.get('title', 'Network Diagram'),
                              titlefont_size=16,
                              showlegend=False,
                              hovermode='closest',
                              margin=dict(b=20,l=5,r=5,t=40),
                              annotations=[ dict(
                                  text="",
                                  showarrow=False,
                                  xref="paper", yref="paper",
                                  x=0.005, y=-0.002,
                                  xanchor='left', yanchor='bottom',
                                  font=dict(color="#888", size=12)
                              ) ],
                              xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                              yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                              height=kwargs.get('height', 600),
                              width=kwargs.get('width', 800)
                          ))
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating network diagram: {e}")
            return None
    
    def _create_edge_trace(self, G: nx.Graph, pos: Dict, edges: List[NetworkEdge]) -> go.Scatter:
        """Create edge trace for network diagram"""
        edge_x = []
        edge_y = []
        edge_info = []
        
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
            
            # Find edge info
            edge_data = G.edges[edge]
            edge_info.append(f"From: {edge[0]}<br>To: {edge[1]}<br>Weight: {edge_data.get('weight', 1)}")
        
        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=2, color='#888'),
            hoverinfo='none',
            mode='lines'
        )
        
        return edge_trace
    
    def _create_node_trace(self, G: nx.Graph, pos: Dict, nodes: List[NetworkNode]) -> go.Scatter:
        """Create node trace for network diagram"""
        node_x = []
        node_y = []
        node_colors = []
        node_sizes = []
        node_text = []
        node_info = []
        
        for node in G.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            
            # Get node data
            node_data = G.nodes[node]
            node_colors.append(node_data.get('color', '#1f77b4'))
            node_sizes.append(node_data.get('size', self.default_node_size))
            node_text.append(node_data.get('label', node))
            
            # Node info for hover
            adjacencies = list(G.neighbors(node))
            node_info.append(f"Node: {node_data.get('label', node)}<br>"
                           f"Connections: {len(adjacencies)}<br>"
                           f"Connected to: {', '.join(adjacencies[:5])}")
        
        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            hoverinfo='text',
            text=node_text,
            textposition="middle center",
            hovertext=node_info,
            marker=dict(
                showscale=True,
                colorscale='Viridis',
                reversescale=True,
                color=node_colors,
                size=node_sizes,
                colorbar=dict(
                    thickness=15,
                    len=0.5,
                    x=1.01,
                    title="Node Connections",
                    xanchor="left",
                    titleside="right"
                ),
                line=dict(width=2, color='white')
            )
        )
        
        return node_trace
    
    def create_hierarchy_diagram(self, hierarchy_data: Dict[str, Any]) -> Optional[go.Figure]:
        """Create hierarchical network diagram"""
        try:
            logger.info("Creating hierarchy diagram")
            
            nodes = []
            edges = []
            
            def process_hierarchy(item: Dict, parent_id: str = None, level: int = 0):
                """Recursively process hierarchy data"""
                node_id = item.get('id', f"node_{len(nodes)}")
                
                # Create node
                node = NetworkNode(
                    id=node_id,
                    label=item.get('label', item.get('name', node_id)),
                    size=max(30 - level * 5, 10),  # Smaller nodes at deeper levels
                    color=px.colors.qualitative.Set1[level % len(px.colors.qualitative.Set1)]
                )
                nodes.append(node)
                
                # Create edge to parent
                if parent_id:
                    edge = NetworkEdge(
                        source=parent_id,
                        target=node_id,
                        weight=1.0
                    )
                    edges.append(edge)
                
                # Process children
                for child in item.get('children', []):
                    process_hierarchy(child, node_id, level + 1)
            
            # Process root node
            root = hierarchy_data.get('root', hierarchy_data)
            process_hierarchy(root)
            
            # Create diagram with hierarchical layout
            fig = self.create_network_diagram(nodes, edges, layout='spring',
                                            title=hierarchy_data.get('title', 'Hierarchy Diagram'))
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating hierarchy diagram: {e}")
            return None
    
    def create_dependency_diagram(self, dependencies: List[Dict[str, Any]]) -> Optional[go.Figure]:
        """Create dependency relationship diagram"""
        try:
            logger.info("Creating dependency diagram")
            
            nodes = []
            edges = []
            node_set = set()
            
            # Extract nodes and edges from dependencies
            for dep in dependencies:
                source = dep.get('source', '')
                target = dep.get('target', '')
                
                if source and target:
                    # Add nodes
                    if source not in node_set:
                        nodes.append(NetworkNode(
                            id=source,
                            label=source,
                            color='#ff7f0e'  # Orange for sources
                        ))
                        node_set.add(source)
                    
                    if target not in node_set:
                        nodes.append(NetworkNode(
                            id=target,
                            label=target,
                            color='#2ca02c'  # Green for targets
                        ))
                        node_set.add(target)
                    
                    # Add edge
                    edges.append(NetworkEdge(
                        source=source,
                        target=target,
                        label=dep.get('type', ''),
                        weight=dep.get('weight', 1.0)
                    ))
            
            fig = self.create_network_diagram(nodes, edges, layout='kamada_kawai',
                                            title='Dependency Diagram')
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating dependency diagram: {e}")
            return None
    
    def create_flow_diagram(self, flow_data: Dict[str, Any]) -> Optional[go.Figure]:
        """Create flow/process diagram"""
        try:
            logger.info("Creating flow diagram")
            
            nodes = []
            edges = []
            
            # Process flow steps
            for i, step in enumerate(flow_data.get('steps', [])):
                node = NetworkNode(
                    id=step.get('id', f"step_{i}"),
                    label=step.get('name', f"Step {i+1}"),
                    size=25,
                    color=self._get_step_color(step.get('type', 'process'))
                )
                nodes.append(node)
            
            # Process flow connections
            for connection in flow_data.get('connections', []):
                edge = NetworkEdge(
                    source=connection['from'],
                    target=connection['to'],
                    label=connection.get('condition', ''),
                    weight=1.0
                )
                edges.append(edge)
            
            fig = self.create_network_diagram(nodes, edges, layout='spring',
                                            title=flow_data.get('title', 'Flow Diagram'))
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating flow diagram: {e}")
            return None
    
    def _get_step_color(self, step_type: str) -> str:
        """Get color for step type"""
        color_map = {
            'start': '#2ca02c',      # Green
            'end': '#d62728',        # Red
            'process': '#1f77b4',    # Blue
            'decision': '#ff7f0e',   # Orange
            'data': '#9467bd',       # Purple
            'connector': '#8c564b'   # Brown
        }
        return color_map.get(step_type, '#1f77b4')
    
    def create_relationship_matrix(self, relationships: List[Dict[str, Any]]) -> Optional[go.Figure]:
        """Create relationship matrix heatmap"""
        try:
            logger.info("Creating relationship matrix")
            
            # Extract entities
            entities = set()
            for rel in relationships:
                entities.add(rel.get('source', ''))
                entities.add(rel.get('target', ''))
            
            entities = sorted(list(entities))
            if not entities:
                return None
            
            # Create matrix
            matrix = [[0 for _ in entities] for _ in entities]
            entity_to_idx = {entity: i for i, entity in enumerate(entities)}
            
            # Fill matrix with relationship strengths
            for rel in relationships:
                source = rel.get('source', '')
                target = rel.get('target', '')
                strength = rel.get('strength', 1)
                
                if source in entity_to_idx and target in entity_to_idx:
                    source_idx = entity_to_idx[source]
                    target_idx = entity_to_idx[target]
                    matrix[source_idx][target_idx] = strength
                    matrix[target_idx][source_idx] = strength  # Make symmetric
            
            # Create heatmap
            fig = go.Figure(data=go.Heatmap(
                z=matrix,
                x=entities,
                y=entities,
                colorscale='Viridis',
                showscale=True
            ))
            
            fig.update_layout(
                title='Relationship Matrix',
                xaxis_title='Entities',
                yaxis_title='Entities',
                height=600,
                width=600
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating relationship matrix: {e}")
            return None
    
    def analyze_network_metrics(self, nodes: List[NetworkNode], edges: List[NetworkEdge]) -> Dict[str, Any]:
        """Analyze network metrics"""
        try:
            # Create NetworkX graph
            G = nx.Graph()
            
            for node in nodes:
                G.add_node(node.id)
            
            for edge in edges:
                if edge.source in G.nodes and edge.target in G.nodes:
                    G.add_edge(edge.source, edge.target, weight=edge.weight)
            
            # Calculate metrics
            metrics = {
                'node_count': len(G.nodes),
                'edge_count': len(G.edges),
                'density': nx.density(G),
                'average_clustering': nx.average_clustering(G),
                'connected_components': nx.number_connected_components(G)
            }
            
            # Centrality measures
            if len(G.nodes) > 0:
                degree_centrality = nx.degree_centrality(G)
                betweenness_centrality = nx.betweenness_centrality(G)
                closeness_centrality = nx.closeness_centrality(G)
                
                metrics['top_degree_nodes'] = sorted(degree_centrality.items(), 
                                                   key=lambda x: x[1], reverse=True)[:5]
                metrics['top_betweenness_nodes'] = sorted(betweenness_centrality.items(), 
                                                        key=lambda x: x[1], reverse=True)[:5]
                metrics['top_closeness_nodes'] = sorted(closeness_centrality.items(), 
                                                       key=lambda x: x[1], reverse=True)[:5]
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error analyzing network metrics: {e}")
            return {}
    
    def export_network_data(self, nodes: List[NetworkNode], edges: List[NetworkEdge], 
                           format: str = 'json') -> Optional[str]:
        """Export network data in various formats"""
        try:
            if format.lower() == 'json':
                import json
                data = {
                    'nodes': [{'id': n.id, 'label': n.label, 'size': n.size, 'color': n.color} for n in nodes],
                    'edges': [{'source': e.source, 'target': e.target, 'weight': e.weight, 'label': e.label} for e in edges]
                }
                return json.dumps(data, indent=2)
            
            elif format.lower() == 'gexf':
                # Create NetworkX graph and export as GEXF
                G = nx.Graph()
                for node in nodes:
                    G.add_node(node.id, label=node.label, size=node.size, color=node.color)
                for edge in edges:
                    G.add_edge(edge.source, edge.target, weight=edge.weight, label=edge.label)
                
                import tempfile
                with tempfile.NamedTemporaryFile(mode='w', suffix='.gexf', delete=False) as f:
                    nx.write_gexf(G, f.name)
                    with open(f.name, 'r') as read_f:
                        return read_f.read()
            
            return None
            
        except Exception as e:
            logger.error(f"Error exporting network data: {e}")
            return None
