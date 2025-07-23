/**
 * Interactive Dashboard Component - Phase 4 Compatible
 */
import React from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  Paper,
  Alert,
  Chip,
  LinearProgress
} from '@mui/material';
import { Dashboard, Analytics, TrendingUp, Speed } from '@mui/icons-material';

export interface InteractiveDashboardProps {
  data?: any;
}

export const InteractiveDashboard: React.FC<InteractiveDashboardProps> = ({ data }) => {
  if (!data) {
    return (
      <Alert severity="info">
        Interactive dashboard will be available after content processing.
      </Alert>
    );
  }

  // Mock metrics based on available data
  const metrics = {
    readabilityScore: data.metrics?.readabilityScore || data.readabilityScore || 75,
    engagementScore: data.metrics?.engagementScore || data.engagementScore || 80,
    technicalScore: data.metrics?.technicalScore || data.technicalScore || 85,
    improvementPotential: data.metrics?.improvementPotential || data.improvementPotential || 20
  };

  return (
    <Box>
      <Typography variant="h5" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
        <Dashboard color="primary" />
        Interactive Dashboard
      </Typography>

      <Grid container spacing={3}>
        {/* Key Metrics */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <Analytics color="primary" />
                Key Performance Indicators
              </Typography>
              
              <Grid container spacing={3}>
                {Object.entries(metrics).map(([key, value]) => (
                  <Grid item xs={6} md={3} key={key}>
                    <Paper sx={{ p: 2, textAlign: 'center' }}>
                      <Typography variant="h4" color="primary" gutterBottom>
                        {value}%
                      </Typography>
                      <Typography variant="body2" textTransform="capitalize">
                        {key.replace(/([A-Z])/g, ' $1').trim()}
                      </Typography>
                      <Box sx={{ mt: 1 }}>
                        <LinearProgress
                          variant="determinate"
                          value={value}
                          sx={{ height: 4, borderRadius: 2 }}
                        />
                      </Box>
                    </Paper>
                  </Grid>
                ))}
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        {/* Content Overview */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Content Overview
              </Typography>
              
              {data.analysis?.structure ? (
                <Grid container spacing={2}>
                  <Grid item xs={6}>
                    <Box textAlign="center">
                      <Typography variant="h5" color="primary">
                        {data.analysis.structure.headings || 0}
                      </Typography>
                      <Typography variant="caption">Headings</Typography>
                    </Box>
                  </Grid>
                  <Grid item xs={6}>
                    <Box textAlign="center">
                      <Typography variant="h5" color="primary">
                        {data.analysis.structure.tables || 0}
                      </Typography>
                      <Typography variant="caption">Tables</Typography>
                    </Box>
                  </Grid>
                  <Grid item xs={6}>
                    <Box textAlign="center">
                      <Typography variant="h5" color="primary">
                        {data.analysis.structure.lists || 0}
                      </Typography>
                      <Typography variant="caption">Lists</Typography>
                    </Box>
                  </Grid>
                  <Grid item xs={6}>
                    <Box textAlign="center">
                      <Typography variant="h5" color="primary">
                        {data.analysis.structure.paragraphs || 0}
                      </Typography>
                      <Typography variant="caption">Paragraphs</Typography>
                    </Box>
                  </Grid>
                </Grid>
              ) : (
                <Typography variant="body2" color="text.secondary">
                  Content structure data not available
                </Typography>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* Enhancement Summary */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <TrendingUp color="primary" />
                Enhancement Summary
              </Typography>
              
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <Typography variant="body2">Table Enhancements</Typography>
                  <Chip 
                    label={data.enhancements?.tables?.length || 0} 
                    size="small" 
                    color="primary"
                  />
                </Box>
                
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <Typography variant="body2">Generated Diagrams</Typography>
                  <Chip 
                    label={data.enhancements?.diagrams?.length || 0} 
                    size="small" 
                    color="secondary"
                  />
                </Box>
                
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <Typography variant="body2">Interactive Elements</Typography>
                  <Chip 
                    label={data.enhancements?.interactions?.length || 0} 
                    size="small" 
                    color="success"
                  />
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Performance Insights */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <Speed color="primary" />
                Performance Insights
              </Typography>
              
              <Alert severity="success" sx={{ mb: 2 }}>
                <Typography variant="subtitle2" gutterBottom>
                  Excellent Progress!
                </Typography>
                <Typography variant="body2">
                  Your content has been successfully analyzed and enhanced. The improvements will make it more readable, 
                  engaging, and technically sound.
                </Typography>
              </Alert>
              
              {data.executiveSummary?.recommendations && (
                <Box>
                  <Typography variant="subtitle2" gutterBottom>
                    Key Recommendations
                  </Typography>
                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                    {data.executiveSummary.recommendations.slice(0, 3).map((rec: string, index: number) => (
                      <Chip 
                        key={index} 
                        label={rec} 
                        size="small" 
                        variant="outlined" 
                        color="info"
                      />
                    ))}
                  </Box>
                </Box>
              )}
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};
