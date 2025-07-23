# Technical Architecture - Confluence Content Intelligence & Enhancement System

## 🔧 **Complete System Architecture**

### **Frontend-Backend Integration Architecture**

```
Frontend (React + TypeScript)          Backend (FastAPI + Python)
├── App.tsx (Main application)     ←→  ├── main.py (FastAPI server)
│   ├── State management            ←→  ├── Phase 1: Content extraction
│   ├── Theme system                ←→  │   ├── content_extractor.py
│   ├── Notification system         ←→  │   ├── confluence_client.py
│   └── Real-time processing        ←→  │   └── auth_handler.py
├── Dashboard.tsx (Multi-tab UI)    ←→  ├── Phase 2: Advanced analysis
│   ├── Tab management              ←→  │   ├── table_processor.py
│   ├── Health monitoring           ←→  │   ├── concept_processor.py
│   └── Process tracking            ←→  │   └── modernization_engine.py
├── ContentInput.tsx (URL input)    ←→  ├── Phase 3: Report generation
│   ├── URL validation              ←→  │   ├── interactive_report.py (493 lines)
│   └── Submission handling         ←→  │   ├── page_creator.py (827+ lines)
├── AnalysisResults.tsx (Display)   ←→  │   └── metrics_collector.py
│   ├── Metrics visualization       ←→  └── Phase 4: API Integration
│   └── Progress indicators         ←→      ├── FastAPI endpoints (15+)
├── EnhancementPreview.tsx (View)   ←→      ├── CORS middleware
│   ├── Preview generation          ←→      └── Error handling
│   └── Page creation trigger       ←→
├── InteractiveDashboard.tsx        ←→  Virtual Environment (.venv)
│   ├── KPI display                 ←→  ├── Python 3.12.0
│   └── Business metrics            ←→  ├── FastAPI, Uvicorn
├── DiagramViewer.tsx               ←→  ├── Pandas, Plotly
│   ├── Mermaid.js integration      ←→  ├── BeautifulSoup4
│   └── Multi-format support        ←→  ├── Requests, PyJWT
├── ChangeReport.tsx                ←→  └── Pydantic, python-multipart
│   ├── Change tracking             ←→
│   └── Modification documentation  ←→  Development Servers:
└── ModernizationPlanner.tsx        ←→  ├── Frontend: http://localhost:3002
    ├── Progress tracking           ←→  └── Backend: http://0.0.0.0:8000
    └── Roadmap display             ←→
                                    ←→  Production Features:
Configuration & Build:              ←→  ├── Docker containerization
├── index.html (App entry point)    ←→  ├── Environment configuration
├── package.json (Dependencies)     ←→  ├── API documentation (/docs)
├── tsconfig.json (TypeScript)      ←→  ├── Health monitoring (/health)
├── vite.config.ts (Build config)   ←→  ├── CORS configuration
└── src/services/api.ts (API layer) ←→  └── Static asset serving
```

## 📁 **Complete File Structure**

### **Frontend Architecture (`/frontend/`)**
```
frontend/
├── index.html (Main HTML entry point - Vite app shell)
├── package.json (Dependencies & scripts)
├── tsconfig.json (TypeScript configuration)
├── vite.config.ts (Build configuration)
├── src/
│   ├── App.tsx (280+ lines - Main application)
│   ├── main.tsx (Application entry point)
│   ├── vite-env.d.ts (Environment types)
│   ├── pages/
│   │   ├── Dashboard.tsx (260+ lines - Multi-tab interface)
│   │   └── ReportViewer.tsx (Report display)
│   ├── components/
│   │   ├── ContentInput.tsx (URL input & validation)
│   │   ├── AnalysisResults.tsx (Analysis display)
│   │   ├── EnhancementPreview.tsx (Preview & creation)
│   │   ├── InteractiveDashboard.tsx (KPI dashboard)
│   │   ├── DiagramViewer.tsx (Mermaid.js integration)
│   │   ├── ChangeReport.tsx (Change tracking)
│   │   └── ModernizationPlanner.tsx (Roadmap display)
│   └── services/
│       └── api.ts (Backend communication layer)
└── node_modules/ (802 packages installed)
```

### **Backend Architecture (`/src/`)**
```
src/
├── __init__.py
├── api/
│   ├── __init__.py
│   ├── auth_handler.py (Authentication & JWT)
│   ├── confluence_client.py (Confluence API integration)
│   ├── content_extractor.py (HTML parsing & extraction)
│   └── page_creator.py (827+ lines - Safe page creation)
├── ai_engine/
│   ├── __init__.py
│   ├── content_analyzer.py (AI-powered analysis)
│   ├── enhancement_engine.py (Content improvements)
│   ├── structure_optimizer.py (Structure analysis)
│   └── visualization_engine.py (Chart generation)
├── processors/
│   ├── __init__.py
│   ├── concept_processor.py (Diagram generation)
│   └── table_processor.py (Table analysis)
├── reports/
│   ├── __init__.py
│   ├── interactive_report.py (493 lines - Report generation)
│   ├── metrics_collector.py (Performance metrics)
│   └── report_generator.py (Report formatting)
├── modernization/
│   ├── __init__.py
│   ├── content_modernizer.py (Content updates)
│   └── technology_modernizer.py (Tech recommendations)
├── models/
│   ├── __init__.py
│   ├── content_model.py (Data structures)
│   ├── enhancement_model.py (Enhancement types)
│   └── visualization_model.py (Chart models)
├── utils/
│   ├── __init__.py
│   ├── config.py (Settings management)
│   └── helpers.py (Utility functions)
└── visualizations/
    ├── __init__.py
    └── dashboard_generator.py (Interactive dashboards)
```

