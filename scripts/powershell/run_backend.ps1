$ErrorActionPreference = "Stop"

Write-Host "Starting Flask backend..."

Set-Location backend

try {
    ..\.venv\Scripts\Activate.ps1
    python app.py
}
finally {
    deactivate
}