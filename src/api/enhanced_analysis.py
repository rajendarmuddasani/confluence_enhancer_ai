"""
Enhanced Content Analysis API
Advanced content processing with table analysis, concept extraction, and modernization capabilities.
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
import logging
from datetime import datetime

from ..processors.table_processor import TableProcessor
from ..processors.concept_processor_enhanced import ConceptProcessor
from ..processors.data_extractor import DataExtractor
from ..visualizations.dashboard_generator import DashboardGenerator
from ..modernization.modernization_engine import ModernizationEngine
from ..api.confluence_client import ConfluenceClient
from ..ai_engine.content_analyzer import ContentAnalyzer

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/enhanced-analysis", tags=["Enhanced Analysis"])

# Request/Response Models
class EnhancedAnalysisRequest(BaseModel):
    confluence_url: str
    analysis_options: Dict[str, bool] = {
        "table_analysis": True,
        "concept_extraction": True,
        "modernization_analysis": True,
        "dashboard_generation": True,
        "diagram_generation": True
    }
    output_format: str = "comprehensive"  # comprehensive, summary, technical

class TableAnalysisResult(BaseModel):
    table_count: int
    processed_tables: List[Dict[str, Any]]
    dashboard_suggestions: List[Dict[str, Any]]
    visualization_potential: str

class ConceptAnalysisResult(BaseModel):
    identified_concepts: Dict[str, List[Dict[str, Any]]]
    total_concept_count: int
    diagram_suggestions: List[Dict[str, Any]]
    generated_diagrams: List[Dict[str, Any]]

class ModernizationAnalysisResult(BaseModel):
    outdated_technologies: List[Dict[str, Any]]
    modernization_suggestions: List[Dict[str, Any]]
    implementation_roadmap: Dict[str, Any]
    risk_assessment: Dict[str, Any]

class EnhancedAnalysisResponse(BaseModel):
    analysis_id: str
    content_metadata: Dict[str, Any]
    table_analysis: Optional[TableAnalysisResult]
    concept_analysis: Optional[ConceptAnalysisResult]
    modernization_analysis: Optional[ModernizationAnalysisResult]
    generated_dashboards: List[Dict[str, Any]]
    processing_summary: Dict[str, Any]
    recommendations: List[Dict[str, Any]]

# Initialize processors
table_processor = TableProcessor()
concept_processor = ConceptProcessor()
data_extractor = DataExtractor()
dashboard_generator = DashboardGenerator()
modernization_engine = ModernizationEngine()
confluence_client = ConfluenceClient()
content_analyzer = ContentAnalyzer()

@router.post("/analyze", response_model=EnhancedAnalysisResponse)
async def enhanced_content_analysis(
    request: EnhancedAnalysisRequest,
    background_tasks: BackgroundTasks
):
    """
    Perform comprehensive enhanced analysis of Confluence content.
    Includes table analysis, concept extraction, modernization suggestions, and visualization generation.
    """
    try:
        analysis_id = f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        logger.info(f"Starting enhanced analysis {analysis_id} for URL: {request.confluence_url}")
        
        # Step 1: Extract content from Confluence
        logger.info("Extracting content from Confluence...")
        content_data = await _extract_confluence_content(request.confluence_url)
        
        if not content_data:
            raise HTTPException(status_code=404, detail="Could not extract content from Confluence URL")
        
        # Initialize response components
        response_data = {
            'analysis_id': analysis_id,
            'content_metadata': {
                'title': content_data.get('title', 'Unknown'),
                'url': request.confluence_url,
                'content_length': len(content_data.get('raw_text', '')),
                'analysis_timestamp': datetime.now().isoformat(),
                'analysis_options': request.analysis_options
            },
            'table_analysis': None,
            'concept_analysis': None,
            'modernization_analysis': None,
            'generated_dashboards': [],
            'processing_summary': {},
            'recommendations': []
        }
        
        # Step 2: Table Analysis and Dashboard Generation
        if request.analysis_options.get("table_analysis", True):
            logger.info("Performing table analysis...")
            table_results = await _perform_table_analysis(content_data)
            response_data['table_analysis'] = table_results
            
            # Generate dashboards if requested
            if request.analysis_options.get("dashboard_generation", True) and table_results['processed_tables']:
                logger.info("Generating interactive dashboards...")
                dashboards = await _generate_dashboards(table_results['processed_tables'])
                response_data['generated_dashboards'] = dashboards
        
        # Step 3: Concept Extraction and Diagram Generation
        if request.analysis_options.get("concept_extraction", True):
            logger.info("Performing concept extraction...")
            concept_results = await _perform_concept_analysis(content_data)
            response_data['concept_analysis'] = concept_results
        
        # Step 4: Modernization Analysis
        if request.analysis_options.get("modernization_analysis", True):
            logger.info("Performing modernization analysis...")
            modernization_results = await _perform_modernization_analysis(content_data)
            response_data['modernization_analysis'] = modernization_results
        
        # Step 5: Generate Processing Summary and Recommendations
        logger.info("Generating summary and recommendations...")
        response_data['processing_summary'] = _generate_processing_summary(response_data)
        response_data['recommendations'] = _generate_comprehensive_recommendations(response_data)
        
        # Schedule background tasks for additional processing
        background_tasks.add_task(_post_process_analysis, analysis_id, response_data)
        
        logger.info(f"Enhanced analysis {analysis_id} completed successfully")
        return EnhancedAnalysisResponse(**response_data)
        
    except Exception as e:
        logger.error(f"Error in enhanced analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

async def _extract_confluence_content(confluence_url: str) -> Optional[Dict[str, Any]]:
    """Extract content from Confluence URL."""
    try:
        # Extract content using the confluence client
        content_data = confluence_client.extract_content(confluence_url)
        
        if not content_data:
            return None
        
        # Parse the content for enhanced analysis
        parsed_content = content_analyzer.parse_content(content_data)
        
        return {
            'title': parsed_content.get('title', ''),
            'raw_text': parsed_content.get('content', ''),
            'html_content': parsed_content.get('html', ''),
            'metadata': parsed_content.get('metadata', {}),
            'soup': parsed_content.get('soup')  # BeautifulSoup object for table extraction
        }
        
    except Exception as e:
        logger.error(f"Error extracting Confluence content: {str(e)}")
        return None

async def _perform_table_analysis(content_data: Dict[str, Any]) -> Dict[str, Any]:
    """Perform comprehensive table analysis."""
    try:
        soup = content_data.get('soup')
        if not soup:
            return {'table_count': 0, 'processed_tables': [], 'dashboard_suggestions': [], 'visualization_potential': 'none'}
        
        # Extract and analyze tables
        processed_tables = table_processor.extract_and_analyze_tables(soup)
        
        # Generate dashboard suggestions
        dashboard_suggestions = []
        total_visualization_potential = 'low'
        
        for table_data in processed_tables:
            if table_data.get('valid', False):
                table_suggestions = table_data.get('visualization_suggestions', [])
                dashboard_suggestions.extend(table_suggestions)
                
                # Update overall visualization potential
                table_potential = table_data.get('analysis', {}).get('visualization_potential', 'low')
                if table_potential == 'high':
                    total_visualization_potential = 'high'
                elif table_potential == 'medium' and total_visualization_potential != 'high':
                    total_visualization_potential = 'medium'
        
        return {
            'table_count': len(processed_tables),
            'processed_tables': processed_tables,
            'dashboard_suggestions': dashboard_suggestions,
            'visualization_potential': total_visualization_potential
        }
        
    except Exception as e:
        logger.error(f"Error in table analysis: {str(e)}")
        return {'table_count': 0, 'processed_tables': [], 'dashboard_suggestions': [], 'visualization_potential': 'error'}

async def _perform_concept_analysis(content_data: Dict[str, Any]) -> Dict[str, Any]:
    """Perform concept extraction and diagram generation."""
    try:
        # Identify concepts and processes
        concept_results = concept_processor.identify_concepts_and_processes(content_data)
        
        # Generate diagrams for identified processes
        generated_diagrams = []
        identified_concepts = concept_results.get('identified_concepts', {})
        
        if 'processes' in identified_concepts:
            processes = identified_concepts['processes']
            diagrams = concept_processor.generate_process_diagrams(processes)
            generated_diagrams.extend(diagrams)
        
        return {
            'identified_concepts': identified_concepts,
            'total_concept_count': concept_results.get('total_count', 0),
            'diagram_suggestions': concept_results.get('diagram_suggestions', []),
            'generated_diagrams': generated_diagrams
        }
        
    except Exception as e:
        logger.error(f"Error in concept analysis: {str(e)}")
        return {
            'identified_concepts': {},
            'total_concept_count': 0,
            'diagram_suggestions': [],
            'generated_diagrams': []
        }

async def _perform_modernization_analysis(content_data: Dict[str, Any]) -> Dict[str, Any]:
    """Perform technology modernization analysis."""
    try:
        # Analyze content for modernization opportunities
        modernization_results = modernization_engine.analyze_and_modernize_content(content_data)
        
        return {
            'outdated_technologies': modernization_results.get('outdated_technologies', []),
            'modernization_suggestions': modernization_results.get('modernization_suggestions', []),
            'implementation_roadmap': modernization_results.get('modernization_roadmap', {}),
            'risk_assessment': modernization_results.get('risk_assessment', {})
        }
        
    except Exception as e:
        logger.error(f"Error in modernization analysis: {str(e)}")
        return {
            'outdated_technologies': [],
            'modernization_suggestions': [],
            'implementation_roadmap': {},
            'risk_assessment': {}
        }

async def _generate_dashboards(processed_tables: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Generate interactive dashboards from processed tables."""
    dashboards = []
    
    try:
        for i, table_data in enumerate(processed_tables):
            if not table_data.get('valid', False):
                continue
            
            visualization_suggestions = table_data.get('visualization_suggestions', [])
            if not visualization_suggestions:
                continue
            
            # Create dashboard
            dashboard = dashboard_generator.create_interactive_dashboard(
                table_data, visualization_suggestions
            )
            
            if dashboard and 'error' not in dashboard:
                dashboard['table_index'] = i
                dashboard['source_table'] = table_data.get('headers', [])
                dashboards.append(dashboard)
        
        return dashboards
        
    except Exception as e:
        logger.error(f"Error generating dashboards: {str(e)}")
        return []

