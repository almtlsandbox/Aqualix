#!/usr/bin/env python3
"""
Test avec une image plus réaliste pour vérifier la correction multiscale fusion
"""

import numpy as np
import cv2
from src.image_processing import ImageProcessor

def create_realistic_underwater_image():
    """Créer une image plus réaliste avec dominante colorée"""
    # Image 200x200
    image = np.zeros((200, 200, 3), dtype=np.uint8)
    
    # Créer un gradient avec dominante bleue-verte (typique sous-marine)
    for i in range(200):
        for j in range(200):
            # Dominante bleue-verte avec variation spatiale
            blue_intensity = 100 + int(50 * np.sin(i * 0.05)) + int(30 * np.cos(j * 0.03))
            green_intensity = 80 + int(40 * np.sin(i * 0.03)) + int(25 * np.cos(j * 0.05))
            red_intensity = 40 + int(20 * np.sin(i * 0.02)) + int(15 * np.cos(j * 0.04))
            
            # Clamp values
            image[i, j] = [
                max(0, min(255, red_intensity)),
                max(0, min(255, green_intensity)), 
                max(0, min(255, blue_intensity))
            ]
    
    # Ajouter quelques zones plus claires (objets)
    cv2.rectangle(image, (50, 50), (100, 100), (120, 140, 180), -1)
    cv2.rectangle(image, (120, 120), (170, 170), (90, 120, 160), -1)
    
    return image

def test_with_realistic_image():
    """Test avec une image plus réaliste"""
    print("=== Test avec image réaliste ===")
    
    # Créer une image de test réaliste
    test_image = create_realistic_underwater_image()
    print(f"Image réaliste - Moyenne R,G,B: {np.mean(test_image, axis=(0,1))}")
    
    # Créer le processeur
    processor = ImageProcessor()
    
    # Activer plusieurs étapes pour avoir un effet plus visible
    processor.set_parameter('white_balance_enabled', True)
    processor.set_parameter('udcp_enabled', True)
    processor.set_parameter('beer_lambert_enabled', True)
    processor.set_parameter('multiscale_fusion_enabled', False)
    
    # Test 1: Pipeline normal SANS fusion
    print("\n1. Pipeline normal SANS fusion:")
    result_without_fusion = processor.process_image(test_image)
    print(f"   Résultat - Moyenne R,G,B: {np.mean(result_without_fusion, axis=(0,1))}")
    
    # Test 2: Même pipeline AVEC fusion
    print("\n2. Pipeline normal AVEC fusion:")
    processor.set_parameter('multiscale_fusion_enabled', True)
    result_with_fusion = processor.process_image(test_image)
    print(f"   Résultat - Moyenne R,G,B: {np.mean(result_with_fusion, axis=(0,1))}")
    
    # Test 3: Modifier des paramètres et voir si ça change
    print("\n3. Modifier paramètres Beer-Lambert (plus visible):")
    processor.set_parameter('beer_lambert_depth_factor', 0.3)  # Double la valeur par défaut
    processor.set_parameter('beer_lambert_enhance_factor', 2.5)  # Plus fort
    
    result_modified = processor.process_image(test_image)
    print(f"   Résultat modifié - Moyenne R,G,B: {np.mean(result_modified, axis=(0,1))}")
    
    # Calculer les différences
    diff_fusion = np.abs(result_with_fusion.astype(float) - result_modified.astype(float))
    mean_diff = np.mean(diff_fusion)
    
    print(f"\n   Différence entre fusion normale vs modifiée: {mean_diff:.2f}")
    
    # Test 4: Vérifier sans fusion aussi
    print("\n4. Même modification SANS fusion (pour comparaison):")
    processor.set_parameter('multiscale_fusion_enabled', False)
    result_without_fusion_mod = processor.process_image(test_image)
    print(f"   Résultat sans fusion modifié - Moyenne R,G,B: {np.mean(result_without_fusion_mod, axis=(0,1))}")
    
    diff_no_fusion = np.abs(result_without_fusion.astype(float) - result_without_fusion_mod.astype(float))
    mean_diff_no_fusion = np.mean(diff_no_fusion)
    
    print(f"   Différence sans fusion normale vs modifiée: {mean_diff_no_fusion:.2f}")
    
    # Évaluation
    print("\n=== ÉVALUATION ===")
    print(f"Effet des paramètres SANS fusion: {mean_diff_no_fusion:.2f}")
    print(f"Effet des paramètres AVEC fusion: {mean_diff:.2f}")
    
    if mean_diff > 1.0 and abs(mean_diff - mean_diff_no_fusion) < mean_diff_no_fusion * 0.5:
        print("✅ SUCCÈS: La multiscale fusion respecte maintenant les changements de paramètres!")
        return True
    elif mean_diff > 1.0:
        print("⚠️  PARTIEL: La fusion respecte les paramètres mais avec une sensibilité différente")
        return True
    else:
        print("❌ ÉCHEC: La multiscale fusion ignore encore les changements de paramètres.")
        return False

if __name__ == "__main__":
    success = test_with_realistic_image()
    exit(0 if success else 1)
