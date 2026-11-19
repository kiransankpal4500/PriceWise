#!/usr/bin/env bash
# Exit on error
set -o errexit

if [ -f "backend/requirements.txt" ]; then
    pip install --upgrade pip
    pip install -r backend/requirements.txt
else
    pip install --upgrade pip
    pip install -r requirements.txt
fi
