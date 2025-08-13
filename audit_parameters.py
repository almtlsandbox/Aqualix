#!/usr/bin/env python3
"""
Audit complet des paramètres exposés dans Aqualix
Vérifie que tous les paramètres des algorithmes sont correctement exposés à l'utilisateur
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))

from src.image_processing import ImageProcessor

def audit_parameters():
    """Audit complet de l'exposition des paramètres"""
    print("🔍 AUDIT COMPLET DES PARAMÈTRES AQUALIX")
    print("=" * 60)
    
    processor = ImageProcessor()
    
    # Récupérer tous les paramètres par défaut
    default_params = processor.get_default_parameters()
    
    # Récupérer les informations UI des paramètres  
    param_info = processor.get_parameter_info()
    
    print(f"\n📊 STATISTIQUES GÉNÉRALES:")
    print(f"   • Paramètres par défaut: {len(default_params)}")
    print(f"   • Paramètres UI: {len(param_info)}")
    
    # Grouper par algorithme
    algorithms = {
        'White Balance': [],
        'UDCP': [],
        'Beer-Lambert': [],
        'Color Rebalancing': [],
        'Histogram Equalization': [],
        'Multiscale Fusion': []
    }
    
    # Classer les paramètres par algorithme
    for param_name in default_params.keys():
        if 'white_balance' in param_name or 'gray_world' in param_name or 'white_patch' in param_name or \
           'shades_of_gray' in param_name or 'grey_edge' in param_name or 'lake_' in param_name:
            algorithms['White Balance'].append(param_name)
        elif 'udcp' in param_name:
            algorithms['UDCP'].append(param_name)
        elif 'beer_lambert' in param_name:
            algorithms['Beer-Lambert'].append(param_name)
        elif 'color_rebalance' in param_name:
            algorithms['Color Rebalancing'].append(param_name)
        elif 'hist_eq' in param_name:
            algorithms['Histogram Equalization'].append(param_name)
        elif 'fusion' in param_name:
            algorithms['Multiscale Fusion'].append(param_name)
    
    # Audit par algorithme
    total_exposed = 0
    total_parameters = 0
    
    for algo_name, params in algorithms.items():
        if not params:
            continue
            
        print(f"\n🔧 {algo_name.upper()}")
        print("-" * 50)
        
        exposed_count = 0
        for param in params:
            total_parameters += 1
            if param in param_info:
                exposed_count += 1
                total_exposed += 1
                ui_info = param_info[param]
                print(f"   ✅ {param}")
                print(f"      Type: {ui_info['type']}, Label: {ui_info.get('label', 'N/A')}")
                if 'min' in ui_info and 'max' in ui_info:
                    print(f"      Range: {ui_info['min']} - {ui_info['max']}")
                if 'visible_when' in ui_info:
                    print(f"      Visible when: {ui_info['visible_when']}")
            else:
                print(f"   ❌ {param} - NON EXPOSÉ")
        
        coverage = (exposed_count / len(params)) * 100 if params else 0
        print(f"\n   📈 Couverture: {exposed_count}/{len(params)} ({coverage:.1f}%)")
    
    # Vérifier les paramètres UI qui n'ont pas de défaut
    orphan_ui_params = set(param_info.keys()) - set(default_params.keys())
    if orphan_ui_params:
        print(f"\n⚠️  PARAMÈTRES UI ORPHELINS (sans défaut):")
        for param in orphan_ui_params:
            print(f"   • {param}")
    
    # Résumé final
    overall_coverage = (total_exposed / total_parameters) * 100 if total_parameters else 0
    print(f"\n🎯 RÉSUMÉ GLOBAL:")
    print(f"   • Total paramètres: {total_parameters}")
    print(f"   • Paramètres exposés: {total_exposed}")
    print(f"   • Couverture globale: {overall_coverage:.1f}%")
    
    if overall_coverage >= 95:
        print("   ✅ EXCELLENT - Presque tous les paramètres sont exposés!")
    elif overall_coverage >= 80:
        print("   ⚠️  BON - Majorité des paramètres exposés")
    else:
        print("   ❌ INSUFFISANT - Beaucoup de paramètres manquants")
    
    return total_parameters, total_exposed, overall_coverage

