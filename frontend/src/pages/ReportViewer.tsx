/**
 * Report Viewer Component
 * Displays interactive enhancement reports
 */
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  Grid,
  Divider,
  Chip,
  Alert,
  CircularProgress,
  IconButton,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Paper,
  List,
  ListItem,
  ListItemText
} from '@mui/material';
import {
  ArrowBack,
  Download,
  Share,
  ExpandMore,
  CheckCircle,
  Warning,
  Info,
  TrendingUp
} from '@mui/icons-material';

// Components
import { DiagramViewer } from '../components/DiagramViewer';
import { AnalysisResults } from '../components/AnalysisResults';

interface ReportData {
  id: string;
  title: string;
  originalUrl: string;
  createdAt: string;
  executiveSummary: {
    overallScore: number;
    keyFindings: string[];
    businessImpact: string[];
    recommendations: string[];
  };
  contentAnalysis: {
    structure: any;
    quality: any;
    modernization: any;
  };
  enhancements: {
    tables: any[];
    diagrams: any[];
    interactions: any[];
  };
  metrics: {
    readabilityScore: number;
    engagementScore: number;
    technicalScore: number;
    improvementPotential: number;
  };
  changeReport: {
    modifications: any[];
    additions: any[];
    recommendations: any[];
  };
}

