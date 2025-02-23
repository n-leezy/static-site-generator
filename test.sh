#!/bin/bash

# Print Python version and location
echo "Using Python at: $(which python3)"
echo "Python version: $(python3 --version)"

# Ensure PYTHONPATH includes the current directory
export PYTHONPATH="${PYTHONPATH:-.}:$(pwd)"

# Clear potentially problematic Python environment variables
unset PYTHONHOME

# Run the tests
python3 -m unittest discover -s src