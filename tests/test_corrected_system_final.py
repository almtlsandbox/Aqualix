"""
Test final du système de score corrigé - VERSION FONCTIONNELLE
Utilise les bonnes conversions d'image
"""

import sys
sys.path.insert(0, '.')

from src.quality_check import PostProcessingQualityChecker
import numpy as np
import cv2

def test_corrected_system_final():
    """Test final avec les bonnes conversions d'image"""
    print("🎉 TEST FINAL - SYSTÈME DE SCORE CORRIGÉ")
    print("=" * 60)
    
    checker = PostProcessingQualityChecker()
    
    # Test 1: Image naturelle sans problèmes
    print("\n🌊 Test 1: Image sous-marine naturelle")
    img_natural = create_natural_underwater_image()
    img_natural_bgr = cv2.cvtColor(img_natural, cv2.COLOR_RGB2BGR)  # Conversion correcte
    
    results1 = checker.run_all_checks(img_natural_bgr, img_natural_bgr)
    score1 = checker._calculate_overall_score(results1)
    red_detected1 = results1.get('unrealistic_colors', {}).get('extreme_red_pixels', 0)
    
    print(f"   Pixels rouges détectés: {red_detected1*100:.2f}%")
    print(f"   Score: {score1:.2f}/10")
    
    # Test 2: Image avec problèmes de rouge modérés
    print("\n🔴 Test 2: Image avec rouge modéré (4% de pixels problématiques)")
    img_moderate = create_moderate_red_problem_image()
    img_moderate_bgr = cv2.cvtColor(img_moderate, cv2.COLOR_RGB2BGR)
    
    results2 = checker.run_all_checks(img_moderate_bgr, img_moderate_bgr)
    score2 = checker._calculate_overall_score(results2)
    red_detected2 = results2.get('unrealistic_colors', {}).get('extreme_red_pixels', 0)
    
    print(f"   Pixels rouges détectés: {red_detected2*100:.2f}%")
    print(f"   Score: {score2:.2f}/10")
    
    # Test 3: Image avec beaucoup de rouge (problème sérieux)
    print("\n🚨 Test 3: Image avec rouge excessif (10% de pixels problématiques)")
    img_heavy = create_heavy_red_problem_image()
    img_heavy_bgr = cv2.cvtColor(img_heavy, cv2.COLOR_RGB2BGR)
    
    results3 = checker.run_all_checks(img_heavy_bgr, img_heavy_bgr)
    score3 = checker._calculate_overall_score(results3)
    red_detected3 = results3.get('unrealistic_colors', {}).get('extreme_red_pixels', 0)
    
    print(f"   Pixels rouges détectés: {red_detected3*100:.2f}%")
    print(f"   Score: {score3:.2f}/10")
    
    # Évaluation finale
    print(f"\n📊 ÉVALUATION FINALE:")
    print(f"   Image naturelle:     {score1:.1f}/10 (rouge: {red_detected1*100:.1f}%)")
    print(f"   Rouge modéré:        {score2:.1f}/10 (rouge: {red_detected2*100:.1f}%)")
    print(f"   Rouge excessif:      {score3:.1f}/10 (rouge: {red_detected3*100:.1f}%)")
    
    # Vérifications
    detection_works = red_detected2 > 0.02 or red_detected3 > 0.05  # Détection fonctionne
    scoring_logical = score1 >= score2 >= score3  # Ordre logique des scores
    good_separation = (score1 - score3) >= 1.0  # Séparation suffisante
    
    print(f"\n✅ VÉRIFICATIONS FINALES:")
    print(f"   🔍 Détection fonctionne:           {'✅' if detection_works else '❌'}")
    print(f"   📈 Ordre des scores logique:       {'✅' if scoring_logical else '❌'}")
    print(f"   📊 Séparation scores suffisante:   {'✅' if good_separation else '❌'}")
    
    if detection_works and scoring_logical and good_separation:
        print(f"\n🏆 SUCCÈS TOTAL!")
        print(f"   ✅ Le problème de score paradoxal est RÉSOLU")
        print(f"   ✅ Plus de rouge = score plus bas (logique correcte)")
        print(f"   ✅ Le système peut maintenant guider l'utilisateur efficacement")
        print(f"\n🎯 CORRECTIONS APPLIQUÉES AVEC SUCCÈS:")
        print(f"   • Seuils de détection optimisés")
        print(f"   • Coefficients de score recalibrés") 
        print(f"   • Problème de conversion d'image identifié")
        return True
    else:
        print(f"\n⚠️ AMÉLIORATIONS ENCORE NÉCESSAIRES")
        return False

def create_natural_underwater_image():
    """Crée une image sous-marine naturelle sans problèmes"""
    img = np.zeros((200, 300, 3), dtype=np.uint8)
    img[:, :] = [35, 55, 85]  # Bleu-vert naturel
    
    # Variations naturelles
    for _ in range(int(200 * 300 * 0.1)):
        y, x = np.random.randint(0, 200), np.random.randint(0, 300)
        img[y, x] = [40, 60, 90]  # Variations légères
    
    return img

def create_moderate_red_problem_image():
    """Crée une image avec problème de rouge modéré"""
    img = np.zeros((200, 300, 3), dtype=np.uint8)
    img[:, :] = [25, 40, 70]  # Fond sous-marin
    
    # 4% de pixels rouge problématique
    red_count = int(200 * 300 * 0.04)
    for _ in range(red_count):
        y, x = np.random.randint(0, 200), np.random.randint(0, 300)
        img[y, x] = [120, 25, 30]  # Rouge modéré qui dépasse les seuils
    
    return img

def create_heavy_red_problem_image():
    """Crée une image avec problème de rouge sérieux"""
    img = np.zeros((200, 300, 3), dtype=np.uint8)
    img[:, :] = [45, 30, 50]  # Fond avec dominante rouge
    
    # 10% de pixels rouge intense
    red_count = int(200 * 300 * 0.10)
    for _ in range(red_count):
        y, x = np.random.randint(0, 200), np.random.randint(0, 300)
        img[y, x] = [150, 20, 25]  # Rouge très saturé
    
    return img

if __name__ == "__main__":
    test_corrected_system_final()
