# 🚀 Quick Start Guide - Phase 2 Integration

Welcome to Phase 2 of the Confluence Enhancer AI project! This guide will help you set up external services and get the system running with real data.

## 📋 Prerequisites

Before starting, make sure you have:
- **Python 3.9+** installed
- **Node.js 18+** installed  
- **Git** installed
- Access to the following services:
  - OpenAI API account
  - Confluence instance (Atlassian Cloud or Server)
  - Oracle Database (optional for full functionality)

## 🏃‍♂️ Quick Setup (Automated)

### Option 1: One-Command Setup
```bash
./setup.sh
```

This automated script will:
1. ✅ Check system requirements
2. ✅ Set up Python virtual environment
3. ✅ Install all dependencies
4. ✅ Configure frontend
5. ✅ Create environment files
6. ✅ Test API connections
7. ✅ Optionally set up database

### Option 2: Manual Setup

If you prefer manual control:

```bash
# 1. Create Python environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Setup frontend
cd frontend
npm install
cd ..

# 4. Create environment file
cp .env.development .env
```

## 🔑 API Configuration

### Step 1: OpenAI API Setup
1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create a new API key
3. Add to `.env` file:
```bash
OPENAI_API_KEY=sk-your-openai-api-key-here
```

### Step 2: Confluence API Setup
1. Go to [Atlassian Account Settings](https://id.atlassian.com/manage-profile/security/api-tokens)
2. Create an API token
3. Add to `.env` file:
```bash
CONFLUENCE_BASE_URL=https://your-company.atlassian.net
CONFLUENCE_USERNAME=your-email@company.com
CONFLUENCE_API_TOKEN=your-api-token-here
```

### Step 3: Database Configuration (Optional)
For Oracle Database:
```bash
ORACLE_HOST=localhost
ORACLE_PORT=1521
ORACLE_SERVICE=XE
ORACLE_USER=confluence_user
ORACLE_PASSWORD=your-password-here
```

### Step 4: Security Configuration
Generate a secure secret key:
```bash
# Generate a secure key
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Add to .env
SECRET_KEY=your-generated-secret-key-here
```

## 🧪 Testing Your Setup

### Test API Connections
```bash
source venv/bin/activate
python scripts/setup_apis.py
```

This will test:
- ✅ OpenAI API connectivity
- ✅ Confluence API authentication
- ✅ Anthropic API (if configured)

Expected output:
```
🚀 Confluence Enhancer AI - Setup Wizard
==================================================

🔧 Testing API Connections:
------------------------------
Openai: ✅ Connected
Confluence: ✅ Connected  
Anthropic: ✅ Connected

🎉 All required services are configured and connected!
You're ready to proceed with Phase 2 integration.
```

### Setup Database (Optional)
```bash
source venv/bin/activate
python scripts/setup_database.py
```

## 🏗️ Running the Application

### Start Backend Server
```bash
# Activate environment
source venv/bin/activate

# Start FastAPI server
python main.py
```

Backend will be available at: http://localhost:8000
API Documentation: http://localhost:8000/docs

### Start Frontend (New Terminal)
```bash
cd frontend
npm run dev
```

Frontend will be available at: http://localhost:3000

## 🔍 Verification Checklist

### ✅ Backend Verification
1. Visit http://localhost:8000/health
2. Should return: `{"status": "healthy", "timestamp": "..."}`
3. Visit http://localhost:8000/docs for API documentation

### ✅ Frontend Verification  
1. Visit http://localhost:3000
2. Should see the Confluence Enhancer AI dashboard
3. All tabs should be accessible

### ✅ API Integration Verification
1. Go to "Content Analysis" tab
2. Enter a Confluence URL
3. Click "Analyze Content"
4. Should see AI analysis results

## 🔧 Troubleshooting

### Common Issues

#### 1. **Import Error: oracledb**
```bash
# Install Oracle client libraries
pip install oracledb[thick]
```

#### 2. **OpenAI API Rate Limits**
- Check your OpenAI account billing
- Verify API key is active
- Consider using lower rate limits in development

#### 3. **Confluence Authentication Failed**
- Verify your API token is correct
- Check if username matches token owner
- Ensure Confluence URL is correct

#### 4. **Frontend Build Errors**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

#### 5. **Python Module Not Found**
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall requirements
pip install -r requirements.txt
```

### Debug Mode
Enable debug mode for detailed error messages:
```bash
# In .env file
DEBUG=true
LOG_LEVEL=DEBUG
```

## 📊 Next Steps

Once everything is running:

1. **Test Basic Functionality**
   - Analyze a Confluence page
   - Generate visualizations
   - Review modernization suggestions

2. **Configure Advanced Features**
   - Set up Redis for caching (optional)
   - Configure email notifications
   - Set up monitoring

3. **Production Deployment**
   - Review `docker-compose.yml`
   - Set up CI/CD pipeline
   - Configure production environment

## 🆘 Getting Help

### Resources
- **Documentation**: See `DEVELOPMENT.md` for detailed implementation info
- **API Reference**: http://localhost:8000/docs (when running)
- **Issue Tracker**: Create GitHub issues for bugs
- **Configuration**: See `.env.development` for all options

### Support Channels
1. Check `logs/confluence_enhancer.log` for error details
2. Run diagnostic scripts:
   ```bash
   python scripts/setup_apis.py
   python test_backend.py
   ```
3. Review the detailed setup logs in the terminal

## 🎉 Success!

If all verification steps pass, congratulations! You now have:
- ✅ Fully configured development environment
- ✅ Working API integrations
- ✅ Functional frontend and backend
- ✅ Database setup (if chosen)
- ✅ Ready for real-world Confluence analysis

**You're ready to start analyzing Confluence content with AI! 🚀**

---

*For detailed implementation information, see `DEVELOPMENT.md`*
*For production deployment, see the Docker configuration files*
