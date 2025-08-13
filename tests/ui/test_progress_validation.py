#!/usr/bin/env python3
"""
Test de validation des barres de progression
Vérifie que les nouvelles barres de progression fonctionnent correctement
"""

import sys
import os
import time
import tkinter as tk
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_progress_components():
    """Test les composants de barre de progression"""
    print("🔍 Test des composants de barre de progression...")
    
    # Test import
    try:
        from progress_bar import ProgressDialog, ProgressManager, show_progress, InlineProgressBar
        print("✅ Import des composants réussi")
    except ImportError as e:
        print(f"❌ Erreur import: {e}")
        return False
    
    # Test création fenêtre racine
    root = tk.Tk()
    root.withdraw()  # Cache la fenêtre principale
    
    try:
        # Test 1: ProgressDialog direct
        print("📊 Test ProgressDialog...")
        dialog = ProgressDialog(root, "Test", "Initialisation...")
        dialog.update_message("Test en cours...")
        dialog.update_progress(50)
        dialog.update_message("Finalisation...")
        dialog.close()
        print("✅ ProgressDialog fonctionne")
        
        # Test 2: ProgressManager context manager
        print("📊 Test ProgressManager...")
        with ProgressManager(root, "Test Manager", "Début...") as progress:
            progress.update_message("Étape 1...")
            time.sleep(0.1)  # Simulation travail
            progress.update_message("Étape 2...")
            time.sleep(0.1)
            progress.update_message("Finalisation...")
        print("✅ ProgressManager fonctionne")
        
        # Test 3: show_progress fonction utilitaire
        print("📊 Test show_progress...")
        with show_progress(root, "Test Utilitaire", "Traitement...") as progress:
            progress.update_message("Simulation chargement...")
            time.sleep(0.1)
            progress.update_message("Simulation traitement...")
            time.sleep(0.1)
        print("✅ show_progress fonctionne")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors des tests: {e}")
        return False
    finally:
        root.destroy()

def test_main_integration():
    """Test l'intégration dans main.py"""
    print("🔍 Test intégration dans main.py...")
    
    try:
        # Test import de main
        import main
        print("✅ Import main.py réussi")
        
        # Vérifier que les méthodes modifiées existent
        app_class = main.ImageProcessorApp
        required_methods = ['load_image', 'save_result', 'update_preview', 'run_quality_check']
        
        for method in required_methods:
            if hasattr(app_class, method):
                print(f"✅ Méthode {method} présente")
            else:
                print(f"❌ Méthode {method} manquante")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur test intégration: {e}")
        return False

def test_imports_and_structure():
    """Test la structure et les imports"""
    print("🔍 Test structure et imports...")
    
    # Vérifier fichiers requis
    required_files = [
        "src/progress_bar.py",
        "src/main.py"
    ]
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path} existe")
        else:
            print(f"❌ {file_path} manquant")
            return False
    
    # Test imports relatifs
    try:
        os.chdir("src")
        import progress_bar
        import main
        print("✅ Imports relatifs fonctionnent")
        return True
    except Exception as e:
        print(f"❌ Erreur imports relatifs: {e}")
        return False
    finally:
        os.chdir("..")

def main():
    """Fonction principale de test"""
    print("🚀 VALIDATION BARRES DE PROGRESSION AQUALIX v2.2.0")
    print("=" * 60)
    
    tests = [
        ("Structure et imports", test_imports_and_structure),
        ("Composants progress bar", test_progress_components),
        ("Intégration main.py", test_main_integration)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}...")
        try:
            result = test_func()
            results.append(result)
            status = "✅ RÉUSSI" if result else "❌ ÉCHEC"
            print(f"   → {status}")
        except Exception as e:
            print(f"   → ❌ ERREUR: {e}")
            results.append(False)
    
    # Résumé final
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    success_rate = (passed / total) * 100 if total > 0 else 0
    
    print(f"Tests réussis: {passed}/{total} ({success_rate:.1f}%)")
    
    if success_rate == 100:
        print("🎉 TOUS LES TESTS RÉUSSIS!")
        print("✅ Barres de progression prêtes pour utilisation")
    elif success_rate >= 80:
        print("⚠️  TESTS MAJORITAIREMENT RÉUSSIS")
        print("🔧 Quelques ajustements nécessaires")
    else:
        print("❌ TESTS MAJORITAIREMENT ÉCHOUÉS")
        print("🚨 Corrections importantes requises")
    
    print("\n💡 Pour tester en conditions réelles:")
    print("   1. Lancez l'application: python main.py")
    print("   2. Chargez une image de grande taille")
    print("   3. Vérifiez l'affichage des barres de progression")
    print("   4. Testez sauvegarde et contrôle qualité")

if __name__ == "__main__":
    main()
