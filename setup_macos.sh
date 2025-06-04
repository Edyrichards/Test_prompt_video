#!/usr/bin/env bash
# 🚀 Setup environment for macOS (Apple Silicon)
set -e

# Step 1: Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Step 2: Upgrade pip
pip install --upgrade pip

# Step 3: Install PyTorch with MPS support (Apple Silicon)
pip install torch==2.3.0 torchvision==0.18.0 torchaudio==2.3.0

# Step 4: Install project dependencies
pip install -r requirements.txt

# Done!
echo "✅ Environment setup complete."
echo "👉 To activate later, run: source venv/bin/activate"

# Step 5: Verify PyTorch MPS (Apple Silicon GPU)
echo "Verifying PyTorch MPS support..."
python3 <<EOF
import torch
if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
    if torch.backends.mps.is_built():
        print("✅ PyTorch MPS is available and built correctly!")
        print("You should be able to leverage your Apple Silicon GPU.")
        # Optional: Small test
        try:
            mps_device = torch.device("mps")
            x = torch.ones(1, device=mps_device)
            print("MPS device test successful.")
        except Exception as e:
            print(f"⚠️ MPS device test failed: {e}")
    else:
        print("⚠️ PyTorch MPS is available but not built correctly. Something might be wrong with your PyTorch installation.")
else:
    print("❌ PyTorch MPS is not available. GPU acceleration will not be used.")
    print("Ensure you are on a Mac with Apple Silicon and have installed PyTorch correctly for MPS.")
EOF
