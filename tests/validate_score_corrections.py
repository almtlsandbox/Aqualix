"""
Validation finale des corrections du système de score
Test simple et direct
"""

import sys
sys.path.insert(0, '.')

from src.quality_check import PostProcessingQualityChecker
import numpy as np

def validate_score_corrections():
    """Validation simple et rapide des corrections"""
    print("✅ VALIDATION FINALE - CORRECTIONS DU SYSTÈME DE SCORE")
    print("=" * 65)
    
    checker = PostProcessingQualityChecker()
    
    # Test 1: Image avec rouge modéré (devrait être détecté maintenant)
    print("\n🔍 Test 1: Image avec rouge modéré")
    img1 = create_test_image_moderate_red()
    results1 = checker.run_all_checks(img1, img1)
    score1 = checker._calculate_overall_score(results1)
    red_detected1 = results1.get('unrealistic_colors', {}).get('extreme_red_pixels', 0)
    
    print(f"   Pixels rouges détectés: {red_detected1*100:.2f}%")
    print(f"   Score: {score1:.2f}/10")
    
    # Test 2: Image naturelle (pas de problème)
    print("\n🔍 Test 2: Image naturelle équilibrée")
    img2 = create_test_image_natural()
    results2 = checker.run_all_checks(img2, img2)
    score2 = checker._calculate_overall_score(results2)
    red_detected2 = results2.get('unrealistic_colors', {}).get('extreme_red_pixels', 0)
    
    print(f"   Pixels rouges détectés: {red_detected2*100:.2f}%")
    print(f"   Score: {score2:.2f}/10")
    
    # Test 3: Image avec beaucoup de rouge (problème sérieux)
    print("\n🔍 Test 3: Image avec beaucoup de rouge")
    img3 = create_test_image_heavy_red()
    results3 = checker.run_all_checks(img3, img3)
    score3 = checker._calculate_overall_score(results3)
    red_detected3 = results3.get('unrealistic_colors', {}).get('extreme_red_pixels', 0)
    
    print(f"   Pixels rouges détectés: {red_detected3*100:.2f}%")
    print(f"   Score: {score3:.2f}/10")
    
    # Évaluation des corrections
    print(f"\n📊 RÉSULTATS DE VALIDATION:")
    print(f"   Image naturelle:     {score2:.1f}/10 (pixels rouges: {red_detected2*100:.1f}%)")
    print(f"   Rouge modéré:        {score1:.1f}/10 (pixels rouges: {red_detected1*100:.1f}%)")
    print(f"   Rouge excessif:      {score3:.1f}/10 (pixels rouges: {red_detected3*100:.1f}%)")
    
    # Vérifications
    detection_works = red_detected1 > 0.01 or red_detected3 > 0.05  # Au moins un cas détecte du rouge
    scoring_logical = score2 >= score1 >= score3  # Score logique: naturel ≥ modéré ≥ excessif
    sufficient_range = (max(score1, score2, score3) - min(score1, score2, score3)) > 0.5  # Plage suffisante
    
    print(f"\n✅ VÉRIFICATIONS:")
    print(f"   Détection fonctionne:     {'✅' if detection_works else '❌'}")
    print(f"   Ordre des scores logique: {'✅' if scoring_logical else '❌'}")
    print(f"   Plage de scores suffisante: {'✅' if sufficient_range else '❌'}")
    
    if detection_works and scoring_logical and sufficient_range:
        print(f"\n🎉 SUCCÈS COMPLET!")
        print(f"   Les corrections du système de score fonctionnent parfaitement.")
        print(f"   Le paradoxe signalé par l'utilisateur est résolu.")
        return True
    else:
        print(f"\n⚠️ AMÉLIORATIONS NÉCESSAIRES")
        if not detection_works:
            print(f"   - La détection des pixels rouges doit être plus sensible")
        if not scoring_logical:
            print(f"   - L'ordre des scores n'est pas logique")
        if not sufficient_range:
            print(f"   - La plage de scores est trop limitée")
        return False

def create_test_image_moderate_red():
    """Image avec un niveau modéré de rouge (cas typique)"""
    img = np.zeros((300, 400, 3), dtype=np.uint8)
    img[:, :] = [30, 50, 80]  # Fond sous-marin
    
    # 4% de pixels rouge modéré
    pixels_count = int(300 * 400 * 0.04)
    for _ in range(pixels_count):
        y, x = np.random.randint(0, 300), np.random.randint(0, 400)
        img[y, x] = [160, 45, 55]  # Rouge modéré mais visible
    
    return img

def create_test_image_natural():
    """Image naturelle sans problèmes de couleur"""
    img = np.zeros((300, 400, 3), dtype=np.uint8)
    img[:, :] = [45, 65, 85]  # Couleurs naturelles équilibrées
    
    # Quelques variations naturelles
    pixels_count = int(300 * 400 * 0.05)
    for _ in range(pixels_count):
        y, x = np.random.randint(0, 300), np.random.randint(0, 400)
        img[y, x] = [60, 75, 95]  # Variations naturelles
    
    return img

def create_test_image_heavy_red():
    """Image avec beaucoup de rouge (problème sérieux)"""
    img = np.zeros((300, 400, 3), dtype=np.uint8)
    img[:, :] = [60, 35, 45]  # Fond avec dominante rouge
    
    # 12% de pixels rouge intense
    pixels_count = int(300 * 400 * 0.12)
    for _ in range(pixels_count):
        y, x = np.random.randint(0, 300), np.random.randint(0, 400)
        img[y, x] = [200, 40, 50]  # Rouge très saturé
    
    return img

if __name__ == "__main__":
    validate_score_corrections()
