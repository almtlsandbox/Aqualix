#!/usr/bin/env python3
"""
Test reset defaults functionality
"""
import numpy as np
from src.image_processing import ImageProcessor

def test_reset_defaults():
    """Test reset defaults functionality"""
    processor = ImageProcessor()
    
    print("=== Testing Reset Defaults Functionality ===")
    
    # Test 1: Modify some color rebalancing parameters
    print("\n1. Original color rebalancing parameters:")
    print(f"   RR: {processor.get_parameter('color_rebalance_rr')}")
    print(f"   RG: {processor.get_parameter('color_rebalance_rg')}")
    print(f"   Saturation limit: {processor.get_parameter('color_rebalance_saturation_limit')}")
    
    # Modify parameters
    processor.set_parameter('color_rebalance_rr', 0.5)
    processor.set_parameter('color_rebalance_rg', 0.3)
    processor.set_parameter('color_rebalance_saturation_limit', 0.6)
    
    print("\n2. After modifications:")
    print(f"   RR: {processor.get_parameter('color_rebalance_rr')}")
    print(f"   RG: {processor.get_parameter('color_rebalance_rg')}")
    print(f"   Saturation limit: {processor.get_parameter('color_rebalance_saturation_limit')}")
    
    # Reset color rebalancing step
    processor.reset_step_parameters('color_rebalance')
    
    print("\n3. After reset:")
    print(f"   RR: {processor.get_parameter('color_rebalance_rr')}")
    print(f"   RG: {processor.get_parameter('color_rebalance_rg')}")
    print(f"   Saturation limit: {processor.get_parameter('color_rebalance_saturation_limit')}")
    
    # Verify values are back to defaults
    expected_values = {
        'color_rebalance_rr': 1.0,
        'color_rebalance_rg': 0.0,
        'color_rebalance_saturation_limit': 1.0
    }
    
    success = True
    for param, expected in expected_values.items():
        actual = processor.get_parameter(param)
        if actual != expected:
            print(f"   ❌ {param}: expected {expected}, got {actual}")
            success = False
        else:
            print(f"   ✅ {param}: correctly reset to {expected}")
    
    if success:
        print("\n🎉 Reset functionality works correctly!")
    else:
        print("\n❌ Reset functionality has issues!")
    
    return success

if __name__ == "__main__":
    test_reset_defaults()

