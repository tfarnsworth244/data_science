"""
Download real employee burnout dataset from Kaggle.

Uses the "Are Your Employees Burning Out?" dataset which contains
employee burn rate data for burnout prediction analysis.
"""

import os
import subprocess
import sys

def download_kaggle_dataset():
    """Download dataset using Kaggle API."""

    print("Downloading employee burnout dataset from Kaggle...")

    # Set up paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(script_dir, '../..')
    raw_data_dir = os.path.join(project_root, 'data/raw')

    os.makedirs(raw_data_dir, exist_ok=True)

    # Check if kaggle API is installed
    try:
        import kaggle
        print("✓ Kaggle API found")
    except ImportError:
        print("Installing Kaggle API...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "kaggle"])
        import kaggle

    # Download dataset
    dataset_name = "blurredmachine/are-your-employees-burning-out"

    print(f"Downloading {dataset_name}...")
    print(f"Saving to: {raw_data_dir}")

    try:
        # Download and extract
        kaggle.api.dataset_download_files(
            dataset_name,
            path=raw_data_dir,
            unzip=True
        )
        print("✓ Dataset downloaded successfully!")

        # List files
        print("\n Files in data/raw/:")
        for file in os.listdir(raw_data_dir):
            file_path = os.path.join(raw_data_dir, file)
            if os.path.isfile(file_path):
                size_mb = os.path.getsize(file_path) / (1024 * 1024)
                print(f"  - {file} ({size_mb:.2f} MB)")

        return True

    except Exception as e:
        print(f"\n❌ Error downloading dataset: {e}")
        print("\nPlease ensure:")
        print("1. Kaggle API is configured (~/.kaggle/kaggle.json)")
        print("2. You have accepted the dataset terms on Kaggle")
        print("3. Your internet connection is working")
        print(f"\nDataset URL: https://www.kaggle.com/datasets/{dataset_name}")
        return False


if __name__ == "__main__":
    success = download_kaggle_dataset()

    if success:
        print("\n✓ Data download complete!")
        print("Next steps:")
        print("  1. Explore the data with: jupyter notebook notebooks/")
        print("  2. Run EDA script: python notebooks/01_eda_burnout_analysis.py")
    else:
        print("\n❌ Data download failed. Please download manually and place in data/raw/")
        sys.exit(1)
