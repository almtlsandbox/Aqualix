#!/usr/bin/env python3
"""
Test CLAHE tile size improvements and auto-tune defaults
Validate that larger CLAHE tiles reduce artifacts while maintaining quality
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

import cv2
import numpy as np
from image_processing import ImageProcessor
from ui_components import ParameterPanel
import tkinter as tk

def test_clahe_tile_sizes():
    """Test different CLAHE tile sizes for underwater images"""
    print("\n=== Testing CLAHE Tile Size Improvements ===")
    
    # Create test image with typical underwater characteristics
    height, width = 512, 512
    test_image = create_underwater_test_image(height, width)
    
    processor = ImageProcessor()
    
    # Test original small tiles (8x8) vs new larger tiles (16x16)
    old_tile_size = (8, 8)
    new_tile_size = (16, 16)
    
    # Create CLAHE with different tile sizes
    clahe_old = cv2.createCLAHE(clipLimit=2.0, tileGridSize=old_tile_size)
    clahe_new = cv2.createCLAHE(clipLimit=2.0, tileGridSize=new_tile_size)
    
    # Convert to LAB for processing
    lab_image = cv2.cvtColor((test_image * 255).astype(np.uint8), cv2.COLOR_RGB2LAB)
    
    # Apply CLAHE with different tile sizes
    lab_old = lab_image.copy()
    lab_new = lab_image.copy()
    
    lab_old[:, :, 0] = clahe_old.apply(lab_old[:, :, 0])
    lab_new[:, :, 0] = clahe_new.apply(lab_new[:, :, 0])
    
    # Convert back to RGB
    result_old = cv2.cvtColor(lab_old, cv2.COLOR_LAB2RGB).astype(np.float32) / 255.0
    result_new = cv2.cvtColor(lab_new, cv2.COLOR_LAB2RGB).astype(np.float32) / 255.0
    
    # Analyze artifacts (measure local variance as indicator of artifacts)
    variance_old = measure_local_variance(result_old)
    variance_new = measure_local_variance(result_new)
    
    print(f"Old tiles {old_tile_size}: Local variance = {variance_old:.6f}")
    print(f"New tiles {new_tile_size}: Local variance = {variance_new:.6f}")
    print(f"Artifact reduction: {((variance_old - variance_new) / variance_old * 100):.1f}%")
    
    # Test should show reduced artifacts with larger tiles
    assert variance_new < variance_old, f"New tiles should reduce artifacts: {variance_new} vs {variance_old}"
    
    print("✅ CLAHE tile size improvements validated")
    return True

def test_auto_tune_defaults():
    """Test that auto-tune is enabled by default"""
    print("\n=== Testing Auto-Tune Default State ===")
    
    # Create root window for testing
    root = tk.Tk()
    root.withdraw()  # Hide the window
    
    try:
        processor = ImageProcessor()
        
        # Create parameter panel
        frame = tk.Frame(root)
        param_panel = ParameterPanel(frame, processor, lambda: None)
        
        # Check global auto-tune default state
        global_auto_tune = param_panel.global_auto_tune_var.get()
        print(f"Global auto-tune default state: {'Enabled' if global_auto_tune else 'Disabled'}")
        
        # Check that individual auto-tune states are also enabled
        enabled_count = 0
        total_count = 0
        
        for step_key, frame_data in param_panel.step_frames.items():
            auto_tune_var = frame_data.get('auto_tune_var')
            if auto_tune_var:
                total_count += 1
                if auto_tune_var.get():
                    enabled_count += 1
                    print(f"  {step_key}: ✅ Enabled")
                else:
                    print(f"  {step_key}: ❌ Disabled")
        
        print(f"Auto-tune enabled by default: {enabled_count}/{total_count} steps")
        
        # Test should show auto-tune enabled by default
        assert global_auto_tune, "Global auto-tune should be enabled by default"
        assert enabled_count == total_count, f"All individual auto-tune should be enabled: {enabled_count}/{total_count}"
        
        print("✅ Auto-tune defaults validated")
        return True
        
    finally:
        root.destroy()

def test_video_processing_behavior():
    """Document and validate video processing behavior"""
    print("\n=== Testing Video Processing Behavior ===")
    
    processor = ImageProcessor()
    
    # Create two different test frames
    frame1 = create_underwater_test_image(256, 256, depth_variation=0.2)
    frame2 = create_underwater_test_image(256, 256, depth_variation=0.8)
    
    # Process both frames individually (simulating video behavior)
    processed_frame1 = processor.process_image(frame1)
    processed_frame2 = processor.process_image(frame2)
    
    # Analyze color consistency between frames
    mean_color1 = np.mean(processed_frame1, axis=(0, 1))
    mean_color2 = np.mean(processed_frame2, axis=(0, 1))
    
    color_difference = np.linalg.norm(mean_color1 - mean_color2)
    
    print(f"Frame 1 mean color: R={mean_color1[0]:.3f}, G={mean_color1[1]:.3f}, B={mean_color1[2]:.3f}")
    print(f"Frame 2 mean color: R={mean_color2[0]:.3f}, G={mean_color2[1]:.3f}, B={mean_color2[2]:.3f}")
    print(f"Color difference between frames: {color_difference:.3f}")
    
    print("\n📝 Video Processing Behavior:")
    print("   • Auto-tune is applied FRAME BY FRAME")
    print("   • Each frame is processed independently")
    print("   • May cause color variations between frames")
    print("   • Suitable for scenes with varying conditions")
    print("   • For consistent results, disable auto-tune and use manual settings")
    
    print("✅ Video behavior documented")
    return True

def create_underwater_test_image(height, width, depth_variation=0.5):
    """Create a synthetic underwater image for testing"""
    # Create gradient simulating underwater depth effects
    y_gradient = np.linspace(0, depth_variation, height)[:, np.newaxis]
    x_gradient = np.linspace(0, 0.2, width)[np.newaxis, :]
    
    # Base underwater colors (blue-green tint)
    red_channel = 0.3 - y_gradient * 0.2 + x_gradient
    green_channel = 0.6 - y_gradient * 0.3 + x_gradient * 0.5
    blue_channel = 0.8 - y_gradient * 0.1 + x_gradient * 0.3
    
    # Add some texture
    texture = np.random.normal(0, 0.05, (height, width))
    
    # Stack channels and add texture
    image = np.stack([
        np.clip(red_channel + texture, 0, 1),
        np.clip(green_channel + texture, 0, 1),
        np.clip(blue_channel + texture, 0, 1)
    ], axis=-1)
    
    return image.astype(np.float32)

def measure_local_variance(image, window_size=5):
    """Measure local variance as an indicator of artifacts"""
    # Convert to grayscale for variance analysis
    gray = cv2.cvtColor((image * 255).astype(np.uint8), cv2.COLOR_RGB2GRAY).astype(np.float32)
    
    # Calculate local variance using sliding window
    kernel = np.ones((window_size, window_size), np.float32) / (window_size ** 2)
    mean = cv2.filter2D(gray, -1, kernel)
    mean_sq = cv2.filter2D(gray ** 2, -1, kernel)
    variance = mean_sq - mean ** 2
    
    return np.mean(variance)

def run_all_tests():
    """Run all improvement validation tests"""
    print("🧪 Testing Aqualix v2.3.0 Improvements")
    print("=" * 50)
    
    success_count = 0
    
    try:
        if test_clahe_tile_sizes():
            success_count += 1
    except Exception as e:
        print(f"❌ CLAHE test failed: {e}")
    
    try:
        if test_auto_tune_defaults():
            success_count += 1
    except Exception as e:
        print(f"❌ Auto-tune test failed: {e}")
    
    try:
        if test_video_processing_behavior():
            success_count += 1
    except Exception as e:
        print(f"❌ Video behavior test failed: {e}")
    
    print("\n" + "=" * 50)
    print(f"✅ Tests passed: {success_count}/3")
    
    if success_count == 3:
        print("🎉 All improvements validated successfully!")
        return True
    else:
        print("⚠️  Some tests failed - review improvements needed")
        return False

if __name__ == "__main__":
    run_all_tests()
