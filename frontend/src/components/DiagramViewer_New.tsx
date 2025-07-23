/**
 * Diagram Viewer Component - Phase 4 Compatible
 */
import React from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Alert,
  Chip,
  Paper
} from '@mui/material';
import { AccountTree, Timeline, Schema } from '@mui/icons-material';

export interface DiagramViewerProps {
  diagram?: any;
  diagrams?: any[];
  type?: string;
  description?: string;
}

export const DiagramViewer: React.FC<DiagramViewerProps> = ({ 
  diagram, 
  diagrams, 
  type, 
  description 
}) => {
  // Handle different prop formats
  const diagramData = diagram || { type, description };
  
  if (!diagramData && (!diagrams || diagrams.length === 0)) {
    return (
      <Alert severity="info">
        No diagrams available to display.
      </Alert>
    );
  }

  const getIconForDiagramType = (diagramType: string) => {
    switch (diagramType?.toLowerCase()) {
      case 'flowchart':
      case 'process':
        return <Timeline color="primary" />;
      case 'architecture':
      case 'system':
        return <Schema color="primary" />;
      default:
        return <AccountTree color="primary" />;
    }
  };

  const renderDiagram = (diag: any, index: number = 0) => (
    <Card key={index} sx={{ mb: 2 }}>
      <CardContent>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
          {getIconForDiagramType(diag.type)}
          <Typography variant="h6">
            {diag.type ? `${diag.type.charAt(0).toUpperCase()}${diag.type.slice(1)} Diagram` : 'Diagram'}
          </Typography>
          <Chip 
            label={diag.type || 'Generated'} 
            size="small" 
            color="primary" 
            variant="outlined"
          />
        </Box>
        
        {diag.description && (
          <Typography variant="body2" color="text.secondary" paragraph>
            {diag.description}
          </Typography>
        )}
        
        <Paper 
          sx={{ 
            p: 3, 
            backgroundColor: 'grey.50', 
            border: '2px dashed',
            borderColor: 'grey.300',
            textAlign: 'center',
            minHeight: 200,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            flexDirection: 'column'
          }}
        >
          {getIconForDiagramType(diag.type)}
          <Typography variant="h6" color="text.secondary" sx={{ mt: 2 }}>
            Interactive Diagram
          </Typography>
          <Typography variant="body2" color="text.secondary">
            {diag.description || 'Diagram would be rendered here'}
          </Typography>
          
          <Box sx={{ mt: 2 }}>
            <Chip label="Mermaid.js Generated" size="small" color="info" />
          </Box>
        </Paper>
        
        {diag.code && (
          <Box sx={{ mt: 2 }}>
            <Typography variant="subtitle2" gutterBottom>
              Diagram Code
            </Typography>
            <Paper sx={{ p: 2, backgroundColor: 'grey.100', fontFamily: 'monospace', fontSize: '0.875rem' }}>
              {diag.code}
            </Paper>
          </Box>
        )}
      </CardContent>
    </Card>
  );

  return (
    <Box>
      <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
        <AccountTree color="primary" />
        Diagram Viewer
      </Typography>
      
      {diagramData && renderDiagram(diagramData)}
      
      {diagrams && diagrams.map((diag, index) => renderDiagram(diag, index))}
      
      {!diagramData && (!diagrams || diagrams.length === 0) && (
        <Alert severity="info">
          Diagrams will appear here after content processing generates them.
        </Alert>
      )}
    </Box>
  );
};
