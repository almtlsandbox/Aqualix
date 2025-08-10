#!/usr/bin/env python3
"""
Test script to verify pipeline description translations
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from image_processing import ImageProcessor
from localization import set_language

def test_pipeline_descriptions():
    """Test pipeline description translations"""
    
    processor = ImageProcessor()
    
    # Test French
    print("=== French Pipeline Descriptions ===")
    set_language('fr')
    pipeline_fr = processor.get_pipeline_description()
    for i, step in enumerate(pipeline_fr, 1):
        print(f"{i}. {step['name']}")
        print(f"   {step['description']}")
        print()
    
    # Test English  
    print("=== English Pipeline Descriptions ===")
    set_language('en')
    pipeline_en = processor.get_pipeline_description()
    for i, step in enumerate(pipeline_en, 1):
        print(f"{i}. {step['name']}")
        print(f"   {step['description']}")
        print()

if __name__ == "__main__":
    test_pipeline_descriptions()
