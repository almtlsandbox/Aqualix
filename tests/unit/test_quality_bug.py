#!/usr/bin/env python3
"""
Test pour identifier le bug du rapport de qualité constant
"""

import sys
import os
import cv2
import numpy as np
from pathlib import Path

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
sys.path.append(os.path.dirname(__file__))

def test_quality_consistency():
    """Test si le contrôle qualité donne des résultats différents selon les paramètres"""
    print("🔍 TEST BUG CONTRÔLE QUALITÉ")
    print("=" * 60)
    
    try:
        from src.image_processing import ImageProcessor
        from src.quality_check import PostProcessingQualityChecker
        
        # Créer une image de test
        test_image = np.random.randint(50, 200, (300, 400, 3), dtype=np.uint8)
        # Ajouter un biais bleu pour simuler une image sous-marine
        test_image[:, :, 0] = test_image[:, :, 0] * 0.6  # Réduire rouge
        test_image[:, :, 1] = test_image[:, :, 1] * 0.8  # Réduire vert
        test_image = test_image.astype(np.uint8)
        
        print(f"📊 Image de test créée: {test_image.shape}")
        
        # Configuration 1: Tous les traitements désactivés
        print(f"\n🔧 TEST 1: Tous traitements DÉSACTIVÉS")
        processor1 = ImageProcessor()
        
        # Désactiver tous les traitements
        processor1.set_parameter('white_balance_enabled', False)
        processor1.set_parameter('udcp_enabled', False) 
        processor1.set_parameter('beer_lambert_enabled', False)
        processor1.set_parameter('color_rebalance_enabled', False)
        processor1.set_parameter('hist_eq_enabled', False)
        processor1.set_parameter('multiscale_fusion_enabled', False)
        
        # Traiter l'image (devrait être identique à l'originale)
        processed1 = processor1.process_image(test_image.copy())
        
        # Analyser la qualité
        quality_checker = PostProcessingQualityChecker()
        results1 = quality_checker.run_all_checks(test_image, processed1)
        score1 = quality_checker._calculate_overall_score(results1)
        
        print(f"   Score qualité (aucun traitement): {score1:.2f}/10")
        
        # Configuration 2: Tous les traitements activés avec auto-tune
        print(f"\n🔧 TEST 2: Tous traitements ACTIVÉS avec auto-tune")
        processor2 = ImageProcessor()
        
        # Activer tous les traitements
        processor2.set_parameter('white_balance_enabled', True)
        processor2.set_parameter('udcp_enabled', True)
        processor2.set_parameter('beer_lambert_enabled', True)
        processor2.set_parameter('color_rebalance_enabled', True)
        processor2.set_parameter('hist_eq_enabled', True)
        processor2.set_parameter('multiscale_fusion_enabled', True)
        
        # Simuler l'auto-tune callback (toujours retourne True)
        processor2.set_auto_tune_callback(lambda step: True)
        
        # Traiter l'image avec auto-tune
        processed2 = processor2.process_image(test_image.copy())
        
        # Analyser la qualité
        results2 = quality_checker.run_all_checks(test_image, processed2)
        score2 = quality_checker._calculate_overall_score(results2)
        
        print(f"   Score qualité (avec traitements): {score2:.2f}/10")
        
        # Configuration 3: Même configuration mais RE-TRAITEMENT
        print(f"\n🔧 TEST 3: RE-TRAITEMENT avec mêmes paramètres")
        processed3 = processor2.process_image(test_image.copy())  # Même processeur, re-traitement
        
        # Analyser la qualité
        results3 = quality_checker.run_all_checks(test_image, processed3)
        score3 = quality_checker._calculate_overall_score(results3)
        
        print(f"   Score qualité (re-traitement): {score3:.2f}/10")
        
        # Analyser les différences
        print(f"\n📊 ANALYSE DES RÉSULTATS:")
        diff_1_2 = abs(score1 - score2)
        diff_2_3 = abs(score2 - score3) 
        
        print(f"   Différence score 1→2: {diff_1_2:.2f}")
        print(f"   Différence score 2→3: {diff_2_3:.2f}")
        
        # Vérifier si les images sont identiques
        image_diff_2_3 = np.mean(np.abs(processed2.astype(float) - processed3.astype(float)))
        print(f"   Différence pixel images 2-3: {image_diff_2_3:.2f}")
        
        if diff_2_3 > 0.1 or image_diff_2_3 > 1.0:
            print(f"\n❌ BUG DÉTECTÉ: Les re-traitements donnent des résultats différents!")
            print(f"   → L'auto-tune change les paramètres à chaque appel")
            print(f"   → Le contrôle qualité ne peut pas être constant")
        else:
            print(f"\n✅ Pas de bug détecté: Les re-traitements sont cohérents")
            
        if diff_1_2 < 0.1:
            print(f"\n❌ BUG DÉTECTÉ: Aucune différence entre traitements ON/OFF!")
            print(f"   → Les traitements ne semblent pas s'appliquer")
        else:
            print(f"\n✅ Les traitements ont bien un impact sur la qualité")
            
        return diff_2_3 > 0.1 or image_diff_2_3 > 1.0
        
    except Exception as e:
        print(f"❌ Erreur dans le test: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_quality_consistency()
