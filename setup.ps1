Write-Host "Creating virtual environment and installing packages..."
python -m venv kd_venv
& ".\kd_venv\Scripts\pip.exe" install -r requirements.txt
Write-Host "Setup complete. To activate the environment, run: .\kd_venv\Scripts\Activate.ps1"
