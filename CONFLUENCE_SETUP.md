# Confluence API Setup Guide

## 🔐 Setting Up Confluence Authentication

To access your Confluence instance, you need to create an API token. Follow these steps:

### Step 1: Create Confluence API Token

1. **Go to Atlassian Account Settings**
   - Visit: https://id.atlassian.com/manage-profile/security/api-tokens
   - Log in with your Atlassian account

2. **Create API Token**
   - Click "Create API token"
   - Give it a label (e.g., "Confluence Enhancer")
   - Copy the generated token (you won't see it again!)

### Step 2: Update .env File

Edit the `.env` file in your project root with your credentials:

```env
CONFLUENCE_BASE_URL=https://rajendarmuddasani.atlassian.net
CONFLUENCE_USERNAME=your-email@domain.com
CONFLUENCE_API_TOKEN=your-api-token-here
```

**Important**: 
- Use your **email address** as username (not your display name)
- Use the **API token** (not your password)

### Step 3: Test Connection

After updating the .env file, restart your backend server:

```bash
# In terminal, stop the current server (Ctrl+C) then restart:
source .venv/bin/activate
python main.py
```

### Example .env Configuration

```env
# Your specific configuration
CONFLUENCE_BASE_URL=https://rajendarmuddasani.atlassian.net
CONFLUENCE_USERNAME=rajendar.mi46@gmail.com
CONFLUENCE_API_TOKEN=ATATT3xFfGF0123456789abcdef...
SECRET_KEY=supersecretkey123
```

### Step 4: Test Your Setup

Try accessing your page again:
- Frontend: http://localhost:3002
- Enter URL: https://rajendarmuddasani.atlassian.net/wiki/spaces/SD/pages/2949124/Claudee
- Click Submit

### Troubleshooting

If you still get authentication errors:

1. **Check token validity**: Make sure your API token is active
2. **Check email**: Use the exact email address associated with your Atlassian account
3. **Check URL**: Ensure the base URL matches your instance
4. **Check permissions**: Make sure your account has read access to the page

### Security Notes

- Never commit the .env file to version control
- Keep your API token secure
- Regenerate tokens periodically for security

## 🔗 Useful Links

- [Atlassian API Tokens](https://id.atlassian.com/manage-profile/security/api-tokens)
- [Confluence REST API Documentation](https://developer.atlassian.com/cloud/confluence/rest/intro/)
- [API Token Best Practices](https://support.atlassian.com/atlassian-account/docs/manage-api-tokens-for-your-atlassian-account/)
