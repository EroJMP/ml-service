import requests
import os
import sys
from pathlib import Path

API_URL = "http://localhost:8000"

def test_api_connection():
    """Test if the API is running."""
    try:
        response = requests.get(f"{API_URL}/")
        if response.status_code == 200:
            print("✅ API is running")
            return True
        else:
            print(f"❌ API returned status code {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the API. Make sure it's running.")
        return False

def test_single_signature(image_path):
    """Test verifying a single signature."""
    if not os.path.exists(image_path):
        print(f"❌ Image file not found: {image_path}")
        return False
    
    try:
        with open(image_path, "rb") as f:
            files = {"file": (os.path.basename(image_path), f, "image/jpeg")}
            response = requests.post(f"{API_URL}/verify-signature", files=files)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Signature verification successful:")
            print(f"   - Filename: {result['filename']}")
            print(f"   - Is authentic: {result['is_authentic']}")
            print(f"   - Confidence: {result['confidence']:.2f}")
            return True
        else:
            print(f"❌ API returned status code {response.status_code}")
            print(response.json())
            return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def main():
    """Run tests."""
    if not test_api_connection():
        sys.exit(1)
    
    # Test single signature verification
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        test_single_signature(image_path)
    else:
        print("No image path provided for testing. Usage: python test_api.py <image_path>")

if __name__ == "__main__":
    main() 