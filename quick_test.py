#!/usr/bin/env python3
"""Quick test of corrected translations."""

from localization import set_language, t

# Test French
set_language('fr')
print(f"Français: '{t('reset_all_parameters')}'")

# Test English
set_language('en') 
print(f"English: '{t('reset_all_parameters')}'")
