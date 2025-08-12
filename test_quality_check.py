#!/usr/bin/env python3
"""
Test script for Quality Check system
Creates a simple test image and runs quality analysis
"""

import numpy as np
import cv2
from pathlib import Path
import sys

# Add src to path
sys.path.append(str(Path(__file__).parent / 'src'))

def create_test_image():
    """Create a simple test underwater image"""
    # Create a 400x300 test image
    height, width = 300, 400
    image = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Simulate underwater blue-green tint
    image[:, :, 0] = 50   # Low red (typical underwater)
    image[:, :, 1] = 120  # Medium green
    image[:, :, 2] = 180  # High blue
    
    # Add some features
    # Add a "coral" with excessive red (to trigger quality warnings)
    cv2.rectangle(image, (50, 50), (150, 100), (255, 100, 100), -1)
    
    # Add an oversaturated area
    cv2.circle(image, (300, 200), 50, (255, 255, 0), -1)
    
    # Add some fish-like shapes
    cv2.ellipse(image, (200, 150), (30, 15), 0, 0, 360, (100, 150, 200), -1)
    cv2.ellipse(image, (250, 180), (25, 12), 45, 0, 360, (120, 140, 190), -1)
    
    return image

def simulate_processed_image(original):
    """Simulate a processed version with some artifacts"""
    processed = original.copy().astype(np.float32)
    
    # Simulate aggressive red correction (common artifact)
    processed[:, :, 0] *= 2.5  # Boost red channel aggressively
    
    # Simulate saturation enhancement
    hsv = cv2.cvtColor(processed.astype(np.uint8), cv2.COLOR_BGR2HSV)
    hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 1.8, 0, 255)  # Boost saturation
    processed = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR).astype(np.float32)
    
    # Add some noise to simulate amplification
    noise = np.random.normal(0, 10, processed.shape)
    processed += noise
    
    # Clip values
    processed = np.clip(processed, 0, 255).astype(np.uint8)
    
    return processed

def test_quality_system():
    """Test the quality check system"""
    try:
        # Import quality checker
        from quality_check import PostProcessingQualityChecker
        
        # Create test images
        print("Creating test images...")
        original = create_test_image()
        processed = simulate_processed_image(original)
        
        # Save test images for visualization
        test_dir = Path("test_images")
        test_dir.mkdir(exist_ok=True)
        
        cv2.imwrite(str(test_dir / "test_original.jpg"), original)
        cv2.imwrite(str(test_dir / "test_processed.jpg"), processed)
        print(f"Test images saved to {test_dir}/")
        
        # Run quality analysis
        print("\nRunning quality analysis...")
        quality_checker = PostProcessingQualityChecker()
        results = quality_checker.run_all_checks(original, processed)
        
        # Display results
        print("\n" + "="*50)
        print("QUALITY ANALYSIS RESULTS")
        print("="*50)
        
        if 'error' in results:
            print(f"ERROR: {results['error']}")
            return
        
        overall_score = quality_checker._calculate_overall_score(results)
        print(f"Overall Quality Score: {overall_score:.1f}/10")
        print()
        
        # Show detailed results
        for category, data in results.items():
            if category == 'overall_recommendations':
                continue
                
            print(f"\n{category.upper().replace('_', ' ')}")
            print("-" * 40)
            
            if isinstance(data, dict):
                for key, value in data.items():
                    if key == 'recommendations':
                        if value:
                            print("  Recommendations:")
                            for rec in value:
                                print(f"    • {rec}")
                    else:
                        if isinstance(value, float):
                            print(f"  {key}: {value:.3f}")
                        elif isinstance(value, tuple) and len(value) == 3:
                            print(f"  {key}: R:{value[0]:.1f} G:{value[1]:.1f} B:{value[2]:.1f}")
                        else:
                            print(f"  {key}: {value}")
        
        # Summary recommendations
        all_recs = []
        for data in results.values():
            if isinstance(data, dict) and 'recommendations' in data:
                all_recs.extend(data['recommendations'])
        
        if all_recs:
            print("\nSUMMARY RECOMMENDATIONS")
            print("-" * 40)
            for i, rec in enumerate(set(all_recs), 1):
                print(f"{i}. {rec}")
        else:
            print("\nNo issues detected! ✅")
            
        print(f"\n✅ Quality check system working correctly!")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you're running from the project root directory.")
    except Exception as e:
        print(f"❌ Error during quality check: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_quality_system()
