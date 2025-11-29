#!/usr/bin/env python3
"""
Test script for signature verification API
"""

import requests
import json
import base64
from PIL import Image
import io

def create_test_signature():
    """Create a simple test signature image"""
    # Create a simple white image with black text
    img = Image.new('RGB', (400, 200), color='white')
    
    # Convert to base64
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    img_data = buffer.getvalue()
    
    # Convert to base64 string
    base64_string = base64.b64encode(img_data).decode('utf-8')
    return f"data:image/png;base64,{base64_string}"

def test_ml_service():
    """Test the ML service endpoints"""
    base_url = "http://localhost:8000"
    
    print("Testing ML Service...")
    
    # Test health check
    try:
        response = requests.get(f"{base_url}/")
        print(f"Health check: {response.status_code}")
        print(f"Response: {response.json()}")
        print()
    except Exception as e:
        print(f"Health check failed: {e}")
        return False
    
    # Test signature verification
    try:
        # Create test signatures
        test_signatures = [create_test_signature() for _ in range(3)]
        
        payload = {
            "signatures": test_signatures,
            "user_id": "test-user-123",
            "signature_type": "student"
        }
        
        response = requests.post(
            f"{base_url}/verify-student-signatures",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Verification test: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Verification ID: {result['verification_id']}")
            print(f"All authentic: {result['all_authentic']}")
            print(f"Flagged indices: {result['flagged_indices']}")
            print(f"Results count: {len(result['results'])}")
            for i, res in enumerate(result['results']):
                print(f"  Signature {i+1}: {'✓' if res['is_authentic'] else '✗'} ({res['confidence']:.2%})")
        else:
            print(f"Error: {response.text}")
        
    except Exception as e:
        print(f"Verification test failed: {e}")
        return False
    
    return True

def test_web_api():
    """Test the web application API"""
    base_url = "http://localhost:3000"
    
    print("\nTesting Web API...")
    
    try:
        # Create test signatures
        test_signatures = [create_test_signature() for _ in range(3)]
        
        payload = {
            "signatures": test_signatures,
            "user_id": "test-user-123",
            "signature_type": "student"
        }
        
        response = requests.post(
            f"{base_url}/api/verify-signatures",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Web API test: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Verification successful")
            print(f"Message: {result.get('message', 'No message')}")
        else:
            print(f"Error: {response.text}")
        
    except Exception as e:
        print(f"Web API test failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("Signature Verification System Test")
    print("=" * 40)
    
    # Test ML service
    ml_success = test_ml_service()
    
    # Test web API (requires authentication, so might fail)
    web_success = test_web_api()
    
    print("\n" + "=" * 40)
    print("Test Results:")
    print(f"ML Service: {'✓ PASS' if ml_success else '✗ FAIL'}")
    print(f"Web API: {'✓ PASS' if web_success else '✗ FAIL (expected if not authenticated)'}")
    
    if ml_success:
        print("\n✅ ML Service is working correctly!")
        print("You can now test the signature verification in the student portal.")
    else:
        print("\n❌ ML Service has issues. Please check:")
        print("1. Is the ML service running on http://localhost:8000?")
        print("2. Is the CNN model file present?")
        print("3. Are all dependencies installed?")

