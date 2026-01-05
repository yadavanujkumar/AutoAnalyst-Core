#!/bin/bash
# Setup script for AutoAnalyst-Core

echo "🚀 Setting up AutoAnalyst-Core..."
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create data directory
echo ""
echo "Creating data directory..."
mkdir -p data

# Copy .env.example to .env if it doesn't exist
if [ ! -f .env ]; then
    echo ""
    echo "Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your OpenAI API key if you want to use NL query features"
fi

# Generate sample data
echo ""
echo "Generating sample data..."
python3 utils/generate_sample_data.py

echo ""
echo "✅ Setup complete!"
echo ""
echo "To start the application:"
echo "  1. Activate the virtual environment: source venv/bin/activate"
echo "  2. Run: streamlit run app.py"
echo ""
echo "For NL query features, edit .env and add your OpenAI API key"
