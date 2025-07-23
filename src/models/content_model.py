"""
Data models for content storage and processing
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field
from enum import Enum


class ContentStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class ContentModel(BaseModel):
    """Model for Confluence content"""
    content_id: Optional[str] = None
    page_url: str
    title: str
    raw_html: str
    raw_text: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    status: ContentStatus = ContentStatus.PENDING
    created_date: Optional[datetime] = None
    updated_date: Optional[datetime] = None
    version_number: int = 1
    
    class Config:
        from_attributes = True


class TableData(BaseModel):
    """Model for table data extraction"""
    table_id: Optional[str] = None
    headers: List[str]
    rows: List[List[str]]
    data_types: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ProcessStep(BaseModel):
    """Model for process steps"""
    step_id: str
    description: str
    step_type: str  # 'process', 'decision', 'data', 'start', 'end'
    inputs: List[str] = Field(default_factory=list)
    outputs: List[str] = Field(default_factory=list)


class ProcessConnection(BaseModel):
    """Model for process connections"""
    from_step: str
    to_step: str
    label: Optional[str] = None
    condition: Optional[str] = None


class ProcessData(BaseModel):
    """Model for process/workflow data"""
    process_id: Optional[str] = None
    name: str
    description: str
    process_type: str  # 'linear_process', 'decision_tree', 'workflow'
    steps: List[ProcessStep]
    connections: List[ProcessConnection]
    metadata: Dict[str, Any] = Field(default_factory=dict)


class AnalysisResult(BaseModel):
    """Model for content analysis results"""
    analysis_id: Optional[str] = None
    content_id: str
    analysis_type: str
    results: Dict[str, Any]
    confidence_score: float = Field(ge=0.0, le=1.0)
    created_date: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class EnhancementSuggestion(BaseModel):
    """Model for content enhancement suggestions"""
    suggestion_id: Optional[str] = None
    content_id: str
    suggestion_type: str
    title: str
    description: str
    implementation_guide: str
    priority: str  # 'high', 'medium', 'low'
    effort_estimate: str
    benefits: List[str] = Field(default_factory=list)
    
    class Config:
        from_attributes = True
