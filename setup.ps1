# Check if the virtual environment directory exists
if (-not (Test-Path -Path "kd_venv" -PathType Container)) {
    Write-Host "Creating virtual environment 'kd_venv'..."
    # Create the virtual environment
    python -m venv kd_venv
    if ($?) {
        Write-Host "Virtual environment created successfully."
    } else {
        Write-Host "Failed to create virtual environment. Please ensure Python and venv are installed and accessible."
        exit 1
    }
} else {
    Write-Host "Virtual environment 'kd_venv' already exists."
}

# Activate the virtual environment and install requirements
Write-Host "Activating virtual environment and installing requirements..."
# The activation is for the current script's scope. 
# The user will need to activate it manually in their terminal after the script runs.
& ".\\kd_venv\\Scripts\\pip.exe" install -r requirements.txt

if ($?) {
    Write-Host "Requirements installed successfully."
    Write-Host "To activate the virtual environment in your terminal, run:"
    Write-Host ".\kd_venv\Scripts\Activate.ps1"
} else {
    Write-Host "Failed to install requirements."
    exit 1
}

Write-Host "Setup complete."
