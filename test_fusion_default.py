#!/usr/bin/env python3
"""
Test to verify that multiscale fusion is disabled by default
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from image_processing import ImageProcessor

def test_fusion_default():
    """Test that fusion is disabled by default"""
    
    print("Testing default fusion state...")
    
    # Create processor
    processor = ImageProcessor()
    
    # Check default parameters
    defaults = processor.get_default_parameters()
    fusion_enabled = defaults.get('multiscale_fusion_enabled', None)
    
    print(f"Default fusion enabled: {fusion_enabled}")
    
    # Check current parameters
    current_fusion = processor.parameters.get('multiscale_fusion_enabled', None)
    print(f"Current fusion enabled: {current_fusion}")
    
    # Verify both are False
    if fusion_enabled is False:
        print("✓ DEFAULT: Fusion is disabled by default")
    else:
        print("✗ DEFAULT: Fusion should be disabled by default")
        
    if current_fusion is False:
        print("✓ CURRENT: Fusion is disabled in current parameters")
    else:
        print("✗ CURRENT: Fusion should be disabled in current parameters")
        
    # Test reset to defaults (create new processor instead)
    processor2 = ImageProcessor()
    after_reset = processor2.parameters.get('multiscale_fusion_enabled', None)
    print(f"After new instance fusion enabled: {after_reset}")
    
    if after_reset is False:
        print("✓ NEW INSTANCE: Fusion remains disabled in new instances")
    else:
        print("✗ NEW INSTANCE: Fusion should be disabled in new instances")
        
    # Summary
    all_correct = (fusion_enabled is False and 
                   current_fusion is False and 
                   after_reset is False)
    
    print("\n" + "="*50)
    if all_correct:
        print("✅ SUCCESS: Fusion is properly disabled by default")
    else:
        print("❌ FAILURE: Fusion default state is incorrect")
    print("="*50)
    
    return all_correct

if __name__ == "__main__":
    test_fusion_default()
