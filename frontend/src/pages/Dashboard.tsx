/**
 * Enhanced Main Dashboard Component - Phase 4
 */
import React, { useState, useEffect } from 'react';
import {
  Container,
  Box,
  Tabs,
  Tab,
  Alert,
  CircularProgress,
  Card,
  CardContent,
  Typography,
  Grid,
  LinearProgress,
  Paper,
  Button
} from '@mui/material';
import ContentInput from '../components/ContentInput';
import TestExtraction from '../components/TestExtraction';
import { AnalysisResults } from '../components/AnalysisResults';
import { InteractiveDashboard } from '../components/InteractiveDashboard';
import { DiagramViewer } from '../components/DiagramViewer';
import { ModernizationPlanner } from '../components/ModernizationPlanner';
import EnhancementPreview from '../components/EnhancementPreview';
import ChangeReport from '../components/ChangeReport';
import { healthAPI } from '../services/api';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}

interface ProcessingState {
  isProcessing: boolean;
  currentPhase: string;
  progress: number;
  results?: any;
  error?: string;
}

interface DashboardProps {
  processingState: ProcessingState;
  enhancementResults: any;
  onUrlSubmit: (url: string) => Promise<void>;
  onPageCreation: (enhancementData: any) => Promise<void>;
}

const Dashboard: React.FC<DashboardProps> = ({
  processingState,
  enhancementResults,
  onUrlSubmit,
  onPageCreation
}) => {
  const [tabValue, setTabValue] = useState(0);
  const [backendHealth, setBackendHealth] = useState<'unknown' | 'healthy' | 'error'>('unknown');

  // Debug logging
  useEffect(() => {
    console.log('Dashboard received enhancementResults:', enhancementResults);
  }, [enhancementResults]);

  // Check backend health on component mount
  useEffect(() => {
    const checkHealth = async () => {
      try {
        await healthAPI.check();
        setBackendHealth('healthy');
        console.log('Backend health check passed');
      } catch (error) {
        console.error('Backend health check failed:', error);
        // Retry health check after a short delay
        setTimeout(async () => {
          try {
            await healthAPI.check();
            setBackendHealth('healthy');
            console.log('Backend health check passed on retry');
          } catch (retryError) {
            setBackendHealth('error');
            console.error('Backend health check failed on retry:', retryError);
          }
        }, 2000);
      }
    };

    checkHealth();
  }, []);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const renderProcessingStatus = () => {
    if (!processingState.isProcessing && !processingState.results && !processingState.error) {
      return null;
    }

    return (
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Processing Status
          </Typography>
          
          {processingState.isProcessing && (
            <Box>
              <Typography variant="body2" color="text.secondary" gutterBottom>
                {processingState.currentPhase}
              </Typography>
              <LinearProgress
                variant="determinate"
                value={processingState.progress}
                sx={{ mb: 1 }}
              />
              <Typography variant="caption" color="text.secondary">
                {processingState.progress}% Complete
              </Typography>
            </Box>
          )}

          {processingState.error && (
            <Alert severity="error">
              {processingState.error}
            </Alert>
          )}

          {processingState.results && !processingState.isProcessing && (
            <Alert severity="success">
              Processing completed successfully!
            </Alert>
          )}
        </CardContent>
      </Card>
    );
  };

  const renderHealthStatus = () => (
    <Box sx={{ mb: 2 }}>
      {backendHealth === 'healthy' && (
        <Alert severity="success">
          Backend service is healthy and ready
        </Alert>
      )}
      {backendHealth === 'error' && (
        <Alert severity="error">
          Backend service is unavailable. Please check your connection.
        </Alert>
      )}
      {backendHealth === 'unknown' && (
        <Alert severity="info">
          Checking backend service...
        </Alert>
      )}
    </Box>
  );

  return (
    <Container maxWidth="xl">
      <Box sx={{ py: 3 }}>
        <Typography variant="h4" gutterBottom>
          Confluence Content Intelligence Dashboard
        </Typography>
        
        {renderHealthStatus()}
        {renderProcessingStatus()}

        <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
          <Tabs value={tabValue} onChange={handleTabChange}>
            <Tab label="Content Input" />
            <Tab label={`Analysis Results ${enhancementResults ? '✓' : '○'}`} disabled={!enhancementResults} />
            <Tab label={`Enhancement Preview ${enhancementResults ? '✓' : '○'}`} disabled={!enhancementResults} />
            <Tab label={`Interactive Dashboard ${enhancementResults ? '✓' : '○'}`} disabled={!enhancementResults} />
            <Tab label={`Diagrams ${enhancementResults ? '✓' : '○'}`} disabled={!enhancementResults} />
            <Tab label={`Change Report ${enhancementResults ? '✓' : '○'}`} disabled={!enhancementResults} />
            <Tab label={`Modernization ${enhancementResults ? '✓' : '○'}`} disabled={!enhancementResults} />
          </Tabs>
        </Box>

        <TabPanel value={tabValue} index={0}>
          <TestExtraction />
          <ContentInput 
            onSubmit={onUrlSubmit} 
            disabled={processingState.isProcessing || backendHealth !== 'healthy'} 
          />
        </TabPanel>

        <TabPanel value={tabValue} index={1}>
          {enhancementResults ? (
            <AnalysisResults data={enhancementResults.analysis} />
          ) : (
            <Typography variant="body1" color="text.secondary">
              Submit a Confluence URL to view analysis results.
            </Typography>
          )}
        </TabPanel>

        <TabPanel value={tabValue} index={2}>
          {enhancementResults ? (
            <Box>
              <EnhancementPreview 
                data={enhancementResults.enhancements} 
                onCreatePage={onPageCreation}
              />
            </Box>
          ) : (
            <Typography variant="body1" color="text.secondary">
              Enhancement preview will appear after content analysis.
            </Typography>
          )}
        </TabPanel>

        <TabPanel value={tabValue} index={3}>
          {enhancementResults ? (
            <InteractiveDashboard data={enhancementResults} />
          ) : (
            <Typography variant="body1" color="text.secondary">
              Interactive dashboard will be available after processing.
            </Typography>
          )}
        </TabPanel>

        <TabPanel value={tabValue} index={4}>
          {enhancementResults?.diagrams ? (
            <Grid container spacing={2}>
              {enhancementResults.diagrams.map((diagram: any, index: number) => (
                <Grid item xs={12} md={6} key={index}>
                  <DiagramViewer diagram={diagram} />
                </Grid>
              ))}
            </Grid>
          ) : (
            <Typography variant="body1" color="text.secondary">
              Generated diagrams will appear here after processing.
            </Typography>
          )}
        </TabPanel>

        <TabPanel value={tabValue} index={5}>
          {enhancementResults ? (
            <ChangeReport data={enhancementResults.changes} />
          ) : (
            <Typography variant="body1" color="text.secondary">
              Change report will be generated after enhancement processing.
            </Typography>
          )}
        </TabPanel>

        <TabPanel value={tabValue} index={6}>
          {enhancementResults ? (
            <ModernizationPlanner data={enhancementResults.modernization} />
          ) : (
            <Typography variant="body1" color="text.secondary">
              Modernization recommendations will appear after analysis.
            </Typography>
          )}
        </TabPanel>
      </Box>
    </Container>
  );
};

export default Dashboard;
