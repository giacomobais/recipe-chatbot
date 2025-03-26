@echo off
python -m venv recipe_venv
call recipes_venv\Scripts\activate

echo Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt

echo Uninstalling CPU torch version if installed...
pip uninstall -y torch

echo Installing CUDA-enabled torch...
pip install torch --index-url https://download.pytorch.org/whl/cu121

echo Setup complete!