#!/usr/bin/env python3
"""
Audit complet des fonctions Auto-Tune dans Aqualix
Vérifie que tous les paramètres exposés sont correctement utilisés dans leurs auto-tune respectifs
"""

import sys
import os
import inspect
import re
sys.path.append(os.path.join(os.path.dirname(__file__)))

from src.image_processing import ImageProcessor

def analyze_autotune_method(processor, method_name: str, algorithm_params: list) -> dict:
    """Analyse une méthode auto-tune spécifique"""
    
    if not hasattr(processor, method_name):
        return {
            'exists': False,
            'callable': False,
            'parameters_used': [],
            'parameters_missing': algorithm_params,
            'coverage': 0.0,
            'source_code': None
        }
    
    method = getattr(processor, method_name)
    if not callable(method):
        return {
            'exists': True,
            'callable': False,
            'parameters_used': [],
            'parameters_missing': algorithm_params,
            'coverage': 0.0,
            'source_code': None
        }
    
    # Récupérer le code source de la méthode
    try:
        source_code = inspect.getsource(method)
    except OSError:
        source_code = "Code source non disponible"
    
    # Analyser quels paramètres sont utilisés dans le code
    parameters_used = []
    parameters_missing = []
    
    for param in algorithm_params:
        # Chercher le paramètre dans le code source
        # Patterns possibles: 'param_name', "param_name", parameters['param_name'], self.parameters.get('param_name')
        patterns = [
            f"'{param}'",
            f'"{param}"',
            f"parameters\\['{param}'\\]",
            f'parameters\\["{param}"\\]',
            f"self\\.parameters\\.get\\('{param}'",
            f'self\\.parameters\\.get\\("{param}"',
            f"self\\.set_parameter\\('{param}'",
            f'self\\.set_parameter\\("{param}"'
        ]
        
        found = False
        for pattern in patterns:
            if re.search(pattern, source_code):
                found = True
                break
        
        if found:
            parameters_used.append(param)
        else:
            parameters_missing.append(param)
    
    coverage = (len(parameters_used) / len(algorithm_params)) * 100 if algorithm_params else 100
    
    return {
        'exists': True,
        'callable': True,
        'parameters_used': parameters_used,
        'parameters_missing': parameters_missing,
        'coverage': coverage,
        'source_code': source_code
    }

