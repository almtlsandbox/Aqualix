"""
Test ultra-rapide pour vérifier les seuils sur IMG_4292.JPG
Utilise un échantillonnage très aggressif
"""

import sys
sys.path.insert(0, '.')

import cv2
import numpy as np
import os

def quick_threshold_test():
    """Test ultra-rapide des seuils"""
    print("⚡ TEST ULTRA-RAPIDE - SEUILS IMG_4292.JPG")
    print("=" * 50)
    
    image_path = r"D:\OneDrive\DOCS\BATEAU-SCUBA\SCUBA\PHOTOS\COLOR CORRECTION\test\IMG_4292.JPG"
    
    if not os.path.exists(image_path):
        print("❌ Image non trouvée")
        return
    
    try:
        # Charger avec résolution très réduite
        img = cv2.imread(image_path)
        if img is None:
            print("❌ Impossible de charger")
            return
            
        # Réduction drastique pour test rapide
        img_small = cv2.resize(img, (300, 225), interpolation=cv2.INTER_AREA)
        print(f"Image réduite: 300x225 pixels")
        
        # Conversion
        img_rgb = cv2.cvtColor(img_small, cv2.COLOR_BGR2RGB)
        img_float = img_rgb.astype(np.float32) / 255.0
        
        red_channel = img_float[:, :, 0]
        green_channel = img_float[:, :, 1]
        blue_channel = img_float[:, :, 2]
        
        # Moyennes
        r_mean, g_mean, b_mean = np.mean(red_channel), np.mean(green_channel), np.mean(blue_channel)
        print(f"Moyennes: R={r_mean:.3f}, G={g_mean:.3f}, B={b_mean:.3f}")
        
        # Test avec différents seuils
        seuils_tests = [
            (0.45, 0.08, "Actuels (sensibles)"),
            (0.50, 0.10, "Précédents (modérés)"),
            (0.60, 0.15, "Stricts"),
            (0.35, 0.05, "Très sensibles")
        ]
        
        print(f"\nTest avec différents seuils:")
        for red_thresh, diff_thresh, nom in seuils_tests:
            red_dominant = (red_channel > red_thresh) & \
                          (red_channel > green_channel + diff_thresh) & \
                          (red_channel > blue_channel + diff_thresh)
            ratio = np.sum(red_dominant) / red_channel.size
            print(f"   {nom}: {ratio*100:.2f}% {'🔴' if ratio > 0.02 else '⚪'}")
        
        # Analyse des maximums
        red_max = np.max(red_channel)
        green_max = np.max(green_channel) 
        blue_max = np.max(blue_channel)
        
        print(f"\nValeurs max: R={red_max:.2f}, G={green_max:.2f}, B={blue_max:.2f}")
        
        # Pixels très rouges (>0.7)
        very_red = np.sum(red_channel > 0.7) / red_channel.size
        print(f"Pixels très rouges (>0.7): {very_red*100:.2f}%")
        
        # Conclusion rapide
        if any(np.sum((red_channel > thresh) & 
                     (red_channel > green_channel + diff) & 
                     (red_channel > blue_channel + diff)) / red_channel.size > 0.02 
               for thresh, diff, _ in seuils_tests):
            print(f"\n🔴 Au moins un seuil détecte du rouge excessif")
            print(f"   → La détection pourrait être justifiée selon certains critères")
        else:
            print(f"\n⚪ Aucun seuil ne détecte de rouge excessif significatif")
            print(f"   → L'image semble avoir une balance correcte")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    quick_threshold_test()
