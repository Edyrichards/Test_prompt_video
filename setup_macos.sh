#!/usr/bin/env bash
# Setup environment for macOS (Apple Silicon)
set -e

python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
# Install PyTorch with MPS support
pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cpu

pip install -r requirements.txt

echo "Environment ready. Activate with 'source venv/bin/activate'"
