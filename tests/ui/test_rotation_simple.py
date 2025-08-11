#!/usr/bin/env python3
"""
Simple test to verify rotation functionality works correctly
"""

import tkinter as tk
from tkinter import ttk
import numpy as np
import cv2
from main import ImageVideoProcessorApp
from ui_components import InteractivePreviewPanel

class SimpleRotationTest:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Rotation Test")
        self.root.geometry("800x600")
        
        # Create test image with directional arrow
        self.test_image = self.create_test_image()
        
        # Initialize main app component - create minimal mock instead
        self.app = type('MockApp', (), {'processor': None, 'root': self.root})()
        
        # Create split view for testing
        self.preview_panel = InteractivePreviewPanel(self.root, self.app)
        self.preview_panel.pack(expand=True, fill='both')
        
        # Load the test image
        self.preview_panel.update_images(self.test_image, self.test_image.copy(), reset_view=True)
        
        # Add test controls
        self.create_test_controls()
        
        print("Rotation Test Started")
        print("- Click 'Rotate Left' (↺) to rotate counter-clockwise (should show arrow pointing left)")
        print("- Click 'Rotate Right' (↻) to rotate clockwise (should show arrow pointing right)")
        print("- Current rotation should be preserved when changing parameters")
        
    def create_test_image(self):
        """Create test image with directional arrow"""
        img = np.ones((400, 400, 3), dtype=np.uint8) * 200  # Light gray background
        
        # Draw a large arrow pointing up initially
        # Arrow shaft
        cv2.rectangle(img, (180, 150), (220, 350), (0, 0, 255), -1)
        
        # Arrow head (triangle pointing up)
        pts = np.array([[200, 100], [150, 200], [250, 200]], np.int32)
        cv2.fillPoly(img, [pts], (0, 0, 255))
        
        # Add text indicating "UP"
        cv2.putText(img, 'UP', (160, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        
        # Convert BGR to RGB for display
        return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    def create_test_controls(self):
        """Create test control buttons"""
        controls_frame = ttk.Frame(self.root)
        controls_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)
        
        # Rotation test buttons
        ttk.Button(controls_frame, text="Test Parameter Change", 
                  command=self.test_parameter_change).pack(side=tk.LEFT, padx=5)
        
        # Current rotation display
        self.rotation_label = ttk.Label(controls_frame, text="Rotation: 0°")
        self.rotation_label.pack(side=tk.LEFT, padx=20)
        
        # Update rotation display periodically
        self.update_rotation_display()
    
    def test_parameter_change(self):
        """Simulate parameter change to test rotation persistence"""
        print(f"Testing parameter change with current rotation: {self.split_view.rotation}°")
        
        # Simulate parameter change (should preserve rotation)
        modified_img = self.test_image.copy()
        # Add slight brightness change to simulate processing
        modified_img = cv2.convertScaleAbs(modified_img, alpha=1.1, beta=10)
        
        # Update with reset_view=False to preserve rotation
        self.split_view.update_images(self.test_image, modified_img, reset_view=False)
        
        print(f"After parameter change, rotation is: {self.split_view.rotation}°")
    
    def update_rotation_display(self):
        """Update rotation display"""
        if hasattr(self.split_view, 'rotation'):
            self.rotation_label.config(text=f"Rotation: {self.split_view.rotation}°")
        self.root.after(100, self.update_rotation_display)
    
    def run(self):
        """Run the test"""
        self.root.mainloop()

if __name__ == "__main__":
    test = SimpleRotationTest()
    test.run()
