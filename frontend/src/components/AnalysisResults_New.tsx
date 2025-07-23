/**
 * Enhanced Analysis Results Component - Phase 4 Compatible
 */
import React from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  Chip,
  Alert,
  Paper,
  List,
  ListItem,
  ListItemText,
  LinearProgress
} from '@mui/material';
import { Assessment, TrendingUp, CheckCircle } from '@mui/icons-material';

export interface AnalysisResultsProps {
  data?: any;
  analysisResults?: any[];
  enhancementSuggestions?: any[];
  loading?: boolean;
}

export const AnalysisResults: React.FC<AnalysisResultsProps> = ({ 
  data, 
  loading = false 
}) => {
  if (loading) {
    return (
      <Box>
        <Typography variant="h6" gutterBottom>
          Analyzing Content...
        </Typography>
        <LinearProgress />
      </Box>
    );
  }

  if (!data) {
    return (
      <Alert severity="info">
        No analysis data available. Please process a Confluence page first.
      </Alert>
    );
  }

  return (
    <Box>
      <Typography variant="h5" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
        <Assessment color="primary" />
        Content Analysis Results
      </Typography>

      <Grid container spacing={3}>
        {/* Structure Analysis */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Content Structure
              </Typography>
              {data.structure ? (
                <Box>
                  <Typography variant="body2" color="text.secondary" gutterBottom>
                    Document organization and hierarchy
                  </Typography>
                  <List dense>
                    <ListItem>
                      <ListItemText primary={`Headings: ${data.structure.headings || 'N/A'}`} />
                    </ListItem>
                    <ListItem>
                      <ListItemText primary={`Paragraphs: ${data.structure.paragraphs || 'N/A'}`} />
                    </ListItem>
                    <ListItem>
                      <ListItemText primary={`Lists: ${data.structure.lists || 'N/A'}`} />
                    </ListItem>
                    <ListItem>
                      <ListItemText primary={`Tables: ${data.structure.tables || 'N/A'}`} />
                    </ListItem>
                  </List>
                </Box>
              ) : (
                <Typography variant="body2" color="text.secondary">
                  Structure analysis data not available
                </Typography>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* Quality Analysis */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Content Quality
              </Typography>
              {data.quality ? (
                <Box>
                  <Typography variant="body2" color="text.secondary" gutterBottom>
                    Readability and completeness metrics
                  </Typography>
                  <List dense>
                    <ListItem>
                      <ListItemText primary={`Readability: ${data.quality.readability || 'N/A'}%`} />
                    </ListItem>
                    <ListItem>
                      <ListItemText primary={`Completeness: ${data.quality.completeness || 'N/A'}%`} />
                    </ListItem>
                    <ListItem>
                      <ListItemText primary={`Accuracy: ${data.quality.accuracy || 'N/A'}%`} />
                    </ListItem>
                  </List>
                </Box>
              ) : (
                <Typography variant="body2" color="text.secondary">
                  Quality analysis data not available
                </Typography>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* Modernization Analysis */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <TrendingUp color="primary" />
                Modernization Assessment
              </Typography>
              {data.modernization ? (
                <Box>
                  <Box sx={{ mb: 2 }}>
                    <Typography variant="body2" color="text.secondary" gutterBottom>
                      Overall Modernization Score
                    </Typography>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                      <LinearProgress 
                        variant="determinate" 
                        value={data.modernization.score || 0} 
                        sx={{ flex: 1, height: 8, borderRadius: 4 }}
                      />
                      <Typography variant="h6" color="primary">
                        {data.modernization.score || 0}%
                      </Typography>
                    </Box>
                  </Box>
                  
                  {data.modernization.areas && (
                    <Box>
                      <Typography variant="subtitle2" gutterBottom>
                        Areas for Improvement
                      </Typography>
                      <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                        {data.modernization.areas.map((area: string, index: number) => (
                          <Chip 
                            key={index} 
                            label={area} 
                            size="small" 
                            color="warning" 
                            variant="outlined"
                          />
                        ))}
                      </Box>
                    </Box>
                  )}
                </Box>
              ) : (
                <Typography variant="body2" color="text.secondary">
                  Modernization analysis data not available
                </Typography>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* Summary */}
        <Grid item xs={12}>
          <Paper sx={{ p: 2, backgroundColor: 'success.main', color: 'success.contrastText' }}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <CheckCircle />
              <Typography variant="h6">
                Analysis Complete
              </Typography>
            </Box>
            <Typography variant="body2" sx={{ mt: 1 }}>
              Content analysis has been completed successfully. Review the results above and proceed to the Enhancement Preview to see suggested improvements.
            </Typography>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};
