#!/usr/bin/env python3
"""
Test script for auto-tune functionality
Tests each step's auto-tune logic with a sample underwater image
"""

import numpy as np
import cv2
from src.image_processing import ImageProcessor

def create_test_underwater_image():
    """Create a synthetic underwater image for testing"""
    # Create a base image with underwater characteristics
    height, width = 400, 600
    
    # Create gradient from blue-green (top) to darker blue (bottom)
    img = np.zeros((height, width, 3), dtype=np.uint8)
    
    for y in range(height):
        # Simulate depth-based color loss
        depth_factor = y / height
        
        # Blue channel (less affected by depth)
        blue_val = int(120 - depth_factor * 40)
        
        # Green channel (moderate loss)
        green_val = int(100 - depth_factor * 60)
        
        # Red channel (strong loss with depth)
        red_val = int(80 - depth_factor * 70)
        
        img[y, :] = [max(0, blue_val), max(0, green_val), max(0, red_val)]
    
    # Add some objects/details
    cv2.circle(img, (150, 100), 30, (60, 80, 40), -1)  # Dark object
    cv2.rectangle(img, (400, 200), (500, 300), (40, 60, 30), -1)  # Another object
    
    # Add some noise for realism
    noise = np.random.normal(0, 10, img.shape).astype(np.int16)
    img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    
    return img

def test_auto_tune_step(processor, step_key, test_image):
    """Test auto-tune for a specific step"""
    print(f"\n=== Testing Auto-Tune: {step_key} ===")
    
    # Get original parameters
    original_params = {}
    param_info = processor.get_parameter_info()
    step_configs = {
        'white_balance': ['white_balance_method', 'gray_world_percentile', 'gray_world_max_adjustment', 'lake_green_reduction'],
        'udcp': ['udcp_omega', 'udcp_t0', 'udcp_window_size', 'udcp_enhance_contrast'],
        'beer_lambert': ['beer_lambert_depth_factor', 'beer_lambert_red_coeff', 'beer_lambert_green_coeff', 'beer_lambert_enhance_factor'],
        'color_rebalance': ['color_rebalance_rr', 'color_rebalance_gg', 'color_rebalance_bb', 'color_rebalance_saturation_limit'],
        'histogram_equalization': ['hist_eq_clip_limit', 'hist_eq_tile_grid_size'],
        'multiscale_fusion': ['fusion_laplacian_levels', 'fusion_contrast_weight', 'fusion_saturation_weight', 'fusion_exposedness_weight']
    }
    
    if step_key in step_configs:
        for param_name in step_configs[step_key]:
            if param_name in param_info:
                original_params[param_name] = processor.get_parameter(param_name)
    
    # Perform auto-tune
    try:
        optimized_params = processor.auto_tune_step(step_key, test_image)
        
        if optimized_params:
            print(f"✅ Auto-tune successful! Optimized {len(optimized_params)} parameters:")
            for param_name, value in optimized_params.items():
                original_val = original_params.get(param_name, "N/A")
                print(f"  • {param_name}: {original_val} → {value}")
            return True
        else:
            print("❌ Auto-tune returned no parameters")
            return False
            
    except Exception as e:
        print(f"❌ Auto-tune failed: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 Testing Aqualix Auto-Tune System")
    print("=" * 50)
    
    # Create processor and test image
    processor = ImageProcessor()
    test_image = create_test_underwater_image()
    
    print(f"📸 Created synthetic underwater image: {test_image.shape}")
    print(f"   Color characteristics: R={np.mean(test_image[:,:,2]):.1f}, "
          f"G={np.mean(test_image[:,:,1]):.1f}, B={np.mean(test_image[:,:,0]):.1f}")
    
    # Test each auto-tune step
    steps_to_test = [
        'white_balance',
        'udcp', 
        'beer_lambert',
        'color_rebalance',
        'histogram_equalization',
        'multiscale_fusion'
    ]
    
    results = {}
    for step in steps_to_test:
        results[step] = test_auto_tune_step(processor, step, test_image)
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 AUTO-TUNE TEST RESULTS:")
    successful_tests = sum(results.values())
    total_tests = len(results)
    
    for step, success in results.items():
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"  {step:<20} {status}")
    
    print(f"\n🎯 Overall Success Rate: {successful_tests}/{total_tests} ({100*successful_tests/total_tests:.1f}%)")
    
    if successful_tests == total_tests:
        print("🎉 All auto-tune tests passed successfully!")
    else:
        print("⚠️  Some auto-tune tests failed. Check implementation.")

if __name__ == "__main__":
    main()