def audit_algorithm_integrity():
    """Audit de l'intégrité des implémentations d'algorithmes"""
    print(f"\n\n🔬 AUDIT INTÉGRITÉ DES ALGORITHMES")
    print("=" * 60)
    
    processor = ImageProcessor()
    
    # Liste des méthodes d'algorithmes à vérifier
    algorithms_to_check = [
        ('White Balance - Gray World', 'gray_world_white_balance'),
        ('White Balance - White Patch', 'white_patch_white_balance'),
        ('White Balance - Shades of Gray', 'shades_of_gray_white_balance'),
        ('White Balance - Grey Edge', 'grey_edge_white_balance'),
        ('White Balance - Lake Green Water', 'lake_green_water_white_balance'),
        ('UDCP', 'underwater_dark_channel_prior'),
        ('Beer-Lambert', 'beer_lambert_correction'),
        ('Color Rebalancing', 'color_rebalance'),
        ('Histogram Equalization', 'adaptive_histogram_equalization'),
        ('Multiscale Fusion', 'multiscale_fusion')
    ]
    
    implementation_status = []
    
    for algo_name, method_name in algorithms_to_check:
        print(f"\n🔍 {algo_name}")
        print("-" * 40)
        
        # Vérifier si la méthode existe
        if hasattr(processor, method_name):
            print(f"   ✅ Méthode {method_name} présente")
            
            # Vérifier la signature de la méthode
            method = getattr(processor, method_name)
            if callable(method):
                print(f"   ✅ Méthode callable")
                implementation_status.append((algo_name, True, "Implémenté"))
            else:
                print(f"   ❌ Méthode non callable")
                implementation_status.append((algo_name, False, "Non callable"))
        else:
            print(f"   ❌ Méthode {method_name} manquante")
            implementation_status.append((algo_name, False, "Méthode manquante"))
    
    # Résumé des implémentations
    implemented = sum(1 for _, status, _ in implementation_status if status)
    total = len(implementation_status)
    
    print(f"\n📋 RÉSUMÉ IMPLÉMENTATIONS:")
    print(f"   • Algorithmes implémentés: {implemented}/{total}")
    
    for algo_name, status, note in implementation_status:
        status_icon = "✅" if status else "❌"
        print(f"   {status_icon} {algo_name}: {note}")
    
    return implementation_status

def main():
    """Exécution de l'audit complet"""
    print("🚀 DÉMARRAGE AUDIT COMPLET AQUALIX")
    print("=" * 60)
    
    # Phase 1: Audit des paramètres
    total_params, exposed_params, coverage = audit_parameters()
    
    # Phase 2: Audit de l'intégrité des algorithmes
    implementations = audit_algorithm_integrity()
    
    # Rapport final
    print(f"\n\n📋 RAPPORT FINAL D'AUDIT")
    print("=" * 60)
    print(f"✅ Paramètres: {exposed_params}/{total_params} exposés ({coverage:.1f}%)")
    
    implemented_algos = sum(1 for _, status, _ in implementations if status)
    total_algos = len(implementations)
    print(f"✅ Algorithmes: {implemented_algos}/{total_algos} implémentés")
    
    if coverage >= 90 and implemented_algos == total_algos:
        print("\n🎉 AUDIT RÉUSSI - Système complet et bien exposé!")
    elif coverage >= 80:
        print("\n⚠️  AUDIT PARTIEL - Améliorations recommandées")
    else:
        print("\n❌ AUDIT ÉCHOUÉ - Corrections majeures nécessaires")

if __name__ == "__main__":
    main()
