"""
Debug du problème de conversion d'image
"""

import sys
sys.path.insert(0, '.')

from src.quality_check import PostProcessingQualityChecker
import numpy as np
import cv2

def debug_image_conversion():
    """Debug du problème de conversion BGR/RGB"""
    print("🔧 DEBUG CONVERSION D'IMAGE")
    print("=" * 40)
    
    # Créer une image avec couleurs connues
    height, width = 100, 150
    img_rgb = np.zeros((height, width, 3), dtype=np.uint8)
    img_rgb[:, :] = [20, 30, 60]  # Fond
    
    # Ajouter des pixels rouges calculés
    red_color = [120, 25, 25]  # RGB
    red_count = int(height * width * 0.1)  # 10%
    
    for _ in range(red_count):
        y, x = np.random.randint(0, height), np.random.randint(0, width)
        img_rgb[y, x] = red_color
    
    print(f"Image créée: {img_rgb.shape}")
    print(f"Couleur rouge: {red_color} (RGB)")
    print(f"Pixels rouges: {red_count} ({red_count/(height*width)*100:.1f}%)")
    
    # Test 1: Passer l'image RGB directement (notre cas actuel)
    print(f"\n🔍 TEST 1: Image RGB directe")
    checker1 = PostProcessingQualityChecker()
    
    # L'image va être convertie BGR->RGB à l'intérieur (double conversion!)
    results1 = checker1.run_all_checks(img_rgb, img_rgb)  # processed, original
    red_detected1 = results1.get('unrealistic_colors', {}).get('extreme_red_pixels', 0)
    
    print(f"   Pixels détectés: {red_detected1*100:.2f}%")
    
    # Test 2: Convertir l'image en BGR d'abord (ce que la méthode attend)
    print(f"\n🔍 TEST 2: Image convertie en BGR d'abord")
    img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
    
    checker2 = PostProcessingQualityChecker()
    results2 = checker2.run_all_checks(img_bgr, img_bgr)  # processed, original
    red_detected2 = results2.get('unrealistic_colors', {}).get('extreme_red_pixels', 0)
    
    print(f"   Pixels détectés: {red_detected2*100:.2f}%")
    
    # Test 3: Vérification manuelle après conversion comme dans la méthode
    print(f"\n🔍 TEST 3: Simulation conversion interne")
    # Simuler ce qui se passe dans run_all_checks
    processed_rgb_internal = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2RGB)  # Double conversion!
    
    img_float = processed_rgb_internal.astype(np.float32) / 255.0
    red_channel = img_float[:, :, 0]
    green_channel = img_float[:, :, 1]
    blue_channel = img_float[:, :, 2]
    
    red_dominant = (red_channel > 0.45) & (red_channel > green_channel + 0.08) & (red_channel > blue_channel + 0.08)
    manual_detection = np.sum(red_dominant) / (height * width)
    
    print(f"   Détection manuelle après double conversion: {manual_detection*100:.2f}%")
    
    # Vérifier quelques pixels
    print(f"\n🔍 ANALYSE DES PIXELS:")
    print(f"   Original RGB: {red_color}")
    print(f"   Après BGR->RGB: {processed_rgb_internal[50, 50]} (exemple)")
    
    if red_detected2 > red_detected1:
        print(f"\n✅ SOLUTION TROUVÉE!")
        print(f"   Le problème était la double conversion RGB->BGR->RGB")
        print(f"   Il faut passer des images BGR à run_all_checks")
    elif red_detected1 > 0.05:
        print(f"\n✅ TEST 1 fonctionne - problème ailleurs")
    else:
        print(f"\n❌ Problème plus profond")

if __name__ == "__main__":
    debug_image_conversion()
