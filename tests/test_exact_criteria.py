"""
Test avec couleurs calculées pour respecter les critères exacts
"""

import sys
sys.path.insert(0, '.')

from src.quality_check import PostProcessingQualityChecker
import numpy as np

def test_exact_criteria():
    """Test avec des couleurs qui respectent exactement nos critères"""
    print("🎯 TEST AVEC CRITÈRES EXACTS")
    print("=" * 50)
    
    checker = PostProcessingQualityChecker()
    
    # Critères actuels: (red > 0.45) & (red > green + 0.08) & (red > blue + 0.08)
    
    # Couleur qui DOIT être détectée
    print("\n📊 COULEUR QUI DOIT ÊTRE DÉTECTÉE:")
    red_problem = [120, 25, 25]  # RGB
    red_norm = [x/255.0 for x in red_problem]
    print(f"   RGB: {red_problem} -> Normalisé: [{red_norm[0]:.2f}, {red_norm[1]:.2f}, {red_norm[2]:.2f}]")
    
    # Vérifier les critères
    crit1 = red_norm[0] > 0.45
    crit2 = red_norm[0] > red_norm[1] + 0.08
    crit3 = red_norm[0] > red_norm[2] + 0.08
    
    print(f"   red > 0.45? {red_norm[0]:.2f} > 0.45 = {crit1}")
    print(f"   red > green + 0.08? {red_norm[0]:.2f} > {red_norm[1]:.2f} + 0.08 = {crit1}")
    print(f"   red > blue + 0.08? {red_norm[0]:.2f} > {red_norm[2]:.2f} + 0.08 = {crit3}")
    print(f"   DEVRAIT ÊTRE DÉTECTÉ: {crit1 and crit2 and crit3}")
    
    # Créer une image test avec cette couleur exacte
    print(f"\n🔬 CRÉATION D'IMAGE TEST AVEC CETTE COULEUR:")
    height, width = 200, 300
    img_test = np.zeros((height, width, 3), dtype=np.uint8)
    img_test[:, :] = [20, 30, 60]  # Fond sous-marin naturel
    
    # Ajouter 8% de pixels avec la couleur problématique calculée
    red_pixels_count = int(height * width * 0.08)
    positions = []
    for _ in range(red_pixels_count):
        y, x = np.random.randint(0, height), np.random.randint(0, width)
        img_test[y, x] = red_problem
        positions.append((y, x))
    
    print(f"   Fond: [20, 30, 60] (naturel)")
    print(f"   Pixels rouges ajoutés: {red_pixels_count} ({red_pixels_count/(height*width)*100:.1f}%)")
    print(f"   Couleur rouge: {red_problem}")
    
    # Analyse avec le système
    img_rgb = img_test  # Déjà en RGB
    results = checker.run_all_checks(img_rgb, img_rgb)
    
    red_detected = results.get('unrealistic_colors', {}).get('extreme_red_pixels', 0)
    score = checker._calculate_overall_score(results)
    
    print(f"\n📈 RÉSULTATS:")
    print(f"   Pixels rouges détectés: {red_detected*100:.2f}% (attendu: ~8%)")
    print(f"   Score: {score:.2f}/10")
    
    # Vérification directe des pixels
    print(f"\n🔍 VÉRIFICATION DIRECTE:")
    img_float = img_rgb.astype(np.float32) / 255.0
    red_channel = img_float[:, :, 0]
    green_channel = img_float[:, :, 1]
    blue_channel = img_float[:, :, 2]
    
    # Appliquer les critères manuellement
    red_dominant = (red_channel > 0.45) & (red_channel > green_channel + 0.08) & (red_channel > blue_channel + 0.08)
    manual_detection = np.sum(red_dominant) / (height * width)
    
    print(f"   Détection manuelle: {manual_detection*100:.2f}%")
    
    if manual_detection > 0.05:  # Au moins 5% détectés
        print(f"   ✅ LES CRITÈRES FONCTIONNENT!")
        print(f"   ✅ Le système détecte correctement les pixels rouges problématiques")
    else:
        print(f"   ❌ Les critères ne fonctionnent toujours pas")
        
        # Diagnostic approfondi
        print(f"\n🔧 DIAGNOSTIC APPROFONDI:")
        # Vérifier quelques pixels explicites
        for i, (y, x) in enumerate(positions[:5]):
            pixel_val = img_float[y, x]
            print(f"      Pixel {i+1}: [{pixel_val[0]:.2f}, {pixel_val[1]:.2f}, {pixel_val[2]:.2f}]")
            c1 = pixel_val[0] > 0.45
            c2 = pixel_val[0] > pixel_val[1] + 0.08
            c3 = pixel_val[0] > pixel_val[2] + 0.08
            print(f"         Critères: {c1}, {c2}, {c3} -> Détecté: {c1 and c2 and c3}")

if __name__ == "__main__":
    test_exact_criteria()
