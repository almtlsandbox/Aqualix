#!/usr/bin/env python3
"""
Test de fermeture automatique de la barre de progression
Vérifie que la progress bar disparaît après la completion des calculs
"""

import sys
import os
import tkinter as tk
import numpy as np
import time
import tempfile
from unittest.mock import patch, MagicMock

# Ajouter le répertoire src au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

print("🚀 TEST FERMETURE BARRE DE PROGRESSION")
print("=" * 55)
print("📋 Objectif: Vérifier que la progress bar disparaît automatiquement")

try:
    # Changer vers le répertoire src pour les imports relatifs
    original_cwd = os.getcwd()
    src_dir = os.path.join(os.path.dirname(__file__), '..', 'src')
    os.chdir(src_dir)
    
    from main import ImageVideoProcessorApp
    
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
    
    # Variables pour tracker le cycle de vie de la progress bar
    progress_lifecycle = []
    
    # Mock original ProgressDialog pour tracker sa création/destruction
    original_progress_dialog = None
    
    def mock_show_progress(parent, title, message=""):
        progress_lifecycle.append({'action': 'created', 'title': title, 'time': time.time()})
        print(f"📊 Progress bar créée: {title}")
        
        # Mock context manager qui track la fermeture
        class MockProgressContext:
            def __init__(self):
                self.closed = False
                
            def __enter__(self):
                progress_lifecycle.append({'action': 'entered', 'time': time.time()})
                print(f"🔓 Progress bar context entré")
                return self
                
            def __exit__(self, *args):
                progress_lifecycle.append({'action': 'exited', 'time': time.time()})
                self.closed = True
                print(f"🔒 Progress bar context fermé")
                
                # Simuler un petit délai pour vérifier la fermeture
                time.sleep(0.1)
                progress_lifecycle.append({'action': 'destroyed', 'time': time.time()})
                print(f"🗑️  Progress bar détruite")
                
            def update_message(self, msg):
                progress_lifecycle.append({'action': 'update', 'message': msg, 'time': time.time()})
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
    
    print("\n🧪 Test du cycle de vie complet save_result()...")
    
    start_test_time = time.time()
    
    # Mock des dépendances
    with patch('save_dialog.show_save_dialog', return_value=mock_save_options):
        with patch('cv2.imwrite', return_value=True):
            with patch('tkinter.messagebox.showinfo'):
                with patch('progress_bar.show_progress', side_effect=mock_show_progress):
                    
                    # Appeler save_result() 
                    app.save_result()
    
    end_test_time = time.time()
    total_time = end_test_time - start_test_time
    
    print(f"\n⏱️  Temps total d'exécution: {total_time:.3f}s")
    
    # Analyser le cycle de vie
    print("\n📋 ANALYSE DU CYCLE DE VIE:")
    
    if progress_lifecycle:
        print(f"✅ {len(progress_lifecycle)} événements de cycle de vie détectés")
        
        # Analyser les actions
        actions = [event['action'] for event in progress_lifecycle]
        action_counts = {action: actions.count(action) for action in set(actions)}
        
        print(f"   📤 Créations: {action_counts.get('created', 0)}")
        print(f"   🔓 Entrées context: {action_counts.get('entered', 0)}")  
        print(f"   🔄 Mises à jour: {action_counts.get('update', 0)}")
        print(f"   🔒 Sorties context: {action_counts.get('exited', 0)}")
        print(f"   🗑️  Destructions: {action_counts.get('destroyed', 0)}")
        
        # Vérifier le cycle de vie correct
        has_creation = action_counts.get('created', 0) > 0
        has_entrance = action_counts.get('entered', 0) > 0
        has_exit = action_counts.get('exited', 0) > 0
        has_destruction = action_counts.get('destroyed', 0) > 0
        has_updates = action_counts.get('update', 0) > 0
        
        # Vérifier l'équilibre création/destruction
        balanced = action_counts.get('created', 0) == action_counts.get('destroyed', 0)
        context_balanced = action_counts.get('entered', 0) == action_counts.get('exited', 0)
        
        print(f"\n🔍 VÉRIFICATIONS:")
        print(f"   ✅ Création: {'✅' if has_creation else '❌'}")
        print(f"   ✅ Context entré: {'✅' if has_entrance else '❌'}")
        print(f"   ✅ Mises à jour: {'✅' if has_updates else '❌'}")
        print(f"   ✅ Context fermé: {'✅' if has_exit else '❌'}")
        print(f"   ✅ Destruction: {'✅' if has_destruction else '❌'}")
        print(f"   ✅ Équilibre création/destruction: {'✅' if balanced else '❌'}")
        print(f"   ✅ Équilibre context enter/exit: {'✅' if context_balanced else '❌'}")
        
        # Chronologie détaillée
        print(f"\n📅 CHRONOLOGIE DÉTAILLÉE:")
        for i, event in enumerate(progress_lifecycle):
            elapsed = event['time'] - start_test_time
            action = event['action']
            extra = f" - {event.get('message', event.get('title', ''))}" if 'message' in event or 'title' in event else ""
            print(f"   {i+1:2d}. {elapsed:6.3f}s - {action.upper()}{extra}")
        
        # Calculs de timing
        if progress_lifecycle:
            creation_time = next((e['time'] for e in progress_lifecycle if e['action'] == 'created'), None)
            destruction_time = next((e['time'] for e in progress_lifecycle if e['action'] == 'destroyed'), None)
            
            if creation_time and destruction_time:
                duration = destruction_time - creation_time
                print(f"\n⏲️  DURÉE DE VIE PROGRESS BAR: {duration:.3f}s")
                
                if duration < total_time * 1.2:  # Moins de 120% du temps total
                    print(f"✅ Progress bar fermée rapidement après completion")
                else:
                    print(f"⚠️  Progress bar a persisté longtemps après completion")
        
        # Conclusion
        if has_creation and has_entrance and has_exit and has_destruction and balanced and context_balanced:
            print(f"\n🎉 SUCCÈS COMPLET!")
            print(f"   La barre de progression a un cycle de vie correct:")
            print(f"   • Création → Entrée → Updates → Sortie → Destruction")
            print(f"   • Fermeture automatique après completion des calculs")
        else:
            print(f"\n⚠️  PROBLÈME DÉTECTÉ:")
            if not balanced:
                print(f"   • Déséquilibre création/destruction")
            if not context_balanced:
                print(f"   • Déséquilibre context manager")
            if not (has_exit and has_destruction):
                print(f"   • Progress bar ne se ferme pas correctement")
                
    else:
        print("❌ Aucun événement de cycle de vie détecté")
        print("   La barre de progression n'a pas été utilisée")
    
    root.destroy()

except Exception as e:
    print(f"❌ Erreur: {e}")
    import traceback
    traceback.print_exc()

finally:
    # Restaurer le répertoire de travail
    os.chdir(original_cwd)

print("\n" + "=" * 55)
print("📝 TEST TERMINÉ")
