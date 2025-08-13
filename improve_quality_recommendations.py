#!/usr/bin/env python3
"""
Script d'amélioration des recommandations de contrôle qualité
Ajoute des conseils précis avec noms des paramètres et valeurs suggérées
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

def create_improved_recommendations():
    """Crée des recommandations améliorées avec vocabulaire précis"""
    
    # Recommandations précises avec noms de paramètres et valeurs
    improved_recommendations_fr = {
        # BEER-LAMBERT RECOMMENDATIONS
        'qc_reduce_red_gain_precise': 'Réduire "Facteur Rouge" de 0.1-0.2 (ex: 1.5 → 1.3)',
        'qc_reduce_blue_compensation': 'Réduire "Facteur Bleu" de 0.1 (ex: 2.0 → 1.9)',
        'qc_adjust_depth_factor': 'Augmenter "Facteur Profondeur" de 0.1-0.2 (ex: 0.5 → 0.7)',
        
        # WHITE BALANCE RECOMMENDATIONS  
        'qc_change_wb_method': 'Changer méthode: "Gray World" → "Shades of Gray" ou "Grey Edge"',
        'qc_reduce_wb_percentile': 'Réduire "Percentile" de 10-15 (ex: 75 → 60)',
        'qc_limit_max_adjustment': 'Limiter "Ajustement Max" à 2.0-2.5 (ex: 3.0 → 2.2)',
        
        # COLOR REBALANCING RECOMMENDATIONS
        'qc_reduce_saturation_limit': 'Réduire "Limite de saturation" de 0.1-0.2 (ex: 0.8 → 0.6)',
        'qc_adjust_matrix_rr': 'Réduire coefficient "RR" de 0.1-0.2 (ex: 1.2 → 1.0)',
        'qc_adjust_matrix_rg': 'Ajuster coefficient "RG" vers 0 (ex: 0.3 → 0.1)',
        'qc_enable_luminance_preserve': 'Activer "Préservation Luminance" si désactivée',
        
        # CLAHE RECOMMENDATIONS
        'qc_reduce_clahe_clip_precise': 'Réduire "Limite Clip" de 1.0-2.0 (ex: 4.0 → 2.5)',
        'qc_increase_clahe_tile_size': 'Augmenter "Taille Tuile" (ex: 8x8 → 12x12)',
        'qc_disable_clahe': 'Désactiver CLAHE temporairement pour tester',
        
        # MULTISCALE FUSION RECOMMENDATIONS
        'qc_reduce_contrast_weight': 'Réduire "Poids Contraste" de 0.2-0.3 (ex: 1.0 → 0.7)',
        'qc_reduce_saturation_weight': 'Réduire "Poids Saturation" de 0.2 (ex: 1.0 → 0.8)',
        'qc_reduce_exposedness_weight': 'Réduire "Poids Exposition" de 0.1-0.2 (ex: 1.0 → 0.8)',
        'qc_reduce_fusion_levels': 'Réduire "Niveaux Laplaciens" de 1-2 (ex: 5 → 3)',
        
        # UDCP RECOMMENDATIONS
        'qc_reduce_omega': 'Réduire "Omega" de 0.05-0.1 (ex: 0.85 → 0.75)',
        'qc_increase_t0': 'Augmenter "T0" de 0.02-0.05 (ex: 0.1 → 0.15)',
        'qc_reduce_udcp_window_size': 'Réduire "Taille Fenêtre" de 2-5 pixels (ex: 15 → 10)',
        'qc_increase_guided_radius': 'Augmenter "Rayon Filtre Guidé" de 10-20 (ex: 40 → 60)',
        
        # GENERAL WORKFLOW RECOMMENDATIONS
        'qc_try_different_sequence': 'Essayer séquence différente: UDCP → Balance → Rebalancing',
        'qc_disable_step_temporarily': 'Désactiver une étape temporairement pour isoler le problème',
        'qc_use_auto_tune': 'Activer Auto-Tune pour optimisation automatique',
        'qc_check_original_quality': 'Vérifier qualité image originale (bruit, netteté)',
    }
    
    improved_recommendations_en = {
        # BEER-LAMBERT RECOMMENDATIONS
        'qc_reduce_red_gain_precise': 'Reduce "Red Factor" by 0.1-0.2 (ex: 1.5 → 1.3)',
        'qc_reduce_blue_compensation': 'Reduce "Blue Factor" by 0.1 (ex: 2.0 → 1.9)',
        'qc_adjust_depth_factor': 'Increase "Depth Factor" by 0.1-0.2 (ex: 0.5 → 0.7)',
        
        # WHITE BALANCE RECOMMENDATIONS  
        'qc_change_wb_method': 'Change method: "Gray World" → "Shades of Gray" or "Grey Edge"',
        'qc_reduce_wb_percentile': 'Reduce "Percentile" by 10-15 (ex: 75 → 60)',
        'qc_limit_max_adjustment': 'Limit "Max Adjustment" to 2.0-2.5 (ex: 3.0 → 2.2)',
        
        # COLOR REBALANCING RECOMMENDATIONS
        'qc_reduce_saturation_limit': 'Reduce "Saturation Limit" by 0.1-0.2 (ex: 0.8 → 0.6)',
        'qc_adjust_matrix_rr': 'Reduce "RR" coefficient by 0.1-0.2 (ex: 1.2 → 1.0)',
        'qc_adjust_matrix_rg': 'Adjust "RG" coefficient toward 0 (ex: 0.3 → 0.1)',
        'qc_enable_luminance_preserve': 'Enable "Preserve Luminance" if disabled',
        
        # CLAHE RECOMMENDATIONS
        'qc_reduce_clahe_clip_precise': 'Reduce "Clip Limit" by 1.0-2.0 (ex: 4.0 → 2.5)',
        'qc_increase_clahe_tile_size': 'Increase "Tile Size" (ex: 8x8 → 12x12)',
        'qc_disable_clahe': 'Disable CLAHE temporarily for testing',
        
        # MULTISCALE FUSION RECOMMENDATIONS
        'qc_reduce_contrast_weight': 'Reduce "Contrast Weight" by 0.2-0.3 (ex: 1.0 → 0.7)',
        'qc_reduce_saturation_weight': 'Reduce "Saturation Weight" by 0.2 (ex: 1.0 → 0.8)',
        'qc_reduce_exposedness_weight': 'Reduce "Exposedness Weight" by 0.1-0.2 (ex: 1.0 → 0.8)',
        'qc_reduce_fusion_levels': 'Reduce "Laplacian Levels" by 1-2 (ex: 5 → 3)',
        
        # UDCP RECOMMENDATIONS
        'qc_reduce_omega': 'Reduce "Omega" by 0.05-0.1 (ex: 0.85 → 0.75)',
        'qc_increase_t0': 'Increase "T0" by 0.02-0.05 (ex: 0.1 → 0.15)',
        'qc_reduce_udcp_window_size': 'Reduce "Window Size" by 2-5 pixels (ex: 15 → 10)',
        'qc_increase_guided_radius': 'Increase "Guided Filter Radius" by 10-20 (ex: 40 → 60)',
        
        # GENERAL WORKFLOW RECOMMENDATIONS
        'qc_try_different_sequence': 'Try different sequence: UDCP → White Balance → Rebalancing',
        'qc_disable_step_temporarily': 'Disable one step temporarily to isolate issue',
        'qc_use_auto_tune': 'Enable Auto-Tune for automatic optimization',
        'qc_check_original_quality': 'Check original image quality (noise, sharpness)',
    }
    
    return improved_recommendations_fr, improved_recommendations_en

def create_parameter_mapping():
    """Crée le mapping entre recommandations et paramètres spécifiques"""
    
    parameter_mapping = {
        # Mapping recommandation → paramètre technique
        'qc_reduce_red_gain': 'beer_lambert_red_factor',
        'qc_reduce_red_compensation': ['white_balance_method', 'color_rebalance_rr'],
        'qc_reduce_saturation': 'color_rebalance_saturation_limit',
        'qc_reduce_clahe_clip_limit': 'hist_eq_clip_limit',
        'qc_halo_artifacts': ['hist_eq_clip_limit', 'multiscale_fusion_contrast_weight'],
        'qc_shadow_detail_lost': ['hist_eq_enabled', 'beer_lambert_depth_factor'],
        'qc_noise_amplification': ['beer_lambert_red_factor', 'color_rebalance_rr'],
    }
    
    return parameter_mapping

def create_severity_based_adjustments():
    """Crée des ajustements basés sur la sévérité des problèmes"""
    
    severity_adjustments = {
        'low': {
            'beer_lambert_red_factor': -0.1,
            'color_rebalance_saturation_limit': -0.1,
            'hist_eq_clip_limit': -1.0,
            'multiscale_fusion_contrast_weight': -0.2,
        },
        'medium': {
            'beer_lambert_red_factor': -0.2,
            'color_rebalance_saturation_limit': -0.2,
            'hist_eq_clip_limit': -2.0,
            'multiscale_fusion_contrast_weight': -0.3,
        },
        'high': {
            'beer_lambert_red_factor': -0.3,
            'color_rebalance_saturation_limit': -0.3,
            'hist_eq_clip_limit': -3.0,
            'multiscale_fusion_contrast_weight': -0.5,
        }
    }
    
    return severity_adjustments

def generate_contextual_recommendations():
    """Génère des recommandations contextuelles basées sur les problèmes détectés"""
    
    contextual_recommendations = {
        # Combinaisons de problèmes courants
        ('extreme_red', 'magenta_shift'): [
            'Problème de sur-correction rouge détecté',
            '1. Réduire "Facteur Rouge" Beer-Lambert de 0.2 (ex: 1.5 → 1.3)',
            '2. Changer méthode Balance → "Shades of Gray"',
            '3. Réduire "RR" matrice couleur de 0.1 (ex: 1.2 → 1.1)'
        ],
        
        ('saturation_clipping', 'halo_artifacts'): [
            'Problème de sur-traitement détecté',
            '1. Réduire "Limite Saturation" de 0.2 (ex: 0.8 → 0.6)',
            '2. Réduire "Limite Clip" CLAHE de 2.0 (ex: 4.0 → 2.0)',
            '3. Réduire "Poids Contraste" fusion de 0.3 (ex: 1.0 → 0.7)'
        ],
        
        ('noise_amplification', 'shadow_detail_lost'): [
            'Problème d\'amplification excessive détecté',
            '1. Augmenter "Facteur Profondeur" Beer-Lambert de 0.1',
            '2. Réduire "Facteur Rouge" de 0.15 (ex: 1.4 → 1.25)',
            '3. Activer "Préservation Luminance" si désactivée'
        ]
    }
    
    return contextual_recommendations

def main():
    """Fonction principale pour tester les améliorations"""
    
    print("🔧 AMÉLIORATION DES RECOMMANDATIONS QUALITÉ")
    print("=" * 60)
    
    # Créer les recommandations améliorées
    rec_fr, rec_en = create_improved_recommendations()
    param_mapping = create_parameter_mapping()
    severity_adj = create_severity_based_adjustments()
    contextual_rec = generate_contextual_recommendations()
    
    print(f"\n✅ Recommandations précises créées:")
    print(f"   • {len(rec_fr)} recommandations françaises")
    print(f"   • {len(rec_en)} recommandations anglaises")
    print(f"   • {len(param_mapping)} mappings paramètres")
    print(f"   • {len(severity_adj)} niveaux de sévérité")
    print(f"   • {len(contextual_rec)} recommandations contextuelles")
    
    print(f"\n📋 Exemples de recommandations précises:")
    for key, value in list(rec_fr.items())[:5]:
        print(f"   • {key}: {value}")
    
    print(f"\n🎯 Exemples de mapping paramètres:")
    for rec, param in list(param_mapping.items())[:3]:
        print(f"   • {rec} → {param}")
    
    print(f"\n⚙️ Ajustements par sévérité (medium):")
    for param, adjust in severity_adj['medium'].items():
        print(f"   • {param}: {adjust:+.1f}")
    
    print(f"\n🔄 Prochaines étapes recommandées:")
    print(f"   1. Intégrer ces recommandations dans quality_check.py")
    print(f"   2. Modifier les clés de traduction dans localization.py")
    print(f"   3. Ajouter logique de recommandation contextuelle")
    print(f"   4. Créer interface pour ajustements automatiques")
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print(f"\n✅ Script terminé avec succès")
    else:
        print(f"\n❌ Erreur dans l'exécution")
