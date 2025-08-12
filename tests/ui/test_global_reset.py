#!/usr/bin/env python3
"""Test script for global reset functionality."""

import sys
import numpy as np
from src.image_processing import ImageProcessor

def test_global_reset():
    """Test the global reset functionality."""
    print("Testing global reset functionality...")
    
    processor = ImageProcessor()
    
    # Get original default parameters
    original_defaults = processor.get_default_parameters()
    print(f"✓ Got {len(original_defaults)} default parameters")
    
    # Modify some parameters to non-default values
    test_changes = {
        'white_balance_enabled': not original_defaults['white_balance_enabled'],
        'udcp_omega': 0.75,  # Different from default 0.95
        'beer_lambert_red_coeff': 0.30,  # Different from default 0.6
        'color_rebalance_rr': 1.2,  # Different from default 1.0
        'hist_eq_enabled': not original_defaults['hist_eq_enabled'],
        'fusion_contrast_weight': 0.5,  # Different from default 1.0
    }
    
    print("\nModifying parameters to non-default values...")
    for param, new_value in test_changes.items():
        old_value = processor.get_parameter(param)
        processor.set_parameter(param, new_value)
        current_value = processor.get_parameter(param)
        print(f"  {param}: {old_value} → {current_value}")
        
        # Verify change was applied
        if current_value != new_value:
            print(f"✗ Failed to set parameter {param}")
            return False
    
    # Reset all parameters using the method similar to UI
    print("\nResetting all parameters to defaults...")
    default_params = processor.get_default_parameters()
    for param_name, default_value in default_params.items():
        processor.set_parameter(param_name, default_value)
    
    # Verify all parameters are back to defaults
    print("\nVerifying reset was successful...")
    all_reset = True
    for param, expected_value in original_defaults.items():
        current_value = processor.get_parameter(param)
        if current_value != expected_value:
            print(f"✗ Parameter {param} not reset: expected {expected_value}, got {current_value}")
            all_reset = False
        else:
            print(f"  ✓ {param}: {current_value}")
    
    return all_reset

def test_pipeline_after_reset():
    """Test that the processing pipeline works after global reset."""
    print("\n" + "="*50)
    print("Testing pipeline functionality after reset...")
    
    processor = ImageProcessor()
    
    # Create test image
    test_image = np.random.randint(50, 200, (100, 150, 3), dtype=np.uint8)
    
    # Process with default parameters
    try:
        result = processor.process_image(test_image)
        
        if result is not None:
            print(f"✓ Pipeline processing successful after reset!")
            print(f"  Input shape: {test_image.shape}, Output shape: {result.shape}")
            print(f"  Input range: [{test_image.min()}, {test_image.max()}]")
            print(f"  Output range: [{result.min()}, {result.max()}]")
            return True
        else:
            print("✗ Pipeline returned None after reset")
            return False
            
    except Exception as e:
        print(f"✗ Pipeline failed after reset: {e}")
        return False

if __name__ == "__main__":
    # Run tests
    reset_ok = test_global_reset()
    pipeline_ok = test_pipeline_after_reset()
    
    if reset_ok and pipeline_ok:
        print("\n🎉 All global reset tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed.")
        sys.exit(1)

