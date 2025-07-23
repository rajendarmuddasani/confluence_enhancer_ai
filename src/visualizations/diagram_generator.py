"""
Flowchart and block diagram creation
"""
import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

from ..models.visualization_model import DiagramModel, DiagramNode, DiagramEdge, VisualizationType


logger = logging.getLogger(__name__)


@dataclass
class MermaidGenerator:
    """Generator for Mermaid diagrams"""
    
    def generate_flowchart(self, process_data: Dict[str, Any]) -> str:
        """Generate Mermaid flowchart syntax"""
        mermaid_code = "flowchart TD\n"
        
        # Add start node
        mermaid_code += "    Start([Start])\n"
        
        # Add process steps
        for i, step in enumerate(process_data.get('steps', [])):
            node_id = f"Step{i+1}"
            if step.get('type') == 'process':
                mermaid_code += f"    {node_id}[{step['description']}]\n"
            elif step.get('type') == 'decision':
                mermaid_code += f"    {node_id}{{{step['description']}}}\n"
            elif step.get('type') == 'data':
                mermaid_code += f"    {node_id}[({step['description']})]\n"
            else:
                mermaid_code += f"    {node_id}[{step.get('description', 'Step')}]\n"
        
        # Add connections
        for connection in process_data.get('connections', []):
            mermaid_code += f"    {connection['from']} --> {connection['to']}\n"
            if connection.get('label'):
                mermaid_code += f"    {connection['from']} -->|{connection['label']}| {connection['to']}\n"
        
        # Add end node
        mermaid_code += "    End([End])\n"
        
        return mermaid_code
    
    def generate_architecture_diagram(self, architecture_data: Dict[str, Any]) -> str:
        """Generate architecture diagram in Mermaid format"""
        if architecture_data.get('style') == 'layered':
            return self._create_layered_architecture(architecture_data)
        elif architecture_data.get('style') == 'microservices':
            return self._create_microservices_diagram(architecture_data)
        else:
            return self._create_basic_architecture(architecture_data)
    
    def _create_layered_architecture(self, data: Dict[str, Any]) -> str:
        """Create layered architecture diagram"""
        mermaid_code = "graph TB\n"
        layers = data.get('layers', [])
        
        for i, layer in enumerate(layers):
            layer_id = f"Layer{i+1}"
            mermaid_code += f"    subgraph {layer_id} [\"{layer['name']}\"]\n"
            for component in layer.get('components', []):
                comp_id = f"{layer_id}_{component.replace(' ', '_')}"
                mermaid_code += f"        {comp_id}[\"{component}\"]\n"
            mermaid_code += "    end\n"
        
        return mermaid_code
    
    def _create_microservices_diagram(self, data: Dict[str, Any]) -> str:
        """Create microservices architecture diagram"""
        mermaid_code = "graph LR\n"
        services = data.get('services', [])
        
        for service in services:
            service_id = service['name'].replace(' ', '_')
            mermaid_code += f"    {service_id}[\"{service['name']}\"]\n"
        
        # Add connections between services
        for connection in data.get('connections', []):
            mermaid_code += f"    {connection['from'].replace(' ', '_')} --> {connection['to'].replace(' ', '_')}\n"
        
        return mermaid_code
    
    def _create_basic_architecture(self, data: Dict[str, Any]) -> str:
        """Create basic architecture diagram"""
        mermaid_code = "graph TD\n"
        components = data.get('components', [])
        
        for component in components:
            comp_id = component['name'].replace(' ', '_')
            mermaid_code += f"    {comp_id}[\"{component['name']}\"]\n"
        
        return mermaid_code


@dataclass 
class GraphvizGenerator:
    """Generator for Graphviz diagrams"""
    
    def generate_network_diagram(self, network_data: Dict[str, Any]) -> str:
        """Generate network diagram in DOT format"""
        dot_code = "digraph NetworkDiagram {\n"
        dot_code += "    rankdir=LR;\n"
        dot_code += "    node [shape=box, style=rounded];\n"
        
        # Add nodes
        for node in network_data.get('nodes', []):
            node_id = node['id']
            label = node.get('label', node_id)
            dot_code += f"    {node_id} [label=\"{label}\"];\n"
        
        # Add edges
        for edge in network_data.get('edges', []):
            from_node = edge['from']
            to_node = edge['to']
            label = edge.get('label', '')
            if label:
                dot_code += f"    {from_node} -> {to_node} [label=\"{label}\"];\n"
            else:
                dot_code += f"    {from_node} -> {to_node};\n"
        
        dot_code += "}\n"
        return dot_code
    
    def generate_hierarchy_diagram(self, hierarchy_data: Dict[str, Any]) -> str:
        """Generate hierarchy diagram in DOT format"""
        dot_code = "digraph HierarchyDiagram {\n"
        dot_code += "    rankdir=TB;\n"
        dot_code += "    node [shape=ellipse];\n"
        
        def add_hierarchy_nodes(parent_id: str, children: List[Dict]):
            for child in children:
                child_id = child['id']
                label = child.get('label', child_id)
                dot_code_local = f"    {child_id} [label=\"{label}\"];\n"
                dot_code_local += f"    {parent_id} -> {child_id};\n"
                
                if 'children' in child:
                    dot_code_local += add_hierarchy_nodes(child_id, child['children'])
                
                return dot_code_local
            return ""
        
        # Add root and hierarchy
        root = hierarchy_data.get('root', {})
        if root:
            root_id = root['id']
            dot_code += f"    {root_id} [label=\"{root.get('label', root_id)}\"];\n"
            if 'children' in root:
                dot_code += add_hierarchy_nodes(root_id, root['children'])
        
        dot_code += "}\n"
        return dot_code


