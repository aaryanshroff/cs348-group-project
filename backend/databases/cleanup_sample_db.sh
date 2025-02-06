#!/bin/bash

# Startup the python virtual environment 
source ../.venv/bin/activate

SAMPLE_DB_FILEPATH="./sample_dataset.db"

if [ -f "$SAMPLE_DB_FILEPATH" ]; then
    echo "Cleaning sample dataset..."
    rm "$SAMPLE_DB_FILEPATH"
    echo "Cleaned sample dataset!"
else
    echo "Nothing to clean."
fi

# Close the python virtual environment 
deactivate