const ReportViewer: React.FC = () => {
  const { reportId } = useParams<{ reportId: string }>();
  const navigate = useNavigate();
  
  const [reportData, setReportData] = useState<ReportData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (reportId) {
      loadReport(reportId);
    }
  }, [reportId]);

  const loadReport = async (id: string) => {
    try {
      setLoading(true);
      // In a real implementation, this would call the backend API
      // For now, we'll simulate loading report data
      
      // Simulate API delay
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Mock report data
      const mockReport: ReportData = {
        id,
        title: "Enhanced Content Analysis Report",
        originalUrl: "https://example.atlassian.net/wiki/spaces/DEMO/pages/123456",
        createdAt: new Date().toISOString(),
        executiveSummary: {
          overallScore: 85,
          keyFindings: [
            "Content structure shows good organization with clear hierarchies",
            "Technical documentation could benefit from interactive diagrams",
            "Tables require modernization for better readability"
          ],
          businessImpact: [
            "Enhanced readability will improve team productivity by 25%",
            "Interactive elements will reduce support queries by 40%",
            "Modernized structure will accelerate onboarding time"
          ],
          recommendations: [
            "Implement interactive diagrams for complex processes",
            "Modernize table formats with enhanced styling",
            "Add navigation aids and content organization"
          ]
        },
        contentAnalysis: {
          structure: {
            headings: 12,
            paragraphs: 45,
            lists: 8,
            tables: 5
          },
          quality: {
            readability: 78,
            completeness: 82,
            accuracy: 90
          },
          modernization: {
            score: 65,
            areas: ["Tables", "Diagrams", "Navigation"]
          }
        },
        enhancements: {
          tables: [
            { id: '1', type: 'comparison', improvements: 'Enhanced styling and sorting' },
            { id: '2', type: 'data', improvements: 'Added filtering and search' }
          ],
          diagrams: [
            { id: '1', type: 'flowchart', description: 'Process workflow diagram' },
            { id: '2', type: 'architecture', description: 'System architecture overview' }
          ],
          interactions: [
            { id: '1', type: 'collapsible', description: 'Expandable content sections' }
          ]
        },
        metrics: {
          readabilityScore: 78,
          engagementScore: 85,
          technicalScore: 82,
          improvementPotential: 23
        },
        changeReport: {
          modifications: [
            { type: 'table', description: 'Enhanced table formatting and functionality' },
            { type: 'structure', description: 'Improved content organization' }
          ],
          additions: [
            { type: 'diagram', description: 'Added interactive process diagrams' },
            { type: 'navigation', description: 'Added table of contents and quick links' }
          ],
          recommendations: [
            { priority: 'high', description: 'Consider adding video explanations for complex topics' },
            { priority: 'medium', description: 'Implement feedback collection mechanism' }
          ]
        }
      };

      setReportData(mockReport);
    } catch (err: any) {
      setError(err.message || 'Failed to load report');
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadReport = () => {
    // Implementation for downloading report
    console.log('Downloading report...');
  };

  const handleShareReport = () => {
    // Implementation for sharing report
    console.log('Sharing report...');
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="50vh">
        <CircularProgress />
        <Typography variant="h6" sx={{ ml: 2 }}>
          Loading Report...
        </Typography>
      </Box>
    );
  }

  if (error) {
    return (
      <Box p={3}>
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
        <Button variant="contained" onClick={() => navigate('/')}>
          Back to Dashboard
        </Button>
      </Box>
    );
  }

  if (!reportData) {
    return (
      <Box p={3}>
        <Alert severity="warning" sx={{ mb: 2 }}>
          Report not found
        </Alert>
        <Button variant="contained" onClick={() => navigate('/')}>
          Back to Dashboard
        </Button>
      </Box>
    );
  }

  return (
    <Box>
      {/* Header */}
      <Box mb={3} display="flex" alignItems="center" justifyContent="space-between">
        <Box display="flex" alignItems="center">
          <IconButton onClick={() => navigate('/')} sx={{ mr: 2 }}>
            <ArrowBack />
          </IconButton>
          <Typography variant="h4">
            {reportData.title}
          </Typography>
        </Box>
        
        <Box>
          <Button
            variant="outlined"
            startIcon={<Share />}
            onClick={handleShareReport}
            sx={{ mr: 2 }}
          >
            Share
          </Button>
          <Button
            variant="contained"
            startIcon={<Download />}
            onClick={handleDownloadReport}
          >
            Download
          </Button>
        </Box>
      </Box>

      {/* Report Metadata */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Grid container spacing={2}>
            <Grid item xs={12} md={6}>
              <Typography variant="subtitle2" color="text.secondary">
                Original URL
              </Typography>
              <Typography variant="body2">
                {reportData.originalUrl}
              </Typography>
            </Grid>
            <Grid item xs={12} md={6}>
              <Typography variant="subtitle2" color="text.secondary">
                Generated
              </Typography>
              <Typography variant="body2">
                {new Date(reportData.createdAt).toLocaleString()}
              </Typography>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {/* Executive Summary */}
      <Accordion defaultExpanded sx={{ mb: 2 }}>
        <AccordionSummary expandIcon={<ExpandMore />}>
          <Box display="flex" alignItems="center">
            <TrendingUp sx={{ mr: 1, color: 'primary.main' }} />
            <Typography variant="h6">Executive Summary</Typography>
            <Chip
              label={`Score: ${reportData.executiveSummary.overallScore}/100`}
              color="primary"
              size="small"
              sx={{ ml: 2 }}
            />
          </Box>
        </AccordionSummary>
        <AccordionDetails>
          <Grid container spacing={3}>
            <Grid item xs={12} md={4}>
              <Typography variant="subtitle1" gutterBottom>
                Key Findings
              </Typography>
              <List dense>
                {reportData.executiveSummary.keyFindings.map((finding, index) => (
                  <ListItem key={index}>
                    <ListItemText primary={finding} />
                  </ListItem>
                ))}
              </List>
            </Grid>
            <Grid item xs={12} md={4}>
              <Typography variant="subtitle1" gutterBottom>
                Business Impact
              </Typography>
              <List dense>
                {reportData.executiveSummary.businessImpact.map((impact, index) => (
                  <ListItem key={index}>
                    <ListItemText primary={impact} />
                  </ListItem>
                ))}
              </List>
            </Grid>
            <Grid item xs={12} md={4}>
              <Typography variant="subtitle1" gutterBottom>
                Recommendations
              </Typography>
              <List dense>
                {reportData.executiveSummary.recommendations.map((rec, index) => (
                  <ListItem key={index}>
                    <ListItemText primary={rec} />
                  </ListItem>
                ))}
              </List>
            </Grid>
          </Grid>
        </AccordionDetails>
      </Accordion>

      {/* Metrics Overview */}
      <Accordion sx={{ mb: 2 }}>
        <AccordionSummary expandIcon={<ExpandMore />}>
          <Box display="flex" alignItems="center">
            <CheckCircle sx={{ mr: 1, color: 'success.main' }} />
            <Typography variant="h6">Metrics Overview</Typography>
          </Box>
        </AccordionSummary>
        <AccordionDetails>
          <Grid container spacing={3}>
            {Object.entries(reportData.metrics).map(([key, value]) => (
              <Grid item xs={6} md={3} key={key}>
                <Paper sx={{ p: 2, textAlign: 'center' }}>
                  <Typography variant="h4" color="primary">
                    {value}%
                  </Typography>
                  <Typography variant="body2" textTransform="capitalize">
                    {key.replace(/([A-Z])/g, ' $1').trim()}
                  </Typography>
                </Paper>
              </Grid>
            ))}
          </Grid>
        </AccordionDetails>
      </Accordion>

      {/* Content Analysis */}
      <Accordion sx={{ mb: 2 }}>
        <AccordionSummary expandIcon={<ExpandMore />}>
          <Box display="flex" alignItems="center">
            <Info sx={{ mr: 1, color: 'info.main' }} />
            <Typography variant="h6">Content Analysis</Typography>
          </Box>
        </AccordionSummary>
        <AccordionDetails>
          <AnalysisResults data={reportData.contentAnalysis} />
        </AccordionDetails>
      </Accordion>

      {/* Enhancements */}
      <Accordion sx={{ mb: 2 }}>
        <AccordionSummary expandIcon={<ExpandMore />}>
          <Box display="flex" alignItems="center">
            <Warning sx={{ mr: 1, color: 'warning.main' }} />
            <Typography variant="h6">Enhancements Applied</Typography>
          </Box>
        </AccordionSummary>
        <AccordionDetails>
          <Grid container spacing={3}>
            <Grid item xs={12} md={4}>
              <Typography variant="subtitle1" gutterBottom>
                Table Enhancements
              </Typography>
              {reportData.enhancements.tables.map((table) => (
                <Card key={table.id} sx={{ mb: 1 }}>
                  <CardContent>
                    <Typography variant="body2">
                      {table.improvements}
                    </Typography>
                  </CardContent>
                </Card>
              ))}
            </Grid>
            <Grid item xs={12} md={4}>
              <Typography variant="subtitle1" gutterBottom>
                Diagram Enhancements
              </Typography>
              {reportData.enhancements.diagrams.map((diagram) => (
                <Card key={diagram.id} sx={{ mb: 1 }}>
                  <CardContent>
                    <DiagramViewer
                      type={diagram.type}
                      description={diagram.description}
                    />
                  </CardContent>
                </Card>
              ))}
            </Grid>
            <Grid item xs={12} md={4}>
              <Typography variant="subtitle1" gutterBottom>
                Interactive Elements
              </Typography>
              {reportData.enhancements.interactions.map((interaction) => (
                <Card key={interaction.id} sx={{ mb: 1 }}>
                  <CardContent>
                    <Typography variant="body2">
                      {interaction.description}
                    </Typography>
                  </CardContent>
                </Card>
              ))}
            </Grid>
          </Grid>
        </AccordionDetails>
      </Accordion>
    </Box>
  );
};

export default ReportViewer;
