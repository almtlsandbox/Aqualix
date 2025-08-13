#!/usr/bin/env python3
"""
Test de performance de l'analyse d'informations image
"""
import time
import sys
import os
import cv2
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))

import numpy as np
from src.image_info import ImageInfoExtractor

def create_test_image(filepath, width=4000, height=3000):
    """Crée une grosse image de test réaliste"""
    print(f"Création d'une image de test {width}x{height} pixels...")
    
    # Créer une image colorée réaliste
    image = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Simulation d'une image sous-marine avec gradients et textures
    for y in range(height):
        for x in range(width):
            # Gradient bleu-vert avec du bruit
            blue_base = int(80 + (y / height) * 120)
            green_base = int(60 + (x / width) * 100)
            red_base = int(20 + np.sin(x * 0.001) * 40)
            
            # Ajouter du bruit
            noise = np.random.randint(-20, 20)
            
            image[y, x] = [
                max(0, min(255, red_base + noise)),
                max(0, min(255, green_base + noise)), 
                max(0, min(255, blue_base + noise))
            ]
    
    # Sauvegarder l'image
    cv2.imwrite(filepath, image)
    print(f"Image créée: {filepath}")
    return image

def test_image_info_performance():
    """Test de performance de l'extraction d'informations"""
    
    test_image_path = "test_large_underwater.jpg"
    
    try:
        # Créer une grosse image de test (12 millions de pixels)
        test_image = create_test_image(test_image_path, width=4000, height=3000)
        
        extractor = ImageInfoExtractor()
        
        print(f"\n=== TEST EXTRACTION INFOS IMAGE ===")
        print(f"Image: {test_image_path} (4000x3000 = 12M pixels)")
        
        # Test 1: Mode normal (complet)
        print("\n1. Mode NORMAL (complet):")
        start_time = time.time()
        info_normal = extractor.get_image_info(test_image_path, test_image, include_hash=False, fast_mode=False)
        normal_duration = time.time() - start_time
        print(f"   Durée: {normal_duration:.2f}s")
        print(f"   Analyse couleur: {info_normal['color_analysis']['brightness']}")
        print(f"   EXIF traité: {len(info_normal['exif']['processed_exif'])} entrées")
        
        # Test 2: Mode rapide (fast_mode)
        print("\n2. Mode RAPIDE (fast_mode):")
        start_time = time.time()
        info_fast = extractor.get_image_info(test_image_path, test_image, include_hash=False, fast_mode=True)
        fast_duration = time.time() - start_time
        print(f"   Durée: {fast_duration:.2f}s")
        print(f"   Analyse couleur: {info_fast['color_analysis']['brightness']}")
        print(f"   EXIF traité: {len(info_fast['exif']['processed_exif'])} entrées")
        
        # Comparaison
        speedup = normal_duration / fast_duration if fast_duration > 0 else float('inf')
        print(f"\n📊 RÉSULTAT:")
        print(f"   • Mode normal: {normal_duration:.2f}s")
        print(f"   • Mode rapide: {fast_duration:.2f}s")
        print(f"   • Accélération: {speedup:.1f}x plus rapide")
        print(f"   • Gain temps: {((normal_duration - fast_duration) / normal_duration * 100):.1f}% plus rapide")
        
        if fast_duration < 0.1:
            print("   ✅ Fast mode suffisamment rapide pour UI non-bloquante")
        else:
            print("   ⚠️ Fast mode encore trop lent, optimisation nécessaire")
            
        # Test spécifique analyse couleur
        print(f"\n3. Test ANALYSE COULEUR isolée:")
        start_time = time.time()
        color_analysis = extractor._analyze_colors(test_image)
        color_duration = time.time() - start_time
        print(f"   Analyse couleur seule: {color_duration:.2f}s")
        print(f"   Brightness calculée: {color_analysis['brightness']}")
        
    finally:
        # Nettoyer
        if os.path.exists(test_image_path):
            os.remove(test_image_path)
            print(f"\nFichier de test supprimé: {test_image_path}")

if __name__ == "__main__":
    print("🧪 TEST DE PERFORMANCE - EXTRACTION INFOS IMAGE")
    print("=" * 55)
    
    test_image_info_performance()
