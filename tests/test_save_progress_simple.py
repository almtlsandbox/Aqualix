#!/usr/bin/env python3
"""
Test simple de la barre de progression lors de la sauvegarde d'image
"""

import sys
import os
import tkinter as tk
import numpy as np
import tempfile
from unittest.mock import patch, MagicMock

# Changer vers le répertoire src pour les imports relatifs
script_dir = os.path.dirname(__file__)
src_dir = os.path.join(script_dir, '..', 'src')
original_cwd = os.getcwd()
os.chdir(src_dir)

try:
    from main import ImageVideoProcessorApp
    
    print("🚀 TEST BARRE DE PROGRESSION SAUVEGARDE - VERSION SIMPLE")
    print("=" * 65)
    
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
        progress_calls.append({'title': title, 'message': message})
        print(f"📊 Barre de progression: {title} - {message}")
        
        # Mock context manager simple
        class MockProgressContext:
            def __enter__(self):
                return self
            def __exit__(self, *args):
                pass
            def update_message(self, msg):
                progress_calls.append({'update': msg})
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
    
    print("🧪 Test de save_image avec barre de progression...")
    
    # Mock des dépendances
    with patch('save_dialog.show_save_dialog', return_value=mock_save_options):
        with patch('cv2.imwrite', return_value=True):
            with patch('tkinter.messagebox.showinfo'):
                with patch('progress_bar.show_progress', side_effect=mock_show_progress):
                    
                    # Appeler save_image
                    app.save_image()
    
    # Vérifier que la barre de progression a été utilisée
    if progress_calls:
        print(f"✅ Barre de progression utilisée {len(progress_calls)} fois:")
        for call in progress_calls:
            if 'title' in call:
                print(f"   📋 Titre: {call['title']}")
                print(f"   💬 Message: {call['message']}")
            elif 'update' in call:
                print(f"   🔄 Update: {call['update']}")
        
        print("✅ Test réussi - La barre de progression fonctionne!")
    else:
        print("❌ Aucun appel à la barre de progression détecté")
    
    root.destroy()
    
except Exception as e:
    print(f"❌ Erreur: {e}")
    import traceback
    traceback.print_exc()

finally:
    # Restaurer le répertoire de travail
    os.chdir(original_cwd)

print("=" * 65)
print("📝 TEST TERMINÉ")
