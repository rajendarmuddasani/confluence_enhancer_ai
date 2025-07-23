/**
 * Enhanced Content Input Component - Phase 4
 */
import React, { useState } from 'react';
import {
  Box,
  TextField,
  Button,
  Paper,
  Typography,
  Alert,
  CircularProgress,
  FormGroup,
  FormControlLabel,
  Checkbox,
  Tabs,
  Tab,
  Divider,
  Chip,
} from '@mui/material';
import { Link, CloudUpload, Analytics } from '@mui/icons-material';

interface ContentInputProps {
  onAnalysisComplete?: (result: any) => void;
  onSubmit?: (url: string) => Promise<void>;
  disabled?: boolean;
}

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
      id={`content-input-tabpanel-${index}`}
      aria-labelledby={`content-input-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ p: 3 }}>
          {children}
        </Box>
      )}
    </div>
  );
}

const ContentInput: React.FC<ContentInputProps> = ({ 
  onAnalysisComplete, 
  onSubmit, 
  disabled = false 
}) => {
  const [tabValue, setTabValue] = useState(0);
  const [pageUrl, setPageUrl] = useState('');
  const [pastedContent, setPastedContent] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [analysisOptions, setAnalysisOptions] = useState({
    structure_analysis: true,
    quality_analysis: true,
    table_analysis: true,
    visualization_generation: true,
    modernization_analysis: true,
  });

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
    setError(null);
  };

  const handleUrlSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    
    if (!pageUrl.trim()) {
      setError('Please enter a valid Confluence page URL');
      return;
    }

    if (!pageUrl.includes('confluence') && !pageUrl.includes('atlassian')) {
      setError('Please enter a valid Confluence URL');
      return;
    }

    setError(null);
    setLoading(true);

    try {
      if (onSubmit) {
        await onSubmit(pageUrl.trim());
      } else if (onAnalysisComplete) {
        // Legacy support - simulate analysis
        const mockResult = {
          url: pageUrl,
          analysis: { status: 'complete' },
          timestamp: new Date().toISOString()
        };
        onAnalysisComplete(mockResult);
      }
      
      // Clear form after successful submission
      setPageUrl('');
    } catch (err: any) {
      setError(err.message || 'Failed to process URL');
    } finally {
      setLoading(false);
    }
  };

  const handleOptionChange = (option: keyof typeof analysisOptions) => {
    setAnalysisOptions(prev => ({
      ...prev,
      [option]: !prev[option]
    }));
  };

  const isFormValid = () => {
    if (tabValue === 0) {
      return pageUrl.trim().length > 0;
    }
    return pastedContent.trim().length > 0;
  };

  return (
    <Paper elevation={2} sx={{ p: 3 }}>
      <Box sx={{ mb: 3 }}>
        <Typography variant="h5" gutterBottom>
          Content Input
        </Typography>
        <Typography variant="body2" color="text.secondary">
          Enter a Confluence page URL or paste content directly for analysis
        </Typography>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 2 }}>
        <Tabs value={tabValue} onChange={handleTabChange}>
          <Tab 
            icon={<Link />} 
            label="Confluence URL" 
            iconPosition="start"
          />
          <Tab 
            icon={<CloudUpload />} 
            label="Paste Content" 
            iconPosition="start" 
            disabled
          />
        </Tabs>
      </Box>

      <TabPanel value={tabValue} index={0}>
        <form onSubmit={handleUrlSubmit}>
          <Box sx={{ mb: 3 }}>
            <TextField
              fullWidth
              label="Confluence Page URL"
              value={pageUrl}
              onChange={(e) => setPageUrl(e.target.value)}
              placeholder="https://your-org.atlassian.net/wiki/spaces/SPACE/pages/123456/Page+Title"
              disabled={loading || disabled}
              helperText="Enter the full URL of the Confluence page you want to analyze"
              InputProps={{
                startAdornment: <Link sx={{ mr: 1, color: 'text.secondary' }} />
              }}
            />
          </Box>

          <Divider sx={{ my: 3 }} />

          <Box sx={{ mb: 3 }}>
            <Typography variant="h6" gutterBottom>
              Analysis Options
            </Typography>
            <FormGroup row>
              {Object.entries(analysisOptions).map(([key, value]) => (
                <FormControlLabel
                  key={key}
                  control={
                    <Checkbox
                      checked={value}
                      onChange={() => handleOptionChange(key as keyof typeof analysisOptions)}
                      disabled={loading || disabled}
                    />
                  }
                  label={
                    <Box display="flex" alignItems="center">
                      {key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                      {value && <Chip size="small" label="Active" color="primary" sx={{ ml: 1 }} />}
                    </Box>
                  }
                />
              ))}
            </FormGroup>
          </Box>

          <Box sx={{ display: 'flex', gap: 2, alignItems: 'center' }}>
            <Button
              type="submit"
              variant="contained"
              size="large"
              disabled={!isFormValid() || loading || disabled}
              startIcon={loading ? <CircularProgress size={20} /> : <Analytics />}
              sx={{ minWidth: 200 }}
            >
              {loading ? 'Processing...' : 'Analyze Content'}
            </Button>

            {disabled && (
              <Alert severity="warning" sx={{ flex: 1 }}>
                Backend service is unavailable
              </Alert>
            )}
          </Box>
        </form>
      </TabPanel>

      <TabPanel value={tabValue} index={1}>
        <Box>
          <Alert severity="info" sx={{ mb: 2 }}>
            Direct content input feature coming soon. Please use the Confluence URL option.
          </Alert>
          
          <TextField
            fullWidth
            multiline
            rows={8}
            label="Paste Content Here"
            value={pastedContent}
            onChange={(e) => setPastedContent(e.target.value)}
            placeholder="Paste your Confluence content here..."
            disabled
            helperText="This feature will be available in a future update"
          />
        </Box>
      </TabPanel>
    </Paper>
  );
};

export default ContentInput;
