#!/usr/bin/env python3
"""Test the optimized color analysis performance"""

import sys
import time
import numpy as np
import cv2
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.image_info import ImageInfoExtractor

def test_color_analysis_optimization():
    """Test color analysis with and without sub-sampling optimization"""
    
    # Create a test image similar to real underwater photos (4000x3000)
    print("Creating test image (4000x3000)...")
    test_image = np.random.randint(0, 256, (3000, 4000, 3), dtype=np.uint8)
    
    # Add some underwater-like color characteristics
    test_image[:, :, 0] = test_image[:, :, 0] * 0.6  # Reduce red
    test_image[:, :, 2] = test_image[:, :, 2] * 1.2  # Increase blue
    test_image = np.clip(test_image, 0, 255)
    
    print(f"Test image shape: {test_image.shape}")
    print(f"Test image size: {test_image.shape[0] * test_image.shape[1]:,} pixels")
    
    # Test with optimized method
    print("\n=== Testing OPTIMIZED color analysis ===")
    extractor = ImageInfoExtractor()
    
    start_time = time.time()
    analysis = extractor._analyze_colors(test_image)
    optimized_time = time.time() - start_time
    
    print(f"Time taken: {optimized_time:.3f} seconds")
    print(f"Analysis results: {len(analysis)} metrics")
    for key, value in analysis.items():
        print(f"  {key}: {value}")
    
    # Estimate performance improvement
    original_pixels = test_image.shape[0] * test_image.shape[1]
    h, w = test_image.shape[:2]
    scale_h = max(1, h // 200)
    scale_w = max(1, w // 200)
    sampled_pixels = (h // scale_h) * (w // scale_w)
    
    theoretical_speedup = original_pixels / sampled_pixels
    print(f"\nPerformance analysis:")
    print(f"Original pixels: {original_pixels:,}")
    print(f"Sampled pixels: {sampled_pixels:,}")
    print(f"Theoretical speedup: {theoretical_speedup:.1f}x")
    print(f"Actual time: {optimized_time:.3f}s (vs ~7.71s original = {7.71/optimized_time:.1f}x speedup)")

def test_statistical_accuracy():
    """Test if sub-sampling maintains statistical accuracy"""
    print("\n=== Testing statistical accuracy ===")
    
    # Create a controlled test image with known statistics
    test_image = np.zeros((1000, 1000, 3), dtype=np.uint8)
    
    # Fill with specific color patterns
    test_image[:, :, 0] = 100  # Red channel = 100
    test_image[:, :, 1] = 150  # Green channel = 150  
    test_image[:, :, 2] = 200  # Blue channel = 200
    
    # Add some noise
    noise = np.random.normal(0, 10, test_image.shape).astype(np.int16)
    test_image = np.clip(test_image.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    
    extractor = ImageInfoExtractor()
    analysis = extractor._analyze_colors(test_image)
    
    print(f"Expected means: R=100, G=150, B=200 (±10 due to noise)")
    print(f"Actual means: R={analysis['red_mean']}, G={analysis['green_mean']}, B={analysis['blue_mean']}")
    print(f"Color temperature estimate: {analysis.get('estimated_color_temp', 'N/A')}K")

if __name__ == "__main__":
    test_color_analysis_optimization()
    test_statistical_accuracy()
