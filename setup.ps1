# Setup script for AutoAnalyst-Core (Windows)

Write-Host "🚀 Setting up AutoAnalyst-Core..." -ForegroundColor Cyan
Write-Host ""

# Check Python version
Write-Host "Checking Python version..."
python --version

# Create virtual environment
Write-Host ""
Write-Host "Creating virtual environment..."
python -m venv venv

# Activate virtual environment
Write-Host "Activating virtual environment..."
.\venv\Scripts\Activate.ps1

# Install dependencies
Write-Host ""
Write-Host "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create data directory
Write-Host ""
Write-Host "Creating data directory..."
New-Item -ItemType Directory -Force -Path data | Out-Null

# Copy .env.example to .env if it doesn't exist
if (-not (Test-Path .env)) {
    Write-Host ""
    Write-Host "Creating .env file..."
    Copy-Item .env.example .env
    Write-Host "⚠️  Please edit .env and add your OpenAI API key if you want to use NL query features" -ForegroundColor Yellow
}

# Generate sample data
Write-Host ""
Write-Host "Generating sample data..."
python utils\generate_sample_data.py

Write-Host ""
Write-Host "✅ Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "To start the application:"
Write-Host "  1. Activate the virtual environment: .\venv\Scripts\Activate.ps1"
Write-Host "  2. Run: streamlit run app.py"
Write-Host ""
Write-Host "For NL query features, edit .env and add your OpenAI API key"
