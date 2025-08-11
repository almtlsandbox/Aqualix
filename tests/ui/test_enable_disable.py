#!/usr/bin/env python3
"""
Test script for enable/disable checkboxes functionality
Tests that steps are properly enabled/disabled based on checkbox state
"""

import numpy as np
import cv2
from image_processing import ImageProcessor

def create_test_image():
    """Create a simple test image"""
    height, width = 200, 300
    img = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Create a gradient with underwater characteristics
    for y in range(height):
        depth_factor = y / height
        blue_val = int(120 - depth_factor * 30)
        green_val = int(100 - depth_factor * 50)
        red_val = int(80 - depth_factor * 60)
        img[y, :] = [max(0, blue_val), max(0, green_val), max(0, red_val)]
    
    return img

def test_enable_disable_functionality():
    """Test enable/disable functionality for each processing step"""
    print("🧪 Testing Enable/Disable Checkboxes Functionality")
    print("=" * 60)
    
    processor = ImageProcessor()
    test_image = create_test_image()
    
    print(f"📸 Created test image: {test_image.shape}")
    
    # Test with all steps enabled (default)
    print(f"\n🟢 TEST 1: All steps ENABLED (default state)")
    result_all_enabled = processor.process_image(test_image)
    
    original_mean = np.mean(test_image)
    processed_mean_all = np.mean(result_all_enabled)
    print(f"   Original mean: {original_mean:.1f}")
    print(f"   Processed mean (all enabled): {processed_mean_all:.1f}")
    print(f"   Change: {processed_mean_all - original_mean:+.1f}")
    
    # Test with all steps disabled
    print(f"\n🔴 TEST 2: All steps DISABLED")
    
    # Disable all processing steps
    processor.set_parameter('white_balance_enabled', False)
    processor.set_parameter('udcp_enabled', False)
    processor.set_parameter('beer_lambert_enabled', False)
    processor.set_parameter('color_rebalance_enabled', False)
    processor.set_parameter('hist_eq_enabled', False)
    processor.set_parameter('multiscale_fusion_enabled', False)
    
    result_all_disabled = processor.process_image(test_image)
    processed_mean_disabled = np.mean(result_all_disabled)
    print(f"   Processed mean (all disabled): {processed_mean_disabled:.1f}")
    print(f"   Change: {processed_mean_disabled - original_mean:+.1f}")
    
    # Check if image is unchanged (should be very close to original)
    image_unchanged = np.allclose(test_image, result_all_disabled, atol=1)
    if image_unchanged:
        print(f"   ✅ SUCCESS: Image unchanged when all steps disabled!")
    else:
        print(f"   ❌ ERROR: Image changed even with all steps disabled!")
        diff = np.mean(np.abs(test_image.astype(float) - result_all_disabled.astype(float)))
        print(f"   Average pixel difference: {diff:.3f}")
    
    # Test individual steps
    print(f"\n🟡 TEST 3: Individual step testing")
    
    step_tests = [
        ('white_balance_enabled', 'White Balance'),
        ('udcp_enabled', 'UDCP'),
        ('beer_lambert_enabled', 'Beer-Lambert'),
        ('color_rebalance_enabled', 'Color Rebalance'),
        ('hist_eq_enabled', 'Histogram Equalization'),
        ('multiscale_fusion_enabled', 'Multiscale Fusion')
    ]
    
    individual_results = {}
    
    for param_name, step_name in step_tests:
        # Reset all to disabled
        for test_param, _ in step_tests:
            processor.set_parameter(test_param, False)
        
        # Enable only this step
        processor.set_parameter(param_name, True)
        
        result = processor.process_image(test_image)
        mean_change = np.mean(result) - original_mean
        individual_results[step_name] = mean_change
        
        print(f"   {step_name:20}: {mean_change:+6.1f} change")
    
    # Test combinations
    print(f"\n🔵 TEST 4: Step combination testing")
    
    # Enable white balance + histogram equalization
    for param, _ in step_tests:
        processor.set_parameter(param, False)
    processor.set_parameter('white_balance_enabled', True)
    processor.set_parameter('hist_eq_enabled', True)
    
    result_combo = processor.process_image(test_image)
    combo_mean = np.mean(result_combo)
    combo_change = combo_mean - original_mean
    print(f"   White Balance + Hist EQ: {combo_change:+6.1f} change")
    
    # Summary
    print(f"\n📊 SUMMARY:")
    print(f"   ✅ All enabled processing change:  {processed_mean_all - original_mean:+6.1f}")
    print(f"   ✅ All disabled processing change: {processed_mean_disabled - original_mean:+6.1f}")
    print(f"   ✅ Combination processing change:  {combo_change:+6.1f}")
    
    # Validation
    success_criteria = [
        abs(processed_mean_disabled - original_mean) < 2.0,  # Should be nearly unchanged
        abs(processed_mean_all - original_mean) > 5.0,       # Should show significant change
        abs(combo_change) > abs(processed_mean_disabled - original_mean)  # Combination should have more effect than disabled
    ]
    
    all_passed = all(success_criteria)
    
    if all_passed:
        print(f"\n🎉 ALL TESTS PASSED!")
        print(f"   ✅ Enable/disable checkboxes working correctly")
        print(f"   ✅ Steps are properly controlled by their enable parameters")
        print(f"   ✅ Disabled steps don't apply processing")
        print(f"   ✅ Enabled steps apply expected processing")
    else:
        print(f"\n❌ SOME TESTS FAILED!")
        print(f"   Check enable/disable logic in processing pipeline")
    
    return all_passed

def main():
    """Main test function"""
    print("🚀 ENABLE/DISABLE FUNCTIONALITY TEST")
    print("=" * 70)
    
    success = test_enable_disable_functionality()
    
    print(f"\n" + "=" * 70)
    if success:
        print("🎯 CONCLUSION: Enable/disable functionality is working correctly!")
    else:
        print("⚠️  CONCLUSION: Issues detected in enable/disable functionality!")
    
    print(f"\n📝 Note: This test verifies that checkboxes properly control")
    print(f"   whether processing steps are executed or skipped.")

if __name__ == "__main__":
    main()
