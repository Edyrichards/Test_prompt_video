#!/usr/bin/env bash
# Basic setup for running the video pipeline
set -e

python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
# Install PyTorch first so xformers can build
pip install torch==2.3.0 torchvision==0.18.0 torchaudio==2.3.0 --extra-index-url https://download.pytorch.org/whl/cpu
# Install remaining dependencies
pip install -r requirements.txt

echo "Environment ready. Activate with 'source venv/bin/activate'"
