#!/usr/bin/env python3
"""
Test final pour valider la correction du bug contrôle qualité
Simule le comportement de l'application
"""

import sys
import os
import cv2
import numpy as np
from pathlib import Path

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
sys.path.append(os.path.dirname(__file__))

def simulate_application_workflow():
    """Simule le workflow complet de l'application"""
    print("🎯 SIMULATION WORKFLOW APPLICATION")
    print("=" * 60)
    
    try:
        from src.image_processing import ImageProcessor
        from src.quality_check import PostProcessingQualityChecker
        
        # Créer une image test sous-marine typique
        test_image = np.random.randint(80, 180, (400, 600, 3), dtype=np.uint8)
        # Simuler l'atténuation sous-marine (perte rouge/vert, dominance bleue)
        test_image[:, :, 0] *= 0.3  # Rouge fortement atténué
        test_image[:, :, 1] *= 0.6  # Vert moyennement atténué 
        test_image[:, :, 2] *= 1.2  # Bleu dominant
        test_image = np.clip(test_image, 0, 255).astype(np.uint8)
        
        print(f"📊 Image test sous-marine: {test_image.shape}")
        print(f"   Moyennes RGB: R={np.mean(test_image[:,:,0]):.1f}, "
              f"G={np.mean(test_image[:,:,1]):.1f}, B={np.mean(test_image[:,:,2]):.1f}")
        
        # Setup processeur comme dans l'application
        processor = ImageProcessor()
        quality_checker = PostProcessingQualityChecker()
        
        # Simuler différents états de l'interface utilisateur
        test_scenarios = [
            {
                "name": "Aucun traitement",
                "config": {
                    'white_balance_enabled': False,
                    'udcp_enabled': False,
                    'beer_lambert_enabled': False,
                    'color_rebalance_enabled': False,
                    'hist_eq_enabled': False,
                    'multiscale_fusion_enabled': False
                }
            },
            {
                "name": "White balance seulement",  
                "config": {
                    'white_balance_enabled': True,
                    'white_balance_method': 'gray_world',
                    'udcp_enabled': False,
                    'beer_lambert_enabled': False,
                    'color_rebalance_enabled': False,
                    'hist_eq_enabled': False,
                    'multiscale_fusion_enabled': False
                }
            },
            {
                "name": "White balance + UDCP",
                "config": {
                    'white_balance_enabled': True,
                    'white_balance_method': 'gray_world',
                    'udcp_enabled': True,
                    'udcp_omega': 0.75,
                    'beer_lambert_enabled': False,
                    'color_rebalance_enabled': False,
                    'hist_eq_enabled': False,
                    'multiscale_fusion_enabled': False
                }
            },
            {
                "name": "Pipeline complet",
                "config": {
                    'white_balance_enabled': True,
                    'udcp_enabled': True,
                    'beer_lambert_enabled': True,
                    'color_rebalance_enabled': True,
                    'hist_eq_enabled': True,
                    'multiscale_fusion_enabled': True
                }
            }
        ]
        
        results = []
        
        for i, scenario in enumerate(test_scenarios):
            print(f"\n🔧 SCÉNARIO {i+1}: {scenario['name']}")
            
            # Appliquer la configuration
            for param, value in scenario['config'].items():
                processor.set_parameter(param, value)
            
            # Désactiver auto-tune pour avoir des résultats prévisibles
            processor.set_auto_tune_callback(lambda step: False)
            
            # Traiter l'image (simule update_preview)
            processed = processor.process_image(test_image.copy())
            
            # Test de stabilité: retraiter avec mêmes paramètres
            processed_repeat = processor.process_image(test_image.copy())
            
            # Analyser la qualité (simule run_quality_check)
            quality_results = quality_checker.run_all_checks(test_image, processed)
            score = quality_checker._calculate_overall_score(quality_results)
            
            # Test répétabilité
            quality_results_repeat = quality_checker.run_all_checks(test_image, processed_repeat)
            score_repeat = quality_checker._calculate_overall_score(quality_results_repeat)
            
            # Calculer différences
            image_diff = np.mean(np.abs(processed.astype(float) - processed_repeat.astype(float)))
            score_diff = abs(score - score_repeat)
            
            result = {
                'scenario': scenario['name'],
                'score': score,
                'score_repeat': score_repeat,
                'score_diff': score_diff,
                'image_diff': image_diff,
                'stable': score_diff < 0.001 and image_diff < 0.1
            }
            results.append(result)
            
            print(f"   Score qualité: {score:.3f}/10")
            print(f"   Score répété: {score_repeat:.3f}/10")
            print(f"   Différence score: {score_diff:.6f}")
            print(f"   Différence image: {image_diff:.3f}")
            print(f"   Stabilité: {'✅' if result['stable'] else '❌'}")
            
        # Analyse globale
        print(f"\n📊 ANALYSE GLOBALE:")
        
        stable_count = sum(1 for r in results if r['stable'])
        print(f"   Scénarios stables: {stable_count}/{len(results)}")
        
        # Vérifier progression logique des scores
        scores = [r['score'] for r in results]
        print(f"   Évolution scores: {' → '.join(f'{s:.2f}' for s in scores)}")
        
        # Les scores devraient généralement augmenter avec plus de traitements
        improvements = []
        for i in range(1, len(scores)):
            improvement = scores[i] - scores[0]  # vs. aucun traitement
            improvements.append(improvement)
            
        positive_improvements = sum(1 for imp in improvements if imp > 0)
        print(f"   Améliorations positives: {positive_improvements}/{len(improvements)}")
        
        # Test des recommandations
        print(f"\n📋 RECOMMANDATIONS:")
        for r in results:
            idx = results.index(r)
            scenario = test_scenarios[idx]
            
            # Reconfigurer le processeur pour ce scénario
            for param, value in scenario['config'].items():
                processor.set_parameter(param, value)
                
            # Traiter et analyser
            scenario_processed = processor.process_image(test_image.copy())
            scenario_results = quality_checker.run_all_checks(test_image, scenario_processed)
            
            total_recs = 0
            for key, value in scenario_results.items():
                if isinstance(value, dict) and 'recommendations' in value:
                    total_recs += len(value['recommendations'])
            print(f"   {r['scenario']}: {total_recs} recommandations")
        
        # Verdict final
        print(f"\n🎯 VERDICT:")
        if stable_count == len(results):
            print(f"   ✅ Tous les scénarios sont stables - BUG CORRIGÉ!")
        else:
            print(f"   ❌ {len(results) - stable_count} scénarios instables - Bug persistant")
            
        if positive_improvements >= len(improvements) * 0.7:
            print(f"   ✅ Les traitements améliorent généralement la qualité")
        else:
            print(f"   ⚠️  Impact qualité incertain")
            
        return stable_count == len(results)
        
    except Exception as e:
        print(f"❌ Erreur dans le test: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = simulate_application_workflow()
    print(f"\n{'🎉 CORRECTION VALIDÉE' if success else '🔧 CORRECTION À AMÉLIORER'}")
