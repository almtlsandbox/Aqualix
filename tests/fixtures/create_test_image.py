#!/usr/bin/env python3
"""
Quick test to create a test image for quality check testing
"""

import numpy as np
import cv2
from pathlib import Path

def create_simple_test_image():
    """Create a simple test underwater image"""
    # Create a 400x300 test image with typical underwater characteristics
    height, width = 300, 400
    image = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Base underwater blue-green background
    image[:, :, 0] = 40   # Low red (typical underwater attenuation)
    image[:, :, 1] = 100  # Medium green  
    image[:, :, 2] = 160  # High blue (water dominance)
    
    # Add gradient to simulate depth/lighting variation
    for y in range(height):
        brightness_factor = 1.0 - (y / height) * 0.3  # Darker as we go down
        image[y, :, :] = (image[y, :, :] * brightness_factor).astype(np.uint8)
    
    # Add some subject matter
    # Coral-like structure (will trigger red correction when processed)
    cv2.rectangle(image, (50, 50), (120, 90), (60, 80, 100), -1)  # Base coral
    cv2.rectangle(image, (60, 40), (110, 80), (70, 90, 110), -1)  # Highlight
    
    # Fish-like shapes
    cv2.ellipse(image, (200, 150), (35, 18), 0, 0, 360, (80, 120, 140), -1)
    cv2.ellipse(image, (300, 100), (25, 12), 45, 0, 360, (90, 130, 150), -1)
    cv2.ellipse(image, (150, 220), (20, 10), -30, 0, 360, (100, 140, 160), -1)
    
    # Add some texture/noise to make it more realistic
    noise = np.random.randint(-10, 10, (height, width, 3))
    image = np.clip(image.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    
    return image

def main():
    # Create test image
    test_image = create_simple_test_image()
    
    # Save to test_images directory
    test_dir = Path("test_images")
    test_dir.mkdir(exist_ok=True)
    
    output_path = test_dir / "underwater_test.jpg"
    cv2.imwrite(str(output_path), test_image)
    
    print(f"✅ Test image created: {output_path}")
    print(f"   Size: {test_image.shape[1]}x{test_image.shape[0]} pixels")
    print(f"   You can now load this image in Aqualix and test the quality check!")

if __name__ == "__main__":
    main()
