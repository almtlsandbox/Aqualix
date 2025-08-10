#!/usr/bin/env python3
"""
Debug UI parameter updates and preview processing
"""
import numpy as np
from image_processing import ImageProcessor

def debug_parameter_updates():
    """Debug parameter updates and their effects"""
    processor = ImageProcessor()
    
    # Create test image
    test_image = np.zeros((200, 200, 3), dtype=np.uint8)
    test_image[50:150, 50:150, 0] = 255  # Red square
    
    print("=== Debugging UI Parameter Updates ===")
    
    # Step 1: Check default parameters
    print("\n1. Default parameters:")
    print(f"   color_rebalance_enabled: {processor.get_parameter('color_rebalance_enabled')}")
    print(f"   color_rebalance_rr: {processor.get_parameter('color_rebalance_rr')}")
    print(f"   color_rebalance_rg: {processor.get_parameter('color_rebalance_rg')}")
    
    # Step 2: Process with defaults
    print("\n2. Processing with defaults:")
    orig_preview, proc_preview, scale = processor.process_image_for_preview(test_image)
    red_default = np.mean(proc_preview[50:150, 50:150, 0])
    print(f"   Red value: {red_default:.1f}")
    
    # Step 3: Simulate UI parameter change
    print("\n3. Simulating UI parameter change (RR=0.3):")
    processor.set_parameter('color_rebalance_rr', 0.3)
    print(f"   New RR value: {processor.get_parameter('color_rebalance_rr')}")
    
    # Step 4: Process again
    print("\n4. Processing with new parameters:")
    orig_preview, proc_preview, scale = processor.process_image_for_preview(test_image)
    red_changed = np.mean(proc_preview[50:150, 50:150, 0])
    print(f"   Red value: {red_changed:.1f}")
    print(f"   Change: {red_changed - red_default:.1f}")
    
    # Step 5: Check if change is significant
    if abs(red_changed - red_default) > 50:
        print("   ✅ Parameter change has visible effect!")
    else:
        print("   ❌ Parameter change has no visible effect!")
        
    # Step 6: Check pipeline order and execution
    print("\n5. Pipeline diagnostics:")
    pipeline = processor.get_pipeline_description()
    print(f"   Pipeline steps: {len(pipeline)}")
    for i, step in enumerate(pipeline, 1):
        print(f"   {i}. {step.get('operation', 'Unknown')}")
        if 'rebalance' in step.get('operation', '').lower():
            print(f"      → Found color rebalance step!")
    
    return abs(red_changed - red_default) > 50

if __name__ == "__main__":
    success = debug_parameter_updates()
    if success:
        print("\n🎉 Color rebalancing is working correctly!")
    else:
        print("\n❌ Color rebalancing is not working!")
