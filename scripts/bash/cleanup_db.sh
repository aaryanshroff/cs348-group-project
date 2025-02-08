#!/bin/bash


# Environment Variables
#
# DB_TYPE: 
#   desc:        use production database or sample?
#   valid input: { "sample", "prod" }
#   defaults:    "sample"

DB_TYPE="${DB_TYPE:-sample}"

# Database filepaths
MAIN_DB_DIR="../../backend/databases"

SAMPLE_DB_DIR="$MAIN_DB_DIR/sample_db"
PROD_DB_DIR="$MAIN_DB_DIR/prod_db"

SAMPLE_DB_FILEPATH="$SAMPLE_DB_DIR/sample_dataset.db"
PROD_DB_FILEPATH="$PROD_DB_DIR/prod_dataset.db"

DB_FILEPATH=""

if [ "$DB_TYPE" = "sample" ]; then
    echo "Cleaning sample database..."
    DB_FILEPATH="$SAMPLE_DB_FILEPATH"
else
    echo "Cleaning production database..."
    DB_FILEPATH="$PROD_DB_FILEPATH"
fi

if [ -f "$DB_FILEPATH" ]; then
    rm "$DB_FILEPATH"
    echo "Cleaned dataset!"
else
    echo "Nothing to clean."
fi
