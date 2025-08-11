#!/usr/bin/env python3
"""
Test script for UDCP (Underwater Dark Channel Prior) functionality
"""

import cv2
import numpy as np
import time
from image_processing import ImageProcessor

def create_underwater_simulation(image):
    """Create a simulated underwater image with haze and color distortion"""
    # Add blue/green tint typical of underwater images
    tinted = image.copy().astype(np.float32) / 255.0
    
    # Reduce red channel (water absorbs red light more)
    tinted[:, :, 0] *= 0.6
    
    # Enhance blue and green channels
    tinted[:, :, 1] *= 1.1  # Green
    tinted[:, :, 2] *= 1.3  # Blue
    
    # Add haze (atmospheric light effect)
    atmospheric_light = np.array([0.4, 0.7, 0.9])  # Blueish underwater light
    transmission = np.random.uniform(0.3, 0.8, image.shape[:2])  # Variable visibility
    transmission = transmission[:, :, np.newaxis]
    
    # Apply haze model: I = J*t + A*(1-t)
    hazed = tinted * transmission + atmospheric_light * (1 - transmission)
    
    # Clip and convert back
    hazed = np.clip(hazed, 0, 1)
    return (hazed * 255).astype(np.uint8)

def test_udcp_functionality():
    """Test the UDCP functionality with various parameters"""
    
    print("=== Testing UDCP (Underwater Dark Channel Prior) ===\n")
    
    # Create a test image
    original_image = np.random.randint(0, 255, (400, 600, 3), dtype=np.uint8)
    
    # Add some structure to make it more realistic
    # Add some bright objects (fish, coral)
    cv2.rectangle(original_image, (100, 100), (200, 200), (255, 200, 100), -1)
    cv2.circle(original_image, (400, 150), 50, (255, 150, 50), -1)
    cv2.rectangle(original_image, (300, 250), (500, 350), (100, 255, 200), -1)
    
    print(f"Created test image: {original_image.shape[1]}x{original_image.shape[0]}")
    
    # Simulate underwater conditions
    underwater_image = create_underwater_simulation(original_image)
    print("Applied underwater simulation (haze + color distortion)")
    
    # Test UDCP with different parameter sets
    processor = ImageProcessor()
    
    test_configs = [
        {
            'name': 'Conservative UDCP',
            'udcp_omega': 0.85,
            'udcp_t0': 0.15,
            'udcp_window_size': 15,
            'udcp_enhance_contrast': 1.0
        },
        {
            'name': 'Aggressive UDCP',
            'udcp_omega': 0.95,
            'udcp_t0': 0.05,
            'udcp_window_size': 7,
            'udcp_enhance_contrast': 1.5
        },
        {
            'name': 'Balanced UDCP',
            'udcp_omega': 0.90,
            'udcp_t0': 0.10,
            'udcp_window_size': 11,
            'udcp_enhance_contrast': 1.2
        }
    ]
    
    for config in test_configs:
        print(f"\n--- Testing {config['name']} ---")
        
        # Set parameters
        for param, value in config.items():
            if param != 'name':
                processor.set_parameter(param, value)
        
        # Enable UDCP
        processor.set_parameter('udcp_enabled', True)
        processor.set_parameter('white_balance_enabled', False)  # Focus on UDCP only
        processor.set_parameter('hist_eq_enabled', False)
        
        # Process image
        start_time = time.time()
        processed = processor.process_image(underwater_image.copy())
        processing_time = time.time() - start_time
        
        print(f"Processing time: {processing_time:.3f} seconds")
        print(f"Parameters: Omega={config['udcp_omega']}, T0={config['udcp_t0']}, "
              f"Window={config['udcp_window_size']}, Contrast={config['udcp_enhance_contrast']}")
        
        # Calculate some metrics
        original_mean = np.mean(underwater_image, axis=(0, 1))
        processed_mean = np.mean(processed, axis=(0, 1))
        
        print(f"Original mean RGB: [{original_mean[0]:.1f}, {original_mean[1]:.1f}, {original_mean[2]:.1f}]")
        print(f"Processed mean RGB: [{processed_mean[0]:.1f}, {processed_mean[1]:.1f}, {processed_mean[2]:.1f}]")
        
        # Calculate color balance improvement (red channel recovery)
        red_improvement = processed_mean[0] / original_mean[0] if original_mean[0] > 0 else 1
        print(f"Red channel improvement: {red_improvement:.2f}x")
        
        # Check for artifacts (values outside valid range)
        min_val, max_val = processed.min(), processed.max()
        print(f"Output range: [{min_val}, {max_val}] (should be [0, 255])")
        
        if min_val < 0 or max_val > 255:
            print("⚠️  Warning: Output values outside valid range detected!")
        else:
            print("✓ Output values within valid range")
    
    # Test with full pipeline
    print(f"\n--- Testing Full Pipeline (White Balance + UDCP + Histogram Eq) ---")
    
    # Reset to defaults and enable all
    processor = ImageProcessor()
    processor.set_parameter('white_balance_enabled', True)
    processor.set_parameter('udcp_enabled', True)
    processor.set_parameter('hist_eq_enabled', True)
    
    start_time = time.time()
    full_processed = processor.process_image(underwater_image.copy())
    full_time = time.time() - start_time
    
    print(f"Full pipeline processing time: {full_time:.3f} seconds")
    
    # Get pipeline description
    pipeline_desc = processor.get_pipeline_description()
    print(f"Pipeline steps: {len(pipeline_desc)}")
    for step in pipeline_desc:
        print(f"  - {step['name']}")
    
    print("\n✅ UDCP functionality test completed successfully!")

if __name__ == "__main__":
    test_udcp_functionality()
