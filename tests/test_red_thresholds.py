"""
Test avancé pour calibrer les seuils de détection de couleurs
"""

import sys
sys.path.insert(0, '.')

import numpy as np
import cv2

def test_red_detection_thresholds():
    """Teste différents niveaux de rouge pour calibrer les seuils"""
    print("🎯 CALIBRATION DES SEUILS DE DÉTECTION")
    print("=" * 60)
    
    height, width = 400, 600
    
    # Tester différents niveaux de rouge
    test_colors = [
        ([150, 40, 40], "Rouge modéré"),      # 0.59, 0.16, 0.16
        ([180, 50, 50], "Rouge visible"),      # 0.71, 0.20, 0.20  
        ([200, 50, 50], "Rouge saturé"),       # 0.78, 0.20, 0.20
        ([220, 60, 60], "Rouge intense"),      # 0.86, 0.24, 0.24
        ([240, 40, 40], "Rouge extrême"),      # 0.94, 0.16, 0.16
    ]
    
    for color, name in test_colors:
        # Créer une image test
        img = np.zeros((height, width, 3), dtype=np.uint8)
        img[:, :] = [40, 60, 90]  # Base naturelle
        
        # Ajouter 10% de pixels de cette couleur
        red_pixels = int(height * width * 0.10)
        for _ in range(red_pixels):
            y, x = np.random.randint(0, height), np.random.randint(0, width)
            img[y, x] = color
        
        # Convertir et analyser
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_float = img_rgb.astype(np.float32) / 255.0
        
        # Appliquer les critères actuels
        red_channel = img_float[:, :, 0]
        green_channel = img_float[:, :, 1]
        blue_channel = img_float[:, :, 2]
        
        # Critères actuels (après correction)
        red_dominant = (red_channel > 0.6) & (red_channel > green_channel + 0.2) & (red_channel > blue_channel + 0.25)
        extreme_red_detected = np.sum(red_dominant) / (height * width)
        
        # Critères plus sensibles pour test
        red_sensitive = (red_channel > 0.5) & (red_channel > green_channel + 0.15) & (red_channel > blue_channel + 0.2)
        sensitive_detected = np.sum(red_sensitive) / (height * width)
        
        print(f"\n📊 {name} RGB{color}:")
        print(f"   Valeurs normalisées: ({color[0]/255:.2f}, {color[1]/255:.2f}, {color[2]/255:.2f})")
        print(f"   Pixels ajoutés: 10%")
        print(f"   Détectés (seuil actuel):   {extreme_red_detected:.3f} ({extreme_red_detected*100:.1f}%)")
        print(f"   Détectés (seuil sensible): {sensitive_detected:.3f} ({sensitive_detected*100:.1f}%)")
        
        # Évaluation
        if extreme_red_detected > 0.05:  # Au moins 5% détectés
            print(f"   ✅ Seuil actuel: DÉTECTE correctement")
        else:
            print(f"   ⚠️  Seuil actuel: PAS ASSEZ SENSIBLE")
            
        if sensitive_detected > 0.07:  # Au moins 7% détectés avec seuil sensible
            print(f"   ✅ Seuil sensible: DÉTECTE correctement")

if __name__ == "__main__":
    test_red_detection_thresholds()
