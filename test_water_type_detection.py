#!/usr/bin/env python3
"""
Test rapide de la détection de type d'eau
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import numpy as np
import cv2
from image_processing import ImageProcessor

def create_test_image(dominant_color):
    """Crée une image de test avec une couleur dominante"""
    img = np.zeros((100, 100, 3), dtype=np.uint8)
    img[:] = dominant_color
    
    # Ajouter un peu de texture pour les contours
    for i in range(10, 90, 20):
        cv2.rectangle(img, (i, i), (i+10, i+10), (255, 255, 255), 2)
    
    return img

def test_water_type_detection():
    """Test de la détection de type d'eau"""
    processor = ImageProcessor()
    
    test_cases = [
        ("Dominance verte (lac)", (20, 150, 50)),    # BGR : forte composante verte
        ("Dominance bleue (océan)", (150, 50, 20)),  # BGR : forte composante bleue  
        ("Faible rouge (tropical)", (100, 100, 20)), # BGR : faible composante rouge
        ("Image équilibrée (standard)", (80, 80, 80)), # BGR : équilibré
        ("Image claire avec contours", (200, 200, 200)), # BGR : clair
    ]
    
    print("🧪 Test de détection du type d'eau")
    print("=" * 50)
    
    for desc, color in test_cases:
        img = create_test_image(color)
        water_type_info = processor.get_water_type(img)
        
        type_tech, desc_fr, desc_en, method = water_type_info
        
        print(f"\n📊 {desc} (BGR: {color})")
        print(f"   Type détecté: {type_tech}")
        print(f"   Description: {desc_fr}")
        print(f"   Méthode recommandée: {method}")
        
        # Calcul des ratios pour vérification
        mean_bgr = np.mean(img.astype(np.float32) / 255.0, axis=(0, 1))
        total = np.sum(mean_bgr)
        if total > 0:
            ratios = mean_bgr / total
            print(f"   Ratios (B/G/R): {ratios[0]:.3f}/{ratios[1]:.3f}/{ratios[2]:.3f}")

if __name__ == "__main__":
    test_water_type_detection()
