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
# This could be done with `pip3 install -r ./src/requirements.txt`
#
# It's done in a more complex way in order to reduce spammy logs when packages are already installed.
# https://github.com/pypa/pip/issues/5900#issuecomment-490216395
set -o pipefail; pip install -r ./src/requirements.txt | { grep -v "already satisfied" || :; }

# Run the program.
# -u is unbuffered mode, to ensure print statements output immediately.
python3 -u ./src/main.py