def _generate_processing_summary(response_data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate processing summary statistics."""
    summary = {
        'total_processing_time': 'calculated_in_background',
        'content_analysis': {
            'content_length': response_data['content_metadata']['content_length'],
            'analysis_completeness': 'full'
        },
        'table_processing': {
            'tables_found': 0,
            'tables_processed': 0,
            'dashboards_generated': len(response_data['generated_dashboards'])
        },
        'concept_extraction': {
            'concepts_identified': 0,
            'diagrams_generated': 0
        },
        'modernization_analysis': {
            'outdated_technologies_found': 0,
            'suggestions_generated': 0
        }
    }
    
    # Update table processing stats
    if response_data['table_analysis']:
        summary['table_processing']['tables_found'] = response_data['table_analysis']['table_count']
        summary['table_processing']['tables_processed'] = len(response_data['table_analysis']['processed_tables'])
    
    # Update concept extraction stats
    if response_data['concept_analysis']:
        summary['concept_extraction']['concepts_identified'] = response_data['concept_analysis']['total_concept_count']
        summary['concept_extraction']['diagrams_generated'] = len(response_data['concept_analysis']['generated_diagrams'])
    
    # Update modernization stats
    if response_data['modernization_analysis']:
        summary['modernization_analysis']['outdated_technologies_found'] = len(response_data['modernization_analysis']['outdated_technologies'])
        summary['modernization_analysis']['suggestions_generated'] = len(response_data['modernization_analysis']['modernization_suggestions'])
    
    return summary

def _generate_comprehensive_recommendations(response_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Generate comprehensive recommendations based on analysis results."""
    recommendations = []
    
    # Dashboard recommendations
    if response_data['generated_dashboards']:
        recommendations.append({
            'type': 'visualization',
            'priority': 'high',
            'title': 'Interactive Dashboards Available',
            'description': f"Generated {len(response_data['generated_dashboards'])} interactive dashboards from your table data.",
            'action': 'Review and embed dashboards into your Confluence page for better data presentation.',
            'benefit': 'Improved data visualization and user engagement'
        })
    
    # Concept diagram recommendations
    if response_data['concept_analysis'] and response_data['concept_analysis']['generated_diagrams']:
        diagram_count = len(response_data['concept_analysis']['generated_diagrams'])
        recommendations.append({
            'type': 'documentation',
            'priority': 'medium',
            'title': 'Process Diagrams Generated',
            'description': f"Identified {diagram_count} processes that can be visualized as flowcharts.",
            'action': 'Add generated flowcharts to improve process documentation clarity.',
            'benefit': 'Enhanced process understanding and documentation quality'
        })
    
    # Modernization recommendations
    if response_data['modernization_analysis'] and response_data['modernization_analysis']['outdated_technologies']:
        tech_count = len(response_data['modernization_analysis']['outdated_technologies'])
        recommendations.append({
            'type': 'modernization',
            'priority': 'high' if tech_count > 3 else 'medium',
            'title': 'Technology Modernization Opportunities',
            'description': f"Found {tech_count} outdated technologies that should be modernized.",
            'action': 'Review modernization roadmap and plan technology updates.',
            'benefit': 'Improved security, performance, and maintainability'
        })
    
    # Content enhancement recommendations
    table_potential = 'none'
    if response_data['table_analysis']:
        table_potential = response_data['table_analysis']['visualization_potential']
    
    if table_potential in ['medium', 'high']:
        recommendations.append({
            'type': 'content_enhancement',
            'priority': 'medium',
            'title': 'Content Enhancement Opportunities',
            'description': f"Your content has {table_potential} potential for interactive enhancements.",
            'action': 'Consider adding more interactive elements and visualizations.',
            'benefit': 'Better user experience and information accessibility'
        })
    
    return recommendations

async def _post_process_analysis(analysis_id: str, response_data: Dict[str, Any]):
    """Background task for additional processing and optimization."""
    try:
        logger.info(f"Starting post-processing for analysis {analysis_id}")
        
        # Additional processing can be added here:
        # - Generate additional visualizations
        # - Perform deeper content analysis
        # - Create optimization suggestions
        # - Generate export formats
        
        logger.info(f"Post-processing completed for analysis {analysis_id}")
        
    except Exception as e:
        logger.error(f"Error in post-processing for {analysis_id}: {str(e)}")

@router.get("/analysis/{analysis_id}/status")
async def get_analysis_status(analysis_id: str):
    """Get the status of an analysis job."""
    # This would typically check a database or cache for job status
    return {
        'analysis_id': analysis_id,
        'status': 'completed',  # completed, processing, failed
        'progress': 100,
        'message': 'Analysis completed successfully'
    }

@router.get("/capabilities")
async def get_analysis_capabilities():
    """Get information about available analysis capabilities."""
    return {
        'table_analysis': {
            'description': 'Extract and analyze table data for visualization opportunities',
            'features': ['Data type detection', 'Pattern identification', 'Visualization suggestions', 'Dashboard generation']
        },
        'concept_extraction': {
            'description': 'Identify concepts and processes suitable for diagramming',
            'features': ['Process identification', 'Workflow extraction', 'Flowchart generation', 'Architecture diagrams']
        },
        'modernization_analysis': {
            'description': 'Analyze content for technology modernization opportunities',
            'features': ['Outdated technology detection', 'Modern alternatives', 'Implementation roadmaps', 'Risk assessment']
        },
        'dashboard_generation': {
            'description': 'Create interactive dashboards from data',
            'features': ['Multiple chart types', 'Interactive filters', 'Real-time updates', 'Export capabilities']
        }
    }
