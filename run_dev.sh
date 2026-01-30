#!/bin/bash

# Drum Visualization Development Server Script
# Supports multiple development scenarios for the drum visualization project

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_header() {
    echo -e "${BLUE}=== $1 ===${NC}"
}

print_success() {
    echo -e "${GREEN} $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}  $1${NC}"
}

print_error() {
    echo -e "${RED} $1${NC}"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to detect project type
detect_project_type() {
    if [ -f "package.json" ] && [ -f "vite.config.ts" ]; then
        echo "vite"
    elif [ -f "package.json" ] && [ -f "vite.config.js" ]; then
        echo "vite"
    elif [ -f "server.py" ]; then
        echo "python"
    elif [ -f "requirements.txt" ]; then
        echo "python"
    else
        echo "unknown"
    fi
}

# Function to start Vite development server
start_vite_dev() {
    print_header "Starting Vite Development Server"
    
    if ! command_exists npm; then
        print_error "npm is not installed. Please install Node.js and npm first."
        exit 1
    fi
    
    if [ ! -f "package.json" ]; then
        print_error "No package.json found. Please run this script from a project directory."
        exit 1
    fi
    
    # Install dependencies if node_modules doesn't exist
    if [ ! -d "node_modules" ]; then
        print_warning "Installing dependencies..."
        npm install
    fi
    
    print_success "Starting development server..."
    print_warning "Available commands:"
    print_warning "  - npm run dev: Start development server with hot reload"
    print_warning "  - npm run build: Build for production"
    print_warning "  - npm run preview: Preview production build"
    echo
    
    npm run dev
}

# Function to start Python HTTP server
start_python_server() {
    print_header "Starting Python HTTP Server"
    
    if ! command_exists python3 && ! command_exists python; then
        print_error "Python is not installed. Please install Python first."
        exit 1
    fi
    
    # Detect Python command
    if command_exists python3; then
        PYTHON_CMD="python3"
    else
        PYTHON_CMD="python"
    fi
    
    PORT=8000
    if [ ! -z "$1" ]; then
        PORT=$1
    fi
    
    print_success "Starting Python HTTP server on port $PORT"
    print_warning "This server is ideal for OBS integration and static file serving"
    print_warning "Open http://localhost:$PORT/ in your browser"
    echo
    
    $PYTHON_CMD -m http.server $PORT
}

# Function to show project information
show_project_info() {
    print_header "Project Information"
    
    echo "Current directory: $(pwd)"
    echo "Project type: $(detect_project_type)"
    echo
    
    if [ -f "package.json" ]; then
        echo "Package.json found:"
        if command_exists jq; then
            jq -r '.name, .version, .description' package.json 2>/dev/null || cat package.json | head -10
        else
            cat package.json | head -10
        fi
        echo
    fi
    
    if [ -f "README.md" ]; then
        echo "README.md found:"
        head -5 README.md
        echo "..."
        echo
    fi
}

# Function to show help
show_help() {
    print_header "Development Server Options"
    echo
    echo "Usage: $0 [OPTION] [PORT]"
    echo
    echo "Options:"
    echo "  dev, vite    Start Vite development server (for React/TypeScript projects)"
    echo "  python       Start Python HTTP server (for static file serving)"
    echo "  auto         Automatically detect and start appropriate server"
    echo "  info         Show project information"
    echo "  help         Show this help message"
    echo
    echo "Examples:"
    echo "  $0 dev              # Start Vite development server"
    echo "  $0 python           # Start Python server on port 8000"
    echo "  $0 python 3000      # Start Python server on port 3000"
    echo "  $0 auto             # Auto-detect and start server"
    echo "  $0 info             # Show project information"
    echo
    echo "For OBS Integration:"
    echo "  Use 'python' server for serving static files to OBS"
    echo "  Use 'dev' for active development with hot reload"
}

# Main script logic
main() {
    case "${1:-auto}" in
        "dev"|"vite")
            start_vite_dev
            ;;
        "python")
            start_python_server "$2"
            ;;
        "auto")
            PROJECT_TYPE=$(detect_project_type)
            case $PROJECT_TYPE in
                "vite")
                    print_warning "Detected Vite project. Starting development server..."
                    start_vite_dev
                    ;;
                "python")
                    print_warning "Detected Python project. Starting HTTP server..."
                    start_python_server "$2"
                    ;;
                *)
                    print_error "Could not detect project type automatically."
                    print_warning "Please specify: $0 dev (for Vite) or $0 python (for Python server)"
                    echo
                    show_project_info
                    ;;
            esac
            ;;
        "info")
            show_project_info
            ;;
        "help"|"-h"|"--help")
            show_help
            ;;
        *)
            print_error "Unknown option: $1"
            echo
            show_help
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"