import React, { useState } from 'react';
import { Button, Box, Alert, Typography } from '@mui/material';
import { contentAPI } from '../services/api';

const TestExtraction: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const testExtraction = async () => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await contentAPI.extractContent({
        page_url: 'https://rajendarmuddasani.atlassian.net/wiki/spaces/SD/pages/2949124/Claudee'
      });
      setResult(response);
    } catch (err: any) {
      setError(err.message || 'Failed to extract content');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ p: 2, border: 1, borderColor: 'grey.300', borderRadius: 1, mb: 2 }}>
      <Typography variant="h6" gutterBottom>
        API Test Component
      </Typography>
      
      <Button 
        variant="contained" 
        onClick={testExtraction} 
        disabled={loading}
        sx={{ mb: 2 }}
      >
        {loading ? 'Testing...' : 'Test Content Extraction'}
      </Button>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      {result && (
        <Alert severity="success" sx={{ mb: 2 }}>
          <Typography variant="body2">
            <strong>Success!</strong><br/>
            Title: {result.title}<br/>
            Status: {result.status}<br/>
            Word Count: {result.metadata?.word_count}
          </Typography>
        </Alert>
      )}
    </Box>
  );
};

export default TestExtraction;