class DiagramGenerator:
    """Main diagram generator class as specified in PRD"""
    
    def __init__(self):
        self.mermaid_generator = MermaidGenerator()
        self.graphviz_generator = GraphvizGenerator()
    
    def generate_flowchart(self, process_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate flowchart from process description"""
        try:
            logger.info(f"Generating flowchart for process: {process_data.get('name', 'Unknown')}")
            
            flowchart_code = self._create_mermaid_flowchart(process_data)
            
            return {
                'type': 'flowchart',
                'code': flowchart_code,
                'format': 'mermaid',
                'title': process_data.get('name', 'Process Flowchart'),
                'description': f"Process flow for {process_data.get('name', 'process')}"
            }
            
        except Exception as e:
            logger.error(f"Error generating flowchart: {e}")
            return {
                'type': 'flowchart',
                'code': 'flowchart TD\n    Error[Error generating flowchart]',
                'format': 'mermaid',
                'title': 'Error',
                'description': 'Failed to generate flowchart'
            }
    
    def _create_mermaid_flowchart(self, process: Dict[str, Any]) -> str:
        """Create Mermaid flowchart syntax"""
        return self.mermaid_generator.generate_flowchart(process)
    
    def generate_architecture_diagram(self, architecture_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate system architecture diagram"""
        try:
            if architecture_data.get('style') == 'layered':
                diagram_code = self._create_layered_architecture(architecture_data)
            elif architecture_data.get('style') == 'microservices':
                diagram_code = self._create_microservices_diagram(architecture_data)
            elif architecture_data.get('style') == 'network':
                diagram_code = self._create_network_diagram(architecture_data)
            else:
                diagram_code = self.mermaid_generator.generate_architecture_diagram(architecture_data)
            
            return {
                'type': 'architecture_diagram',
                'code': diagram_code,
                'format': 'mermaid' if 'graph' in diagram_code else 'graphviz',
                'title': architecture_data.get('name', 'Architecture Diagram'),
                'description': f"Architecture diagram for {architecture_data.get('name', 'system')}"
            }
            
        except Exception as e:
            logger.error(f"Error generating architecture diagram: {e}")
            return {
                'type': 'architecture_diagram',
                'code': 'graph TD\n    Error[Error generating diagram]',
                'format': 'mermaid',
                'title': 'Error',
                'description': 'Failed to generate architecture diagram'
            }
    
    def _create_layered_architecture(self, architecture_data: Dict[str, Any]) -> str:
        """Create layered architecture diagram"""
        return self.mermaid_generator._create_layered_architecture(architecture_data)
    
    def _create_microservices_diagram(self, architecture_data: Dict[str, Any]) -> str:
        """Create microservices diagram"""
        return self.mermaid_generator._create_microservices_diagram(architecture_data)
    
    def _create_network_diagram(self, architecture_data: Dict[str, Any]) -> str:
        """Create network diagram"""
        return self.graphviz_generator.generate_network_diagram(architecture_data)
    
    def generate_decision_tree(self, decision_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate decision tree diagram"""
        try:
            mermaid_code = "flowchart TD\n"
            
            # Add start node
            mermaid_code += "    Start([Start Decision Process])\n"
            
            # Process decision nodes
            for i, decision in enumerate(decision_data.get('decisions', [])):
                node_id = f"Decision{i+1}"
                mermaid_code += f"    {node_id}{{{decision['question']}}}\n"
                
                # Add outcome branches
                for j, outcome in enumerate(decision.get('outcomes', [])):
                    outcome_id = f"{node_id}_Outcome{j+1}"
                    mermaid_code += f"    {outcome_id}[{outcome['result']}]\n"
                    mermaid_code += f"    {node_id} -->|{outcome['condition']}| {outcome_id}\n"
            
            return {
                'type': 'decision_tree',
                'code': mermaid_code,
                'format': 'mermaid',
                'title': decision_data.get('name', 'Decision Tree'),
                'description': f"Decision tree for {decision_data.get('name', 'process')}"
            }
            
        except Exception as e:
            logger.error(f"Error generating decision tree: {e}")
            return {
                'type': 'decision_tree',
                'code': 'flowchart TD\n    Error[Error generating decision tree]',
                'format': 'mermaid',
                'title': 'Error',
                'description': 'Failed to generate decision tree'
            }
    
    def generate_workflow_diagram(self, workflow_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate workflow diagram with swim lanes"""
        try:
            mermaid_code = "flowchart TD\n"
            
            # Add swim lanes
            lanes = workflow_data.get('swim_lanes', [])
            for lane in lanes:
                lane_id = lane['id']
                mermaid_code += f"    subgraph {lane_id} [\"{lane['name']}\"]\n"
                
                for step in lane.get('steps', []):
                    step_id = f"{lane_id}_{step['id']}"
                    mermaid_code += f"        {step_id}[{step['name']}]\n"
                
                mermaid_code += "    end\n"
            
            # Add connections between lanes
            for connection in workflow_data.get('connections', []):
                mermaid_code += f"    {connection['from']} --> {connection['to']}\n"
            
            return {
                'type': 'workflow_diagram',
                'code': mermaid_code,
                'format': 'mermaid',
                'title': workflow_data.get('name', 'Workflow Diagram'),
                'description': f"Workflow diagram for {workflow_data.get('name', 'process')}"
            }
            
        except Exception as e:
            logger.error(f"Error generating workflow diagram: {e}")
            return {
                'type': 'workflow_diagram',
                'code': 'flowchart TD\n    Error[Error generating workflow]',
                'format': 'mermaid',
                'title': 'Error',
                'description': 'Failed to generate workflow diagram'
            }
