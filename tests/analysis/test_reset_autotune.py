#!/usr/bin/env python3
"""
Test script to verify reset buttons uncheck auto-tune checkboxes
"""

import sys
import os
import cv2
import numpy as np

# Add src directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, 'src')
sys.path.insert(0, src_path)

from src.image_processing import ImageProcessor
from src.ui_components import ParameterPanel
import tkinter as tk

def create_test_image():
    """Create a simple test underwater-like image"""
    # Create a blue-green tinted image
    image = np.zeros((400, 600, 3), dtype=np.uint8)
    image[:, :, 0] = 50  # Red
    image[:, :, 1] = 120  # Green (dominant)  
    image[:, :, 2] = 100  # Blue
    
    # Add some texture/detail
    for i in range(0, 400, 20):
        for j in range(0, 600, 30):
            image[i:i+10, j:j+15] = [70, 140, 120]
    
    return image

def test_reset_unchecks_autotune():
    """Test that reset buttons uncheck auto-tune checkboxes"""
    print("Testing reset button auto-tune behavior...")
    
    # Create test image
    test_image = create_test_image()
    
    # Create processor
    processor = ImageProcessor()
    
    # Create basic Tkinter window
    root = tk.Tk()
    root.title("Reset Auto-tune Test")
    root.geometry("800x600")
    
    # Create parameter panel with image callback
    def get_image():
        return test_image
        
    def update_preview():
        print("Preview updated")
    
    param_panel = ParameterPanel(root, processor, update_preview, get_image)
    param_panel.pack(fill=tk.BOTH, expand=True)
    
    # Setup auto-tune callback
    processor.set_auto_tune_callback(param_panel.is_auto_tune_enabled)
    
    # Instructions
    instructions = tk.Label(root, 
        text="Test Instructions:\n"
             "1. Expand a processing step section\n"
             "2. Check the Auto-Tune checkbox (should trigger auto-tune)\n"
             "3. Click the Reset button for that step\n"
             "4. Verify the Auto-Tune checkbox is unchecked\n"
             "5. Try the 'Reset All Parameters' button too",
        justify=tk.LEFT, bg="lightblue", padx=10, pady=5)
    instructions.pack(side=tk.TOP, fill=tk.X, before=param_panel)
    
    print("Test UI created.")
    print("Expected behavior:")
    print("- When you check an auto-tune box: 'Auto-tune for [step]: enabled'")
    print("- When you click Reset: 'Auto-tune disabled for [step]' + parameters reset")
    print("- When you click Reset All: 'All auto-tune checkboxes disabled' + all parameters reset")
    print("\nLaunch the UI now...")
    
    root.mainloop()

if __name__ == "__main__":
    test_reset_unchecks_autotune()
