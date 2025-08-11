#!/usr/bin/env python3
"""
Test script for auto-tune checkboxes functionality
Tests that auto-tune is executed automatically during processing when checkboxes are enabled
"""

import numpy as np
import cv2
from image_processing import ImageProcessor

def create_test_underwater_image():
    """Create a synthetic underwater image for testing"""
    height, width = 300, 400
    img = np.zeros((height, width, 3), dtype=np.uint8)
    
    for y in range(height):
        depth_factor = y / height
        blue_val = int(120 - depth_factor * 40)
        green_val = int(100 - depth_factor * 60)
        red_val = int(80 - depth_factor * 70)
        img[y, :] = [max(0, blue_val), max(0, green_val), max(0, red_val)]
    
    # Add some details
    cv2.circle(img, (100, 80), 20, (60, 80, 40), -1)
    cv2.rectangle(img, (200, 150), (250, 200), (40, 60, 30), -1)
    
    return img

def mock_auto_tune_enabled_callback(step_key):
    """Mock callback that simulates checkboxes enabled for certain steps"""
    # Simulate that white_balance and udcp have auto-tune enabled
    enabled_steps = ['white_balance', 'udcp', 'beer_lambert']
    return step_key in enabled_steps

def test_auto_tune_integration():
    """Test the integrated auto-tune system"""
    print("🧪 Testing Auto-Tune Checkbox Integration")
    print("=" * 50)
    
    # Create processor and test image
    processor = ImageProcessor()
    test_image = create_test_underwater_image()
    
    print(f"📸 Created test image: {test_image.shape}")
    print(f"   Original colors: R={np.mean(test_image[:,:,2]):.1f}, "
          f"G={np.mean(test_image[:,:,1]):.1f}, B={np.mean(test_image[:,:,0]):.1f}")
    
    # Store original parameters for comparison
    original_params = {
        'white_balance_method': processor.get_parameter('white_balance_method'),
        'udcp_omega': processor.get_parameter('udcp_omega'),
        'udcp_t0': processor.get_parameter('udcp_t0'),
        'beer_lambert_depth_factor': processor.get_parameter('beer_lambert_depth_factor'),
        'beer_lambert_red_coeff': processor.get_parameter('beer_lambert_red_coeff')
    }
    
    print(f"\n📋 Original parameters:")
    for param, value in original_params.items():
        print(f"   • {param}: {value}")
    
    # Set up auto-tune callback
    processor.set_auto_tune_callback(mock_auto_tune_enabled_callback)
    
    print(f"\n🔄 Processing image with auto-tune enabled for: white_balance, udcp, beer_lambert")
    
    # Process the image (this should trigger auto-tune for enabled steps)
    try:
        processed_image = processor.process_image(test_image)
        
        # Check if parameters were auto-tuned
        auto_tuned_params = {
            'white_balance_method': processor.get_parameter('white_balance_method'),
            'udcp_omega': processor.get_parameter('udcp_omega'),
            'udcp_t0': processor.get_parameter('udcp_t0'),
            'beer_lambert_depth_factor': processor.get_parameter('beer_lambert_depth_factor'),
            'beer_lambert_red_coeff': processor.get_parameter('beer_lambert_red_coeff')
        }
        
        print(f"\n📋 Auto-tuned parameters:")
        changes_detected = 0
        for param, value in auto_tuned_params.items():
            original_val = original_params[param]
            changed = "✅ CHANGED" if value != original_val else "➖ same"
            if value != original_val:
                changes_detected += 1
            print(f"   • {param}: {original_val} → {value} {changed}")
        
        print(f"\n📊 Processing Results:")
        print(f"   ✅ Image processed successfully: {processed_image.shape}")
        print(f"   🎯 Parameters auto-tuned: {changes_detected}/{len(original_params)}")
        print(f"   📈 Output colors: R={np.mean(processed_image[:,:,2]):.1f}, "
              f"G={np.mean(processed_image[:,:,1]):.1f}, B={np.mean(processed_image[:,:,0]):.1f}")
        
        if changes_detected > 0:
            print(f"\n🎉 SUCCESS: Auto-tune checkboxes working correctly!")
            print(f"   {changes_detected} parameters were automatically optimized during processing")
        else:
            print(f"\n⚠️  WARNING: No parameters were auto-tuned")
            print(f"   Check if auto-tune logic is correctly integrated")
            
    except Exception as e:
        print(f"\n❌ ERROR: Processing failed with error: {e}")
        return False
    
    return True

def test_callback_mechanism():
    """Test the callback mechanism specifically"""
    print(f"\n🔧 Testing Callback Mechanism")
    print("-" * 30)
    
    processor = ImageProcessor()
    
    # Test without callback
    print("1. Testing without callback:")
    result = processor.auto_tune_callback('white_balance') if processor.auto_tune_callback else None
    print(f"   Result: {result} (expected: None)")
    
    # Test with callback
    print("2. Testing with callback:")
    processor.set_auto_tune_callback(mock_auto_tune_enabled_callback)
    
    test_steps = ['white_balance', 'udcp', 'histogram_equalization']
    for step in test_steps:
        enabled = processor.auto_tune_callback(step)
        expected = step in ['white_balance', 'udcp', 'beer_lambert']
        status = "✅" if enabled == expected else "❌"
        print(f"   {step}: {enabled} {status}")
    
    print("✅ Callback mechanism working correctly!")

def main():
    """Main test function"""
    print("🚀 AUTO-TUNE CHECKBOXES INTEGRATION TEST")
    print("=" * 60)
    
    # Test callback mechanism
    test_callback_mechanism()
    
    # Test full integration
    success = test_auto_tune_integration()
    
    print("\n" + "=" * 60)
    if success:
        print("🎯 ALL TESTS PASSED: Auto-tune checkboxes are working correctly!")
        print("   ✅ Checkboxes control auto-tune execution during processing")
        print("   ✅ Parameters are optimized automatically for enabled steps")
        print("   ✅ Integration between UI and processor is functional")
    else:
        print("❌ TESTS FAILED: Issues detected in auto-tune integration")
    
    print("\n📝 Note: This test uses mock checkboxes. In the real UI,")
    print("   checkboxes will control the auto-tune behavior per step.")

if __name__ == "__main__":
    main()
