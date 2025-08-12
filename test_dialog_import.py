#!/usr/bin/env python3
"""
Test script for Quality Check Dialog - Tests the dialog import and initialization
"""

import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / 'src'))

def test_dialog_import():
    """Test that the quality check dialog can be imported and initialized"""
    try:
        # Import required modules
        import importlib.util
        from pathlib import Path
        import tkinter as tk
        
        # Import localization
        from src.localization import LocalizationManager
        
        # Test dynamic import of quality check dialog (same way as in main.py)
        dialog_path = Path(__file__).parent / "src" / "quality_check_dialog.py"
        dialog_spec = importlib.util.spec_from_file_location("quality_check_dialog", dialog_path)
        
        if dialog_spec is None or dialog_spec.loader is None:
            print("❌ Could not create dialog spec")
            return False
            
        dialog_module = importlib.util.module_from_spec(dialog_spec)
        dialog_spec.loader.exec_module(dialog_module)
        
        print("✅ Quality check dialog module imported successfully")
        print(f"   Module: {dialog_module}")
        print(f"   QualityCheckDialog class: {dialog_module.QualityCheckDialog}")
        
        # Test basic initialization (without actually showing the dialog)
        root = tk.Tk()
        root.withdraw()  # Hide the test window
        
        localization = LocalizationManager()
        
        # Mock quality results
        mock_results = {
            'unrealistic_colors': {
                'extreme_red_pixels': 0.01,
                'magenta_pixels': 0.005,
                'red_dominance_ratio': 1.2,
                'recommendations': ['qc_reduce_red_gain']
            },
            'overall_recommendations': []
        }
        
        # Test dialog class instantiation (but don't show it)
        dialog = dialog_module.QualityCheckDialog(
            root, mock_results, "test_image.jpg", localization
        )
        
        print("✅ Quality check dialog initialized successfully")
        print("✅ All imports working correctly!")
        
        # Clean up
        root.destroy()
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing dialog: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Testing Quality Check Dialog Import...")
    if test_dialog_import():
        print("\n🎉 All tests passed! Dialog is ready for use.")
    else:
        print("\n💥 Tests failed. Check errors above.")
