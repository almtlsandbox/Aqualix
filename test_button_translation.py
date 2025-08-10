#!/usr/bin/env python3
"""Test script to verify language translations for reset button."""

import sys
from localization import set_language, t

def test_translations():
    """Test the translations for reset button."""
    print("Testing reset button translations...")
    
    # Test French
    print("\n--- Testing French ---")
    set_language('fr')
    
    french_text = t('reset_all_parameters')
    french_tooltip = t('reset_all_parameters_tooltip')
    print(f"French button text: '{french_text}'")
    print(f"French tooltip: '{french_tooltip}'")
    
    # Test English
    print("\n--- Testing English ---")
    set_language('en')
    
    english_text = t('reset_all_parameters')
    english_tooltip = t('reset_all_parameters_tooltip')
    print(f"English button text: '{english_text}'")
    print(f"English tooltip: '{english_tooltip}'")
    
    # Check if translations are different
    if french_text != english_text:
        print(f"\n✓ Translations are different: '{french_text}' vs '{english_text}'")
        return True
    else:
        print(f"\n✗ Translations are the same: '{french_text}' = '{english_text}'")
        return False

if __name__ == "__main__":
    if test_translations():
        print("\n✓ Translation test passed!")
        sys.exit(0)
    else:
        print("\n✗ Translation test failed!")
        sys.exit(1)
