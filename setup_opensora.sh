#!/usr/bin/env bash
# Minimal Open-Sora setup script for macOS
set -e

# Clone repository if needed
if [ ! -d Open-Sora ]; then
    git clone https://github.com/hpcaitech/Open-Sora
fi
cd Open-Sora

python3 -m venv venv
source venv/bin/activate

# Upgrade pip and install dependencies
pip install --upgrade pip
pip install -v .
pip install xformers==0.0.27.post2 --index-url https://download.pytorch.org/whl/cu121
pip install flash-attn --no-build-isolation

# Optional: download pretrained weights
pip install "huggingface_hub[cli]" modelscope

echo "Run 'huggingface-cli download hpcai-tech/Open-Sora-v2 --local-dir ./ckpts' to fetch the model"
