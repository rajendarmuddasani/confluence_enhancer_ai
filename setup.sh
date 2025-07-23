#!/bin/bash

# Confluence Enhancer AI - Setup Script
# This script sets up the development environment for Phase 2

set -e  # Exit on any error

echo "🚀 Confluence Enhancer AI - Phase 2 Setup"
echo "=========================================="
echo

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}$1${NC}"
}

# Check if Python is installed
check_python() {
    print_header "Checking Python installation..."
    
    if command -v python3 &> /dev/null; then
        python_version=$(python3 --version | cut -d' ' -f2)
        print_status "Python $python_version is installed"
        
        # Check if version is 3.9 or higher
        python3 -c "import sys; exit(0 if sys.version_info >= (3, 9) else 1)" 2>/dev/null
        if [ $? -eq 0 ]; then
            print_status "Python version is compatible (3.9+)"
        else
            print_error "Python 3.9+ is required. Current version: $python_version"
            exit 1
        fi
    else
        print_error "Python 3 is not installed. Please install Python 3.9+ first."
        exit 1
    fi
}

# Check if Node.js is installed
check_nodejs() {
    print_header "Checking Node.js installation..."
    
    if command -v node &> /dev/null; then
        node_version=$(node --version)
        print_status "Node.js $node_version is installed"
        
        # Check if version is 18 or higher
        node -e "process.exit(process.version.slice(1).split('.')[0] >= 18 ? 0 : 1)" 2>/dev/null
        if [ $? -eq 0 ]; then
            print_status "Node.js version is compatible (18+)"
        else
            print_error "Node.js 18+ is required. Current version: $node_version"
            exit 1
        fi
    else
        print_error "Node.js is not installed. Please install Node.js 18+ first."
        exit 1
    fi
}

# Create Python virtual environment
setup_python_env() {
    print_header "Setting up Python virtual environment..."
    
    if [ ! -d "venv" ]; then
        print_status "Creating virtual environment..."
        python3 -m venv venv
    else
        print_status "Virtual environment already exists"
    fi
    
    print_status "Activating virtual environment..."
    source venv/bin/activate
    
    print_status "Upgrading pip..."
    pip install --upgrade pip
    
    print_status "Installing Python dependencies..."
    pip install -r requirements.txt
    
    print_status "Python environment setup complete!"
}

# Setup frontend dependencies
setup_frontend() {
    print_header "Setting up frontend dependencies..."
    
    if [ -d "frontend" ]; then
        cd frontend
        
        if [ ! -d "node_modules" ]; then
            print_status "Installing Node.js dependencies..."
            npm install
        else
            print_status "Node.js dependencies already installed"
        fi
        
        cd ..
        print_status "Frontend setup complete!"
    else
        print_warning "Frontend directory not found. Skipping frontend setup."
    fi
}

# Create environment file
setup_environment() {
    print_header "Setting up environment configuration..."
    
    if [ ! -f ".env" ]; then
        if [ -f ".env.development" ]; then
            print_status "Copying .env.development to .env..."
            cp .env.development .env
            print_warning "Please edit .env file and add your API keys and database credentials"
        else
            print_error ".env.development template not found!"
            exit 1
        fi
    else
        print_status "Environment file (.env) already exists"
    fi
}

# Create necessary directories
create_directories() {
    print_header "Creating necessary directories..."
    
    directories=(
        "logs"
        "storage"
        "storage/exports"
        "storage/cache"
        "storage/uploads"
        "temp"
    )
    
    for dir in "${directories[@]}"; do
        if [ ! -d "$dir" ]; then
            mkdir -p "$dir"
            print_status "Created directory: $dir"
        else
            print_status "Directory already exists: $dir"
        fi
    done
}

# Test API configuration
test_apis() {
    print_header "Testing API configuration..."
    
    if [ -f "venv/bin/activate" ]; then
        source venv/bin/activate
        
        print_status "Running API configuration test..."
        python scripts/setup_apis.py
    else
        print_warning "Virtual environment not found. Skipping API test."
    fi
}

# Setup database (optional)
setup_database_optional() {
    print_header "Database setup (optional)..."
    
    read -p "Do you want to set up the Oracle database now? (y/N): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        if [ -f "venv/bin/activate" ]; then
            source venv/bin/activate
            
            print_status "Setting up Oracle database..."
            python scripts/setup_database.py
        else
            print_error "Virtual environment not found. Cannot setup database."
        fi
    else
        print_status "Skipping database setup. You can run it later with: python scripts/setup_database.py"
    fi
}

# Display final instructions
show_final_instructions() {
    print_header "Setup Complete! 🎉"
    echo
    print_status "Your Confluence Enhancer AI development environment is ready!"
    echo
    echo "Next steps:"
    echo "1. Edit the .env file with your API keys and database credentials:"
    echo "   - OPENAI_API_KEY=your_openai_key"
    echo "   - CONFLUENCE_BASE_URL=https://your-company.atlassian.net"
    echo "   - CONFLUENCE_API_TOKEN=your_token"
    echo "   - CONFLUENCE_USERNAME=your_username"
    echo "   - ORACLE_PASSWORD=your_db_password"
    echo
    echo "2. Start the backend server:"
    echo "   source venv/bin/activate"
    echo "   python main.py"
    echo
    echo "3. Start the frontend (in a new terminal):"
    echo "   cd frontend"
    echo "   npm run dev"
    echo
    echo "4. Open your browser to http://localhost:3000"
    echo
    echo "For database setup, run: python scripts/setup_database.py"
    echo "For API testing, run: python scripts/setup_apis.py"
    echo
    print_status "Happy coding! 🚀"
}

# Main execution
main() {
    # Check system requirements
    check_python
    check_nodejs
    
    # Setup environment
    setup_python_env
    setup_frontend
    setup_environment
    create_directories
    
    # Test configuration
    test_apis
    
    # Optional database setup
    setup_database_optional
    
    # Show final instructions
    show_final_instructions
}

# Run main function
main
