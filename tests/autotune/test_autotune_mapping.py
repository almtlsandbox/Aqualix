#!/usr/bin/env python3
"""
Test du système Auto-Tune Mapping (Étape 3)
Valide l'intégration complète du système de mapping auto-tune
"""

import sys
import os
import numpy as np
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.image_processing import ImageProcessor

def test_autotune_mapping_system():
    """Test complet du système de mapping auto-tune"""
    
    print("🚀 TEST SYSTÈME AUTO-TUNE MAPPING - ÉTAPE 3")
    print("=" * 60)
    
    # 1. Initialisation
    print("\n1️⃣ INITIALISATION")
    print("-" * 30)
    
    processor = ImageProcessor()
    
    # Test d'initialisation du mapping
    success = processor.initialize_autotune_mapping()
    if not success:
        print("❌ Échec d'initialisation du système de mapping")
        return False
    
    mapper = processor.get_autotune_mapper()
    if mapper is None:
        print("❌ Impossible d'obtenir le mapper auto-tune")
        return False
    
    print("✅ Système de mapping initialisé avec succès")
    
    # 2. Test de validation d'intégration
    print("\n2️⃣ VALIDATION D'INTÉGRATION")
    print("-" * 30)
    
    validation_report = mapper.validate_auto_tune_integration()
    
    if validation_report['integration_status'] not in ['excellent', 'good']:
        print("❌ Intégration insuffisante")
        return False
    
    print(f"✅ Intégration validée: {validation_report['integration_status']}")
    
    # 3. Test des modes standard vs enhanced
    print("\n3️⃣ TEST MODES STANDARD/ENHANCED")
    print("-" * 30)
    
    # Créer une image de test
    test_image = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
    
    # Test mode standard
    mapper.set_enhanced_mode(False)
    std_results = mapper.execute_auto_tune('white_balance', test_image)
    print(f"Mode standard: {len(std_results)} paramètres")
    
    # Test mode enhanced
    mapper.set_enhanced_mode(True)
    enh_results = mapper.execute_auto_tune('white_balance', test_image)
    print(f"Mode enhanced: {len(enh_results)} paramètres")
    
    # 4. Test du pipeline complet
    print("\n4️⃣ TEST PIPELINE COMPLET")
    print("-" * 30)
    
    # Test avec algorithmes spécifiques
    test_algorithms = ['white_balance', 'udcp', 'beer_lambert']
    pipeline_results = mapper.execute_pipeline_auto_tune(test_image, test_algorithms)
    
    success_count = len([r for r in pipeline_results.values() if r])
    print(f"✅ Pipeline testé: {success_count}/{len(test_algorithms)} algorithmes réussis")
    
    # 5. Test des informations d'algorithmes
    print("\n5️⃣ TEST INFORMATIONS ALGORITHMES")
    print("-" * 30)
    
    available = mapper.get_available_algorithms()
    print(f"Algorithmes disponibles: {len(available)}")
    
    for algo in available:
        info = mapper.get_algorithm_info(algo)
        if info:
            params_std = len(info['parameters'])
            params_enh = len(info.get('enhanced_parameters', []))
            print(f"  • {info['display_name']}: {params_std} std, {params_enh} enhanced")
    
    # 6. Test de l'intégration avec ImageProcessor
    print("\n6️⃣ TEST INTÉGRATION IMAGEPROCESSOR")
    print("-" * 30)
    
    # Test de la méthode auto_tune_functions
    processor_results = processor.auto_tune_functions(test_image, ['white_balance', 'udcp'])
    processor_success = len([r for r in processor_results.values() if r])
    print(f"✅ Intégration ImageProcessor: {processor_success} algorithmes réussis")
    
    # 7. Résumé final
    print("\n🎯 RÉSUMÉ TEST ÉTAPE 3")
    print("=" * 60)
    
    total_tests = 6
    passed_tests = 0
    
    if success:
        passed_tests += 1
    if validation_report['integration_status'] in ['excellent', 'good']:
        passed_tests += 1
    if std_results or enh_results:
        passed_tests += 1
    if success_count > 0:
        passed_tests += 1
    if len(available) > 0:
        passed_tests += 1
    if processor_success > 0:
        passed_tests += 1
    
    success_rate = (passed_tests / total_tests) * 100
    
    print(f"📊 Tests réussis: {passed_tests}/{total_tests} ({success_rate:.1f}%)")
    
    if success_rate >= 80:
        print("✅ ÉTAPE 3 RÉUSSIE - Système de mapping auto-tune opérationnel")
        return True
    else:
        print("❌ ÉTAPE 3 ÉCHEC - Système de mapping nécessite des corrections")
        return False

if __name__ == "__main__":
    success = test_autotune_mapping_system()
    sys.exit(0 if success else 1)
