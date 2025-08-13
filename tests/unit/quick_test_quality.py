#!/usr/bin/env python3
"""
Test rapide pour vérifier que la correction du bug contrôle qualité fonctionne
Exécute en 30 secondes - à lancer pendant les tests manuels
"""

import sys
import os
import cv2
import numpy as np
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))

# Add src directory to path
sys.path.append(str(Path(__file__).parent.parent.parent / 'src'))

def quick_quality_test():
    """Test rapide de la correction bug contrôle qualité"""
    print("⚡ TEST RAPIDE - CORRECTION BUG CONTRÔLE QUALITÉ")
    print("=" * 55)
    
    try:
        from src.image_processing import ImageProcessor
        from src.quality_check import PostProcessingQualityChecker
        
        # Image test simple
        test_img = np.random.randint(80, 150, (200, 300, 3), dtype=np.uint8).astype(np.float32)
        test_img[:, :, 0] *= 0.5  # Simule atténuation rouge sous-marine
        test_img[:, :, 2] *= 1.3  # Simule dominance bleue
        test_img = np.clip(test_img, 0, 255).astype(np.uint8)
        
        processor = ImageProcessor()
        quality_checker = PostProcessingQualityChecker()
        
        print(f"🔧 Test 1: Configuration A (White balance seulement)")
        # Config A
        processor.set_parameter('white_balance_enabled', True)
        processor.set_parameter('udcp_enabled', False)
        processor.set_parameter('beer_lambert_enabled', False)
        processor.set_parameter('color_rebalance_enabled', False)
        processor.set_parameter('hist_eq_enabled', False)
        processor.set_parameter('multiscale_fusion_enabled', False)
        processor.set_auto_tune_callback(lambda step: False)  # Pas d'auto-tune
        
        # Premier traitement
        processed_A1 = processor.process_image(test_img.copy())
        result_A1 = quality_checker.run_all_checks(test_img, processed_A1)
        score_A1 = quality_checker._calculate_overall_score(result_A1)
        
        # Répéter traitement (même config)
        processed_A2 = processor.process_image(test_img.copy())
        result_A2 = quality_checker.run_all_checks(test_img, processed_A2)
        score_A2 = quality_checker._calculate_overall_score(result_A2)
        
        print(f"   Score 1: {score_A1:.4f}")
        print(f"   Score 2: {score_A2:.4f}")
        diff_A = abs(score_A1 - score_A2)
        print(f"   Différence: {diff_A:.6f} {'✅' if diff_A < 0.001 else '❌'}")
        
        print(f"\n🔧 Test 2: Configuration B (Tous traitements)")
        # Config B
        processor.set_parameter('white_balance_enabled', True)
        processor.set_parameter('udcp_enabled', True)
        processor.set_parameter('beer_lambert_enabled', True)
        processor.set_parameter('color_rebalance_enabled', True)
        processor.set_parameter('hist_eq_enabled', True)
        processor.set_parameter('multiscale_fusion_enabled', True)
        
        processed_B = processor.process_image(test_img.copy())
        result_B = quality_checker.run_all_checks(test_img, processed_B)
        score_B = quality_checker._calculate_overall_score(result_B)
        
        print(f"   Score: {score_B:.4f}")
        diff_AB = abs(score_A1 - score_B)
        print(f"   vs Config A: {diff_AB:.4f} {'✅' if diff_AB > 0.01 else '⚠️'}")
        
        print(f"\n📊 RÉSULTATS:")
        print(f"   Stabilité config A: {'✅ STABLE' if diff_A < 0.001 else '❌ INSTABLE'}")
        print(f"   Sensibilité A→B: {'✅ SENSIBLE' if diff_AB > 0.01 else '⚠️ FAIBLE'}")
        
        # Test image differences
        img_diff_A = np.mean(np.abs(processed_A1.astype(float) - processed_A2.astype(float)))
        img_diff_AB = np.mean(np.abs(processed_A1.astype(float) - processed_B.astype(float)))
        
        print(f"   Diff images même config: {img_diff_A:.3f} {'✅' if img_diff_A < 1.0 else '❌'}")
        print(f"   Diff images config diff: {img_diff_AB:.3f} {'✅' if img_diff_AB > 5.0 else '⚠️'}")
        
        success = (diff_A < 0.001) and (diff_AB > 0.01) and (img_diff_A < 1.0)
        
        print(f"\n🎯 VERDICT: {'✅ CORRECTION VALIDÉE' if success else '❌ PROBLÈME DÉTECTÉ'}")
        
        if success:
            print(f"   → Les rapports qualité sont maintenant cohérents!")
            print(f"   → Même config = même score (répétabilité)")
            print(f"   → Config différente = score différent (sensibilité)")
        else:
            print(f"   → Le bug pourrait persister, vérifiez les tests manuels")
        
        return success
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return False

if __name__ == "__main__":
    quick_quality_test()
