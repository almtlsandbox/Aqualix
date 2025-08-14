#!/usr/bin/env python3
"""
Test du système de progression granulaire
Valide que les callbacks de progression fonctionnent correctement
"""

import sys
import os
sys.path.insert(0, '.')

def test_granular_progress():
    """Test le système de progression granulaire"""
    print("🧪 TEST: Progression granulaire pendant traitement")
    print("=" * 60)
    
    try:
        from src.image_processing import ImageProcessor
        from src.main import ImageVideoProcessorApp
        import tkinter as tk
        import numpy as np
        
        print("✅ Imports réussis")
        
        # Test 1: Vérifier que process_image accepte un callback
        processor = ImageProcessor()
        test_image = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        
        progress_updates = []
        
        def test_callback(message, percentage):
            progress_updates.append((message, percentage))
            print(f"  📊 Progress: {percentage:3.0f}% - {message}")
        
        print("\n1️⃣ Test process_image avec callback:")
        processed = processor.process_image(test_image, progress_callback=test_callback)
        
        print(f"   ✅ Image traitée: {processed is not None}")
        print(f"   ✅ Callbacks reçus: {len(progress_updates)}")
        
        # Vérifier la progression logique
        is_increasing = True
        if progress_updates:
            percentages = [p[1] for p in progress_updates]
            is_increasing = all(percentages[i] <= percentages[i+1] for i in range(len(percentages)-1))
            print(f"   ✅ Progression croissante: {is_increasing}")
            print(f"   📊 Range: {min(percentages):.0f}% → {max(percentages):.0f}%")
        
        print(f"\n2️⃣ Test get_full_resolution_processed_image avec callback:")
        
        # Test avec main app
        root = tk.Tk()
        root.withdraw()
        app = ImageVideoProcessorApp(root)
        app.original_image = test_image
        
        app_progress_updates = []
        def app_callback(message, percentage):
            app_progress_updates.append((message, percentage))
            print(f"  📊 App Progress: {percentage:3.0f}% - {message}")
        
        processed_full = app.get_full_resolution_processed_image(progress_callback=app_callback)
        
        print(f"   ✅ Image full-res traitée: {processed_full is not None}")
        print(f"   ✅ Callbacks app reçus: {len(app_progress_updates)}")
        
        root.destroy()
        
        print(f"\n3️⃣ Test des étapes de progression:")
        
        # Vérifier que les étapes sont logiques
        expected_steps = [
            "Balance des blancs",
            "Correction de canal sombre",
            "Beer-Lambert", 
            "Rééquilibrage des couleurs",
            "Égalisation d'histogramme",
            "Fusion multi-échelle"
        ]
        
        step_messages = [update[0] for update in progress_updates]
        found_steps = 0
        
        for step in expected_steps:
            if any(step.lower() in msg.lower() for msg in step_messages):
                found_steps += 1
                print(f"   ✅ Étape trouvée: {step}")
        
        print(f"   📊 Étapes détectées: {found_steps}/{len(expected_steps)}")
        
        # Résumé final
        print(f"\n🎯 RÉSUMÉ DES TESTS:")
        print(f"   • Callback ImageProcessor: {'✅' if progress_updates else '❌'}")
        print(f"   • Callback App: {'✅' if app_progress_updates else '❌'}")
        print(f"   • Progression logique: {'✅' if progress_updates and is_increasing else '❌'}")
        print(f"   • Étapes détaillées: {'✅' if found_steps > 2 else '❌'}")
        
        all_tests_passed = (
            len(progress_updates) > 0 and 
            len(app_progress_updates) > 0 and
            is_increasing and
            found_steps > 2
        )
        
        if all_tests_passed:
            print("🎉 TOUS LES TESTS PASSÉS - Progression granulaire fonctionnelle!")
            return True
        else:
            print("⚠️  Certains tests ont échoué")
            return False
            
    except Exception as e:
        print(f"❌ Erreur pendant les tests: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_granular_progress()
    sys.exit(0 if success else 1)
