#!/bin/bash

# If either building or populating the sample database fails, we automatically remove the SAMPLE_DB

# Startup the python virtual environment 
source ../.venv/bin/activate

SAMPLE_DB_FILEPATH="./sample_dataset.db"

if [ -f "$SAMPLE_DB_FILEPATH" ]; then
    echo "Sample database already exists, wiping and recreating it..."
    rm "$SAMPLE_DB_FILEPATH"
fi

echo "Building sample database schema..."
python ./sample_db_files/build_sample_db_schema.py
if [ $? -ne 0 ]; then
    echo -e "Failed to build sample database schema!\nWill try to destroy sample db before exiting!"
    rm "$SAMPLE_DB_FILEPATH" 2> /dev/null # If SAMPLE_DB DNE it isn't a problem so don't print error msg
    exit 1
fi

echo "Populating sample database with data..."
python ./sample_db_files/populate_sample_db.py
if [ $? -ne 0 ]; then
    echo -e "Failed to populate sample database!\nWill try to destroy sample db before exiting!"
    rm "$SAMPLE_DB_FILEPATH" 2> /dev/null # If SAMPLE_DB DNE it isn't a problem so don't print error msg
    exit 1
fi

echo "Success!"

# Close the python virtual environment 
deactivate
