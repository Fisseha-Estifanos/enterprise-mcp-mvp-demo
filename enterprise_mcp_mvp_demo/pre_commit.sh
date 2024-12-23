#!/bin/bash

# Define folders to exclude
# EXCLUDE_FOLDERS="folder_to_exclude|another_folder"
# EXCLUDE_FOLDERS_LIST="folder_to_exclude,another_folder"
EXCLUDE_FOLDERS="mcp_servers"
EXCLUDE_FOLDERS_LIST="mcp_servers,db/v2,db/populate_table.py,db/database.py"
LINE_LENGTH=88

# Run black with exclusions
echo "Running black..."
black . --exclude "$EXCLUDE_FOLDERS" --line-length=$LINE_LENGTH

echo "Running autopep8..."
autopep8 --in-place --recursive .

# Run pylint with exclusions
echo "Running pylint..."
pylint **/*.py --ignore=$EXCLUDE_FOLDERS_LIST

# Run flake8 with exclusions
echo "Running flake8..."
flake8 . --exclude="$EXCLUDE_FOLDERS_LIST" --max-line-length=$LINE_LENGTH