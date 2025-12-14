#!/bin/bash

# Dengue Dashboard Setup and Run Script
# For Zamboanga Sibugay Epidemiological Analysis

echo "🦟 Dengue Epidemiological Dashboard Setup"
echo "=========================================="
echo ""

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python3 found: $(python3 --version)"
echo ""

# Check if requirements.txt exists
if [ ! -f "requirements.txt" ]; then
    echo "❌ requirements.txt not found!"
    exit 1
fi

echo "📦 Installing dependencies..."
pip install -q -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo ""

# Check if data file exists
if [ ! -f "sibugay_dengue_cases_dataset.csv" ]; then
    echo "⚠️  Warning: sibugay_dengue_cases_dataset.csv not found!"
    echo "   Please ensure the dataset is in the current directory."
fi

echo ""
echo "🚀 Launching Streamlit Dashboard..."
echo "   The application will open in your default browser"
echo "   If not, navigate to: http://localhost:8501"
echo ""

streamlit run app.py
