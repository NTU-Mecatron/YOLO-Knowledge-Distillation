#!/bin/bash

# Function to check Python version
check_python_version() {
    python3 -c 'import sys; exit(0) if sys.version_info >= (3, 12) else exit(1)'
    return $?
}

# Check for Python 3.12+
if ! check_python_version; then
    echo "Error: Python 3.12 or newer is required."
    echo "Please install a compatible Python version and ensure 'python3' points to it."
    exit 1
fi

# Check if the virtual environment directory exists
if [ ! -d "kd_venv" ]; then
    echo "Creating virtual environment 'kd_venv'..."
    # Create the virtual environment
    python3 -m venv kd_venv
    if [ $? -eq 0 ]; then
        echo "Virtual environment created successfully."
    else
        echo "Failed to create virtual environment. Please ensure 'python3-venv' is installed."
        exit 1
    fi
else
    echo "Virtual environment 'kd_venv' already exists."
fi

# Activate the virtual environment and install requirements
echo "Activating virtual environment and installing requirements..."
source kd_venv/bin/activate
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "Requirements installed successfully."
    echo "To activate the virtual environment in your terminal, run:"
    echo "source kd_venv/bin/activate"
else
    echo "Failed to install requirements."
    exit 1
fi

echo "Setup complete."
