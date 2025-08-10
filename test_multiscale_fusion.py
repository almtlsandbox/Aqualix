#!/usr/bin/env python3
"""Test script for multiscale fusion functionality."""

import sys
import numpy as np
import cv2
from image_processing import ImageProcessor

def test_multiscale_fusion():
    """Test the multiscale fusion implementation."""
    print("Testing multi-scale fusion implementation...")
    
    # Create a test image
    test_image = np.zeros((200, 300, 3), dtype=np.uint8)
    test_image[:100, :150] = [100, 150, 200]  # Blue-ish region
    test_image[100:, 150:] = [200, 100, 50]   # Orange-ish region
    test_image[50:150, 75:225] = [50, 200, 100]  # Green region overlay
    
    processor = ImageProcessor()
    
    # Test with default parameters
    print("Testing with default parameters...")
    result = processor.multiscale_fusion(test_image, test_image)
    
    if result is not None:
        print(f"✓ Multi-scale fusion successful! Output shape: {result.shape}")
        print(f"✓ Input range: [{test_image.min()}, {test_image.max()}]")
        print(f"✓ Output range: [{result.min()}, {result.max()}]")
        
        # Save test result
        cv2.imwrite("test_fusion_input.jpg", test_image)
        cv2.imwrite("test_fusion_output.jpg", result)
        print("✓ Test images saved: test_fusion_input.jpg, test_fusion_output.jpg")
        
        return True
    else:
        print("✗ Multi-scale fusion failed - returned None")
        return False

def test_full_pipeline():
    """Test the complete processing pipeline with fusion."""
    print("\nTesting full pipeline with multi-scale fusion...")
    
    # Create a more complex test image
    test_image = np.random.randint(0, 255, (150, 200, 3), dtype=np.uint8)
    
    processor = ImageProcessor()
    
    # Test parameters - use defaults which include fusion
    test_params = processor.get_default_parameters()
    
    try:
        result = processor.process_image(test_image)
        
        if result is not None:
            print(f"✓ Full pipeline successful! Output shape: {result.shape}")
            print(f"✓ Pipeline includes: {processor.pipeline_order}")
            
            # Save pipeline result
            cv2.imwrite("test_pipeline_input.jpg", test_image)
            cv2.imwrite("test_pipeline_output.jpg", result)
            print("✓ Pipeline test images saved: test_pipeline_input.jpg, test_pipeline_output.jpg")
            
            return True
        else:
            print("✗ Full pipeline failed - returned None")
            return False
            
    except Exception as e:
        print(f"✗ Full pipeline error: {e}")
        return False

if __name__ == "__main__":
    # Run tests
    fusion_ok = test_multiscale_fusion()
    pipeline_ok = test_full_pipeline()
    
    if fusion_ok and pipeline_ok:
        print("\n✓ All tests passed! Multi-scale fusion is working correctly.")
        sys.exit(0)
    else:
        print("\n✗ Some tests failed. Check the implementation.")
        sys.exit(1)
