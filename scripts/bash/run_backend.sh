#!/bin/bash

set -e

echo "Starting Flask backend..."

cd backend
source .venv/bin/activate
python3 app.py

deactivate