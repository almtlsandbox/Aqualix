#!/usr/bin/env python3
"""
Test spécifique pour vérifier la barre de progression du chargement d'image
"""

import sys
import os
from pathlib import Path

# Assurer le chemin vers le projet
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_image_loading_progress():
    """Test la barre de progression lors du chargement d'image"""
    print("🔍 Test barre de progression - Chargement d'image")
    
    try:
        # Import du main module
        from src.main import ImageProcessorApp
        import tkinter as tk
        
        print("✅ Import réussi")
        
        # Créer l'application
        root = tk.Tk()
        app = ImageProcessorApp(root)
        
        print("✅ Application créée")
        
        # Simuler le chargement d'une image de test
        test_image_path = "test_images/underwater_test.jpg"
        if os.path.exists(test_image_path):
            print(f"📸 Test avec image: {test_image_path}")
            
            # Définir le fichier courant
            app.files_list = [test_image_path]
            app.current_index = 0
            
            # Simuler le chargement
            print("🚀 Lancement du chargement avec barre de progression...")
            app.load_current_file()
            
            print("✅ Chargement terminé!")
            
        else:
            print(f"❌ Image de test non trouvée: {test_image_path}")
        
        # Nettoyer
        root.destroy()
        print("✅ Test complété")
        
    except Exception as e:
        print(f"❌ Erreur durant le test: {e}")
        import traceback
        traceback.print_exc()

def test_progress_dialog_directly():
    """Test direct du composant ProgressDialog"""
    print("\n🔍 Test direct ProgressDialog")
    
    try:
        import tkinter as tk
        
        # Import du composant
        sys.path.insert(0, str(Path(__file__).parent / "src"))
        from progress_bar import ProgressDialog, show_progress
        
        print("✅ Import progress_bar réussi")
        
        # Test avec contexte manager
        root = tk.Tk()
        root.withdraw()  # Cache la fenêtre principale
        
        print("📊 Test avec show_progress...")
        with show_progress(root, "Test Chargement", "Simulation chargement image...") as progress:
            import time
            
            progress.update_message("Lecture du fichier...")
            time.sleep(0.5)
            
            progress.update_message("Conversion RGB...")
            time.sleep(0.5)
            
            progress.update_message("Auto-tune...")
            time.sleep(0.5)
            
            progress.update_message("Génération aperçu...")
            time.sleep(0.3)
        
        print("✅ Test show_progress réussi!")
        
        # Test direct ProgressDialog
        print("📊 Test ProgressDialog direct...")
        dialog = ProgressDialog(root, "Test Direct", "Initialisation...")
        dialog.show()
        
        import time
        time.sleep(0.3)
        dialog.update_message("Étape 1...")
        time.sleep(0.3)
        dialog.update_message("Étape 2...")
        time.sleep(0.3)
        dialog.update_message("Finalisation...")
        time.sleep(0.3)
        
        dialog.hide()
        print("✅ Test ProgressDialog direct réussi!")
        
        root.destroy()
        
    except Exception as e:
        print(f"❌ Erreur test direct: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 TEST BARRES DE PROGRESSION - CHARGEMENT D'IMAGE")
    print("=" * 60)
    
    test_progress_dialog_directly()
    test_image_loading_progress()
    
    print("\n" + "=" * 60)
    print("💡 Pour test manuel:")
    print("   1. Lancez: python main.py")
    print("   2. Cliquez 'Browse File'")
    print("   3. Sélectionnez une image")
    print("   4. Observez la barre de progression")
