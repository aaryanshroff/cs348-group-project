$ErrorActionPreference = "Stop"

$BACKEND_DIR = "backend"
$FRONTEND_DIR = "frontend"

Write-Host "Starting the development environment setup..."

Write-Host "Setting up the Flask backend..."

Set-Location $BACKEND_DIR
if (-not (Test-Path ".venv")) {
    Write-Host "Creating Python virtual environment..."
    python -m venv .venv
}

Write-Host "Activating virtual environment..."
.\.venv\Scripts\Activate.ps1

Write-Host "Upgrading pip..."
python -m pip install --upgrade pip

Write-Host "Installing Python dependencies..."
pip install -r requirements.txt

Write-Host "Deactivating virtual environment..."
deactivate

Set-Location ..

Write-Host "Setting up the React frontend with Vite..."

Set-Location $FRONTEND_DIR

Write-Host "Installing Node.js dependencies..."
npm install

Set-Location ..

Write-Host "Development environment setup is complete!"
Write-Host "You can now run ./run_backend.ps1 and ./run_frontend.ps1 to start the servers."