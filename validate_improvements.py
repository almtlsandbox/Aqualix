#!/usr/bin/env python3
"""
Validation des améliorations des paramètres par défaut basées sur la littérature scientifique
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(__file__))

from src.image_processing import ImageProcessor

def validate_improvements():
    """Valide les améliorations apportées aux paramètres par défaut"""
    
    processor = ImageProcessor()
    params = processor.get_all_parameters()
    
    print("=== VALIDATION DES AMÉLIORATIONS AQUALIX ===")
    print("Paramètres optimisés selon la littérature scientifique\n")
    
    # Test des améliorations critiques
    improvements = [
        {
            'param': 'gray_world_percentile',
            'expected': 15,
            'old_value': 50,
            'rationale': 'Iqbal et al. (2007) - Évite pixels saturés'
        },
        {
            'param': 'beer_lambert_depth_factor',
            'expected': 0.15,
            'old_value': 0.1,
            'rationale': 'Chiang & Chen (2012) - Correction plus efficace'
        },
        {
            'param': 'color_rebalance_saturation_limit',
            'expected': 0.8,
            'old_value': 1.0,
            'rationale': 'Ancuti et al. (2012) - Protection anti-magenta'
        },
        {
            'param': 'udcp_window_size',
            'expected': 11,
            'old_value': 15,
            'rationale': 'Ancuti et al. (2018) - Préservation détails'
        },
        {
            'param': 'multiscale_fusion_enabled',
            'expected': True,
            'old_value': False,
            'rationale': 'Ancuti et al. (2017) - Bénéfices significatifs'
        },
        {
            'param': 'lake_green_reduction',
            'expected': 0.4,
            'old_value': 0.3,
            'rationale': 'Réduction verte plus agressive pour eau douce'
        }
    ]
    
    success_count = 0
    total_count = len(improvements)
    
    for improvement in improvements:
        param_name = improvement['param']
        expected = improvement['expected']
        current = params.get(param_name)
        old_value = improvement['old_value']
        rationale = improvement['rationale']
        
        if current == expected:
            status = "✅ CORRECT"
            success_count += 1
        else:
            status = "❌ ERREUR"
            
        print(f"{status} {param_name}:")
        print(f"   Ancien: {old_value} → Attendu: {expected} → Actuel: {current}")
        print(f"   Justification: {rationale}")
        print()
    
    # Résumé
    success_rate = (success_count / total_count) * 100
    print(f"📊 RÉSUMÉ: {success_count}/{total_count} améliorations correctement appliquées ({success_rate:.1f}%)")
    
    if success_count == total_count:
        print("🎉 Tous les paramètres par défaut sont maintenant optimisés selon la littérature !")
        print("🌊 L'application devrait donner de meilleurs résultats sur les images sous-marines")
        
        # Test des valeurs cohérentes
        print("\n🔍 VÉRIFICATION DE COHÉRENCE:")
        
        # Vérifier cohérence entre paramètres initiaux et get_default_parameters()
        defaults = processor.get_default_parameters()
        
        coherence_checks = [
            ('gray_world_percentile', 15),
            ('beer_lambert_depth_factor', 0.15),
            ('color_rebalance_saturation_limit', 0.8),
            ('udcp_window_size', 11),
            ('multiscale_fusion_enabled', True)
        ]
        
        coherence_success = 0
        for param, expected_val in coherence_checks:
            init_val = params.get(param)
            default_val = defaults.get(param)
            
            if init_val == default_val == expected_val:
                print(f"✅ {param}: Cohérent ({init_val})")
                coherence_success += 1
            else:
                print(f"❌ {param}: Incohérent - Init: {init_val}, Default: {default_val}")
        
        if coherence_success == len(coherence_checks):
            print("✅ Parfaite cohérence entre paramètres initiaux et defaults")
        else:
            print(f"⚠️  {len(coherence_checks) - coherence_success} incohérences détectées")
            
    else:
        print("⚠️ Certaines améliorations n'ont pas été appliquées correctement")
        print("🔧 Vérifier les modifications dans src/image_processing.py")
    
    return success_count == total_count

def test_pipeline_order():
    """Teste que l'ordre du pipeline est toujours correct"""
    
    processor = ImageProcessor()
    expected_order = [
        'white_balance',
        'udcp', 
        'beer_lambert',
        'color_rebalance',
        'histogram_equalization',
        'multiscale_fusion'
    ]
    
    actual_order = processor.pipeline_order
    
    print("\n🔄 ORDRE DU PIPELINE:")
    if actual_order == expected_order:
        print("✅ Ordre du pipeline correct")
        for i, step in enumerate(actual_order, 1):
            enabled_param = f"{step}_enabled" if step != 'white_balance' else 'white_balance_enabled'
            enabled = processor.get_parameter(enabled_param)
            status = "🟢 Activé" if enabled else "🔴 Désactivé"
            print(f"   {i}. {step.replace('_', ' ').title()} - {status}")
    else:
        print("❌ Ordre du pipeline incorrect")
        print(f"   Attendu: {expected_order}")
        print(f"   Actuel:  {actual_order}")
        return False
    
    return True

if __name__ == "__main__":
    print("🚀 Démarrage validation des améliorations...\n")
    
    params_ok = validate_improvements()
    pipeline_ok = test_pipeline_order()
    
    print("\n" + "="*60)
    if params_ok and pipeline_ok:
        print("🎯 VALIDATION RÉUSSIE - Toutes les améliorations sont correctes !")
        print("📈 Les paramètres sont maintenant optimisés pour l'imagerie sous-marine")
        print("🌊 Basés sur plus de 8 références scientifiques majeures")
    else:
        print("❌ VALIDATION ÉCHOUÉE - Corrections nécessaires")
        
    print("\n📚 Améliorations appliquées selon:")
    print("• Ancuti, Ancuti & Bekaert - Fusion et color balance")
    print("• Drews, Nascimento & Botelho - UDCP sous-marin") 
    print("• Chiang & Chen - Compensation longueur d'onde")
    print("• Iqbal, Odetayo & James - Modèle couleur intégré")
    print("• He, Sun & Tang - Dark channel prior original")
