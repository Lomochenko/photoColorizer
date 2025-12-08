#!/usr/bin/env python3
"""
Download required model files for PhotoColorizer
"""

import os
import sys
import urllib.request
from pathlib import Path

# Model URLs and paths
MODELS = {
    "colorization_deploy_v2.prototxt": {
        "url": "https://raw.githubusercontent.com/richzhang/colorization/master/models/colorization_deploy_v2.prototxt",
        "description": "Caffe model architecture definition"
    },
    "colorization_release_v2.caffemodel": {
        "url": "https://people.eecs.berkeley.edu/~rich.zhang/projects/2016_colorization/files/demo_v2/colorization_release_v2.caffemodel",
        "description": "Pre-trained model weights"
    },
    "pts_in_hull.npy": {
        "url": "https://raw.githubusercontent.com/richzhang/colorization/master/resources/pts_in_hull.npy",
        "description": "Color cluster centers"
    }
}

def download_file(url: str, destination: str, description: str = "") -> bool:
    """Download a file from URL to destination"""
    try:
        print(f"Downloading {description}...")
        print(f"URL: {url}")
        print(f"Destination: {destination}")
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        
        # Download the file
        urllib.request.urlretrieve(url, destination)
        
        # Check if file was downloaded successfully
        if os.path.exists(destination) and os.path.getsize(destination) > 0:
            size = os.path.getsize(destination)
            print(f"✓ Downloaded successfully ({size:,} bytes)")
            return True
        else:
            print(f"✗ Download failed or file is empty")
            return False
            
    except Exception as e:
        print(f"✗ Error downloading {description}: {e}")
        return False

def main():
    """Main function to download all models"""
    
    # Get the script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    models_dir = os.path.join(script_dir, "..", "models")
    
    print("PhotoColorizer Model Downloader")
    print("=" * 50)
    print(f"Models will be saved to: {models_dir}")
    print()
    
    success_count = 0
    total_count = len(MODELS)
    
    for filename, info in MODELS.items():
        destination = os.path.join(models_dir, filename)
        
        # Check if file already exists
        if os.path.exists(destination):
            size = os.path.getsize(destination)
            print(f"✓ {filename} already exists ({size:,} bytes)")
            success_count += 1
            continue
        
        # Download the file
        if download_file(info["url"], destination, info["description"]):
            success_count += 1
        
        print()  # Empty line between downloads
    
    # Summary
    print("=" * 50)
    print(f"Download Summary: {success_count}/{total_count} files ready")
    
    if success_count == total_count:
        print("✓ All models downloaded successfully!")
        print("You can now run the PhotoColorizer application.")
        return 0
    else:
        print("✗ Some models failed to download.")
        print("Please check your internet connection and try again.")
        return 1

if __name__ == "__main__":
    sys.exit(main())