## 🔄 **Data Flow Architecture**

### **Request Processing Flow**
```
User Input (URL) → ContentInput.tsx
    ↓
API Service Layer (api.ts)
    ↓
FastAPI Backend (main.py)
    ↓
Phase 1: Content Extraction
├── confluence_client.py (Fetch content)
├── content_extractor.py (Parse HTML)
└── auth_handler.py (Authentication)
    ↓
Phase 2: Advanced Analysis
├── table_processor.py (Table analysis)
├── concept_processor.py (Diagram generation)
└── modernization_engine.py (Tech analysis)
    ↓
Phase 3: Report Generation
├── interactive_report.py (Comprehensive reports)
├── page_creator.py (Safe page creation)
└── metrics_collector.py (Performance tracking)
    ↓
Phase 4: Frontend Display
├── AnalysisResults.tsx (Show analysis)
├── EnhancementPreview.tsx (Preview changes)
├── InteractiveDashboard.tsx (Display metrics)
└── Real-time progress updates
```

### **State Management Flow**
```
App.tsx (Global State)
├── processingState: {
│   ├── isProcessing: boolean
│   ├── currentPhase: string
│   ├── progress: number
│   └── results?: any
│   }
├── enhancementResults: any
├── notifications: NotificationArray
└── darkMode: boolean
    ↓
Dashboard.tsx (Tab Management)
├── tabValue: number
├── backendHealth: string
└── Component routing
    ↓
Individual Components
├── ContentInput (URL handling)
├── AnalysisResults (Data display)
├── EnhancementPreview (Preview & actions)
└── Other specialized components
```

## 🌐 **API Architecture**

### **Core Endpoints**
```
Backend Server (http://0.0.0.0:8000)
├── GET /health (System health check)
├── GET /docs (API documentation)
├── POST /api/extract/content (Content extraction)
├── POST /api/analysis/comprehensive (AI analysis)
├── POST /api/enhancement/generate (Enhancement creation)
├── POST /api/pages/create-enhanced (Safe page creation)
├── GET /api/reports/{id} (Report retrieval)
└── WebSocket /ws (Real-time updates)
```

### **Frontend API Integration**
```
ApiService Class (api.ts)
├── extractContent(url: string)
├── analyzeContent(content: any)
├── generateEnhancements(analysis: any)
├── createEnhancedPage(data: any)
├── getReport(reportId: string)
└── healthCheck()
```

### **Application Entry Point**
```
index.html (Vite App Shell)
├── HTML5 structure & metadata
├── Material-UI font imports (Roboto)
├── Material Icons integration
├── SEO optimization tags
├── Loading spinner (pre-React)
├── Responsive viewport setup
└── Module script entry (/src/main.tsx)
```

## 🔧 **Technology Stack Details**

### **Frontend Technologies**
- **React 18.2.0**: Modern hooks, concurrent features
- **TypeScript 5.0+**: Full type safety, strict mode
- **Material-UI 5.14+**: Component library, theming
- **Vite 4.4+**: Fast build tool, hot reload
- **Plotly.js 2.26+**: Interactive visualizations
- **Mermaid 10.6+**: Diagram generation
- **Axios 1.6+**: HTTP client with interceptors

### **Backend Technologies**
- **FastAPI 0.104+**: Modern async Python framework
- **Python 3.12**: Latest Python with performance improvements
- **Uvicorn**: ASGI server with auto-reload
- **Pandas**: Data analysis and manipulation
- **BeautifulSoup4**: HTML parsing and extraction
- **Plotly**: Server-side chart generation
- **PyJWT**: JSON Web Token handling
- **Pydantic**: Data validation and serialization

### **Development & Deployment**
- **Docker**: Containerization with multi-stage builds
- **Git**: Version control with comprehensive history
- **npm**: Frontend package management (802 packages)
- **pip**: Python package management (virtual environment)
- **Environment Variables**: Configuration management
- **CORS**: Cross-origin resource sharing configured

## 🚀 **Production Architecture**

### **Deployment Configuration**
```
Production Environment
├── Frontend Container (nginx + React build)
│   ├── Static asset serving
│   ├── Gzip compression
│   └── Cache headers
├── Backend Container (Python + FastAPI)
│   ├── Gunicorn WSGI server
│   ├── Multiple worker processes
│   └── Health check endpoints
├── Database Container (Oracle/PostgreSQL)
│   ├── Connection pooling
│   ├── Backup automation
│   └── Performance monitoring
└── Load Balancer (nginx/HAProxy)
    ├── SSL termination
    ├── Request routing
    └── Health monitoring
```

### **Monitoring & Observability**
```
System Monitoring
├── Application Metrics
│   ├── Request latency
│   ├── Error rates
│   └── Throughput
├── Infrastructure Metrics
│   ├── CPU/Memory usage
│   ├── Disk I/O
│   └── Network traffic
└── Business Metrics
    ├── Content processing rates
    ├── Enhancement success rates
    └── User engagement metrics
```

## 🔐 **Security Architecture**

### **Authentication & Authorization**
```
Security Layer
├── Frontend Security
│   ├── JWT token storage
│   ├── Automatic token refresh
│   └── Route protection
├── Backend Security
│   ├── CORS configuration
│   ├── Input validation
│   └── Rate limiting
└── API Security
    ├── OAuth 2.0 integration
    ├── Confluence API tokens
    └── Secure headers
```

This technical architecture provides a comprehensive view of the complete system structure, data flow, and technology integration for the Confluence Content Intelligence & Enhancement System.
