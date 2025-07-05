#!/bin/bash

echo "--- Setting up MP4-RAG Project ---"

# 1. Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "Error: Failed to create virtual environment. Please ensure Python 3 is installed." >&2
        exit 1
    fi
    echo "Virtual environment created."
else
    echo "Virtual environment already exists. Skipping creation."
fi

# 2. Activate virtual environment
# Note: This script will activate the venv for its own execution.
# Users will still need to activate it manually for subsequent commands.
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "Error: Failed to activate virtual environment." >&2
    exit 1
fi
echo "Virtual environment activated for setup."

# 3. Install/Upgrade pip
echo "Ensuring pip is up to date..."
pip install --upgrade pip
if [ $? -ne 0 ]; then
    echo "Error: Failed to upgrade pip." >&2
    exit 1
fi

# 4. Install dependencies
if [ -f "requirements.txt" ]; then
    echo "Installing Python dependencies from requirements.txt..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "Error: Failed to install dependencies. Please check requirements.txt and your internet connection." >&2
        exit 1
    fi
    echo "Dependencies installed."
else
    echo "Warning: requirements.txt not found. Skipping dependency installation." >&2
fi

# 5. Prompt for API keys and save to .env
if [ ! -f ".env" ]; then
    touch .env
    echo ".env file created."
fi

# Check and prompt for OPENAI_API_KEY
if ! grep -q "OPENAI_API_KEY" .env; then
    read -p "Enter your OpenAI API Key: " OPENAI_API_KEY_INPUT
    echo "OPENAI_API_KEY='$OPENAI_API_KEY_INPUT'" >> .env
    echo "OPENAI_API_KEY added to .env"
else
    echo "OPENAI_API_KEY already exists in .env. Skipping."
fi

# Check and prompt for GOOGLE_API_KEY
if ! grep -q "GOOGLE_API_KEY" .env; then
    read -p "Enter your Google API Key (for Gemini): " GOOGLE_API_KEY_INPUT
    echo "GOOGLE_API_KEY='$GOOGLE_API_KEY_INPUT'" >> .env
    echo "GOOGLE_API_KEY added to .env"
else
    echo "GOOGLE_API_KEY already exists in .env. Skipping."
fi

echo "--- Setup Complete! ---"
echo "To activate the virtual environment in your current shell, run: source venv/bin/activate"
