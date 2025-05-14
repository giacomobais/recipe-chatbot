#!/bin/bash
set -e  # Stop on first error

echo "Creating virtual environment..."
python3 -m venv recipes_venv
source recipes_venv/bin/activate  # Activate venv

echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Installing CPU-only PyTorch..."
pip install torch torchvision torchaudio


echo "Setup complete! CPU-only PyTorch installed."
