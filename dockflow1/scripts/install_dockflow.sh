#!/bin/bash

# =========================================================
# DockFlow Full Dependency Installation Script (WSL / Ubuntu)
# =========================================================

set -e

echo "========================================"
echo "Updating system packages..."
echo "========================================"

sudo apt update
sudo apt upgrade -y

echo "========================================"
echo "Installing basic Linux dependencies..."
echo "========================================"

sudo apt install -y \
    build-essential \
    wget \
    curl \
    git \
    unzip \
    software-properties-common \
    python3 \
    python3-pip \
    python3-venv \
    openbabel \
    fpocket

echo "========================================"
echo "Checking Python..."
echo "========================================"
python3 --version
pip3 --version

echo "========================================"
echo "Installing AutoDock Vina..."
echo "========================================"
if command -v vina &> /dev/null
then
    echo "Vina already installed"
else
    sudo apt install -y autodock-vina || true
    if ! command -v vina &> /dev/null
    then
        echo "Vina not found via apt."
        echo "Please install AutoDock Vina manually if required."
    fi
fi

echo "========================================"
echo "Checking Vina..."
echo "========================================"
if command -v vina &> /dev/null
then
    echo "SUCCESS: vina found"
    vina --help | head -n 5 || true
else
    echo "WARNING: vina still missing"
fi

echo "========================================"
echo "Installing AutoDockTools support..."
echo "========================================"
if command -v prepare_receptor4.py &> /dev/null
then
    echo "prepare_receptor4.py already available"
else
    echo "prepare_receptor4.py not found."
    echo "You must install AutoDockTools manually."
    echo "Usually: sudo apt install autodocktools -y"
    echo "or install MGLTools manually."
fi

echo "========================================"
echo "Creating Python virtual environment..."
echo "========================================"
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate

echo "========================================"
echo "Upgrading pip..."
echo "========================================"
pip install --upgrade pip setuptools wheel

echo "========================================"
echo "Installing Python scientific packages..."
echo "========================================"
pip install -r requirements.txt || true

echo "========================================"
echo "Installing DockFlow package..."
echo "========================================"
pip install -e .

echo "========================================"
echo "Final dependency check"
echo "========================================"
for tool in vina obabel fpocket prepare_receptor4.py
do
    if command -v $tool &> /dev/null
    then
        echo "SUCCESS: $tool found"
    else
        echo "MISSING: $tool"
    fi
done

echo ""
echo "INSTALLATION COMPLETE"
echo "Next step:"
echo "dockflow check"
echo "Then test with:"
echo "dockflow run -pro protein.pdb -lig ligands.csv"
