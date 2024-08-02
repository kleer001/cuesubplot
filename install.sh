#!/bin/bash

# Function to clean up on failure
cleanup() {
    log "Cleaning up..."
    rm -rf cuesubplot
    rm -rf venv
}

# Function to log messages
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Set up logging
setup_logging() {
    LOG_DIR="./logs"
    mkdir -p "$LOG_DIR"
    LOG_FILE="$LOG_DIR/install.log"
    if [ -f "$LOG_FILE" ]; then
        i=1
        while [ -f "$LOG_DIR/install_$i.log" ]; do
            ((i++))
        done
        LOG_FILE="$LOG_DIR/install_$i.log"
    fi
    touch "$LOG_FILE"
    log "Logging started"
}

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
check_prerequisites() {
    log "Checking prerequisites..."
    if ! command_exists git; then
        log "Error: git is not installed. Please install git and try again."
        exit 1
    fi
    if ! command_exists python3; then
        log "Error: python3 is not installed. Please install python3 and try again."
        exit 1
    fi
}

# Clone the repository
clone_repo() {
    log "Cloning the repository..."
    git clone https://github.com/kleer001/cuesubplot.git
    cd cuesubplot
}

# Set up virtual environment
setup_venv() {
    log "Setting up virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
}

# Create runme.sh script
create_runme_script() {
    log "Creating runme.sh script..."
    cat > runme.sh << EOL
#!/bin/bash
source venv/bin/activate
python stage.py
deactivate
EOL
    chmod +x runme.sh
}

# Main execution
main() {
    setup_logging
    trap cleanup EXIT

    check_prerequisites
    clone_repo
    setup_venv
    create_runme_script

    log "Installation complete. You can now run ./runme.sh to start the program."
    trap - EXIT  # Remove the trap if installation is successful
}

# Run the main function
main
cd cuesubplot
