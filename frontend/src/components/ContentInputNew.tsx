/**
 * Enhanced Content Input Component
 * Supports multiple input methods: Confluence URLs and pasted content
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
  TextareaAutosize,
  Chip,
} from '@mui/material';
import { AnalysisRequest, contentAPI } from '../services/api';

interface ContentInputProps {
  onAnalysisComplete: (result: any) => void;
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
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}

const ContentInput: React.FC<ContentInputProps> = ({ onAnalysisComplete }) => {
  const [inputMethod, setInputMethod] = useState(0);
  const [url, setUrl] = useState('');
  const [pastedContent, setPastedContent] = useState('');
  const [contentTitle, setContentTitle] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [analysisOptions, setAnalysisOptions] = useState({
    structure_analysis: true,
    quality_analysis: true,
    table_analysis: true,
    visualization_generation: true,
    modernization_analysis: true,
  });

  const validateUrl = (url: string): boolean => {
    const confluenceUrlPattern = /^https?:\/\/.*\/display\/[A-Z0-9]+\/.*$/i;
    return confluenceUrlPattern.test(url);
  };

  const validatePastedContent = (): boolean => {
    return pastedContent.trim().length > 100 && contentTitle.trim().length > 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    let request: AnalysisRequest;
    
    if (inputMethod === 0) {
      if (!url.trim()) {
        setError('Please enter a valid Confluence URL');
        return;
      }
      if (!validateUrl(url)) {
        setError('Please enter a valid Confluence URL (format: https://your-confluence.com/display/SPACE/Page-Title)');
        return;
      }
      request = {
        page_url: url.trim(),
        analysis_options: analysisOptions,
      };
    } else {
      if (!validatePastedContent()) {
        setError('Please provide both content title and content (minimum 100 characters)');
        return;
      }
      request = {
        page_url: `pasted_content://${encodeURIComponent(contentTitle)}`,
        analysis_options: {
          ...analysisOptions,
          pasted_content: pastedContent.trim()
        },
      };
    }

    setLoading(true);
    setError(null);

    try {
      const result = await contentAPI.analyzeContent(request);
      onAnalysisComplete(result);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to analyze content');
    } finally {
      setLoading(false);
    }
  };

  const handleOptionChange = (option: keyof typeof analysisOptions) => {
    setAnalysisOptions(prev => ({
      ...prev,
      [option]: !prev[option],
    }));
  };

  return (
    <Paper elevation={3} sx={{ p: 3, maxWidth: 800, margin: 'auto' }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Content Enhancement System
      </Typography>
      
      <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
        Choose how you want to provide content for AI-powered analysis and enhancement
      </Typography>

      <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
        <Tabs value={inputMethod} onChange={(e, newValue) => setInputMethod(newValue)}>
          <Tab label="🔗 Confluence URL" />
          <Tab label="📝 Paste Content" />
        </Tabs>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <TabPanel value={inputMethod} index={0}>
        <Box component="form" onSubmit={handleSubmit}>
          <Typography variant="h6" gutterBottom>
            Confluence Page URL
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
            Enter the URL of an existing Confluence page to analyze and enhance
          </Typography>
          
          <TextField
            fullWidth
            label="Confluence Page URL"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="https://your-confluence.com/display/SPACE/Page-Title"
            variant="outlined"
            sx={{ mb: 2 }}
            helperText="The original page will never be modified - we only create new enhanced pages"
          />
          
          <Box sx={{ mb: 2 }}>
            <Chip label="✅ Read-Only Access" color="success" size="small" sx={{ mr: 1 }} />
            <Chip label="🔒 Original Protected" color="primary" size="small" sx={{ mr: 1 }} />
            <Chip label="🆕 Creates New Page" color="secondary" size="small" />
          </Box>

          <Button
            type="submit"
            variant="contained"
            disabled={loading || !url.trim()}
            startIcon={loading ? <CircularProgress size={20} /> : null}
          >
            {loading ? 'Analyzing...' : 'Analyze Confluence Page'}
          </Button>
        </Box>
      </TabPanel>
      
      <TabPanel value={inputMethod} index={1}>
        <Box component="form" onSubmit={handleSubmit}>
          <Typography variant="h6" gutterBottom>
            Paste Content
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
            Paste content from any source (external websites, documents, etc.) for AI enhancement
          </Typography>
          
          <TextField
            fullWidth
            label="Content Title"
            value={contentTitle}
            onChange={(e) => setContentTitle(e.target.value)}
            placeholder="Enter a title for your content"
            variant="outlined"
            sx={{ mb: 2 }}
            required
          />
          
          <Typography variant="body2" sx={{ mb: 1 }}>
            Content *
          </Typography>
          <TextareaAutosize
            minRows={10}
            placeholder="Paste your content here...

Examples:
• Documentation from external websites
• Process descriptions  
• Technical specifications
• Meeting notes
• Project documentation"
            value={pastedContent}
            onChange={(e) => setPastedContent(e.target.value)}
            style={{
              width: '100%',
              minHeight: '300px',
              padding: '12px',
              border: '1px solid #c4c4c4',
              borderRadius: '4px',
              fontSize: '14px',
              fontFamily: 'inherit',
              resize: 'vertical'
            }}
          />
          
          <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: 'block' }}>
            Character count: {pastedContent.length} (minimum 100 required)
          </Typography>

          <Button
            type="submit"
            variant="contained"
            disabled={loading || !validatePastedContent()}
            startIcon={loading ? <CircularProgress size={20} /> : null}
            sx={{ mt: 2 }}
          >
            {loading ? 'Analyzing...' : 'Analyze Pasted Content'}
          </Button>
        </Box>
      </TabPanel>

      <Box sx={{ mt: 3 }}>
        <Typography variant="h6" gutterBottom>
          Analysis Options
        </Typography>
        <FormGroup>
          <FormControlLabel
            control={
              <Checkbox
                checked={analysisOptions.structure_analysis}
                onChange={() => handleOptionChange('structure_analysis')}
              />
            }
            label="Structure Analysis & Optimization"
          />
          <FormControlLabel
            control={
              <Checkbox
                checked={analysisOptions.quality_analysis}
                onChange={() => handleOptionChange('quality_analysis')}
              />
            }
            label="Content Quality Assessment"
          />
          <FormControlLabel
            control={
              <Checkbox
                checked={analysisOptions.table_analysis}
                onChange={() => handleOptionChange('table_analysis')}
              />
            }
            label="Table Analysis & Dashboard Generation"
          />
          <FormControlLabel
            control={
              <Checkbox
                checked={analysisOptions.visualization_generation}
                onChange={() => handleOptionChange('visualization_generation')}
              />
            }
            label="Visualization & Diagram Generation"
          />
          <FormControlLabel
            control={
              <Checkbox
                checked={analysisOptions.modernization_analysis}
                onChange={() => handleOptionChange('modernization_analysis')}
              />
            }
            label="Technology Modernization Analysis"
          />
        </FormGroup>
      </Box>
    </Paper>
  );
};

export default ContentInput;