def audit_autotune_functions():
    """Audit complet des fonctions auto-tune"""
    print("🔍 AUDIT COMPLET DES FONCTIONS AUTO-TUNE")
    print("=" * 60)
    
    processor = ImageProcessor()
    
    # Récupérer tous les paramètres par défaut
    default_params = processor.get_default_parameters()
    
    # Définir les algorithmes et leurs méthodes auto-tune correspondantes
    algorithms_autotune = {
        'White Balance': {
            'method': '_auto_tune_white_balance',
            'enhanced_method': '_enhanced_auto_tune_white_balance',
            'parameters': [
                'white_balance_enabled', 'white_balance_method',
                'gray_world_percentile', 'gray_world_max_adjustment',
                'white_patch_percentile', 'white_patch_max_adjustment',
                'shades_of_gray_norm', 'shades_of_gray_percentile', 'shades_of_gray_max_adjustment',
                'grey_edge_norm', 'grey_edge_sigma', 'grey_edge_max_adjustment',
                'lake_green_reduction', 'lake_magenta_strength', 'lake_gray_world_influence'
            ]
        },
        'UDCP': {
            'method': '_auto_tune_udcp',
            'enhanced_method': '_enhanced_auto_tune_udcp',
            'parameters': [
                'udcp_enabled', 'udcp_omega', 'udcp_t0', 'udcp_window_size',
                'udcp_guided_radius', 'udcp_guided_epsilon', 'udcp_enhance_factor'
            ]
        },
        'Beer-Lambert': {
            'method': '_auto_tune_beer_lambert',
            'enhanced_method': '_enhanced_auto_tune_beer_lambert',
            'parameters': [
                'beer_lambert_enabled', 'beer_lambert_depth_factor',
                'beer_lambert_red_coeff', 'beer_lambert_green_coeff',
                'beer_lambert_blue_coeff', 'beer_lambert_enhance_factor'
            ]
        },
        'Color Rebalancing': {
            'method': '_auto_tune_color_rebalance',
            'enhanced_method': '_enhanced_auto_tune_color_rebalancing',
            'parameters': [
                'color_rebalance_enabled', 'color_rebalance_rr', 'color_rebalance_rg', 'color_rebalance_rb',
                'color_rebalance_gr', 'color_rebalance_gg', 'color_rebalance_gb',
                'color_rebalance_br', 'color_rebalance_bg', 'color_rebalance_bb',
                'color_rebalance_saturation_limit', 'color_rebalance_preserve_luminance'
            ]
        },
        'Histogram Equalization': {
            'method': '_auto_tune_histogram_equalization',
            'enhanced_method': '_enhanced_auto_tune_histogram_equalization',
            'parameters': [
                'hist_eq_enabled', 'hist_eq_method', 'hist_eq_clip_limit', 'hist_eq_tile_grid_size'
            ]
        },
        'Multiscale Fusion': {
            'method': '_auto_tune_multiscale_fusion',
            'enhanced_method': '_enhanced_auto_tune_multiscale_fusion',
            'parameters': [
                'multiscale_fusion_enabled', 'fusion_laplacian_levels',
                'fusion_contrast_weight', 'fusion_saturation_weight', 'fusion_exposedness_weight',
                'fusion_sigma_contrast', 'fusion_sigma_saturation', 'fusion_sigma_exposedness'
            ]
        }
    }
    
    print(f"\n📊 ANALYSE AUTO-TUNE:")
    print(f"   • {len(algorithms_autotune)} algorithmes à analyser")
    print(f"   • {sum(len(algo['parameters']) for algo in algorithms_autotune.values())} paramètres total")
    
    total_coverage = []
    audit_results = {}
    
    for algo_name, algo_info in algorithms_autotune.items():
        print(f"\n🔧 {algo_name.upper()}")
        print("-" * 50)
        
        # Analyser la méthode auto-tune standard
        standard_analysis = analyze_autotune_method(
            processor, algo_info['method'], algo_info['parameters']
        )
        
        print(f"\n   📋 Méthode Standard: {algo_info['method']}")
        if standard_analysis['exists'] and standard_analysis['callable']:
            print(f"   ✅ Méthode présente et callable")
            print(f"   📈 Couverture: {len(standard_analysis['parameters_used'])}/{len(algo_info['parameters'])} ({standard_analysis['coverage']:.1f}%)")
            
            if standard_analysis['parameters_used']:
                print(f"   ✅ Paramètres utilisés:")
                for param in standard_analysis['parameters_used']:
                    print(f"      • {param}")
            
            if standard_analysis['parameters_missing']:
                print(f"   ❌ Paramètres NON utilisés:")
                for param in standard_analysis['parameters_missing']:
                    print(f"      • {param}")
        else:
            if not standard_analysis['exists']:
                print(f"   ❌ Méthode manquante")
            else:
                print(f"   ❌ Méthode non callable")
            print(f"   📈 Couverture: 0.0%")
        
        # Analyser la méthode enhanced si elle existe
        enhanced_analysis = None
        if algo_info['enhanced_method']:
            enhanced_analysis = analyze_autotune_method(
                processor, algo_info['enhanced_method'], algo_info['parameters']
            )
            
            print(f"\n   📋 Méthode Enhanced: {algo_info['enhanced_method']}")
            if enhanced_analysis['exists'] and enhanced_analysis['callable']:
                print(f"   ✅ Méthode enhanced présente et callable")
                print(f"   📈 Couverture Enhanced: {len(enhanced_analysis['parameters_used'])}/{len(algo_info['parameters'])} ({enhanced_analysis['coverage']:.1f}%)")
                
                if enhanced_analysis['parameters_used']:
                    print(f"   ✅ Paramètres enhanced utilisés:")
                    for param in enhanced_analysis['parameters_used']:
                        print(f"      • {param}")
            else:
                if not enhanced_analysis['exists']:
                    print(f"   ❌ Méthode enhanced manquante")
                else:
                    print(f"   ❌ Méthode enhanced non callable")
        
        # Stocker les résultats
        audit_results[algo_name] = {
            'standard': standard_analysis,
            'enhanced': enhanced_analysis,
            'parameters': algo_info['parameters']
        }
        
        # Calculer la couverture globale (utilise enhanced si disponible, sinon standard)
        best_coverage = standard_analysis['coverage']
        if enhanced_analysis and enhanced_analysis['coverage'] > best_coverage:
            best_coverage = enhanced_analysis['coverage']
        
        total_coverage.append(best_coverage)
    
    # Résumé global
    overall_coverage = sum(total_coverage) / len(total_coverage) if total_coverage else 0
    
    print(f"\n🎯 RÉSUMÉ GLOBAL AUTO-TUNE:")
    print(f"   • Couverture moyenne: {overall_coverage:.1f}%")
    
    excellent_algos = sum(1 for c in total_coverage if c >= 90)
    good_algos = sum(1 for c in total_coverage if 70 <= c < 90)
    poor_algos = sum(1 for c in total_coverage if c < 70)
    
    print(f"   • Algorithmes excellents (≥90%): {excellent_algos}")
    print(f"   • Algorithmes bons (70-89%): {good_algos}")
    print(f"   • Algorithmes insuffisants (<70%): {poor_algos}")
    
    if overall_coverage >= 80:
        print("   ✅ AUTO-TUNE GLOBAL: BON")
    elif overall_coverage >= 60:
        print("   ⚠️  AUTO-TUNE GLOBAL: MOYEN - Améliorations recommandées")
    else:
        print("   ❌ AUTO-TUNE GLOBAL: INSUFFISANT - Corrections nécessaires")
    
    return audit_results, overall_coverage

