/**
 * Modernization Planner Component - Phase 4 Compatible
 */
import React from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Alert,
  LinearProgress,
  Grid,
  Paper,
  Chip
} from '@mui/material';
import { 
  TrendingUp as ModernizeIcon,
  CheckCircle as CompleteIcon,
  Schedule as PendingIcon,
  Build as ToolIcon 
} from '@mui/icons-material';

export interface ModernizationPlannerProps {
  data?: any;
}

export const ModernizationPlanner: React.FC<ModernizationPlannerProps> = ({ data }) => {
  if (!data) {
    return (
      <Alert severity="info">
        Modernization plan will be available after content analysis.
      </Alert>
    );
  }

  const mockPlan = {
    currentScore: data.score || data.currentScore || 65,
    targetScore: data.targetScore || 85,
    areas: data.areas || ['Tables', 'Diagrams', 'Navigation'],
    timeline: data.timeline || '2-4 weeks',
    priority: data.priority || 'medium',
    ...data
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'complete':
        return <CompleteIcon color="success" />;
      case 'in-progress':
        return <PendingIcon color="warning" />;
      default:
        return <ToolIcon color="action" />;
    }
  };

  return (
    <Box>
      <Typography variant="h5" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
        <ModernizeIcon color="primary" />
        Modernization Planner
      </Typography>

      <Grid container spacing={3}>
        {/* Current Status */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Modernization Progress
              </Typography>
              
              <Box sx={{ mb: 2 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                  <Typography variant="body2">Current Score</Typography>
                  <Typography variant="body2" fontWeight="bold">
                    {mockPlan.currentScore}%
                  </Typography>
                </Box>
                <LinearProgress
                  variant="determinate"
                  value={mockPlan.currentScore}
                  sx={{ height: 8, borderRadius: 4 }}
                />
              </Box>

              <Box sx={{ mb: 2 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                  <Typography variant="body2">Target Score</Typography>
                  <Typography variant="body2" fontWeight="bold">
                    {mockPlan.targetScore}%
                  </Typography>
                </Box>
                <LinearProgress
                  variant="determinate"
                  value={mockPlan.targetScore}
                  color="success"
                  sx={{ height: 8, borderRadius: 4 }}
                />
              </Box>

              <Paper sx={{ p: 2, backgroundColor: 'info.main', color: 'info.contrastText' }}>
                <Typography variant="subtitle2">
                  Improvement Potential: {mockPlan.targetScore - mockPlan.currentScore}%
                </Typography>
              </Paper>
            </CardContent>
          </Card>
        </Grid>

        {/* Areas for Improvement */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Focus Areas
              </Typography>
              
              {mockPlan.areas && mockPlan.areas.length > 0 ? (
                <Box>
                  <List dense>
                    {mockPlan.areas.map((area: string, index: number) => (
                      <ListItem key={index}>
                        <ListItemIcon>
                          {getStatusIcon('pending')}
                        </ListItemIcon>
                        <ListItemText
                          primary={area}
                          secondary="Identified for improvement"
                        />
                        <Chip 
                          label="Priority" 
                          size="small" 
                          color="warning" 
                          variant="outlined"
                        />
                      </ListItem>
                    ))}
                  </List>
                </Box>
              ) : (
                <Typography variant="body2" color="text.secondary">
                  No specific areas identified
                </Typography>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* Action Plan */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Modernization Action Plan
              </Typography>
              
              <List>
                <ListItem>
                  <ListItemIcon>
                    <CompleteIcon color="success" />
                  </ListItemIcon>
                  <ListItemText
                    primary="Content Analysis"
                    secondary="Comprehensive analysis of current content structure and quality"
                  />
                  <Chip label="Completed" color="success" size="small" />
                </ListItem>

                <ListItem>
                  <ListItemIcon>
                    <CompleteIcon color="success" />
                  </ListItemIcon>
                  <ListItemText
                    primary="Enhancement Generation"
                    secondary="Automated improvements for tables, diagrams, and interactive elements"
                  />
                  <Chip label="Completed" color="success" size="small" />
                </ListItem>

                <ListItem>
                  <ListItemIcon>
                    <PendingIcon color="warning" />
                  </ListItemIcon>
                  <ListItemText
                    primary="Page Creation"
                    secondary="Create enhanced Confluence page with all improvements"
                  />
                  <Chip label="Ready" color="primary" size="small" />
                </ListItem>

                <ListItem>
                  <ListItemIcon>
                    <ToolIcon color="action" />
                  </ListItemIcon>
                  <ListItemText
                    primary="Continuous Optimization"
                    secondary="Monitor usage and gather feedback for future enhancements"
                  />
                  <Chip label="Future" color="default" size="small" />
                </ListItem>
              </List>
            </CardContent>
          </Card>
        </Grid>

        {/* Timeline & Next Steps */}
        <Grid item xs={12}>
          <Alert severity="success">
            <Typography variant="subtitle1" gutterBottom>
              Ready for Modernization!
            </Typography>
            <Typography variant="body2">
              Your content has been successfully analyzed and enhanced. 
              Proceed to create the enhanced Confluence page to complete the modernization process.
            </Typography>
          </Alert>
        </Grid>
      </Grid>
    </Box>
  );
};
