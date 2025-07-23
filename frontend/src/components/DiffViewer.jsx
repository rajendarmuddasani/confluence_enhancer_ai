import React, { useState, useEffect } from 'react';
import './DiffViewer.css';

const DiffViewer = ({ originalContent, enhancedContent, diffAnalysis }) => {
    const [viewMode, setViewMode] = useState('side-by-side'); // 'side-by-side', 'unified', 'slider'
    const [selectedSection, setSelectedSection] = useState('all');
    const [showMetrics, setShowMetrics] = useState(true);

    const renderSideBySideView = () => (
        <div className="diff-side-by-side">
            <div className="diff-panel original">
                <div className="diff-panel-header">
                    <h3>Original Content</h3>
                    <span className="word-count">
                        {diffAnalysis?.metadata?.original_word_count || 0} words
                    </span>
                </div>
                <div className="diff-content">
                    {renderContentSections(originalContent, 'original')}
                </div>
            </div>
            
            <div className="diff-panel enhanced">
                <div className="diff-panel-header">
                    <h3>AI Enhanced Content</h3>
                    <span className="word-count">
                        {diffAnalysis?.metadata?.enhanced_word_count || 0} words
                    </span>
                </div>
                <div className="diff-content">
                    {renderContentSections(enhancedContent, 'enhanced')}
                </div>
            </div>
        </div>
    );

    const renderSliderView = () => {
        const [sliderValue, setSliderValue] = useState(50);
        
        return (
            <div className="diff-slider-container">
                <div className="slider-controls">
                    <span>Original</span>
                    <input
                        type="range"
                        min="0"
                        max="100"
                        value={sliderValue}
                        onChange={(e) => setSliderValue(e.target.value)}
                        className="diff-slider"
                    />
                    <span>Enhanced</span>
                </div>
                
                <div 
                    className="diff-slider-view"
                    style={{
                        background: `linear-gradient(to right, 
                            rgba(255,200,200,${(100-sliderValue)/100}) 0%, 
                            rgba(255,200,200,${(100-sliderValue)/100}) ${sliderValue}%, 
                            rgba(200,255,200,${sliderValue/100}) ${sliderValue}%, 
                            rgba(200,255,200,${sliderValue/100}) 100%)`
                    }}
                >
                    <div 
                        className="content-overlay original"
                        style={{ opacity: (100 - sliderValue) / 100 }}
                    >
                        {renderContentSections(originalContent, 'original')}
                    </div>
                    <div 
                        className="content-overlay enhanced"
                        style={{ opacity: sliderValue / 100 }}
                    >
                        {renderContentSections(enhancedContent, 'enhanced')}
                    </div>
                </div>
            </div>
        );
    };

    const renderUnifiedView = () => (
        <div className="diff-unified">
            {diffAnalysis?.sections?.map((section, index) => (
                <div key={index} className={`diff-section ${section.type}`}>
                    <div className="section-header">
                        <h4>{section.name}</h4>
                        <span className={`change-badge ${section.type}`}>
                            {section.type.toUpperCase()}
                        </span>
                    </div>
                    <div 
                        className="section-diff"
                        dangerouslySetInnerHTML={{ __html: section.diff_html }}
                    />
                </div>
            ))}
        </div>
    );

    const renderContentSections = (content, type) => {
        if (!content || !content.sections) {
            return <div className="no-content">No content available</div>;
        }

        return content.sections.map((section, index) => (
            <div key={index} className={`content-section ${type}`}>
                <h4 className="section-title">{section.title || `Section ${index + 1}`}</h4>
                <div className="section-content">
                    {section.content}
                </div>
                {section.visualizations && (
                    <div className="section-visualizations">
                        <h5>Visualizations Added:</h5>
                        {section.visualizations.map((viz, vizIndex) => (
                            <div key={vizIndex} className="visualization-item">
                                <span className="viz-type">{viz.type}</span>
                                <span className="viz-title">{viz.title}</span>
                            </div>
                        ))}
                    </div>
                )}
            </div>
        ));
    };

    const renderMetrics = () => (
        <div className="diff-metrics">
            <div className="metrics-header">
                <h3>Enhancement Metrics</h3>
                <button 
                    className="toggle-metrics"
                    onClick={() => setShowMetrics(!showMetrics)}
                >
                    {showMetrics ? 'Hide' : 'Show'} Metrics
                </button>
            </div>
            
            {showMetrics && (
                <div className="metrics-content">
                    <div className="metric-row">
                        <div className="metric-item">
                            <span className="metric-label">Total Changes</span>
                            <span className="metric-value">{diffAnalysis?.summary?.metrics?.['Total Changes'] || 0}</span>
                        </div>
                        <div className="metric-item">
                            <span className="metric-label">Content Additions</span>
                            <span className="metric-value">{diffAnalysis?.summary?.metrics?.['Content Additions'] || 0}</span>
                        </div>
                        <div className="metric-item">
                            <span className="metric-label">Visualizations Added</span>
                            <span className="metric-value">{diffAnalysis?.summary?.metrics?.['Visualizations Added'] || 0}</span>
                        </div>
                        <div className="metric-item">
                            <span className="metric-label">Readability Improvement</span>
                            <span className="metric-value">{diffAnalysis?.summary?.metrics?.['Readability Improvement'] || '0%'}</span>
                        </div>
                    </div>
                    
                    <div className="improvement-score">
                        <div className="score-label">Overall Improvement Score</div>
                        <div className="score-bar">
                            <div 
                                className="score-fill"
                                style={{ 
                                    width: `${diffAnalysis?.summary?.improvement_score || 0}%`,
                                    backgroundColor: getScoreColor(diffAnalysis?.summary?.improvement_score || 0)
                                }}
                            />
                        </div>
                        <div className="score-value">
                            {diffAnalysis?.summary?.improvement_score?.toFixed(1) || '0.0'}/100
                        </div>
                    </div>
                </div>
            )}
        </div>
    );

    const getScoreColor = (score) => {
        if (score >= 80) return '#4CAF50'; // Green
        if (score >= 60) return '#FF9800'; // Orange
        if (score >= 40) return '#FFC107'; // Yellow
        return '#F44336'; // Red
    };

    const renderSectionFilter = () => {
        const sections = diffAnalysis?.sections || [];
        
        return (
            <div className="section-filter">
                <label htmlFor="section-select">Filter by section:</label>
                <select 
                    id="section-select"
                    value={selectedSection}
                    onChange={(e) => setSelectedSection(e.target.value)}
                >
                    <option value="all">All Sections</option>
                    {sections.map((section, index) => (
                        <option key={index} value={section.name}>
                            {section.name} ({section.type})
                        </option>
                    ))}
                </select>
            </div>
        );
    };

    return (
        <div className="diff-viewer">
            <div className="diff-header">
                <h2>Content Enhancement Comparison</h2>
                
                <div className="diff-controls">
                    <div className="view-mode-selector">
                        <button 
                            className={viewMode === 'side-by-side' ? 'active' : ''}
                            onClick={() => setViewMode('side-by-side')}
                        >
                            Side by Side
                        </button>
                        <button 
                            className={viewMode === 'slider' ? 'active' : ''}
                            onClick={() => setViewMode('slider')}
                        >
                            Before/After Slider
                        </button>
                        <button 
                            className={viewMode === 'unified' ? 'active' : ''}
                            onClick={() => setViewMode('unified')}
                        >
                            Unified Diff
                        </button>
                    </div>
                    
                    {renderSectionFilter()}
                </div>
            </div>

            {renderMetrics()}

            <div className="diff-body">
                {viewMode === 'side-by-side' && renderSideBySideView()}
                {viewMode === 'slider' && renderSliderView()}
                {viewMode === 'unified' && renderUnifiedView()}
            </div>

            <div className="diff-footer">
                <div className="enhancement-summary">
                    <p>{diffAnalysis?.summary?.overview || 'Enhancement analysis completed.'}</p>
                </div>
            </div>
        </div>
    );
};

export default DiffViewer;
