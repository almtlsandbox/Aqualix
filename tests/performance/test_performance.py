#!/usr/bin/env python3
"""
Test script for performance optimization with large images
"""

import cv2
import numpy as np
import time
from image_processing import ImageProcessor

def test_performance_optimization():
    """Test the performance difference between preview and full processing"""
    
    # Create a large test image (5000x4000 similar to user's case)
    large_image = np.random.randint(0, 255, (4000, 5000, 3), dtype=np.uint8)
    print(f"Created test image: {large_image.shape[1]}x{large_image.shape[0]} pixels")
    
    processor = ImageProcessor()
    
    # Test 1: Preview processing (optimized)
    print("\n=== Preview Processing (Optimized) ===")
    start_time = time.time()
    
    original_preview, processed_preview, scale_factor = processor.process_image_for_preview(large_image)
    
    preview_time = time.time() - start_time
    
    print(f"Original size: {large_image.shape[1]}x{large_image.shape[0]}")
    print(f"Preview size: {original_preview.shape[1]}x{original_preview.shape[0]}")
    print(f"Scale factor: {scale_factor:.3f}")
    print(f"Preview processing time: {preview_time:.3f} seconds")
    
    # Test 2: Full resolution processing
    print("\n=== Full Resolution Processing ===")
    start_time = time.time()
    
    processed_full = processor.process_image(large_image)
    
    full_time = time.time() - start_time
    
    print(f"Full resolution processing time: {full_time:.3f} seconds")
    
    # Performance comparison
    print("\n=== Performance Analysis ===")
    if full_time > 0:
        speedup = full_time / preview_time
        print(f"Preview is {speedup:.1f}x faster than full resolution")
        
        pixels_original = large_image.shape[0] * large_image.shape[1]
        pixels_preview = original_preview.shape[0] * original_preview.shape[1]
        pixel_ratio = pixels_original / pixels_preview
        print(f"Pixel ratio: {pixel_ratio:.1f}x fewer pixels in preview")
        
        time_per_pixel_preview = preview_time / pixels_preview * 1e6  # microseconds
        time_per_pixel_full = full_time / pixels_original * 1e6
        
        print(f"Time per pixel (preview): {time_per_pixel_preview:.3f} μs")
        print(f"Time per pixel (full): {time_per_pixel_full:.3f} μs")
        
    # Test 3: Multiple preview updates (simulating UI interaction)
    print("\n=== Multiple Preview Updates (UI Simulation) ===")
    num_updates = 5
    start_time = time.time()
    
    for i in range(num_updates):
        # Simulate parameter change
        processor.parameters['gray_world_percentile'] = 50 + i * 5
        original_preview, processed_preview, scale_factor = processor.process_image_for_preview(large_image)
    
    multi_preview_time = time.time() - start_time
    avg_preview_time = multi_preview_time / num_updates
    
    print(f"Average time per preview update: {avg_preview_time:.3f} seconds")
    print(f"Total time for {num_updates} updates: {multi_preview_time:.3f} seconds")
    
    # What full resolution would take
    estimated_full_time = full_time * num_updates
    print(f"Estimated time if using full resolution: {estimated_full_time:.3f} seconds")
    
    if estimated_full_time > 0:
        ui_speedup = estimated_full_time / multi_preview_time
        print(f"UI responsiveness improved by: {ui_speedup:.1f}x")

if __name__ == "__main__":
    test_performance_optimization()
