#!/usr/bin/env python3
"""
Test spécifique pour valider la correction du bug contrôle qualité
"""

import sys
import os
import cv2
import numpy as np
from pathlib import Path

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
sys.path.append(os.path.dirname(__file__))

def test_quality_fix():
    """Test la correction du bug contrôle qualité"""
    print("🔧 TEST CORRECTION BUG CONTRÔLE QUALITÉ")
    print("=" * 60)
    
    try:
        from src.image_processing import ImageProcessor
        from src.quality_check import PostProcessingQualityChecker
        
        # Créer une image de test caractéristique
        test_image = np.ones((300, 400, 3), dtype=np.uint8) * 128
        # Ajouter un pattern pour différencier les traitements
        test_image[100:200, 100:300, 0] = 50   # Zone rouge sombre
        test_image[100:200, 100:300, 2] = 200  # Zone bleue forte (simule eau profonde)
        
        print(f"📊 Image de test créée avec pattern bleu")
        
        # Setup processeur avec paramètres fixes (sans auto-tune)
        processor = ImageProcessor()
        
        # Configuration de test : Activer seulement white balance
        processor.set_parameter('white_balance_enabled', True)
        processor.set_parameter('white_balance_method', 'gray_world')
        processor.set_parameter('gray_world_percentile', 75.0)  # Paramètre fixe
        
        processor.set_parameter('udcp_enabled', False)
        processor.set_parameter('beer_lambert_enabled', False)
        processor.set_parameter('color_rebalance_enabled', False)
        processor.set_parameter('hist_eq_enabled', False)
        processor.set_parameter('multiscale_fusion_enabled', False)
        
        # Désactiver auto-tune complètement
        processor.set_auto_tune_callback(lambda step: False)
        
        print(f"\n🔧 Configuration: White balance uniquement (paramètres fixes)")
        
        # Traitement 1
        processed1 = processor.process_image(test_image.copy())
        
        # Analyse qualité 1
        quality_checker = PostProcessingQualityChecker()
        results1 = quality_checker.run_all_checks(test_image, processed1)
        score1 = quality_checker._calculate_overall_score(results1)
        
        print(f"   Premier traitement - Score: {score1:.3f}/10")
        
        # Traitement 2 (même paramètres)
        processed2 = processor.process_image(test_image.copy())
        
        # Analyse qualité 2
        results2 = quality_checker.run_all_checks(test_image, processed2)
        score2 = quality_checker._calculate_overall_score(results2)
        
        print(f"   Deuxième traitement - Score: {score2:.3f}/10")
        
        # Changement de paramètre
        processor.set_parameter('gray_world_percentile', 50.0)  # Changement
        print(f"\n🔧 Changement paramètre: gray_world_percentile 75→50")
        
        # Traitement 3 (paramètres différents)
        processed3 = processor.process_image(test_image.copy())
        
        # Analyse qualité 3
        results3 = quality_checker.run_all_checks(test_image, processed3)
        score3 = quality_checker._calculate_overall_score(results3)
        
        print(f"   Troisième traitement - Score: {score3:.3f}/10")
        
        # Analyse des résultats
        print(f"\n📊 ANALYSE:")
        diff_1_2 = abs(score1 - score2)
        diff_2_3 = abs(score2 - score3)
        
        print(f"   Différence scores identiques (1-2): {diff_1_2:.3f}")
        print(f"   Différence scores différents (2-3): {diff_2_3:.3f}")
        
        # Vérifier images
        image_diff_1_2 = np.mean(np.abs(processed1.astype(float) - processed2.astype(float)))
        image_diff_2_3 = np.mean(np.abs(processed2.astype(float) - processed3.astype(float)))
        
        print(f"   Différence images identiques: {image_diff_1_2:.3f}")
        print(f"   Différence images différentes: {image_diff_2_3:.3f}")
        
        # Résultats attendus
        print(f"\n🎯 ÉVALUATION:")
        
        if diff_1_2 < 0.001:
            print(f"   ✅ Stabilité: Paramètres identiques → scores identiques")
        else:
            print(f"   ❌ Instabilité: Même config donne scores différents!")
            
        if diff_2_3 > 0.01:  # Seuil minimum pour détecter un changement
            print(f"   ✅ Sensibilité: Paramètres différents → scores différents")
        else:
            print(f"   ⚠️  Insensibilité: Changement paramètre pas détecté")
            
        if image_diff_1_2 < 1.0:
            print(f"   ✅ Consistance images: Même config → même résultat")
        else:
            print(f"   ❌ Images inconsistantes avec même config!")
            
        # Test du détail des résultats
        print(f"\n📋 DÉTAILS PREMIERS RÉSULTATS:")
        for key, value in results1.items():
            if isinstance(value, dict) and 'recommendations' in value:
                recs = value['recommendations']
                print(f"   {key}: {len(recs)} recommandations")
                
        # Test stabilité des recommandations
        matching_recs = 0
        total_recs = 0
        for key in results1.keys():
            if key in results2 and isinstance(results1[key], dict) and isinstance(results2[key], dict):
                if 'recommendations' in results1[key] and 'recommendations' in results2[key]:
                    recs1 = set(results1[key]['recommendations'])
                    recs2 = set(results2[key]['recommendations']) 
                    total_recs += len(recs1.union(recs2))
                    matching_recs += len(recs1.intersection(recs2))
        
        if total_recs > 0:
            rec_stability = matching_recs / total_recs
            print(f"   Stabilité recommandations: {rec_stability:.2%}")
            if rec_stability > 0.95:
                print(f"   ✅ Recommandations stables")
            else:
                print(f"   ❌ Recommandations instables!")
        
        return diff_1_2 < 0.001 and diff_2_3 > 0.01
        
    except Exception as e:
        print(f"❌ Erreur dans le test: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_quality_fix()
    print(f"\n{'✅ TEST RÉUSSI' if success else '❌ TEST ÉCHOUÉ'}")
