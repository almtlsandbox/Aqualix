#!/usr/bin/env python3
"""
Test script for white balance methods
Tests all four white balance algorithms with different parameters
"""

import sys
import numpy as np
import cv2
from pathlib import Path

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

from src.image_processing import ImageProcessor

def create_test_image():
    """Create a test image with color cast"""
    # Create a simple test image with different colors
    image = np.zeros((300, 400, 3), dtype=np.uint8)
    
    # Add some colored regions
    image[50:150, 50:150] = [100, 100, 200]  # Blue-ish
    image[50:150, 200:300] = [200, 100, 100]  # Red-ish
    image[150:250, 50:150] = [100, 200, 100]  # Green-ish
    image[150:250, 200:300] = [150, 150, 150]  # Gray
    
    # Add some white regions
    image[50:100, 320:370] = [220, 200, 180]  # Warm white
    image[100:150, 320:370] = [180, 200, 220]  # Cool white
    
    # Add color cast (warm/yellowish)
    cast = np.array([1.2, 1.1, 0.8])
    image = (image.astype(np.float32) * cast).clip(0, 255).astype(np.uint8)
    
    return image

def test_white_balance_methods():
    """Test all white balance methods"""
    print("Testing White Balance Methods")
    print("=" * 40)
    
    # Create test image
    test_image = create_test_image()
    print(f"Created test image: {test_image.shape}")
    
    # Initialize processor
    processor = ImageProcessor()
    
    # Test each method
    methods = ['gray_world', 'white_patch', 'shades_of_gray', 'grey_edge']
    
    for method in methods:
        print(f"\nTesting {method}...")
        try:
            # Configure method
            processor.set_parameter('white_balance_method', method)
            processor.set_parameter('white_balance_enabled', True)
            
            # Process image
            result = processor.apply_white_balance(test_image)
            
            # Basic validation
            assert result.shape == test_image.shape, f"Shape mismatch for {method}"
            assert result.dtype == test_image.dtype, f"Dtype mismatch for {method}"
            
            # Check if processing actually changed the image
            if np.array_equal(result, test_image):
                print(f"  WARNING: {method} returned unchanged image")
            else:
                print(f"  ✓ {method} processed successfully")
                
            # Calculate some basic stats
            original_means = np.mean(test_image, axis=(0,1))
            result_means = np.mean(result, axis=(0,1))
            
            print(f"    Original RGB means: {original_means}")
            print(f"    Result RGB means: {result_means}")
            print(f"    Change: {result_means - original_means}")
            
        except Exception as e:
            print(f"  ✗ Error testing {method}: {e}")
    
    # Test pipeline
    print(f"\nTesting complete pipeline...")
    try:
        processor.set_parameter('hist_eq_enabled', True)
        result = processor.process_image(test_image)
        print(f"  ✓ Complete pipeline processed successfully")
    except Exception as e:
        print(f"  ✗ Error in complete pipeline: {e}")
    
    # Test parameter info
    print(f"\nTesting parameter info...")
    try:
        param_info = processor.get_parameter_info()
        wb_methods = [p for p in param_info if 'white_balance' in p]
        print(f"  ✓ Found {len(wb_methods)} white balance parameters")
        
        for method in methods:
            method_params = [p for p in param_info if method in p]
            print(f"    {method}: {len(method_params)} parameters")
            
    except Exception as e:
        print(f"  ✗ Error getting parameter info: {e}")
    
    # Test pipeline description
    print(f"\nTesting pipeline description...")
    try:
        desc = processor.get_pipeline_description()
        print(f"  ✓ Pipeline has {len(desc)} steps")
        for i, step in enumerate(desc):
            print(f"    {i+1}. {step['name']}")
    except Exception as e:
        print(f"  ✗ Error getting pipeline description: {e}")

if __name__ == "__main__":
    test_white_balance_methods()
    print("\nTest completed!")

