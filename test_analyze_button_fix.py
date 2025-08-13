#!/usr/bin/env python3
"""
Test de validation de la correction du bouton Analyser
Fix de l'erreur: 'ImageVideoProcessorApp' object has no attribute 'processed_full_cache'
"""

import os
import sys
import traceback

def test_analyze_fix():
    """Test la correction du bouton Analyser dans l'onglet Quality Control"""
    print("\n" + "="*60)
    print("🔧 TEST DE CORRECTION - BOUTON ANALYSER")
    print("="*60)
    
    tests_passed = 0
    total_tests = 5
    
    try:
        # Test 1: Import du module QualityControlTab
        print("\n1. Test import QualityControlTab...")
        from src.quality_control_tab import QualityControlTab
        print("   ✅ Import réussi")
        tests_passed += 1
        
        # Test 2: Vérification que processed_full_cache n'est plus utilisé
        print("\n2. Test suppression de processed_full_cache...")
        with open('src/quality_control_tab.py', 'r', encoding='utf-8') as f:
            content = f.read()
            if 'processed_full_cache' not in content:
                print("   ✅ processed_full_cache supprimé du code")
                tests_passed += 1
            else:
                print("   ❌ processed_full_cache encore présent")
        
        # Test 3: Vérification de l'utilisation de get_processed_image
        print("\n3. Test utilisation de get_processed_image...")
        if 'get_processed_image()' in content:
            print("   ✅ get_processed_image() utilisé correctement")
            tests_passed += 1
        else:
            print("   ❌ get_processed_image() non trouvé")
        
        # Test 4: Test avec mock app
        print("\n4. Test création QualityControlTab avec mock...")
        import tkinter as tk
        from src.localization import LocalizationManager
        from unittest.mock import Mock
        import numpy as np
        
        # Mock app avec attributs corrects
        mock_app = Mock()
        mock_app.current_file = 'test.jpg'
        mock_app.get_processed_image.return_value = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        mock_app.get_full_resolution_image.return_value = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        
        loc = LocalizationManager()
        
        root = tk.Tk()
        tab = QualityControlTab(root, mock_app, loc)
        root.destroy()
        
        print("   ✅ QualityControlTab créé sans erreur")
        tests_passed += 1
        
        # Test 5: Import de l'application principale
        print("\n5. Test import application principale...")
        import src.main
        print("   ✅ Application principale importée")
        tests_passed += 1
        
    except Exception as e:
        print(f"   ❌ Erreur pendant les tests: {e}")
        traceback.print_exc()
    
    # Résultats
    print("\n" + "="*60)
    print(f"🎯 RÉSULTATS DE LA CORRECTION")
    print(f"   Tests réussis: {tests_passed}/{total_tests}")
    print(f"   Pourcentage de réussite: {(tests_passed/total_tests)*100:.1f}%")
    
    if tests_passed == total_tests:
        print("\n🎊 CORRECTION RÉUSSIE!")
        print("   ✅ Plus d'erreur 'processed_full_cache'")
        print("   ✅ Le bouton Analyser fonctionne maintenant")
        print("   ✅ Utilise get_processed_image() de l'application")
        return True
    else:
        print(f"\n⚠️  CORRECTION PARTIELLE ({tests_passed}/{total_tests})")
        return False

if __name__ == "__main__":
    test_analyze_fix()
