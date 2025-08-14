#!/usr/bin/env python3
"""
Test de la nouvelle position de la barre de progression
Teste que la barre de progression apparaît lors du clic "Sauvegarder le résultat" 
pour les calculs lents (get_full_resolution_processed_image), 
pas lors de l'écriture du fichier.
"""

import sys
import os
import tkinter as tk
import numpy as np
import time
import tempfile
from unittest.mock import patch, MagicMock

# Changer vers le répertoire src pour les imports relatifs
script_dir = os.path.dirname(__file__)
src_dir = os.path.join(script_dir, '..', 'src')
original_cwd = os.getcwd()
os.chdir(src_dir)

try:
    from main import ImageVideoProcessorApp
    
    print("🚀 TEST BARRE DE PROGRESSION - NOUVEAU POSITIONNEMENT")
    print("=" * 70)
    print("📋 Objectif: Progress bar au clic 'Sauvegarder le résultat' pendant calculs")
    
    # Créer une instance de l'app
    root = tk.Tk()
    root.withdraw()  # Cacher la fenêtre principale
    
    app = ImageVideoProcessorApp(root)
    
    # Créer une image test
    test_image = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
    app.original_image = test_image
    app.processed_image = test_image.copy()
    app.current_file = "test_image.jpg"
    
    print("✅ App créée avec image test")
    
    # Variable pour tracker l'usage de la barre de progression
    progress_calls = []
    
    def mock_show_progress(parent, title, message=""):
        progress_calls.append({'title': title, 'message': message, 'stage': 'init'})
        print(f"📊 Barre de progression: {title} - {message}")
        
        # Mock context manager
        class MockProgressContext:
            def __enter__(self):
                return self
            def __exit__(self, *args):
                progress_calls.append({'stage': 'close'})
                print(f"🔚 Barre de progression fermée")
            def update_message(self, msg):
                progress_calls.append({'update': msg, 'stage': 'update'})
                print(f"🔄 Mise à jour: {msg}")
        
        return MockProgressContext()
    
    # Options de sauvegarde mock
    mock_save_options = {
        'filename': tempfile.mktemp(suffix='.jpg'),
        'format': 'jpg',
        'quality': 95,
        'progressive': False,
        'preserve_metadata': False
    }
    
    print("🧪 Test de save_result() avec barre de progression...")
    
    # Mock des dépendances
    with patch('save_dialog.show_save_dialog', return_value=mock_save_options):
        with patch('cv2.imwrite', return_value=True):
            with patch('tkinter.messagebox.showinfo'):
                with patch('progress_bar.show_progress', side_effect=mock_show_progress):
                    
                    # Appeler save_result() (qui est maintenant le bouton principal)
                    start_time = time.time()
                    app.save_result()
                    elapsed_time = time.time() - start_time
    
    print(f"⏱️  Temps d'exécution: {elapsed_time:.3f}s")
    
    # Vérifications
    print("\n📋 RÉSULTATS DE L'ANALYSE:")
    
    if progress_calls:
        print(f"✅ Barre de progression utilisée - {len(progress_calls)} événements:")
        
        # Analyser les appels
        init_calls = [call for call in progress_calls if call.get('stage') == 'init']
        update_calls = [call for call in progress_calls if call.get('stage') == 'update']
        close_calls = [call for call in progress_calls if call.get('stage') == 'close']
        
        print(f"   📤 Initialisation: {len(init_calls)}")
        print(f"   🔄 Mises à jour: {len(update_calls)}")
        print(f"   🔚 Fermetures: {len(close_calls)}")
        
        # Vérifier le titre
        if init_calls:
            title = init_calls[0]['title']
            if "Sauvegarder le résultat" in title:
                print(f"✅ Titre correct: '{title}'")
            else:
                print(f"❌ Titre inattendu: '{title}' (attendu: contenant 'Sauvegarder le résultat')")
        
        # Vérifier les étapes
        print("\n📝 Étapes de progression détectées:")
        for i, call in enumerate(update_calls):
            print(f"   {i+1}. {call['update']}")
            
        # Vérifier les étapes importantes
        update_messages = [call['update'] for call in update_calls]
        expected_stages = [
            "Traitement à la résolution complète",
            "Préparation", 
            "Sauvegarde"
        ]
        
        stages_found = []
        for stage in expected_stages:
            found = any(stage.lower() in msg.lower() for msg in update_messages)
            stages_found.append(found)
            status = "✅" if found else "❌"
            print(f"   {status} Étape '{stage}': {'Trouvée' if found else 'Manquante'}")
        
        if all(stages_found):
            print("\n🎉 SUCCÈS COMPLET: Barre de progression correctement positionnée!")
            print("   • Progress bar s'affiche au clic 'Sauvegarder le résultat'")  
            print("   • Couvre les calculs lents (traitement pleine résolution)")
            print("   • Étapes de progression appropriées affichées")
        else:
            print(f"\n⚠️  PARTIEL: {sum(stages_found)}/{len(expected_stages)} étapes trouvées")
            
    else:
        print("❌ Aucun appel à la barre de progression détecté")
        print("   Vérifiez que show_progress est bien appelé dans save_result()")
    
    root.destroy()
    
    print("\n" + "=" * 70)
    if progress_calls and len(init_calls) > 0 and "Sauvegarder le résultat" in init_calls[0]['title']:
        print("🏆 TEST RÉUSSI: Barre de progression repositionnée correctement!")
    else:
        print("❌ TEST ÉCHOUÉ: Problème avec le positionnement de la progress bar")

except Exception as e:
    print(f"❌ Erreur: {e}")
    import traceback
    traceback.print_exc()

finally:
    # Restaurer le répertoire de travail
    os.chdir(original_cwd)

print("📝 TEST TERMINÉ")
