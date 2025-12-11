import requests
import zipfile
import io
import os

# URL of the GitHub repository zip file
repo_url = "https://github.com/guilherme-mariano98/BOSS-SHOP/archive/refs/heads/main.zip"

print("Downloading repository...")
response = requests.get(repo_url)

if response.status_code == 200:
    print("Download completed. Extracting files...")
    
    # Create a ZipFile object
    zip_file = zipfile.ZipFile(io.BytesIO(response.content))
    
    # Extract all contents
    zip_file.extractall(".")
    
    print("Repository extracted successfully!")
else:
    print(f"Failed to download repository. Status code: {response.status_code}")