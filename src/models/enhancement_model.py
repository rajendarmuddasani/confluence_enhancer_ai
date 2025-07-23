"""
Data models for enhancement tracking
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field
from enum import Enum


class EnhancementType(str, Enum):
    CONTENT_RESTRUCTURE = "content_restructure"
    VISUALIZATION_ADDED = "visualization_added"
    TECHNOLOGY_MODERNIZATION = "technology_modernization"
    PROCESS_DIAGRAM = "process_diagram"
    LINK_VALIDATION = "link_validation"
    CONTENT_OPTIMIZATION = "content_optimization"


class ModernizationUrgency(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class TechnologyCategory(str, Enum):
    PROGRAMMING_LANGUAGE = "programming_language"
    FRAMEWORK = "framework"
    DATABASE = "database"
    TOOL = "tool"
    INFRASTRUCTURE = "infrastructure"
    LIBRARY = "library"


class OutdatedTechnology(BaseModel):
    """Model for outdated technology detection"""
    technology: str
    category: TechnologyCategory
    version: Optional[str] = None
    found_context: str
    urgency: ModernizationUrgency
    end_of_life_date: Optional[datetime] = None


class ModernAlternative(BaseModel):
    """Model for modern technology alternatives"""
    technology: str
    version: str
    category: TechnologyCategory
    benefits: List[str]
    migration_effort: str  # 'low', 'medium', 'high'
    implementation_guide: str
    learning_curve: str  # 'easy', 'moderate', 'steep'
    cost_impact: str  # 'none', 'low', 'medium', 'high'


class ModernizationSuggestion(BaseModel):
    """Model for modernization suggestions"""
    suggestion_id: Optional[str] = None
    content_id: str
    outdated_tech: OutdatedTechnology
    modern_alternative: ModernAlternative
    justification: str
    implementation_steps: List[str]
    estimated_timeline: str
    resource_requirements: Dict[str, Any] = Field(default_factory=dict)
    risk_assessment: Dict[str, Any] = Field(default_factory=dict)
    created_date: Optional[datetime] = None


class EnhancementMetrics(BaseModel):
    """Model for tracking enhancement metrics"""
    content_id: str
    original_word_count: int
    enhanced_word_count: int
    tables_found: int
    visualizations_created: int
    processes_identified: int
    diagrams_created: int
    outdated_technologies: int
    modernization_suggestions: int
    broken_links_found: int
    links_fixed: int
    readability_score_before: float
    readability_score_after: float
    enhancement_score: float  # Overall enhancement score


class EnhancementModel(BaseModel):
    """Model for content enhancement tracking"""
    enhancement_id: Optional[str] = None
    content_id: str
    enhancement_type: EnhancementType
    title: str
    description: str
    before_content: Optional[str] = None
    after_content: Optional[str] = None
    changes_summary: List[str] = Field(default_factory=list)
    metrics: Optional[EnhancementMetrics] = None
    status: str = "completed"
    created_date: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class RoadmapPhase(BaseModel):
    """Model for modernization roadmap phases"""
    phase_name: str
    duration: str
    technologies: List[ModernizationSuggestion]
    priority: str  # 'high', 'medium', 'low'
    dependencies: List[str] = Field(default_factory=list)
    resources_needed: Dict[str, Any] = Field(default_factory=dict)


class ModernizationRoadmap(BaseModel):
    """Model for technology modernization roadmap"""
    roadmap_id: Optional[str] = None
    content_id: str
    title: str
    description: str
    phases: List[RoadmapPhase]
    total_timeline: str
    total_cost_estimate: Optional[str] = None
    risk_level: str  # 'low', 'medium', 'high'
    success_criteria: List[str] = Field(default_factory=list)
    created_date: Optional[datetime] = None
    
    class Config:
        from_attributes = True
