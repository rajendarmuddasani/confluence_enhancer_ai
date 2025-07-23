/**
 * Enhanced Enhancement Preview Component - Phase 4 Compatible
 */
import React from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  Grid,
  Alert,
  Chip,
  List,
  ListItem,
  ListItemText,
  Divider
} from '@mui/material';
import { Preview, Create, CheckCircle } from '@mui/icons-material';

export interface EnhancementPreviewProps {
  data?: any;
  onCreatePage?: (enhancementData: any) => Promise<void>;
}

const EnhancementPreview: React.FC<EnhancementPreviewProps> = ({ 
  data, 
  onCreatePage 
}) => {
  const handleCreatePage = async () => {
    if (onCreatePage && data) {
      try {
        await onCreatePage(data);
      } catch (error) {
        console.error('Failed to create page:', error);
      }
    }
  };

  if (!data) {
    return (
      <Alert severity="info">
        Enhancement preview will be available after content analysis is complete.
      </Alert>
    );
  }

  return (
    <Box>
      <Typography variant="h5" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
        <Preview color="primary" />
        Enhancement Preview
      </Typography>

      <Grid container spacing={3}>
        {/* Table Enhancements */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Table Enhancements
              </Typography>
              {data.tables && data.tables.length > 0 ? (
                <List dense>
                  {data.tables.map((table: any, index: number) => (
                    <ListItem key={index}>
                      <ListItemText
                        primary={table.type || `Table ${index + 1}`}
                        secondary={table.improvements || 'Enhanced styling and functionality'}
                      />
                      <Chip label="Enhanced" color="success" size="small" />
                    </ListItem>
                  ))}
                </List>
              ) : (
                <Typography variant="body2" color="text.secondary">
                  No table enhancements available
                </Typography>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* Diagram Enhancements */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Diagram Enhancements
              </Typography>
              {data.diagrams && data.diagrams.length > 0 ? (
                <List dense>
                  {data.diagrams.map((diagram: any, index: number) => (
                    <ListItem key={index}>
                      <ListItemText
                        primary={diagram.type || `Diagram ${index + 1}`}
                        secondary={diagram.description || 'Interactive diagram generated'}
                      />
                      <Chip label="Generated" color="primary" size="small" />
                    </ListItem>
                  ))}
                </List>
              ) : (
                <Typography variant="body2" color="text.secondary">
                  No diagram enhancements available
                </Typography>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* Interactive Elements */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Interactive Elements
              </Typography>
              {data.interactions && data.interactions.length > 0 ? (
                <List dense>
                  {data.interactions.map((interaction: any, index: number) => (
                    <ListItem key={index}>
                      <ListItemText
                        primary={interaction.type || `Interactive Element ${index + 1}`}
                        secondary={interaction.description || 'Enhanced user interaction'}
                      />
                      <Chip label="Interactive" color="secondary" size="small" />
                    </ListItem>
                  ))}
                </List>
              ) : (
                <Typography variant="body2" color="text.secondary">
                  No interactive enhancements available
                </Typography>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* Action Buttons */}
        <Grid item xs={12}>
          <Card sx={{ backgroundColor: 'primary.main', color: 'primary.contrastText' }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <Box>
                  <Typography variant="h6" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <CheckCircle />
                    Ready to Create Enhanced Page
                  </Typography>
                  <Typography variant="body2" sx={{ opacity: 0.9 }}>
                    Your enhanced Confluence page is ready. Click below to create it safely.
                  </Typography>
                </Box>
                
                <Button
                  variant="contained"
                  color="secondary"
                  size="large"
                  startIcon={<Create />}
                  onClick={handleCreatePage}
                  disabled={!onCreatePage}
                >
                  Create Enhanced Page
                </Button>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Box sx={{ mt: 3 }}>
        <Alert severity="info">
          <Typography variant="subtitle2" gutterBottom>
            🔒 Safety First
          </Typography>
          <Typography variant="body2">
            The enhanced page will be created as a new page. Your original content will remain unchanged and safe.
          </Typography>
        </Alert>
      </Box>
    </Box>
  );
};

export default EnhancementPreview;
