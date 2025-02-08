#!/bin/bash

# Check if docker-compose exists
if command -v docker-compose &> /dev/null; then
    docker-compose up -d --build
else
    # Fallback to local Python if Docker is not available
    source venv/bin/activate
    python torrentino.py
fi

# Check if Python 3.11 is installed
if ! command -v python3.11 &> /dev/null; then
    echo "Python 3.11 is not installed. Installing via brew..."
    brew install python@3.11
    # Add Python 3.11 to PATH
    export PATH="/opt/homebrew/opt/python@3.11/bin:$PATH"
fi

# Remove existing venv if creation failed
if [ -d "venv" ]; then
    echo "Removing existing virtual environment..."
    rm -rf venv
fi

# Create virtual environment
echo "Creating virtual environment..."
python3.11 -m venv venv || {
    echo "Failed to create virtual environment. Trying with --without-pip option..."
    python3.11 -m venv venv --without-pip
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    ./venv/bin/python3 get-pip.py
    rm get-pip.py
}

# Activate virtual environment
source venv/bin/activate || {
    echo "Failed to activate virtual environment"
    exit 1
}

# Upgrade pip
echo "Upgrading pip..."
./venv/bin/pip install --upgrade pip

# Install specific version of python-telegram-bot
echo "Installing python-telegram-bot..."
./venv/bin/pip install python-telegram-bot==13.7

# Install other requirements
echo "Installing other requirements..."
./venv/bin/pip install -r requirements.txt

# Run the bot
echo "Starting the bot..."
./venv/bin/python torrentino.py