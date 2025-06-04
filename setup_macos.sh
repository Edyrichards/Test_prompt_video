#!/usr/bin/env bash
# Setup environment for macOS (Apple Silicon)
set -e

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install PyTorch with MPS (Metal Performance Shaders) support for macOS
pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cpu

# Install project dependencies
pip install -r requirements.txt

echo "✅ Environment setup complete."
echo "👉 Activate with: source venv/bin/activate"
