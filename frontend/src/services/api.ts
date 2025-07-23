/**
 * API service for communicating with the backend
 */
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    // Skip auth for content extraction and health endpoints
    const skipAuthUrls = ['/analysis/extract', '/health', '/analysis/analyze', '/enhancement/optimize', '/api/pages/create-enhanced'];
    const shouldSkipAuth = skipAuthUrls.some(url => config.url?.includes(url));
    
    if (!shouldSkipAuth) {
      const token = localStorage.getItem('access_token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Skip redirect for content extraction and health endpoints
    const skipRedirectUrls = ['/analysis/extract', '/health', '/analysis/analyze', '/enhancement/optimize', '/api/pages/create-enhanced'];
    const shouldSkipRedirect = skipRedirectUrls.some(url => error.config?.url?.includes(url));
    
    if (error.response?.status === 401 && !shouldSkipRedirect) {
      localStorage.removeItem('access_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export interface AnalysisRequest {
  page_url: string;
  analysis_options?: {
    structure_analysis?: boolean;
    quality_analysis?: boolean;
    table_analysis?: boolean;
    visualization_generation?: boolean;
    modernization_analysis?: boolean;
  };
}

export interface AuthRequest {
  username: string;
  password: string;
}

export interface ConfluenceAuthRequest {
  base_url: string;
  username: string;
  api_token: string;
}

// Authentication APIs
export const authAPI = {
  login: async (credentials: AuthRequest) => {
    const response = await api.post('/auth/login', credentials);
    return response.data;
  },

  verifyConfluence: async (confluenceAuth: ConfluenceAuthRequest) => {
    const response = await api.post('/auth/confluence', confluenceAuth);
    return response.data;
  },
};

// Content Analysis APIs
export const contentAPI = {
  extractContent: async (request: AnalysisRequest) => {
    const response = await api.post('/analysis/extract', request);
    return response.data;
  },

  analyzeContent: async (request: AnalysisRequest) => {
    const response = await api.post('/analysis/analyze', request);
    return response.data;
  },

  optimizeContent: async (contentId: string, enhancementTypes: string[]) => {
    const response = await api.post('/enhancement/optimize', {
      content_id: contentId,
      enhancement_types: enhancementTypes,
    });
    return response.data;
  },
};

// Visualization APIs
export const visualizationAPI = {
  getDashboard: async (contentId: string) => {
    const response = await api.get(`/visualization/dashboard/${contentId}`);
    return response.data;
  },
};

// Reports APIs
export const reportsAPI = {
  getEnhancementReport: async (contentId: string) => {
    const response = await api.get(`/reports/${contentId}`);
    return response.data;
  },
};

// Health check
export const healthAPI = {
  check: async () => {
    const response = await api.get('/health');
    return response.data;
  },
};

// Unified ApiService class for backward compatibility with App.tsx
export class ApiService {
  // Extract content from Confluence URL
  async extractContent(url: string) {
    try {
      const response = await api.post('/analysis/extract', {
        page_url: url,
        analysis_options: {
          structure_analysis: true,
          quality_analysis: true,
          table_analysis: true,
          visualization_generation: true,
          modernization_analysis: true
        }
      });
      return response.data;
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Failed to extract content');
    }
  }

  // Analyze extracted content
  async analyzeContent(extractedContent: any) {
    try {
      const response = await api.post('/analysis/analyze', {
        page_url: extractedContent.metadata?.url || extractedContent.url || extractedContent.page_url,
        analysis_options: {
          structure_analysis: true,
          quality_analysis: true,
          table_analysis: true,
          visualization_generation: true,
          modernization_analysis: true
        }
      });
      
      // Combine extraction and analysis data
      return {
        ...response.data,
        extraction: extractedContent,
        analysis: response.data.analysis
      };
    } catch (error: any) {
      console.error('Analysis error:', error.response?.data);
      throw new Error(error.response?.data?.detail || JSON.stringify(error.response?.data) || 'Failed to analyze content');
    }
  }

  // Generate enhancements
  async generateEnhancements(analysisResult: any) {
    try {
      const response = await api.post('/enhancement/optimize', {
        content_id: analysisResult.content_id || 'temp-id',
        enhancement_types: ['tables', 'diagrams', 'structure', 'modernization']
      });
      
      // Combine all data into a unified structure
      return {
        content_id: response.data.content_id,
        extraction: analysisResult.extraction,
        analysis: analysisResult.analysis,
        enhancements: response.data.optimization_results,
        optimization_results: response.data.optimization_results,
        diagrams: [
          {
            id: 'structure-diagram',
            title: 'Content Structure Diagram', 
            type: 'mermaid',
            content: `graph TD
              A[Original Content] --> B[Structure Analysis]
              B --> C[Quality Assessment]
              C --> D[Enhancement Generation]
              D --> E[Optimized Content]`,
            description: 'Visual representation of content enhancement process'
          }
        ],
        changes: {
          summary: 'Content has been optimized for better readability and structure',
          improvements: response.data.optimization_results?.enhancements_applied || [],
          metrics: response.data.optimization_results?.metrics || {}
        },
        modernization: {
          status: 'analyzed',
          recommendations: [
            'Update content structure for better readability',
            'Add interactive elements where appropriate',
            'Improve visual hierarchy'
          ],
          priority: 'medium'
        },
        timestamp: response.data.timestamp
      };
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Failed to generate enhancements');
    }
  }

  // Create enhanced Confluence page
  async createEnhancedPage(enhancementData: any) {
    try {
      const response = await api.post('/api/pages/create-enhanced', {
        enhancement_data: enhancementData
      });
      return response.data;
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Failed to create enhanced page');
    }
  }

  // Get report by ID
  async getReport(reportId: string) {
    try {
      const response = await api.get(`/reports/${reportId}`);
      return response.data;
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Failed to load report');
    }
  }

  // Health check
  async healthCheck() {
    try {
      const response = await api.get('/health');
      return response.data;
    } catch (error: any) {
      throw new Error('Backend service unavailable');
    }
  }
}

export default api;
