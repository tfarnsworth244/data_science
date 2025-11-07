#!/bin/bash

# Setup script for Kaggle API and dataset downloads

echo "========================================="
echo "Kaggle API Setup for Portfolio Projects"
echo "========================================="
echo ""

# Check if kaggle is installed
if ! command -v kaggle &> /dev/null; then
    echo "Installing Kaggle API..."
    pip install -q kaggle
    echo "✓ Kaggle API installed"
else
    echo "✓ Kaggle API already installed"
fi

# Check for Kaggle credentials
if [ ! -f ~/.kaggle/kaggle.json ]; then
    echo ""
    echo "⚠️  Kaggle API credentials not found!"
    echo ""
    echo "To set up Kaggle API:"
    echo "1. Go to https://www.kaggle.com/settings"
    echo "2. Scroll to 'API' section"
    echo "3. Click 'Create New Token' (downloads kaggle.json)"
    echo "4. Move the file: mv ~/Downloads/kaggle.json ~/.kaggle/"
    echo "5. Set permissions: chmod 600 ~/.kaggle/kaggle.json"
    echo "6. Re-run this script"
    echo ""
    exit 1
else
    echo "✓ Kaggle API credentials found"
    chmod 600 ~/.kaggle/kaggle.json
fi

echo ""
echo "========================================="
echo "Downloading Datasets for All Projects"
echo "========================================="
echo ""

# Function to download dataset for a project
download_project_data() {
    project_num=$1
    project_name=$2

    echo "[$project_num] $project_name"
    cd "/home/user/data_science/projects/$project_name/src/data"

    if [ -f "download_data.py" ]; then
        python download_data.py
        if [ $? -eq 0 ]; then
            echo "✓ Downloaded successfully"
        else
            echo "❌ Download failed"
        fi
    else
        echo "⚠️  No download script (using generated data)"
    fi

    echo ""
    cd /home/user/data_science
}

# Download data for each project
download_project_data "01" "01-employee-burnout"
download_project_data "02" "02-wellness-optimization"
download_project_data "04" "04-sleep-pattern-analytics"
download_project_data "05" "05-hiring-success-prediction"
download_project_data "06" "06-learning-path-optimization"
download_project_data "10" "10-engagement-cnn"

echo "========================================="
echo "Projects using synthetic data:"
echo "========================================="
echo "03 - Cognitive Bias Detection (limited real data availability)"
echo "07 - Team Composition Analysis (using generated network data)"
echo "08 - Meeting Effectiveness NLP (using generated transcripts)"
echo "09 - Burnout Time Series (using generated longitudinal data)"
echo ""
echo "To generate synthetic data for these projects, run:"
echo "  python projects/XX-project-name/src/data/generate_data.py"
echo ""

echo "========================================="
echo "Setup Complete!"
echo "========================================="
echo ""
echo "Next steps:"
echo "1. Explore the downloaded datasets"
echo "2. Run EDA notebooks for each project"
echo "3. Build models and analyses"
echo ""
