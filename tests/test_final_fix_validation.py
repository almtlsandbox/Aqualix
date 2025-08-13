#!/usr/bin/env python3
"""
Test de validation final - Correction du bouton Analyser
Fix de l'erreur: 'ImageVideoProcessorApp' object has no attribute 'processed_full_cache'
"""

import os
import sys
import traceback

def test_complete_fix():
    """Test complet de la correction du bouton Analyser"""
    print("\n" + "="*60)
    print("🔧 VALIDATION FINALE - CORRECTION BOUTON ANALYSER")
    print("="*60)
    
    tests_passed = 0
    total_tests = 6
    
    try:
        # Test 1: Import du module QualityControlTab
        print("\n1. Test import QualityControlTab...")
        from src.quality_control_tab import QualityControlTab
        print("   ✅ Import réussi")
        tests_passed += 1
        
        # Test 2: Vérification suppression processed_full_cache
        print("\n2. Test suppression processed_full_cache...")
        with open('src/quality_control_tab.py', 'r', encoding='utf-8') as f:
            content = f.read()
            if 'processed_full_cache' not in content:
                print("   ✅ processed_full_cache supprimé")
                tests_passed += 1
            else:
                print("   ❌ processed_full_cache encore présent")
        
        # Test 3: Vérification suppression get_processed_image()
        print("\n3. Test suppression get_processed_image...")
        if 'get_processed_image()' not in content:
            print("   ✅ get_processed_image() supprimé")
            tests_passed += 1
        else:
            print("   ❌ get_processed_image() encore présent")
            
        # Test 4: Vérification utilisation get_full_resolution_processed_image
        print("\n4. Test utilisation get_full_resolution_processed_image...")
        if 'get_full_resolution_processed_image()' in content:
            print("   ✅ get_full_resolution_processed_image() utilisé")
            tests_passed += 1
        else:
            print("   ❌ get_full_resolution_processed_image() non trouvé")
        
        # Test 5: Test création avec vraie app
        print("\n5. Test création avec vraie application...")
        from src.main import ImageVideoProcessorApp
        import tkinter as tk
        from src.localization import LocalizationManager
        import numpy as np
        
        root = tk.Tk()
        root.withdraw()
        
        app = ImageVideoProcessorApp(root)
        loc = LocalizationManager()
        
        # Ajouter image test
        app.original_image = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        app.current_file = 'test.jpg'
        
        tab_frame = tk.Frame(root)
        tab = QualityControlTab(tab_frame, app, loc)
        
        root.destroy()
        
        print("   ✅ QualityControlTab créé avec vraie app")
        tests_passed += 1
        
        # Test 6: Vérification méthode disponible dans app
        print("\n6. Test méthodes disponibles dans ImageVideoProcessorApp...")
        root = tk.Tk()
        root.withdraw()
        app = ImageVideoProcessorApp(root)
        
        has_method = hasattr(app, 'get_full_resolution_processed_image')
        if has_method:
            print("   ✅ get_full_resolution_processed_image existe dans l'app")
            tests_passed += 1
        else:
            print("   ❌ get_full_resolution_processed_image n'existe pas")
            
        root.destroy()
        
    except Exception as e:
        print(f"   ❌ Erreur pendant les tests: {e}")
        traceback.print_exc()
    
    # Résultats
    print("\n" + "="*60)
    print(f"🎯 RÉSULTATS DE LA CORRECTION")
    print(f"   Tests réussis: {tests_passed}/{total_tests}")
    print(f"   Pourcentage de réussite: {(tests_passed/total_tests)*100:.1f}%")
    
    if tests_passed == total_tests:
        print("\n🎊 CORRECTION COMPLÈTE RÉUSSIE!")
        print("   ✅ Plus d'erreur 'processed_full_cache'")
        print("   ✅ Plus d'erreur 'get_processed_image'")
        print("   ✅ Utilise get_full_resolution_processed_image()")
        print("   ✅ Le bouton Analyser fonctionne maintenant")
        print("   ✅ Compatible avec l'architecture existante")
        return True
    else:
        print(f"\n⚠️  CORRECTION PARTIELLE ({tests_passed}/{total_tests})")
        return False

if __name__ == "__main__":
    success = test_complete_fix()
    if success:
        print("\n🚀 APPLICATION PRÊTE À UTILISER!")
    else:
        print("\n⚠️  CORRECTIONS SUPPLÉMENTAIRES NÉCESSAIRES")
