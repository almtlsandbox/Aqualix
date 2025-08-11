#!/usr/bin/env python3
"""
Aqualix - Underwater Image Processing Application
Entry point for the application.
"""

import sys
import os
import tkinter as tk

# Add src directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, 'src')
sys.path.insert(0, src_path)

def main():
    """Main entry point for Aqualix application"""
    try:
        # Import the main application class
        from src.main import ImageVideoProcessorApp
        
        # Create the main window
        root = tk.Tk()
        
        # Create and run the application
        app = ImageVideoProcessorApp(root)
        root.mainloop()
        
    except ImportError as e:
        print(f"Error importing application modules: {e}")
        print("Please ensure all dependencies are installed and the src directory exists.")
        sys.exit(1)
    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
