"""
Mock model for development/testing when TensorFlow can't be installed due to path length issues.
This provides the same interface as the real model but returns random predictions.
"""

import numpy as np
import random

class MockModel:
    """Mock CNN model that simulates signature verification"""
    
    def __init__(self):
        self.loaded = True
        print("Mock model loaded successfully")
    
    def predict(self, img_array):
        """
        Mock prediction that returns random but realistic confidence scores.
        Returns array with shape (1, 2) where:
        - index 0: confidence for "real" signature
        - index 1: confidence for "fake" signature
        """
        # Generate realistic confidence scores
        # Most signatures should be "real" for testing
        real_confidence = random.uniform(0.6, 0.95)  # Usually high confidence for real
        fake_confidence = 1.0 - real_confidence
        
        # Occasionally return a "fake" signature for testing
        if random.random() < 0.2:  # 20% chance of fake
            real_confidence = random.uniform(0.3, 0.6)  # Lower confidence for fake
            fake_confidence = 1.0 - real_confidence
        
        return np.array([[real_confidence, fake_confidence]])
    
    def summary(self):
        """Mock summary method"""
        print("Mock CNN Signature Verification Model")
        print("=" * 40)
        print("Input shape: (None, 224, 224, 3)")
        print("Output shape: (None, 2)")
        print("Classes: [real, fake]")
        print("Note: This is a mock model for development/testing")

def load_mock_model():
    """Load the mock model"""
    return MockModel()

