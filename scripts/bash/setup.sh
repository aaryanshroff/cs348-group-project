#!/bin/bash

set -e

BACKEND_DIR="backend"
FRONTEND_DIR="frontend"

echo "Starting the development environment setup..."

echo "Setting up the Flask backend..."

cd $BACKEND_DIR
if [ ! -d ".venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv .venv
fi

echo "Activating virtual environment..."
source .venv/bin/activate

echo "Upgrading pip..."
pip install --upgrade pip

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Deactivating virtual environment..."
deactivate

cd ..

echo "Setting up the React frontend with Vite..."

cd $FRONTEND_DIR

echo "Installing Node.js dependencies..."
npm install

cd ..

echo "Development environment setup is complete!"
echo "You can now run ./run_backend.sh and ./run_frontend.sh to start the servers."