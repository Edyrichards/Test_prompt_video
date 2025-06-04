#!/usr/bin/env bash
# Basic setup for running the video pipeline
set -e

python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
# Install dependencies pinned in requirements.txt
pip install -r requirements.txt

echo "Environment ready. Activate with 'source venv/bin/activate'"
