"""
Test de détection de rouge avec des scénarios réalistes
"""

import sys
sys.path.insert(0, '.')

import numpy as np
import cv2

def test_realistic_red_scenarios():
    """Teste avec des scénarios d'images sous-marines réalistes"""
    print("🌊 TEST AVEC SCÉNARIOS SOUS-MARINS RÉALISTES")
    print("=" * 60)
    
    height, width = 400, 600
    
    # Scénario 1: Image sous-marine normale (dominante bleue)
    print("\n🎯 SCÉNARIO 1: Image sous-marine normale")
    img1 = np.zeros((height, width, 3), dtype=np.uint8)
    img1[:, :] = [20, 40, 80]  # Fond bleu naturel sous-marin
    
    # Ajouter quelques pixels rouges artificiels (sur-correction)
    red_pixels = int(height * width * 0.05)  # 5%
    for _ in range(red_pixels):
        y, x = np.random.randint(0, height), np.random.randint(0, width)
        img1[y, x] = [180, 30, 30]  # Rouge artificiel typique
    
    # Test détection
    img1_rgb = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
    detected1 = test_detection(img1_rgb, "Fond bleu + rouge artificiel")
    
    # Scénario 2: Image avec balance rouge excessive  
    print("\n🎯 SCÉNARIO 2: Balance rouge excessive")
    img2 = np.zeros((height, width, 3), dtype=np.uint8)
    img2[:, :] = [60, 35, 45]  # Fond avec dominante rouge
    
    # Ajouter des pixels encore plus rouges
    red_pixels = int(height * width * 0.08)  # 8%
    for _ in range(red_pixels):
        y, x = np.random.randint(0, height), np.random.randint(0, width)
        img2[y, x] = [200, 40, 50]  # Rouge saturé
    
    detected2 = test_detection(img2, "Dominante rouge + pixels saturés")
    
    # Scénario 3: Image naturelle (pas de problème rouge)
    print("\n🎯 SCÉNARIO 3: Image naturelle équilibrée")
    img3 = np.zeros((height, width, 3), dtype=np.uint8)
    img3[:, :] = [45, 65, 85]  # Couleurs naturelles équilibrées
    
    # Ajouter quelques objets colorés naturels
    natural_pixels = int(height * width * 0.03)  # 3%
    for _ in range(natural_pixels):
        y, x = np.random.randint(0, height), np.random.randint(0, width)
        img3[y, x] = [120, 80, 60]  # Couleur naturelle (corail, etc.)
    
    detected3 = test_detection(img3, "Couleurs naturelles équilibrées")
    
    print(f"\n📊 RÉSUMÉ:")
    print(f"   Scénario problématique 1: {detected1*100:.1f}% détectés ({'✅' if detected1 > 0.02 else '❌'})")
    print(f"   Scénario problématique 2: {detected2*100:.1f}% détectés ({'✅' if detected2 > 0.04 else '❌'})")  
    print(f"   Scénario naturel:         {detected3*100:.1f}% détectés ({'✅' if detected3 < 0.01 else '❌ faux positif!'})")

def test_detection(img_rgb, scenario_name):
    """Teste la détection sur une image"""
    img_float = img_rgb.astype(np.float32) / 255.0
    red_channel = img_float[:, :, 0]
    green_channel = img_float[:, :, 1]
    blue_channel = img_float[:, :, 2]
    
    # Critères actuels
    red_dominant = (red_channel > 0.5) & (red_channel > green_channel + 0.1) & (red_channel > blue_channel + 0.1)
    detected_ratio = np.sum(red_dominant) / img_rgb.shape[0] / img_rgb.shape[1]
    
    print(f"   {scenario_name}: {detected_ratio*100:.1f}% pixels rouges détectés")
    
    # Afficher quelques statistiques
    avg_red = np.mean(red_channel)
    avg_green = np.mean(green_channel)
    avg_blue = np.mean(blue_channel)
    print(f"   Moyennes: R={avg_red:.2f}, G={avg_green:.2f}, B={avg_blue:.2f}")
    
    return detected_ratio

if __name__ == "__main__":
    test_realistic_red_scenarios()
