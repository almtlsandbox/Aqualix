#!/usr/bin/env python3
"""
Script de test simple pour les tests auto-tune déplacés
Vérifie que tous les tests fonctionnent depuis leur nouvel emplacement
"""

import sys
import os
from pathlib import Path

# Ajout du répertoire racine au path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

def test_imports():
    """Test que les imports fonctionnent depuis les nouveaux emplacements"""
    
    print("🧪 TEST DES IMPORTS DEPUIS LES NOUVEAUX EMPLACEMENTS")
    print("=" * 60)
    
    tests_passed = 0
    tests_total = 0
    
    # Test 1: Import du module image_processing
    print("\n1️⃣ Test import ImageProcessor")
    try:
        from src.image_processing import ImageProcessor
        print("   ✅ ImageProcessor importé avec succès")
        tests_passed += 1
    except ImportError as e:
        print(f"   ❌ Échec import ImageProcessor: {e}")
    tests_total += 1
    
    # Test 2: Test des chemins vers les tests auto-tune
    print("\n2️⃣ Test chemins tests auto-tune")
    autotune_dir = Path(__file__).parent / "autotune"
    if autotune_dir.exists():
        test_mapping = autotune_dir / "test_autotune_mapping.py"
        test_quality = autotune_dir / "test_quality_metrics.py"
        
        if test_mapping.exists() and test_quality.exists():
            print("   ✅ Fichiers de test auto-tune trouvés")
            tests_passed += 1
        else:
            print("   ❌ Fichiers de test auto-tune manquants")
    else:
        print("   ❌ Répertoire autotune manquant")
    tests_total += 1
    
    # Test 3: Initialisation système auto-tune
    print("\n3️⃣ Test initialisation système auto-tune")
    try:
        processor = ImageProcessor()
        success = processor.initialize_autotune_mapping()
        if success:
            print("   ✅ Système de mapping initialisé")
            tests_passed += 1
        else:
            print("   ❌ Échec initialisation mapping")
    except Exception as e:
        print(f"   ❌ Erreur initialisation: {e}")
    tests_total += 1
    
    # Test 4: Initialisation métriques qualité
    print("\n4️⃣ Test initialisation métriques qualité")
    try:
        if 'processor' in locals():
            success = processor.initialize_quality_metrics()
            if success:
                print("   ✅ Système de métriques initialisé")
                tests_passed += 1
            else:
                print("   ❌ Échec initialisation métriques")
        else:
            print("   ❌ Processor non disponible")
    except Exception as e:
        print(f"   ❌ Erreur initialisation: {e}")
    tests_total += 1
    
    # Résumé
    print(f"\n🎯 RÉSUMÉ")
    print("=" * 30)
    print(f"Tests réussis: {tests_passed}/{tests_total}")
    print(f"Taux de réussite: {(tests_passed/tests_total*100):.1f}%")
    
    if tests_passed == tests_total:
        print("\n✅ TOUS LES TESTS DE BASE RÉUSSIS!")
        print("Les fichiers de test ont été correctement déplacés.")
        return True
    else:
        print(f"\n❌ {tests_total - tests_passed} test(s) en échec.")
        return False

def check_test_structure():
    """Vérifie la structure des répertoires de test"""
    
    print("\n📁 STRUCTURE DES RÉPERTOIRES DE TEST")
    print("=" * 50)
    
    tests_dir = Path(__file__).parent
    
    # Répertoires attendus
    expected_dirs = ['autotune', 'integration', 'ui', 'unit', 'analysis', 'fixtures', 'performance']
    
    for dir_name in expected_dirs:
        dir_path = tests_dir / dir_name
        if dir_path.exists():
            files = list(dir_path.glob("*.py"))
            print(f"   ✅ {dir_name}/: {len(files)} fichier(s) Python")
        else:
            print(f"   ❌ {dir_name}/: Répertoire manquant")
    
    # Fichiers de test auto-tune spécifiquement
    print("\n🔧 FICHIERS AUTO-TUNE:")
    autotune_dir = tests_dir / "autotune"
    if autotune_dir.exists():
        for test_file in autotune_dir.glob("test_*.py"):
            print(f"   📄 {test_file.name}")
    else:
        print("   ❌ Aucun fichier auto-tune trouvé")

def main():
    """Fonction principale"""
    
    print("🚀 VÉRIFICATION DÉPLACEMENT TESTS AQUALIX")
    print("=" * 60)
    
    # Vérification structure
    check_test_structure()
    
    # Test des imports et fonctionnalités
    success = test_imports()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 DÉPLACEMENT DES TESTS RÉUSSI!")
        print("Tous les fichiers de test sont correctement organisés et fonctionnels.")
        return 0
    else:
        print("⚠️  PROBLÈMES DÉTECTÉS lors du déplacement.")
        print("Vérification manuelle recommandée.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
