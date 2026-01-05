#!/bin/bash
#
# Launcher Script for warning_scraper Tool
#

set -e  # Exit on any error

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Source common utilities
source "$SCRIPT_DIR/common_utils.sh"

# Configuration
PROJECT_DIR="$SCRIPT_DIR"
VENV_DIR="$PROJECT_DIR/venv"
REQUIREMENTS_FILE="$PROJECT_DIR/requirements.txt"
MAIN_SCRIPT="warning_scraper.py"

print_header "Warning Scraper Launcher"

# Validate we're in the right directory and files exist
check_working_directory "$MAIN_SCRIPT" || exit 1

# Check system dependencies
check_system_dependencies "Standalone Launcher" || exit 1

# Setup virtual environment
setup_virtual_environment "$VENV_DIR" "$REQUIREMENTS_FILE" || exit 1

# Launch the monitor in standalone mode
echo -e "${GREEN}Launching Warning Scraper...${NC}"
echo "====================================="

# Run the script
if ! python3 "$PROJECT_DIR/warning_scraper.py" "$@"; then
    echo -e "${RED}Warning Scraper exited with an error${NC}"
    exit 1
fi

echo -e "${GREEN}Warning Scraper closed normally${NC}"
