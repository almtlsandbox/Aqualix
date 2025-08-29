"""
Test et correction du système de score de qualité
Identifie et corrige les problèmes de calibration
"""

import sys
sys.path.insert(0, '.')

from src.quality_check import PostProcessingQualityChecker
import numpy as np
import cv2

def test_score_issues():
    """Test le système actuel et identifie les problèmes"""
    print("🔍 DIAGNOSTIC DU SYSTÈME DE SCORE DE QUALITÉ")
    print("=" * 60)
    
    # Créer des images de test
    height, width = 400, 600
    
    # Image 1: Peu de rouge (devrait avoir un BON score)
    img_good = np.zeros((height, width, 3), dtype=np.uint8)
    img_good[:, :] = [50, 80, 120]  # Couleur bleu-vert naturelle
    # Ajouter quelques pixels rouges réalistes (2%)
    red_pixels = int(height * width * 0.02)
    for _ in range(red_pixels):
        y, x = np.random.randint(0, height), np.random.randint(0, width)
        img_good[y, x] = [200, 50, 50]  # Rouge modéré
    
    # Image 2: Beaucoup de rouge (devrait avoir un MAUVAIS score)
    img_bad = np.zeros((height, width, 3), dtype=np.uint8)
    img_bad[:, :] = [30, 60, 90]  # Base sombre
    # Ajouter beaucoup de pixels rouges extrêmes (15%)
    red_pixels = int(height * width * 0.15)
    for _ in range(red_pixels):
        y, x = np.random.randint(0, height), np.random.randint(0, width)
        img_bad[y, x] = [250, 30, 30]  # Rouge très saturé
    
    # Analyser avec le système actuel
    checker = PostProcessingQualityChecker()
    
    # Test image "bonne"
    results_good = checker.run_all_checks(img_good, img_good)
    score_good = checker._calculate_overall_score(results_good)
    
    # Test image "mauvaise"  
    results_bad = checker.run_all_checks(img_bad, img_bad)
    score_bad = checker._calculate_overall_score(results_bad)
    
    print(f"📊 RÉSULTATS ACTUELS:")
    print(f"   Image avec PEU de rouge:     Score = {score_good:.2f}/10")
    print(f"   Image avec BEAUCOUP de rouge: Score = {score_bad:.2f}/10")
    print()
    
    # Analyser les détails
    print("🔬 ANALYSE DÉTAILLÉE:")
    print("\n   Image 'BONNE' (peu de rouge):")
    red_data_good = results_good.get('unrealistic_colors', {})
    print(f"      Pixels rouges extrêmes: {red_data_good.get('extreme_red_pixels', 0):.4f}")
    print(f"      Pixels magenta: {red_data_good.get('magenta_pixels', 0):.4f}")
    
    print("\n   Image 'MAUVAISE' (beaucoup de rouge):")
    red_data_bad = results_bad.get('unrealistic_colors', {})
    print(f"      Pixels rouges extrêmes: {red_data_bad.get('extreme_red_pixels', 0):.4f}")
    print(f"      Pixels magenta: {red_data_bad.get('magenta_pixels', 0):.4f}")
    
    # Vérifier la logique
    print(f"\n✅ VÉRIFICATION LOGIQUE:")
    if score_good > score_bad:
        print(f"   ✅ Bon: Image avec peu de rouge a un meilleur score")
        print(f"   🎯 Le système fonctionne correctement pour ce test!")
    else:
        print(f"   ❌ Problème: Image avec beaucoup de rouge a un meilleur score")
        print(f"   🔧 Le système nécessite des ajustements")
    
    return results_good, results_bad, score_good, score_bad

if __name__ == "__main__":
    test_score_issues()
