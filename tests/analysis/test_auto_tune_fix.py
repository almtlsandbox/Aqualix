#!/usr/bin/env python3
"""
Test script to verify auto-tune checkbox functionality
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

def test_auto_tune_trigger():
    """Test that auto-tune checkboxes trigger the methods"""
    print("Testing auto-tune functionality...")
    
    # Create test image
    test_image = create_test_image()
    
    # Create processor
    processor = ImageProcessor()
    
    # Create basic Tkinter window
    root = tk.Tk()
    root.title("Auto-tune Test")
    root.geometry("800x600")
    
    # Create parameter panel with image callback
    def get_image():
        return test_image
        
    def update_preview():
        print("Preview would be updated here")
    
    param_panel = ParameterPanel(root, processor, update_preview, get_image)
    param_panel.pack(fill=tk.BOTH, expand=True)
    
    # Setup auto-tune callback
    processor.set_auto_tune_callback(param_panel.is_auto_tune_enabled)
    
    # Instructions
    instructions = tk.Label(root, 
        text="Test Instructions:\n1. Click on a step to expand it\n2. Check an Auto-Tune checkbox\n3. Watch console for auto-tune messages",
        justify=tk.LEFT, bg="lightyellow", padx=10, pady=5)
    instructions.pack(side=tk.TOP, fill=tk.X, before=param_panel)
    
    print("Test UI created. Check the auto-tune checkboxes to test functionality.")
    print("Expected behavior: When you check an auto-tune box, you should see:")
    print("- 'Auto-tune for [step]: enabled' message")
    print("- Auto-tuning calculation messages")
    print("- Parameter values should update in the UI")
    print("\nLaunch the UI now...")
    
    root.mainloop()

if __name__ == "__main__":
    test_auto_tune_trigger()
