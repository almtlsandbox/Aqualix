#!/usr/bin/env python3
"""
Test script to verify that all translation keys for step titles exist.
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from localization import t, set_language

def test_translations():
    """Test translation keys for both languages"""
    
    translation_keys = [
        'white_balance_step_title',
        'white_balance_step_desc', 
        'udcp_step_title',
        'udcp_step_desc',
        'histogram_equalization_step_title',
        'histogram_equalization_step_desc'
    ]
    
    print("Testing French translations:")
    set_language('fr')
    for key in translation_keys:
        value = t(key)
        print(f"  {key}: '{value}'")
    
    print("\nTesting English translations:")
    set_language('en')
    for key in translation_keys:
        value = t(key)
        print(f"  {key}: '{value}'")

if __name__ == "__main__":
    test_translations()
