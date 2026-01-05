#!/bin/bash
#
# Common bash utilities for install and lauching python tools
#
# This file contains shared functions used by multiple scripts to avoid code duplication.
# Source this file in other scripts using: source "$(dirname "$0")/common_utils.sh"

# Color codes for output (can be reused by sourcing scripts)
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

#
# Check system dependencies
#
check_system_dependencies() {
    local script_name="${1:-Poco Stability Monitor}"

    echo -e "${BLUE}Checking system dependencies...${NC}"

    # Check Python 3
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}Error: python3 not found${NC}"
        echo "Please install Python 3.8+ with: sudo apt install python3"
        return 1
    fi

    # Check venv module
    if ! python3 -c "import venv" 2>/dev/null; then
        echo -e "${RED}Error: venv module not found${NC}"
        echo "Please install it with: sudo apt install python3-venv"
        return 1
    fi

    return 0
}

#
# Setup and activate virtual environment
#
setup_virtual_environment() {
    local venv_dir="$1"
    local requirements_file="$2"

    if [ -z "$venv_dir" ]; then
        echo -e "${RED}Error: Virtual environment directory not specified${NC}"
        return 1
    fi

    if [ -z "$requirements_file" ]; then
        echo -e "${RED}Error: Requirements file not specified${NC}"
        return 1
    fi

    if [ ! -f "$requirements_file" ]; then
        echo -e "${RED}Error: Requirements file not found: $requirements_file${NC}"
        return 1
    fi

    echo -e "${BLUE}Setting up virtual environment...${NC}"

    # Create virtual environment if it doesn't exist
    if [ ! -d "$venv_dir" ]; then
        echo "Creating virtual environment at $venv_dir..."
        python3 -m venv "$venv_dir"
        if [ $? -ne 0 ]; then
            echo -e "${RED}Error: Failed to create virtual environment${NC}"
            return 1
        fi
    fi

    # Activate virtual environment
    if [ -f "$venv_dir/bin/activate" ]; then
        echo "Activating virtual environment..."
        source "$venv_dir/bin/activate"
        if [ $? -ne 0 ]; then
            echo -e "${RED}Error: Failed to activate virtual environment${NC}"
            return 1
        fi
    else
        echo -e "${RED}Error: Virtual environment activation script not found${NC}"
        return 1
    fi

    # Upgrade pip and install dependencies inside venv
    echo "Installing/updating Python dependencies..."
    pip install --upgrade pip > /dev/null 2>&1
    if [ $? -ne 0 ]; then
        echo -e "${YELLOW}Warning: Failed to upgrade pip${NC}"
    fi

    # Try to install requirements inside venv
    echo "Installing from: $requirements_file"
    if ! pip install -r "$requirements_file"; then
        echo -e "${RED}Error: Failed to install requirements from $requirements_file${NC}"
        echo -e "${YELLOW}You can try installing manually with:${NC}"
        echo -e "  source $venv_dir/bin/activate"
        echo -e "  pip install -r $requirements_file"
        return 1
    fi

    echo -e "${GREEN}Virtual environment ready${NC}"
    return 0
}

#
# Print script header
#
print_header() {
    local title="$1"
    local separator_length=${#title}
    local separator=$(printf '=%.0s' $(seq 1 $separator_length))

    echo -e "${BLUE}$title${NC}"
    echo "$separator"
}

#
# Check if we're in the expected directory
#
check_working_directory() {
    local expected_script="$1"
    local script_dir="$(cd "$(dirname "${BASH_SOURCE[1]}")" && pwd)"

    if [ ! -f "$script_dir/$expected_script" ]; then
        echo -e "${RED}Error: $expected_script not found in current directory${NC}"
        echo "Please run this script from the correct directory"
        return 1
    fi

    return 0
}
