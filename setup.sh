#!/bin/bash
set -e  # Stop on first error

echo "Creating virtual environment..."
python -m venv recipes_venv
source recipes_venv/bin/activate  # Activate venv

echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Uninstalling CPU torch version if installed..."
pip uninstall -y torch

echo "Installing CUDA-enabled torch..."
pip install torch --index-url https://download.pytorch.org/whl/cu121

echo "Setup complete! CUDA-enabled PyTorch installed."