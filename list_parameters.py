#!/usr/bin/env python3
"""List all available parameters for testing."""

from image_processing import ImageProcessor

def list_parameters():
    """List all available parameters."""
    processor = ImageProcessor()
    defaults = processor.get_default_parameters()
    
    print("Available parameters:")
    for param_name, default_value in sorted(defaults.items()):
        print(f"  '{param_name}': {default_value}")

if __name__ == "__main__":
    list_parameters()
