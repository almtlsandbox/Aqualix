#!/usr/bin/env python3
"""Test script to verify Beer-Lambert depth factor reset functionality"""

import sys
import os

# Add the project root to the Python path to allow proper imports
sys.path.insert(0, os.path.dirname(__file__))

# Import from src package
from src.image_processing import ImageProcessor

def test_beer_lambert_reset():
    """Test that Beer-Lambert depth factor resets to 0.1 (not 10.0)"""
    
    # Create image processor instance
    processor = ImageProcessor()
    
    print("=== Testing Beer-Lambert Reset Functionality ===")
    
    # Check initial parameter value
    initial_value = processor.get_parameter('beer_lambert_depth_factor')
    print(f"1. Initial beer_lambert_depth_factor: {initial_value}")
    
    # Change the parameter to a different value
    test_value = 0.5
    processor.set_parameter('beer_lambert_depth_factor', test_value)
    changed_value = processor.get_parameter('beer_lambert_depth_factor')
    print(f"2. Changed beer_lambert_depth_factor to: {changed_value}")
    
    # Get default parameters (this is what reset uses)
    default_params = processor.get_default_parameters()
    default_depth_factor = default_params.get('beer_lambert_depth_factor')
    print(f"3. Default beer_lambert_depth_factor from get_default_parameters(): {default_depth_factor}")
    
    # Test the expected behavior
    if default_depth_factor == 0.1:
        print("✅ SUCCESS: Beer-Lambert depth factor default is correct (0.1)")
    else:
        print(f"❌ ERROR: Beer-Lambert depth factor default is incorrect ({default_depth_factor}), should be 0.1")
    
    # Simulate a reset by setting parameter to default value
    processor.set_parameter('beer_lambert_depth_factor', default_depth_factor)
    reset_value = processor.get_parameter('beer_lambert_depth_factor')
    print(f"4. After simulated reset: {reset_value}")
    
    if reset_value == 0.1:
        print("✅ SUCCESS: Reset sets depth factor to correct value (0.1)")
        return True
    else:
        print(f"❌ ERROR: Reset sets depth factor to incorrect value ({reset_value}), should be 0.1")
        return False

if __name__ == "__main__":
    success = test_beer_lambert_reset()
    if success:
        print("\n🎉 All tests passed! Beer-Lambert reset functionality is working correctly.")
    else:
        print("\n💥 Tests failed! Beer-Lambert reset functionality needs fixing.")
    
    sys.exit(0 if success else 1)
