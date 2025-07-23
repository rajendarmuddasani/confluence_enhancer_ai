/**
 * Enhanced Main App Component
 * Confluence Content Intelligence & Enhancement System Frontend
 */
import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { 
  ThemeProvider, 
  createTheme, 
  CssBaseline, 
  AppBar, 
  Toolbar, 
  Typography, 
  Container,
  Box,
  IconButton,
  Alert,
  Snackbar
} from '@mui/material';
import { Brightness4, Brightness7, Settings } from '@mui/icons-material';

// Components
import Dashboard from './pages/Dashboard';
import ReportViewer from './pages/ReportViewer';

// Services
import { ApiService } from './services/api';

// Types
interface ProcessingState {
  isProcessing: boolean;
  currentPhase: string;
  progress: number;
  results?: any;
  error?: string;
}

interface AppState {
  darkMode: boolean;
  processingState: ProcessingState;
  enhancementResults: any;
  notifications: Array<{
    id: string;
    message: string;
    severity: 'success' | 'error' | 'warning' | 'info';
  }>;
}

const App: React.FC = () => {
  const [appState, setAppState] = useState<AppState>({
    darkMode: localStorage.getItem('darkMode') === 'true',
    processingState: {
      isProcessing: false,
      currentPhase: '',
      progress: 0
    },
    enhancementResults: null,
    notifications: []
  });

  // Create theme based on dark mode preference
  const theme = createTheme({
    palette: {
      mode: appState.darkMode ? 'dark' : 'light',
      primary: {
        main: '#1976d2',
      },
      secondary: {
        main: '#dc004e',
      },
      background: {
        default: appState.darkMode ? '#121212' : '#f5f5f5',
      },
    },
    typography: {
      h4: {
        fontWeight: 600,
      },
      h5: {
        fontWeight: 500,
      },
    },
    components: {
      MuiCard: {
        styleOverrides: {
          root: {
            borderRadius: 12,
            boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
          },
        },
      },
      MuiButton: {
        styleOverrides: {
          root: {
            borderRadius: 8,
            textTransform: 'none',
            fontWeight: 500,
          },
        },
      },
    },
  });

  // Toggle dark mode
  const toggleDarkMode = () => {
    const newDarkMode = !appState.darkMode;
    setAppState(prev => ({ ...prev, darkMode: newDarkMode }));
    localStorage.setItem('darkMode', newDarkMode.toString());
  };

  // Add notification
  const addNotification = (message: string, severity: 'success' | 'error' | 'warning' | 'info') => {
    const id = Date.now().toString();
    setAppState(prev => ({
      ...prev,
      notifications: [...prev.notifications, { id, message, severity }]
    }));

    // Auto-remove notification after 5 seconds
    setTimeout(() => {
      setAppState(prev => ({
        ...prev,
        notifications: prev.notifications.filter(n => n.id !== id)
      }));
    }, 5000);
  };

  // Handle Confluence URL processing
  const handleUrlSubmit = async (url: string) => {
    try {
      setAppState(prev => ({
        ...prev,
        processingState: {
          isProcessing: true,
          currentPhase: 'Initializing...',
          progress: 0
        }
      }));

      addNotification('Starting content analysis...', 'info');

      // Start the enhancement process
      const apiService = new ApiService();
      
      // Phase 1: Content Extraction
      setAppState(prev => ({
        ...prev,
        processingState: { ...prev.processingState, currentPhase: 'Extracting content...', progress: 20 }
      }));
      
      const extractionResult = await apiService.extractContent(url);
      
      // Phase 2: Advanced Analysis
      setAppState(prev => ({
        ...prev,
        processingState: { ...prev.processingState, currentPhase: 'Analyzing content...', progress: 40 }
      }));
      
      const analysisResult = await apiService.analyzeContent(extractionResult);
      
      // Phase 3: Enhancement Generation
      setAppState(prev => ({
        ...prev,
        processingState: { ...prev.processingState, currentPhase: 'Generating enhancements...', progress: 70 }
      }));
      
      const enhancementResult = await apiService.generateEnhancements(analysisResult);
      
      // Complete processing
      console.log('Enhancement result:', enhancementResult);
      setAppState(prev => ({
        ...prev,
        processingState: {
          isProcessing: false,
          currentPhase: 'Complete',
          progress: 100,
          results: enhancementResult
        },
        enhancementResults: enhancementResult
      }));

      console.log('App state updated with enhancementResults:', enhancementResult);
      addNotification('Content enhancement completed successfully!', 'success');
      
    } catch (error: any) {
      setAppState(prev => ({
        ...prev,
        processingState: {
          isProcessing: false,
          currentPhase: 'Error',
          progress: 0,
          error: error.message
        }
      }));

      addNotification(`Error: ${error.message}`, 'error');
    }
  };

  // Handle enhanced page creation
  const handlePageCreation = async (enhancementData: any) => {
    try {
      addNotification('Creating enhanced Confluence page...', 'info');
      
      const apiService = new ApiService();
      const result = await apiService.createEnhancedPage(enhancementData);
      
      if (result.success) {
        addNotification(`Enhanced page created successfully: ${result.page_title}`, 'success');
      } else {
        throw new Error(result.error || 'Failed to create enhanced page');
      }
      
    } catch (error: any) {
      addNotification(`Failed to create page: ${error.message}`, 'error');
    }
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
          {/* App Bar */}
          <AppBar position="static" elevation={1}>
            <Toolbar>
              <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                🚀 Confluence Content Intelligence & Enhancement System
              </Typography>
              
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <IconButton onClick={toggleDarkMode} color="inherit">
                  {appState.darkMode ? <Brightness7 /> : <Brightness4 />}
                </IconButton>
                <IconButton color="inherit">
                  <Settings />
                </IconButton>
              </Box>
            </Toolbar>
          </AppBar>

          {/* Main Content */}
          <Container maxWidth="xl" sx={{ flex: 1, py: 3 }}>
            <Routes>
              <Route 
                path="/" 
                element={
                  <Dashboard 
                    processingState={appState.processingState}
                    enhancementResults={appState.enhancementResults}
                    onUrlSubmit={handleUrlSubmit}
                    onPageCreation={handlePageCreation}
                  />
                } 
              />
              <Route 
                path="/reports/:reportId" 
                element={<ReportViewer />} 
              />
              <Route path="/dashboard" element={<Navigate to="/" replace />} />
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </Container>

          {/* Notifications */}
          {appState.notifications.map((notification) => (
            <Snackbar
              key={notification.id}
              open={true}
              anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
            >
              <Alert severity={notification.severity} sx={{ width: '100%' }}>
                {notification.message}
              </Alert>
            </Snackbar>
          ))}
        </Box>
      </Router>
    </ThemeProvider>
  );
};

export default App;
