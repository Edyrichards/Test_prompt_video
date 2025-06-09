#!/usr/bin/env bash
# Setup environment for macOS (Apple Silicon)
set -e

python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
# Install PyTorch with MPS support
pip install torch==2.3.0 torchvision==0.18.0 torchaudio==2.3.0 --extra-index-url https://download.pytorch.org/whl/cpu

pip install -r requirements.txt

echo "Environment ready. Activate with 'source venv/bin/activate'"
