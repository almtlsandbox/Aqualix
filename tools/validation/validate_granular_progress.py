#!/usr/bin/env python3
"""
Validation de la progression granulaire - système complet
Vérifie que le système de callbacks et progression détaillée fonctionne
"""

import sys
import os

# Ajouter le répertoire racine au path  
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

def validate_granular_system():
    """Valide le système de progression granulaire complet"""
    print("🚀 VALIDATION PROGRESSION GRANULAIRE COMPLÈTE")
    print("=" * 65)
    
    try:
        # Test 1: Import et fonctionnement des callbacks
        print("📋 Test 1: Système de callbacks")
        
        from src.image_processing import ImageProcessor
        from src.main import ImageVideoProcessorApp
        import tkinter as tk
        import numpy as np
        
        # Test ImageProcessor avec callbacks
        processor = ImageProcessor()
        test_image = np.random.randint(0, 255, (50, 50, 3), dtype=np.uint8)
        
        callback_calls = []
        def test_callback(message, percentage):
            callback_calls.append((message, percentage))
        
        processed = processor.process_image(test_image, progress_callback=test_callback)
        
        print(f"   • Callbacks reçus: {len(callback_calls)} ✅")
        print(f"   • Image traitée: {'✅' if processed is not None else '❌'}")
        
        # Test 2: Messages en français
        print("\n📋 Test 2: Messages contextuels français")
        
        french_terms = [
            "Balance des blancs",
            "canal sombre", 
            "Beer-Lambert",
            "Rééquilibrage",
            "histogramme",
            "multi-échelle"
        ]
        
        messages = [call[0] for call in callback_calls]
        found_terms = 0
        
        for term in french_terms:
            if any(term.lower() in msg.lower() for msg in messages):
                print(f"   • Terme '{term}': ✅")
                found_terms += 1
            else:
                print(f"   • Terme '{term}': ❌")
        
        # Test 3: Progression logique
        print("\n📋 Test 3: Logique de progression")
        
        is_increasing = False
        good_range = False
        
        if callback_calls:
            percentages = [call[1] for call in callback_calls]
            is_increasing = all(percentages[i] <= percentages[i+1] for i in range(len(percentages)-1))
            good_range = 10 <= min(percentages) and max(percentages) <= 85
            
            print(f"   • Progression croissante: {'✅' if is_increasing else '❌'}")
            print(f"   • Range approprié (10-85%): {'✅' if good_range else '❌'}")
            print(f"   • Nombre d'étapes: {len(callback_calls)} ({'✅' if len(callback_calls) >= 4 else '❌'})")
        
        # Test 4: Intégration main app
        print("\n📋 Test 4: Intégration application principale")
        
        root = tk.Tk()
        root.withdraw()
        app = ImageVideoProcessorApp(root)
        app.original_image = test_image
        
        app_callbacks = []
        def app_callback(msg, pct):
            app_callbacks.append((msg, pct))
        
        full_res = app.get_full_resolution_processed_image(progress_callback=app_callback)
        
        print(f"   • App callbacks reçus: {len(app_callbacks)} ✅")
        print(f"   • Full-res traitée: {'✅' if full_res is not None else '❌'}")
        
        root.destroy()
        
        # Test 5: Validation fichiers organisés
        print("\n📋 Test 5: Organisation des fichiers")
        
        test_files = [
            ("tests/test_granular_progress.py", "Test progression granulaire"),
            ("tests/test_video_progress.py", "Test progression vidéo"),
            ("tools/validation/validate_progress_closure.py", "Validation fermeture"),
            ("tools/validation/validate_progress_repositioning.py", "Validation positionnement")
        ]
        
        organized_files = 0
        base_path = os.path.join(os.path.dirname(__file__), '..', '..')
        
        for file_path, description in test_files:
            full_path = os.path.join(base_path, file_path)
            if os.path.exists(full_path):
                print(f"   • {description}: ✅")
                organized_files += 1
            else:
                print(f"   • {description}: ❌ (cherché: {full_path})")
        
        # Résumé final
        print(f"\n🎯 RÉSUMÉ VALIDATION:")
        print(f"   • Callbacks fonctionnels: {'✅' if len(callback_calls) > 0 else '❌'}")
        print(f"   • Messages français: {found_terms}/6 ({'✅' if found_terms >= 4 else '❌'})")
        print(f"   • Progression logique: {'✅' if is_increasing and good_range else '❌'}")
        print(f"   • Intégration app: {'✅' if len(app_callbacks) > 0 else '❌'}")
        print(f"   • Fichiers organisés: {organized_files}/4 ({'✅' if organized_files >= 3 else '❌'})")
        
        # Validation globale
        validations_passed = (
            len(callback_calls) > 0 and
            found_terms >= 4 and
            is_increasing and good_range and
            len(app_callbacks) > 0 and
            organized_files >= 3
        )
        
        if validations_passed:
            print("\n🎉 PROGRESSION GRANULAIRE ENTIÈREMENT VALIDÉE!")
            print("   ✅ Système de callbacks opérationnel")
            print("   ✅ Messages contextuels en français")
            print("   ✅ Progression mathématiquement cohérente") 
            print("   ✅ Intégration application complète")
            print("   ✅ Organisation des fichiers correcte")
            return True
        else:
            print("\n⚠️  Validation incomplète")
            return False
            
    except Exception as e:
        print(f"❌ Erreur pendant validation: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = validate_granular_system()
    print("\n" + "=" * 65)
    print("📝 VALIDATION TERMINÉE")
    sys.exit(0 if success else 1)
