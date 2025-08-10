#!/usr/bin/env python3
"""
Test script for image subsampling functionality
"""

import cv2
import numpy as np
from image_processing import create_preview_image, ImageProcessor

def test_subsampling():
    """Test the subsampling functionality with different image sizes"""
    
    # Test different image sizes
    test_sizes = [
        (800, 600),    # Small image - should not be subsampled
        (1920, 1080),  # Large image - should be subsampled
        (4000, 3000),  # Very large image - should be heavily subsampled
        (1024, 768),   # Edge case - should not be subsampled
        (1025, 768),   # Just over limit - should be subsampled
    ]
    
    print("Testing image subsampling functionality:\n")
    
    for width, height in test_sizes:
        # Create a test image
        test_image = np.random.randint(0, 255, (height, width, 3), dtype=np.uint8)
        
        # Test subsampling
        preview_image, scale_factor = create_preview_image(test_image, max_size=1024)
        
        preview_height, preview_width = preview_image.shape[:2]
        
        print(f"Original: {width}x{height}")
        print(f"Preview:  {preview_width}x{preview_height}")
        print(f"Scale factor: {scale_factor:.3f}")
        print(f"Max dimension: {max(preview_width, preview_height)}")
        
        # Verify that the max dimension is within limits
        assert max(preview_width, preview_height) <= 1024, f"Preview too large: {max(preview_width, preview_height)}"
        
        # Verify scale factor is correct
        expected_scale = min(1.0, 1024 / max(width, height))
        assert abs(scale_factor - expected_scale) < 0.001, f"Scale factor incorrect: {scale_factor} vs {expected_scale}"
        
        print("✓ Test passed\n")
    
    # Test with ImageProcessor
    print("Testing with ImageProcessor:")
    processor = ImageProcessor()
    
    # Create a large test image
    large_image = np.random.randint(0, 255, (2000, 1500, 3), dtype=np.uint8)
    print(f"Large test image: {large_image.shape[1]}x{large_image.shape[0]}")
    
    # Process for preview
    original_preview, processed_preview, scale_factor = processor.process_image_for_preview(large_image)
    
    print(f"Original preview: {original_preview.shape[1]}x{original_preview.shape[0]}")
    print(f"Processed preview: {processed_preview.shape[1]}x{processed_preview.shape[0]}")
    print(f"Scale factor: {scale_factor:.3f}")
    
    # Verify shapes match
    assert original_preview.shape == processed_preview.shape, "Preview images have different shapes"
    
    # Verify max dimension is within limits
    assert max(original_preview.shape[:2]) <= 1024, "Preview too large"
    
    print("✓ ImageProcessor test passed")
    
    print("\n🎉 All tests passed! Subsampling is working correctly.")

if __name__ == "__main__":
    test_subsampling()