def analyze_autotune_integration():
    """Analyse l'intégration des auto-tune dans le système"""
    print(f"\n\n🔗 AUDIT INTÉGRATION AUTO-TUNE")
    print("=" * 60)
    
    processor = ImageProcessor()
    
    # Vérifier les méthodes d'intégration
    integration_methods = [
        'auto_tune_step',
        'enhanced_auto_tune_step',
        'toggle_enhanced_autotune'
    ]
    
    print(f"\n📋 MÉTHODES D'INTÉGRATION:")
    for method_name in integration_methods:
        if hasattr(processor, method_name):
            method = getattr(processor, method_name)
            if callable(method):
                print(f"   ✅ {method_name} - Présente et callable")
                
                # Analyser la signature
                try:
                    sig = inspect.signature(method)
                    params = list(sig.parameters.keys())
                    print(f"      Parameters: {params}")
                except Exception as e:
                    print(f"      Signature non analysable: {e}")
            else:
                print(f"   ❌ {method_name} - Non callable")
        else:
            print(f"   ❌ {method_name} - Manquante")
    
    # Vérifier la méthode de mapping des auto-tune
    if hasattr(processor, 'auto_tune_functions'):
        auto_tune_mapping = processor.auto_tune_functions
        print(f"\n📋 MAPPING AUTO-TUNE:")
        
        if callable(auto_tune_mapping):
            print(f"   • Méthode auto_tune_functions détectée (callable)")
        elif hasattr(auto_tune_mapping, 'items'):
            # Traiter comme un dictionnaire
            try:
                mapping_items = list(auto_tune_mapping.items())
                print(f"   • {len(mapping_items)} algorithmes mappés")
                for algo, method_name in mapping_items:
                    if hasattr(processor, method_name):
                        print(f"   ✅ {algo} → {method_name}")
                    else:
                        print(f"   ❌ {algo} → {method_name} (méthode manquante)")
            except Exception as e:
                print(f"   ❌ Erreur lors de l'analyse du mapping: {e}")
        else:
            print(f"   ⚠️  Type inattendu pour auto_tune_functions: {type(auto_tune_mapping)}")
    else:
        print(f"\n❌ MAPPING AUTO-TUNE: auto_tune_functions non trouvée")

def main():
    """Exécution de l'audit complet auto-tune"""
    print("🚀 DÉMARRAGE AUDIT AUTO-TUNE AQUALIX")
    print("=" * 60)
    
    # Phase 1: Audit des fonctions auto-tune
    audit_results, coverage = audit_autotune_functions()
    
    # Phase 2: Audit de l'intégration
    analyze_autotune_integration()
    
    # Rapport final
    print(f"\n\n📋 RAPPORT FINAL AUDIT AUTO-TUNE")
    print("=" * 60)
    print(f"📊 Couverture paramètres auto-tune: {coverage:.1f}%")
    
    # Recommandations
    print(f"\n💡 RECOMMANDATIONS:")
    if coverage >= 80:
        print(f"   ✅ Auto-tune bien implémenté - Optimisations mineures possibles")
    elif coverage >= 60:
        print(f"   ⚠️  Améliorer la couverture des paramètres dans auto-tune")
        print(f"   • Ajouter les paramètres manquants dans les méthodes auto-tune")
        print(f"   • Vérifier les enhanced auto-tune methods")
    else:
        print(f"   ❌ Auto-tune nécessite corrections majeures")
        print(f"   • Réimplémenter les méthodes auto-tune manquantes")
        print(f"   • Assurer la couverture complète des paramètres")
    
    return audit_results, coverage

if __name__ == "__main__":
    main()
