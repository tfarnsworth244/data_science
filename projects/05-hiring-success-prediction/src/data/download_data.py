"""
Download real hiring/recruitment dataset from Kaggle.

Uses the 70k+ Job Applicants Data (Human Resource) dataset.
"""

import os
import subprocess
import sys

def download_kaggle_dataset():
    """Download dataset using Kaggle API."""

    print("Downloading 70k+ job applicants dataset from Kaggle...")

    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(script_dir, '../..')
    raw_data_dir = os.path.join(project_root, 'data/raw')

    os.makedirs(raw_data_dir, exist_ok=True)

    try:
        import kaggle
        print("✓ Kaggle API found")
    except ImportError:
        print("Installing Kaggle API...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "kaggle"])
        import kaggle

    dataset_name = "ayushtankha/70k-job-applicants-data-human-resource"

    print(f"Downloading {dataset_name}...")
    print(f"Saving to: {raw_data_dir}")

    try:
        kaggle.api.dataset_download_files(
            dataset_name,
            path=raw_data_dir,
            unzip=True
        )
        print("✓ Dataset downloaded successfully!")

        print("\nFiles in data/raw/:")
        for file in os.listdir(raw_data_dir):
            file_path = os.path.join(raw_data_dir, file)
            if os.path.isfile(file_path):
                size_mb = os.path.getsize(file_path) / (1024 * 1024)
                print(f"  - {file} ({size_mb:.2f} MB)")

        return True

    except Exception as e:
        print(f"\n❌ Error downloading dataset: {e}")
        print(f"\nDataset URL: https://www.kaggle.com/datasets/{dataset_name}")
        return False


if __name__ == "__main__":
    success = download_kaggle_dataset()
    if success:
        print("\n✓ Data download complete!")
    else:
        sys.exit(1)
