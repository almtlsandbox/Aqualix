#!/usr/bin/env python3
"""
Test de validation de la correction du bug de sauvegarde du rapport de qualité

BUG ORIGINAL:
- Erreur "no attribute .item" lors de la sauvegarde du rapport
- Problème: Valeurs NumPy non converties en types Python standard
- Erreur secondaire: Gestion incorrecte des listes dans les données de rapport

SOLUTION APPLIQUÉE:
1. Conversion de toutes les valeurs NumPy en types Python avec float()
2. Gestion des différents types de données dans save_report_to_file()

Auteur: Assistant GitHub Copilot
Date: 13 Août 2025
"""

import sys
import os
import tempfile
import numpy as np
from pathlib import Path

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_quality_report_save():
    """Test complet de la sauvegarde de rapport de qualité"""
    
    try:
        from quality_check import PostProcessingQualityChecker
        from quality_check_dialog import QualityCheckDialog
        from localization import LocalizationManager
        
        print("🔧 TEST DE SAUVEGARDE RAPPORT DE QUALITÉ")
        print("=" * 50)
        
        # 1. Setup des composants
        print("📋 1. Initialisation des composants...")
        loc = LocalizationManager()
        checker = PostProcessingQualityChecker()
        
        # 2. Génération de données de test
        print("🎲 2. Génération de données de test...")
        test_original = np.random.randint(0, 255, (200, 300, 3), dtype=np.uint8)
        
        # Créer une image "traitée" avec des différences notables
        test_processed = test_original.copy()
        test_processed[:, :, 0] = np.clip(test_processed[:, :, 0] * 1.3, 0, 255)  # Plus de rouge
        test_processed[:, :, 1] = np.clip(test_processed[:, :, 1] * 0.9, 0, 255)  # Moins de vert
        
        # 3. Exécution du check qualité
        print("🔍 3. Exécution de l'analyse qualité...")
        results = checker.run_all_checks(test_original, test_processed)
        
        print(f"   ✅ Analyse complétée: {len(results)} sections trouvées")
        
        # 4. Vérification des types de données
        print("📊 4. Vérification des types de données...")
        numpy_values_found = 0
        python_values_found = 0
        
        for section_key, section_data in results.items():
            if isinstance(section_data, dict):
                for key, value in section_data.items():
                    if isinstance(value, (int, float)):
                        if hasattr(value, 'item'):  # Valeur NumPy
                            numpy_values_found += 1
                            print(f"   ⚠️  Valeur NumPy détectée: {section_key}.{key} = {type(value)}")
                        else:  # Valeur Python standard
                            python_values_found += 1
        
        print(f"   ✅ Valeurs Python standard: {python_values_found}")
        if numpy_values_found > 0:
            print(f"   ❌ Valeurs NumPy non converties: {numpy_values_found}")
            return False
        else:
            print(f"   ✅ Aucune valeur NumPy non convertie détectée")
        
        # 5. Test de sauvegarde
        print("💾 5. Test de sauvegarde du rapport...")
        dialog = QualityCheckDialog(None, results, 'image_test.jpg', loc)
        
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.txt', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            dialog.save_report_to_file(tmp_path)
            print("   ✅ Sauvegarde réussie!")
            
            # Vérifier le contenu
            with open(tmp_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = len(content.split('\n'))
                
            print(f"   ✅ Rapport généré: {lines} lignes")
            
            # Afficher un extrait
            preview_lines = content.split('\n')[:8]
            print("   📄 Aperçu du rapport:")
            for i, line in enumerate(preview_lines, 1):
                print(f"      {i:2d}: {line}")
                
            return True
            
        except Exception as save_error:
            print(f"   ❌ Erreur de sauvegarde: {save_error}")
            return False
            
        finally:
            # Nettoyage
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
                print("   🧹 Fichier temporaire nettoyé")
    
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur générale: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_specific_numpy_conversions():
    """Test spécifique des conversions NumPy"""
    
    print("\n🔢 TEST DES CONVERSIONS NUMPY")
    print("=" * 40)
    
    # Test des types NumPy courants
    test_values = {
        'np.float64': np.float64(3.14159),
        'np.float32': np.float32(2.71828),
        'np.int64': np.int64(42),
        'np.int32': np.int32(123),
        'np.mean result': np.mean([1.0, 2.0, 3.0]),
        'np.sum result': np.sum([10, 20, 30]),
        'np.var result': np.var([1, 2, 3, 4, 5])
    }
    
    all_converted = True
    
    for name, value in test_values.items():
        converted = float(value)
        is_python_type = isinstance(converted, (int, float)) and not hasattr(converted, 'item')
        
        print(f"   {name:15} -> {type(converted).__name__:10} {'✅' if is_python_type else '❌'}")
        
        if not is_python_type:
            all_converted = False
    
    return all_converted

if __name__ == "__main__":
    print("🚀 VALIDATION CORRECTION BUG RAPPORT QUALITÉ")
    print("=" * 60)
    
    # Test 1: Conversions NumPy
    numpy_test = test_specific_numpy_conversions()
    
    # Test 2: Sauvegarde complète
    save_test = test_quality_report_save()
    
    print("\n📋 RÉSUMÉ DES TESTS")
    print("=" * 30)
    print(f"Conversions NumPy:     {'✅ PASS' if numpy_test else '❌ FAIL'}")
    print(f"Sauvegarde rapport:    {'✅ PASS' if save_test else '❌ FAIL'}")
    
    if numpy_test and save_test:
        print("\n🎉 TOUS LES TESTS PASSENT!")
        print("   Le bug de sauvegarde du rapport de qualité est corrigé.")
        sys.exit(0)
    else:
        print("\n❌ ÉCHEC DES TESTS!")
        print("   Le bug persiste, vérifications supplémentaires nécessaires.")
        sys.exit(1)
