#!/usr/bin/env bash
# 🚀 Setup environment for macOS (Apple Silicon)
set -e

# Step 1: Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Step 2: Upgrade pip
pip install --upgrade pip

# Step 3: Install PyTorch with MPS support (Apple Silicon)
pip install torch==2.3.0 torchvision==0.18.0 torchaudio==2.3.0 --extra-index-url https://download.pytorch.org/whl/cpu

# Step 4: Install project dependencies
pip install -r requirements.txt

# Done!
echo "✅ Environment setup complete."
echo "👉 To activate later, run: source venv/bin/activate"
