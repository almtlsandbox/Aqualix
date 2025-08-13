#!/usr/bin/env python3
"""
Script de test global pour Aqualix
Exécute tous les tests du système auto-tune
"""

import sys
import os
import subprocess
from pathlib import Path

def run_test(test_path, test_name):
    """
    Exécute un test spécifique
    
    Args:
        test_path: Chemin vers le fichier de test
        test_name: Nom descriptif du test
    """
    print(f"\n🧪 EXÉCUTION: {test_name}")
    print("=" * 50)
    
    try:
        # Exécuter depuis le répertoire racine du projet
        root_dir = Path(__file__).parent.parent
        result = subprocess.run([sys.executable, test_path], 
                               capture_output=True, text=True, cwd=root_dir)
        
        if result.returncode == 0:
            print(f"✅ {test_name}: RÉUSSI")
            return True
        else:
            print(f"❌ {test_name}: ÉCHEC")
            if result.stderr:
                print(f"Erreur: {result.stderr[:200]}...")
            return False
            
    except Exception as e:
        print(f"❌ {test_name}: ERREUR D'EXÉCUTION - {e}")
        return False

def main():
    """Exécute tous les tests du système auto-tune"""
    
    print("🚀 SUITE DE TESTS GLOBALE AQUALIX AUTO-TUNE")
    print("=" * 60)
    
    tests_root = Path(__file__).parent
    
    # Tests auto-tune (nos nouveaux tests)
    autotune_tests = [
        (tests_root / "autotune" / "test_autotune_mapping.py", "Auto-Tune Mapping System (Étape 3)"),
        (tests_root / "autotune" / "test_quality_metrics.py", "Quality Metrics Integration (Étape 4)"),
    ]
    
    # Tests d'intégration
    integration_tests = [
        (tests_root / "integration" / "test_quality_check.py", "Quality Check Integration"),
    ]
    
    # Tests UI (si ils fonctionnent)
    ui_tests = [
        (tests_root / "ui" / "test_dialog_import.py", "Dialog Import Test"),
    ]
    
    results = []
    
    # Exécution des tests auto-tune
    print("\n📂 TESTS AUTO-TUNE")
    print("-" * 30)
    for test_path, test_name in autotune_tests:
        if test_path.exists():
            success = run_test(test_path, test_name)
            results.append((test_name, success))
        else:
            print(f"⚠️  {test_name}: Fichier non trouvé - {test_path}")
            results.append((test_name, False))
    
    # Exécution des tests d'intégration
    print("\n📂 TESTS INTÉGRATION")
    print("-" * 30)
    for test_path, test_name in integration_tests:
        if test_path.exists():
            success = run_test(test_path, test_name)
            results.append((test_name, success))
        else:
            print(f"⚠️  {test_name}: Fichier non trouvé - {test_path}")
            results.append((test_name, False))
    
    # Exécution des tests UI
    print("\n📂 TESTS UI")
    print("-" * 30)
    for test_path, test_name in ui_tests:
        if test_path.exists():
            success = run_test(test_path, test_name)
            results.append((test_name, success))
        else:
            print(f"⚠️  {test_name}: Fichier non trouvé - {test_path}")
            results.append((test_name, False))
    
    # Résumé final
    print("\n🎯 RÉSUMÉ GLOBAL")
    print("=" * 60)
    
    total_tests = len(results)
    passed_tests = sum(1 for _, success in results if success)
    failed_tests = total_tests - passed_tests
    
    print(f"📊 Tests exécutés: {total_tests}")
    print(f"✅ Tests réussis: {passed_tests}")
    print(f"❌ Tests échoués: {failed_tests}")
    print(f"📈 Taux de réussite: {(passed_tests/total_tests*100):.1f}%")
    
    print("\n📋 DÉTAILS:")
    for test_name, success in results:
        status = "✅" if success else "❌"
        print(f"   {status} {test_name}")
    
    if passed_tests == total_tests:
        print(f"\n🎉 TOUS LES TESTS RÉUSSIS! Système auto-tune opérationnel.")
        return 0
    else:
        print(f"\n⚠️  {failed_tests} test(s) en échec. Vérification nécessaire.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
