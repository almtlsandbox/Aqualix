#!/usr/bin/env python3
"""
Simple manual test to verify that rotation buttons work correctly
Just run the main app and load an image to test rotation manually
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    print("=" * 60)
    print("MANUAL ROTATION TEST")
    print("=" * 60)
    print()
    print("1. Run the main application by executing: python main.py")
    print("2. Load an image (preferably one with clear directionality)")
    print("3. Test rotation buttons:")
    print("   - ↺ (Rotate Left): Should rotate counter-clockwise by 90°")
    print("   - ↻ (Rotate Right): Should rotate clockwise by 90°")
    print()
    print("4. Test rotation persistence:")
    print("   - Rotate the image to any angle")
    print("   - Change any parameter (e.g., White Balance temperature)")
    print("   - Verify that the rotation is PRESERVED")
    print()
    print("5. Test rotation reset on new image:")
    print("   - Rotate current image")
    print("   - Load a different image")
    print("   - Verify that rotation resets to 0° for the new image")
    print()
    print("Expected behavior:")
    print("✓ Left button rotates counter-clockwise")
    print("✓ Right button rotates clockwise") 
    print("✓ Rotation persists when parameters change")
    print("✓ Rotation resets when loading new images")
    print()
    
    # Try to run the main application
    try:
        print("Starting main application...")
        from main import main as run_main
        run_main()
    except ImportError as e:
        print(f"Could not import main: {e}")
        print("\nPlease run manually: python main.py")
    except Exception as e:
        print(f"Error starting application: {e}")
        print("\nPlease run manually: python main.py")

if __name__ == "__main__":
    main()
