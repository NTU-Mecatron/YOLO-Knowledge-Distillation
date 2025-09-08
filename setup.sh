#!/bin/bash
echo "Creating virtual environment and installing packages..."
python3 -m venv kd_venv
source kd_venv/bin/activate
pip install -r requirements.txt
echo "Setup complete. The virtual environment is now active."
