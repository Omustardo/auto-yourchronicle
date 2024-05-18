#!/bin/bash

# Exit if any command fails.
set -e

# Check if virtual environment directory exists
if [ ! -d "src/venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv src/venv
fi

# Start the python virtual environment.
source ./src/venv/bin/activate

# Install the list of dependencies.
pip3 install -r ./src/requirements.txt

# Run the program.
# -u is unbuffered mode, to ensure print statements output immediately.
python3 -u ./src/main.py
