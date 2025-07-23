import React, { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  Typography,
  Button,
  Grid,
  Chip,
  Card,
  CardContent,
  CardActions,
  LinearProgress,
  Alert,
  Tabs,
  Tab,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Switch,
  FormControlLabel,
  FormGroup
} from '@mui/material';
import {
  ExpandMore as ExpandMoreIcon,
  TableChart as TableIcon,
  Timeline as TimelineIcon,
  Update as UpdateIcon,
  Dashboard as DashboardIcon,
  Assessment as AssessmentIcon,
  TrendingUp as TrendingUpIcon,
  Warning as WarningIcon,
  CheckCircle as CheckCircleIcon
} from '@mui/icons-material';

interface EnhancedAnalysisProps {
  confluenceUrl: string;
  onAnalysisComplete: (results: any) => void;
}

interface AnalysisOptions {
  table_analysis: boolean;
  concept_extraction: boolean;
  modernization_analysis: boolean;
  dashboard_generation: boolean;
  diagram_generation: boolean;
}

interface AnalysisResults {
  analysis_id: string;
  content_metadata: any;
  table_analysis?: any;
  concept_analysis?: any;
  modernization_analysis?: any;
  generated_dashboards: any[];
  processing_summary: any;
  recommendations: any[];
}

const EnhancedAnalysisPanel: React.FC<EnhancedAnalysisProps> = ({
  confluenceUrl,
  onAnalysisComplete
}) => {
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisProgress, setAnalysisProgress] = useState(0);
  const [analysisResults, setAnalysisResults] = useState<AnalysisResults | null>(null);
  const [selectedTab, setSelectedTab] = useState(0);
  const [error, setError] = useState<string | null>(null);
  
  const [analysisOptions, setAnalysisOptions] = useState<AnalysisOptions>({
    table_analysis: true,
    concept_extraction: true,
    modernization_analysis: true,
    dashboard_generation: true,
    diagram_generation: true
  });

  const handleAnalysisOptionChange = (option: keyof AnalysisOptions) => {
    setAnalysisOptions(prev => ({
      ...prev,
      [option]: !prev[option]
    }));
  };

  const startEnhancedAnalysis = async () => {
    if (!confluenceUrl) {
      setError('Please provide a Confluence URL');
      return;
    }

    setIsAnalyzing(true);
    setAnalysisProgress(0);
    setError(null);
    
    try {
      // Simulate progress updates
      const progressInterval = setInterval(() => {
        setAnalysisProgress(prev => {
          if (prev >= 90) {
            clearInterval(progressInterval);
            return 90;
          }
          return prev + 10;
        });
      }, 500);

      const response = await fetch('/api/v1/enhanced-analysis/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          confluence_url: confluenceUrl,
          analysis_options: analysisOptions,
          output_format: 'comprehensive'
        }),
      });

      if (!response.ok) {
        throw new Error(`Analysis failed: ${response.statusText}`);
      }

      const results = await response.json();
      
      clearInterval(progressInterval);
      setAnalysisProgress(100);
      setAnalysisResults(results);
      onAnalysisComplete(results);
      
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Analysis failed');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const TabPanel = ({ children, value, index }: any) => (
    <div hidden={value !== index}>
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );

  const renderTableAnalysis = () => {
    const tableAnalysis = analysisResults?.table_analysis;
    if (!tableAnalysis) return null;

    return (
      <Box>
        <Typography variant="h6" gutterBottom>
          Table Analysis Results
        </Typography>
        
        <Grid container spacing={3}>
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Box display="flex" alignItems="center" mb={2}>
                  <TableIcon color="primary" sx={{ mr: 1 }} />
                  <Typography variant="h6">Tables Found</Typography>
                </Box>
                <Typography variant="h3" color="primary">
                  {tableAnalysis.table_count}
                </Typography>
                <Typography variant="body2" color="textSecondary">
                  Data tables identified
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Box display="flex" alignItems="center" mb={2}>
                  <DashboardIcon color="secondary" sx={{ mr: 1 }} />
                  <Typography variant="h6">Dashboards</Typography>
                </Box>
                <Typography variant="h3" color="secondary">
                  {analysisResults?.generated_dashboards.length || 0}
                </Typography>
                <Typography variant="body2" color="textSecondary">
                  Interactive dashboards generated
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Box display="flex" alignItems="center" mb={2}>
                  <AssessmentIcon color="success" sx={{ mr: 1 }} />
                  <Typography variant="h6">Visualization Potential</Typography>
                </Box>
                <Chip 
                  label={tableAnalysis.visualization_potential.toUpperCase()}
                  color={
                    tableAnalysis.visualization_potential === 'high' ? 'success' : 
                    tableAnalysis.visualization_potential === 'medium' ? 'warning' : 'default'
                  }
                  size="large"
                />
              </CardContent>
            </Card>
          </Grid>
        </Grid>

        <Box mt={3}>
          <Typography variant="h6" gutterBottom>
            Generated Dashboards
          </Typography>
          <Grid container spacing={2}>
            {analysisResults?.generated_dashboards.map((dashboard, index) => (
              <Grid item xs={12} md={6} lg={4} key={index}>
                <Card>
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      {dashboard.title}
                    </Typography>
                    <Typography variant="body2" color="textSecondary" paragraph>
                      Charts: {dashboard.charts?.length || 0}
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                      Layout: {dashboard.layout}
                    </Typography>
                  </CardContent>
                  <CardActions>
                    <Button size="small" color="primary">
                      View Dashboard
                    </Button>
                    <Button size="small">
                      Export
                    </Button>
                  </CardActions>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Box>
      </Box>
    );
  };

  const renderConceptAnalysis = () => {
    const conceptAnalysis = analysisResults?.concept_analysis;
    if (!conceptAnalysis) return null;

    return (
      <Box>
        <Typography variant="h6" gutterBottom>
          Concept Extraction Results
        </Typography>
        
        <Grid container spacing={3} mb={3}>
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Box display="flex" alignItems="center" mb={2}>
                  <TimelineIcon color="primary" sx={{ mr: 1 }} />
                  <Typography variant="h6">Concepts Identified</Typography>
                </Box>
                <Typography variant="h3" color="primary">
                  {conceptAnalysis.total_concept_count}
                </Typography>
                <Typography variant="body2" color="textSecondary">
                  Processes, workflows, and concepts
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Box display="flex" alignItems="center" mb={2}>
                  <TrendingUpIcon color="secondary" sx={{ mr: 1 }} />
                  <Typography variant="h6">Diagrams Generated</Typography>
                </Box>
                <Typography variant="h3" color="secondary">
                  {conceptAnalysis.generated_diagrams?.length || 0}
                </Typography>
                <Typography variant="body2" color="textSecondary">
                  Flowcharts and process diagrams
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>

        <Accordion>
          <AccordionSummary expandIcon={<ExpandMoreIcon />}>
            <Typography variant="h6">Identified Concepts</Typography>
          </AccordionSummary>
          <AccordionDetails>
            {Object.entries(conceptAnalysis.identified_concepts).map(([type, concepts]) => (
              <Box key={type} mb={2}>
                <Typography variant="subtitle1" gutterBottom>
                  {type.charAt(0).toUpperCase() + type.slice(1)}
                </Typography>
                <List dense>
                  {(concepts as any[]).map((concept, index) => (
                    <ListItem key={index}>
                      <ListItemIcon>
                        <CheckCircleIcon color="success" />
                      </ListItemIcon>
                      <ListItemText
                        primary={concept.name || `${type} ${index + 1}`}
                        secondary={concept.description || concept.complexity}
                      />
                    </ListItem>
                  ))}
                </List>
              </Box>
            ))}
          </AccordionDetails>
        </Accordion>
      </Box>
    );
  };

  const renderModernizationAnalysis = () => {
    const modernizationAnalysis = analysisResults?.modernization_analysis;
    if (!modernizationAnalysis) return null;

    return (
      <Box>
        <Typography variant="h6" gutterBottom>
          Technology Modernization Analysis
        </Typography>
        
        <Grid container spacing={3} mb={3}>
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Box display="flex" alignItems="center" mb={2}>
                  <UpdateIcon color="warning" sx={{ mr: 1 }} />
                  <Typography variant="h6">Outdated Technologies</Typography>
                </Box>
                <Typography variant="h3" color="warning.main">
                  {modernizationAnalysis.outdated_technologies?.length || 0}
                </Typography>
                <Typography variant="body2" color="textSecondary">
                  Technologies requiring updates
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Box display="flex" alignItems="center" mb={2}>
                  <TrendingUpIcon color="success" sx={{ mr: 1 }} />
                  <Typography variant="h6">Modernization Suggestions</Typography>
                </Box>
                <Typography variant="h3" color="success.main">
                  {modernizationAnalysis.modernization_suggestions?.length || 0}
                </Typography>
                <Typography variant="body2" color="textSecondary">
                  Modern alternatives identified
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>

        {modernizationAnalysis.outdated_technologies?.length > 0 && (
          <Accordion>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <Typography variant="h6">Outdated Technologies</Typography>
            </AccordionSummary>
            <AccordionDetails>
              <List>
                {modernizationAnalysis.outdated_technologies.map((tech: any, index: number) => (
                  <ListItem key={index}>
                    <ListItemIcon>
                      <WarningIcon 
                        color={tech.modernization_urgency === 'critical' ? 'error' : 'warning'} 
                      />
                    </ListItemIcon>
                    <ListItemText
                      primary={tech.technology}
                      secondary={
                        <Box>
                          <Typography variant="body2">
                            Category: {tech.category}
                          </Typography>
                          <Typography variant="body2">
                            Urgency: {tech.modernization_urgency}
                          </Typography>
                          <Typography variant="body2">
                            Migration Effort: {tech.migration_effort}
                          </Typography>
                        </Box>
                      }
                    />
                    <Chip
                      label={tech.modernization_urgency}
                      color={tech.modernization_urgency === 'critical' ? 'error' : 'warning'}
                      size="small"
                    />
                  </ListItem>
                ))}
              </List>
            </AccordionDetails>
          </Accordion>
        )}

        {modernizationAnalysis.implementation_roadmap?.phases && (
          <Accordion>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <Typography variant="h6">Implementation Roadmap</Typography>
            </AccordionSummary>
            <AccordionDetails>
              <Typography variant="body1" gutterBottom>
                Total Timeline: {modernizationAnalysis.implementation_roadmap.total_timeline}
              </Typography>
              <Typography variant="body1" gutterBottom>
                Total Effort: {modernizationAnalysis.implementation_roadmap.total_effort}
              </Typography>
              
              <Box mt={2}>
                {modernizationAnalysis.implementation_roadmap.phases.map((phase: any, index: number) => (
                  <Card key={index} sx={{ mb: 2 }}>
                    <CardContent>
                      <Typography variant="h6">{phase.phase}</Typography>
                      <Typography variant="body2" color="textSecondary">
                        Priority: {phase.priority} | Duration: {phase.duration}
                      </Typography>
                      <Typography variant="body2" mt={1}>
                        Technologies: {phase.technologies.join(', ')}
                      </Typography>
                    </CardContent>
                  </Card>
                ))}
              </Box>
            </AccordionDetails>
          </Accordion>
        )}
      </Box>
    );
  };

  const renderRecommendations = () => {
    const recommendations = analysisResults?.recommendations;
    if (!recommendations || recommendations.length === 0) return null;

    return (
      <Box>
        <Typography variant="h6" gutterBottom>
          Recommendations
        </Typography>
        
        <Grid container spacing={2}>
          {recommendations.map((recommendation, index) => (
            <Grid item xs={12} key={index}>
              <Card>
                <CardContent>
                  <Box display="flex" alignItems="center" mb={2}>
                    <Chip
                      label={recommendation.priority}
                      color={
                        recommendation.priority === 'high' ? 'error' :
                        recommendation.priority === 'medium' ? 'warning' : 'info'
                      }
                      size="small"
                      sx={{ mr: 2 }}
                    />
                    <Typography variant="h6">{recommendation.title}</Typography>
                  </Box>
                  
                  <Typography variant="body1" paragraph>
                    {recommendation.description}
                  </Typography>
                  
                  <Typography variant="body2" color="primary" gutterBottom>
                    <strong>Action:</strong> {recommendation.action}
                  </Typography>
                  
                  <Typography variant="body2" color="success.main">
                    <strong>Benefit:</strong> {recommendation.benefit}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Box>
    );
  };

  return (
    <Paper elevation={3} sx={{ p: 3, mt: 3 }}>
      <Typography variant="h5" gutterBottom>
        Enhanced Content Analysis
      </Typography>
      
      {!analysisResults && (
        <Box>
          <Typography variant="body1" paragraph>
            Configure and run advanced analysis on your Confluence content to generate interactive dashboards, 
            identify concepts for diagramming, and discover modernization opportunities.
          </Typography>
          
          <Box mb={3}>
            <Typography variant="h6" gutterBottom>
              Analysis Options
            </Typography>
            <FormGroup>
              <FormControlLabel
                control={
                  <Switch
                    checked={analysisOptions.table_analysis}
                    onChange={() => handleAnalysisOptionChange('table_analysis')}
                  />
                }
                label="Table Analysis & Dashboard Generation"
              />
              <FormControlLabel
                control={
                  <Switch
                    checked={analysisOptions.concept_extraction}
                    onChange={() => handleAnalysisOptionChange('concept_extraction')}
                  />
                }
                label="Concept Extraction & Diagram Generation"
              />
              <FormControlLabel
                control={
                  <Switch
                    checked={analysisOptions.modernization_analysis}
                    onChange={() => handleAnalysisOptionChange('modernization_analysis')}
                  />
                }
                label="Technology Modernization Analysis"
              />
            </FormGroup>
          </Box>
          
          <Button
            variant="contained"
            color="primary"
            size="large"
            onClick={startEnhancedAnalysis}
            disabled={isAnalyzing || !confluenceUrl}
            sx={{ mr: 2 }}
          >
            {isAnalyzing ? 'Analyzing...' : 'Start Enhanced Analysis'}
          </Button>
          
          {isAnalyzing && (
            <Box mt={2}>
              <Typography variant="body2" gutterBottom>
                Analysis in progress... {analysisProgress}%
              </Typography>
              <LinearProgress variant="determinate" value={analysisProgress} />
            </Box>
          )}
        </Box>
      )}

      {error && (
        <Alert severity="error" sx={{ mt: 2 }}>
          {error}
        </Alert>
      )}

      {analysisResults && (
        <Box mt={3}>
          <Typography variant="h6" gutterBottom>
            Analysis Results
          </Typography>
          
          <Alert severity="success" sx={{ mb: 3 }}>
            Enhanced analysis completed successfully! 
            Analysis ID: {analysisResults.analysis_id}
          </Alert>
          
          <Tabs value={selectedTab} onChange={(_, newValue) => setSelectedTab(newValue)}>
            <Tab label="Table Analysis" />
            <Tab label="Concept Extraction" />
            <Tab label="Modernization" />
            <Tab label="Recommendations" />
          </Tabs>
          
          <TabPanel value={selectedTab} index={0}>
            {renderTableAnalysis()}
          </TabPanel>
          
          <TabPanel value={selectedTab} index={1}>
            {renderConceptAnalysis()}
          </TabPanel>
          
          <TabPanel value={selectedTab} index={2}>
            {renderModernizationAnalysis()}
          </TabPanel>
          
          <TabPanel value={selectedTab} index={3}>
            {renderRecommendations()}
          </TabPanel>
        </Box>
      )}
    </Paper>
  );
};

export default EnhancedAnalysisPanel;
