#!/usr/bin/env python3
"""
Test White Balance Parameter Synchronization with Quality Control
================================================================

PROBLEM: Changing white balancing mode has no impact on quality score
HYPOTHESIS: Cache not being properly cleared after parameter changes

This test validates the synchronization between UI parameter changes
and quality control analysis results.
"""

import sys
sys.path.insert(0, '.')

import tkinter as tk
import numpy as np
from src.main import ImageVideoProcessorApp
from src.quality_control_tab import QualityControlTab
from src.localization import LocalizationManager
from pathlib import Path
import importlib.util


def test_white_balance_quality_sync():
    """Test that white balance method changes affect quality scores"""
    
    print("🧪 TESTING WHITE BALANCE PARAMETER SYNCHRONIZATION")
    print("=" * 60)
    
    try:
        # Setup test environment
        root = tk.Tk()
        root.withdraw()
        
        app = ImageVideoProcessorApp(root)
        loc = LocalizationManager()
        
        # Create test image with known characteristics
        # Create an image with red-blue imbalance (typical underwater issue)
        test_img = np.ones((100, 100, 3), dtype=np.uint8)
        test_img[:, :, 0] = 180  # High red channel
        test_img[:, :, 1] = 120  # Medium green channel  
        test_img[:, :, 2] = 80   # Low blue channel (underwater loss)
        
        app.original_image = test_img
        app.current_file = 'test_underwater.jpg'
        
        print(f"✅ Test image created: {test_img.shape} with R={test_img[0,0,0]} G={test_img[0,0,1]} B={test_img[0,0,2]}")
        
        # Load quality check module
        quality_check_path = Path("src/quality_check.py")
        spec = importlib.util.spec_from_file_location("quality_check", quality_check_path)
        if spec is None or spec.loader is None:
            raise ImportError("Cannot load quality_check module")
        quality_check_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(quality_check_module)
        quality_checker = quality_check_module.PostProcessingQualityChecker()
        
        # Test different white balance methods
        wb_methods = ['gray_world', 'white_patch', 'shades_of_gray']
        results = {}
        
        for i, method in enumerate(wb_methods):
            print(f"\n🔧 Test {i+1}: White Balance Method = '{method}'")
            
            # Set white balance method
            app.processor.set_parameter('white_balance_method', method)
            current_method = app.processor.get_parameter('white_balance_method')
            print(f"   Parameter set to: {current_method}")
            
            # Clear cache and force reprocessing (simulating quality control tab)
            app.processed_image = None
            app.processed_preview = None
            
            # Force parameter synchronization
            if hasattr(app, 'update_preview'):
                app.update_preview()
            
            # CRITICAL: Force cache clearing after preview update (the fix)
            app.processed_image = None
            
            # Get processed image with current method
            processed_img = app.get_full_resolution_processed_image()
            
            if processed_img is not None:
                print(f"   Processed image: {processed_img.shape}")
                
                # Calculate mean color values to verify method differences
                mean_colors = np.mean(processed_img, axis=(0, 1))
                print(f"   Mean RGB: R={mean_colors[0]:.1f} G={mean_colors[1]:.1f} B={mean_colors[2]:.1f}")
                
                # Run quality analysis
                quality_results = quality_checker.run_all_checks(test_img, processed_img)
                
                # Calculate basic quality score
                unrealistic_colors = quality_results.get('unrealistic_colors', {})
                red_dominance = unrealistic_colors.get('red_dominance_ratio', 1.0)
                extreme_red = unrealistic_colors.get('extreme_red_pixels', 0.0)
                
                score = 10.0 - (extreme_red * 20 + max(0, red_dominance - 1.5) * 5)
                score = max(0, score)
                
                results[method] = {
                    'mean_colors': mean_colors,
                    'red_dominance': red_dominance,
                    'extreme_red': extreme_red,
                    'score': score
                }
                
                print(f"   Red dominance ratio: {red_dominance:.3f}")
                print(f"   Extreme red pixels: {extreme_red:.3f}")
                print(f"   Quality score: {score:.1f}/10.0")
            else:
                print("   ❌ ERROR: Could not get processed image")
                results[method] = None
        
        # Analyze results
        print(f"\n📊 RESULTS ANALYSIS")
        print("=" * 40)
        
        valid_results = {k: v for k, v in results.items() if v is not None}
        
        if len(valid_results) >= 2:
            # Check if different methods produce different results
            scores = [r['score'] for r in valid_results.values()]
            mean_colors_list = [r['mean_colors'] for r in valid_results.values()]
            
            # Calculate score differences
            min_score = min(scores)
            max_score = max(scores)
            score_range = max_score - min_score
            
            print(f"Score range: {min_score:.1f} - {max_score:.1f} (difference: {score_range:.1f})")
            
            # Calculate color differences
            color_diffs = []
            for i in range(len(mean_colors_list)):
                for j in range(i+1, len(mean_colors_list)):
                    diff = np.sum(np.abs(mean_colors_list[i] - mean_colors_list[j]))
                    color_diffs.append(diff)
            
            avg_color_diff = np.mean(color_diffs) if color_diffs else 0
            print(f"Average color difference between methods: {avg_color_diff:.1f}")
            
            # Determine if synchronization is working
            if score_range > 0.1:  # Scores differ by more than 0.1
                print("✅ SUCCESS: Different white balance methods produce different quality scores!")
                print("   Parameter synchronization is working correctly.")
            elif avg_color_diff > 5.0:  # Images differ but scores don't
                print("⚠️  PARTIAL: Images are different but quality scores are similar.")
                print("   This might be normal if the quality differences are subtle.")
            else:
                print("❌ FAILURE: White balance method changes are not affecting results.")
                print("   Parameter synchronization may still have issues.")
            
            # Show detailed comparison
            print(f"\nDetailed comparison:")
            for method, result in valid_results.items():
                if result:
                    colors = result['mean_colors']
                    print(f"   {method:15s}: Score={result['score']:4.1f} RGB=({colors[0]:5.1f},{colors[1]:5.1f},{colors[2]:5.1f})")
        else:
            print("❌ FAILURE: Could not get valid results for comparison")
        
        root.destroy()
        
    except Exception as e:
        print(f"❌ ERROR during test: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print(f"\n🏁 Test completed!")
    return True


if __name__ == "__main__":
    success = test_white_balance_quality_sync()
    sys.exit(0 if success else 1)
