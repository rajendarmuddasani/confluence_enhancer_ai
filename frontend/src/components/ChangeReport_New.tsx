/**
 * Change Report Component - Phase 4 Compatible
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
  Chip,
  Alert,
  Grid,
  Divider
} from '@mui/material';
import { 
  Add as AddIcon, 
  Edit as EditIcon, 
  Lightbulb as RecommendationIcon,
  Assessment as ReportIcon 
} from '@mui/icons-material';

export interface ChangeReportProps {
  data?: any;
}

const ChangeReport: React.FC<ChangeReportProps> = ({ data }) => {
  if (!data) {
    return (
      <Alert severity="info">
        Change report will be generated after content enhancement processing.
      </Alert>
    );
  }

  const getPriorityColor = (priority: string) => {
    switch (priority?.toLowerCase()) {
      case 'high':
      case 'critical':
        return 'error';
      case 'medium':
        return 'warning';
      case 'low':
        return 'info';
      default:
        return 'default';
    }
  };

  return (
    <Box>
      <Typography variant="h5" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
        <ReportIcon color="primary" />
        Change Report
      </Typography>

      <Grid container spacing={3}>
        {/* Modifications */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <EditIcon color="primary" />
                Modifications
              </Typography>
              
              {data.modifications && data.modifications.length > 0 ? (
                <List dense>
                  {data.modifications.map((mod: any, index: number) => (
                    <ListItem key={index}>
                      <ListItemIcon>
                        <EditIcon color="action" />
                      </ListItemIcon>
                      <ListItemText
                        primary={mod.type || 'Content Update'}
                        secondary={mod.description || 'Content modification applied'}
                      />
                    </ListItem>
                  ))}
                </List>
              ) : (
                <Typography variant="body2" color="text.secondary">
                  No modifications recorded
                </Typography>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* Additions */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <AddIcon color="primary" />
                Additions
              </Typography>
              
              {data.additions && data.additions.length > 0 ? (
                <List dense>
                  {data.additions.map((addition: any, index: number) => (
                    <ListItem key={index}>
                      <ListItemIcon>
                        <AddIcon color="success" />
                      </ListItemIcon>
                      <ListItemText
                        primary={addition.type || 'New Content'}
                        secondary={addition.description || 'New content added'}
                      />
                    </ListItem>
                  ))}
                </List>
              ) : (
                <Typography variant="body2" color="text.secondary">
                  No additions recorded
                </Typography>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* Recommendations */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <RecommendationIcon color="primary" />
                Recommendations
              </Typography>
              
              {data.recommendations && data.recommendations.length > 0 ? (
                <List dense>
                  {data.recommendations.map((rec: any, index: number) => (
                    <ListItem key={index}>
                      <ListItemIcon>
                        <RecommendationIcon color="info" />
                      </ListItemIcon>
                      <ListItemText
                        primary={
                          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                            <span>Future Enhancement</span>
                            {rec.priority && (
                              <Chip 
                                label={rec.priority} 
                                size="small" 
                                color={getPriorityColor(rec.priority) as any}
                                variant="outlined"
                              />
                            )}
                          </Box>
                        }
                        secondary={rec.description || 'Recommended improvement'}
                      />
                    </ListItem>
                  ))}
                </List>
              ) : (
                <Typography variant="body2" color="text.secondary">
                  No recommendations available
                </Typography>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* Summary */}
        <Grid item xs={12}>
          <Alert severity="success">
            <Typography variant="subtitle1" gutterBottom>
              Change Report Summary
            </Typography>
            <Typography variant="body2">
              {data.modifications?.length || 0} modifications, {data.additions?.length || 0} additions, 
              and {data.recommendations?.length || 0} recommendations have been identified and applied 
              to enhance your Confluence content.
            </Typography>
          </Alert>
        </Grid>
      </Grid>
    </Box>
  );
};

export default ChangeReport;
