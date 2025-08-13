#!/usr/bin/env python3
"""
Script d'intégration des recommandations améliorées dans le système qualité
Met à jour quality_check.py avec des recommandations précises et pratiques
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

def update_quality_check_recommendations():
    """Met à jour le fichier quality_check.py avec les nouvelles recommandations"""
    
    quality_check_path = os.path.join('src', 'quality_check.py')
    
    # Nouvelles fonctions à ajouter
    additional_methods = '''
    
    def _get_precise_recommendations(self, issue_type: str, severity: float, current_values: dict = None) -> List[str]:
        """
        Génère des recommandations précises avec noms de paramètres et valeurs suggérées
        
        Args:
            issue_type: Type de problème détecté
            severity: Sévérité du problème (0-1)  
            current_values: Valeurs actuelles des paramètres (optionnel)
            
        Returns:
            Liste de recommandations précises avec actions concrètes
        """
        recommendations = []
        
        # Déterminer le niveau de sévérité
        if severity < 0.3:
            sev_level = 'low'
        elif severity < 0.7:
            sev_level = 'medium'
        else:
            sev_level = 'high'
            
        # Recommandations basées sur le type de problème
        if issue_type == 'extreme_red_colors':
            recommendations.extend([
                f'qc_reduce_red_gain_precise_detailed',
                f'qc_adjust_wb_method_for_red',
                f'qc_check_beer_lambert_settings'
            ])
            
        elif issue_type == 'saturation_clipping':
            recommendations.extend([
                f'qc_reduce_saturation_limit_precise',
                f'qc_enable_luminance_preserve',
                f'qc_check_matrix_coefficients'
            ])
            
        elif issue_type == 'halo_artifacts':
            recommendations.extend([
                f'qc_reduce_clahe_clip_precise',
                f'qc_increase_clahe_tile_size',
                f'qc_reduce_fusion_weights'
            ])
            
        elif issue_type == 'noise_amplification':
            recommendations.extend([
                f'qc_reduce_amplification_factors',
                f'qc_increase_depth_factor',
                f'qc_consider_preprocessing'
            ])
            
        return recommendations
    
    def _calculate_parameter_adjustments(self, issue_type: str, severity: float, current_params: dict) -> dict:
        """
        Calcule les ajustements précis de paramètres basés sur l'analyse
        
        Args:
            issue_type: Type de problème
            severity: Sévérité (0-1)
            current_params: Paramètres actuels
            
        Returns:
            Dictionnaire des ajustements suggérés
        """
        adjustments = {}
        
        # Facteurs d'ajustement basés sur sévérité
        severity_multiplier = 1.0 + severity  # 1.0 à 2.0
        
        if issue_type == 'extreme_red_colors':
            adjustments['beer_lambert_red_factor'] = {
                'current': current_params.get('beer_lambert_red_factor', 1.5),
                'suggested': max(1.0, current_params.get('beer_lambert_red_factor', 1.5) - 0.1 * severity_multiplier),
                'reason': 'Réduire sur-correction rouge'
            }
            
        elif issue_type == 'saturation_clipping':
            adjustments['color_rebalance_saturation_limit'] = {
                'current': current_params.get('color_rebalance_saturation_limit', 0.8),
                'suggested': max(0.3, current_params.get('color_rebalance_saturation_limit', 0.8) - 0.15 * severity_multiplier),
                'reason': 'Éviter écrêtage saturation'
            }
            
        elif issue_type == 'halo_artifacts':
            adjustments['hist_eq_clip_limit'] = {
                'current': current_params.get('hist_eq_clip_limit', 4.0),
                'suggested': max(1.0, current_params.get('hist_eq_clip_limit', 4.0) - 1.5 * severity_multiplier),
                'reason': 'Réduire artefacts de halo'
            }
            
        return adjustments
    
    def _format_actionable_recommendation(self, param_name: str, adjustment: dict) -> str:
        """
        Formate une recommandation actionnable avec valeurs précises
        
        Args:
            param_name: Nom du paramètre
            adjustment: Dictionnaire d'ajustement
            
        Returns:
            Recommandation formatée avec action concrète
        """
        current = adjustment['current']
        suggested = adjustment['suggested']
        reason = adjustment['reason']
        
        # Mapping des noms techniques vers noms interface utilisateur
        param_display_names = {
            'beer_lambert_red_factor': 'Facteur Rouge (Beer-Lambert)',
            'color_rebalance_saturation_limit': 'Limite de saturation (Rééquilibrage)',
            'hist_eq_clip_limit': 'Limite Clip (CLAHE)',
            'multiscale_fusion_contrast_weight': 'Poids Contraste (Fusion)',
            'white_balance_percentile': 'Percentile (Balance des Blancs)',
            'udcp_omega': 'Omega (UDCP)',
        }
        
        display_name = param_display_names.get(param_name, param_name)
        
        return f"Ajuster '{display_name}': {current:.2f} → {suggested:.2f} ({reason})"
    
    def _generate_workflow_suggestions(self, detected_issues: List[str]) -> List[str]:
        """
        Génère des suggestions de workflow basées sur les problèmes détectés
        
        Args:
            detected_issues: Liste des problèmes détectés
            
        Returns:
            Liste de suggestions de workflow
        """
        suggestions = []
        
        # Analyse des combinaisons de problèmes
        if 'extreme_red_colors' in detected_issues and 'magenta_shift' in detected_issues:
            suggestions.extend([
                "Problème de sur-correction rouge majeur détecté",
                "Séquence recommandée: 1) Réduire Beer-Lambert, 2) Ajuster Balance, 3) Vérifier Rééquilibrage"
            ])
            
        elif 'saturation_clipping' in detected_issues and 'halo_artifacts' in detected_issues:
            suggestions.extend([
                "Sur-traitement détecté sur multiple fronts",
                "Recommandation: Réduire intensité globale de tous les algorithmes"
            ])
            
        elif len(detected_issues) > 3:
            suggestions.extend([
                "Multiples problèmes détectés - Image potentiellement difficile",
                "Considérer: 1) Auto-tune, 2) Prétraitement, 3) Séquence différente"
            ])
            
        return suggestions'''
    
    return additional_methods

def update_localization_file():
    """Met à jour le fichier de localisation avec les nouvelles clés"""
    
    # Nouvelles clés de traduction françaises
    new_keys_fr = {
        # Recommandations précises Beer-Lambert
        'qc_reduce_red_gain_precise_detailed': 'Réduire "Facteur Rouge" (Beer-Lambert) de 0.1-0.2 unités',
        'qc_adjust_wb_method_for_red': 'Essayer "Shades of Gray" ou "Grey Edge" pour réduire dominante rouge',
        'qc_check_beer_lambert_settings': 'Vérifier tous paramètres Beer-Lambert (Rouge, Bleu, Profondeur)',
        
        # Recommandations précises Saturation
        'qc_reduce_saturation_limit_precise': 'Réduire "Limite de saturation" (Rééquilibrage) de 0.15-0.25 unités',
        'qc_enable_luminance_preserve': 'Activer "Préservation Luminance" dans Rééquilibrage Couleur',
        'qc_check_matrix_coefficients': 'Vérifier coefficients matrice 3x3, réduire RR et RG si élevés',
        
        # Recommandations précises CLAHE
        'qc_reduce_clahe_clip_precise': 'Réduire "Limite Clip" (CLAHE) de 1.5-2.5 unités',
        'qc_increase_clahe_tile_size': 'Augmenter "Taille Tuile" CLAHE de 4x4 à 8x8 ou plus',
        'qc_reduce_fusion_weights': 'Réduire poids "Contraste" et "Saturation" dans Fusion Multi-échelle',
        
        # Recommandations workflow
        'qc_reduce_amplification_factors': 'Réduire tous facteurs d\'amplification (Rouge, Contraste) de 15%',
        'qc_increase_depth_factor': 'Augmenter "Facteur Profondeur" Beer-Lambert de 0.1-0.2',
        'qc_consider_preprocessing': 'Considérer prétraitement image (débruitage) avant correction',
        
        # Messages contextuels
        'qc_multiple_issues_detected': 'Multiples problèmes détectés - Réduction globale recommandée',
        'qc_over_correction_pattern': 'Pattern de sur-correction détecté',
        'qc_workflow_suggestion': 'Suggestion de workflow',
        'qc_parameter_adjustment': 'Ajustement de paramètre',
        'qc_try_auto_tune': 'Essayer Auto-Tune pour optimisation automatique',
    }
    
    # Nouvelles clés de traduction anglaises  
    new_keys_en = {
        # Precise Beer-Lambert recommendations
        'qc_reduce_red_gain_precise_detailed': 'Reduce "Red Factor" (Beer-Lambert) by 0.1-0.2 units',
        'qc_adjust_wb_method_for_red': 'Try "Shades of Gray" or "Grey Edge" to reduce red dominance',
        'qc_check_beer_lambert_settings': 'Check all Beer-Lambert parameters (Red, Blue, Depth)',
        
        # Precise Saturation recommendations
        'qc_reduce_saturation_limit_precise': 'Reduce "Saturation Limit" (Rebalancing) by 0.15-0.25 units',
        'qc_enable_luminance_preserve': 'Enable "Preserve Luminance" in Color Rebalancing',
        'qc_check_matrix_coefficients': 'Check 3x3 matrix coefficients, reduce RR and RG if high',
        
        # Precise CLAHE recommendations
        'qc_reduce_clahe_clip_precise': 'Reduce "Clip Limit" (CLAHE) by 1.5-2.5 units',
        'qc_increase_clahe_tile_size': 'Increase CLAHE "Tile Size" from 4x4 to 8x8 or more',
        'qc_reduce_fusion_weights': 'Reduce "Contrast" and "Saturation" weights in Multiscale Fusion',
        
        # Workflow recommendations
        'qc_reduce_amplification_factors': 'Reduce all amplification factors (Red, Contrast) by 15%',
        'qc_increase_depth_factor': 'Increase Beer-Lambert "Depth Factor" by 0.1-0.2',
        'qc_consider_preprocessing': 'Consider image preprocessing (denoising) before correction',
        
        # Contextual messages
        'qc_multiple_issues_detected': 'Multiple issues detected - Global reduction recommended',
        'qc_over_correction_pattern': 'Over-correction pattern detected',
        'qc_workflow_suggestion': 'Workflow suggestion',
        'qc_parameter_adjustment': 'Parameter adjustment',
        'qc_try_auto_tune': 'Try Auto-Tune for automatic optimization',
    }
    
    return new_keys_fr, new_keys_en

def create_integration_patch():
    """Crée un patch pour intégrer les améliorations"""
    
    patch_content = '''
# PATCH D'AMÉLIORATION DES RECOMMANDATIONS QUALITÉ
# À intégrer dans quality_check.py

# 1. Ajouter dans __init__():
self.param_display_names = {
    'beer_lambert_red_factor': 'Facteur Rouge (Beer-Lambert)',
    'beer_lambert_blue_factor': 'Facteur Bleu (Beer-Lambert)', 
    'beer_lambert_depth_factor': 'Facteur Profondeur (Beer-Lambert)',
    'white_balance_percentile': 'Percentile (Balance des Blancs)',
    'white_balance_max_adjustment': 'Ajustement Max (Balance des Blancs)',
    'color_rebalance_saturation_limit': 'Limite de saturation (Rééquilibrage)',
    'color_rebalance_rr': 'Coefficient RR (Matrice Couleur)',
    'color_rebalance_rg': 'Coefficient RG (Matrice Couleur)',
    'hist_eq_clip_limit': 'Limite Clip (CLAHE)',
    'hist_eq_tile_size': 'Taille Tuile (CLAHE)',
    'multiscale_fusion_contrast_weight': 'Poids Contraste (Fusion)',
    'multiscale_fusion_saturation_weight': 'Poids Saturation (Fusion)',
    'udcp_omega': 'Omega (UDCP)',
    'udcp_t0': 'T0 (UDCP)',
}

# 2. Modifier les méthodes d'analyse pour utiliser get_precise_recommendations()

# 3. Dans _check_saturation_clipping(), remplacer:
if clipped_saturation > 0.02:
    self.analysis_results['saturation_analysis']['recommendations'].append('qc_reduce_saturation')

# Par:
if clipped_saturation > 0.02:
    severity = min(1.0, clipped_saturation * 10)  # 0.02 → 0.2, 0.1 → 1.0
    precise_recs = self._get_precise_recommendations('saturation_clipping', severity)
    self.analysis_results['saturation_analysis']['recommendations'].extend(precise_recs)
    
    # Ajouter ajustements calculés
    adjustments = self._calculate_parameter_adjustments('saturation_clipping', severity, {})
    self.analysis_results['saturation_analysis']['parameter_adjustments'] = adjustments

# 4. Similaire pour les autres checks...
'''
    
    return patch_content

def main():
    """Fonction principale"""
    
    print("🔧 INTÉGRATION RECOMMANDATIONS QUALITÉ AMÉLIORÉES")
    print("=" * 65)
    
    # Générer les améliorations
    additional_methods = update_quality_check_recommendations()
    new_keys_fr, new_keys_en = update_localization_file()
    patch_content = create_integration_patch()
    
    print(f"✅ Améliorations générées:")
    print(f"   • 4 nouvelles méthodes pour quality_check.py")
    print(f"   • {len(new_keys_fr)} nouvelles clés de traduction françaises")
    print(f"   • {len(new_keys_en)} nouvelles clés de traduction anglaises")
    print(f"   • Patch d'intégration créé")
    
    print(f"\n📋 Exemples nouvelles recommandations:")
    for key, value in list(new_keys_fr.items())[:4]:
        print(f"   • {key}: {value}")
    
    print(f"\n🔧 Modifications principales à appliquer:")
    print(f"   1. Ajouter méthodes dans quality_check.py")
    print(f"   2. Intégrer nouvelles clés dans localization.py")
    print(f"   3. Modifier logique de génération des recommandations")
    print(f"   4. Ajouter calculs d'ajustements de paramètres")
    
    # Sauvegarder les améliorations dans des fichiers
    try:
        # Sauvegarder patch d'intégration
        with open('quality_improvements_patch.txt', 'w', encoding='utf-8') as f:
            f.write("# PATCH D'AMÉLIORATION RECOMMANDATIONS QUALITÉ\\n")
            f.write("# Méthodes à ajouter dans quality_check.py\\n\\n")
            f.write(additional_methods)
            f.write("\\n\\n# Patch d'intégration:\\n")
            f.write(patch_content)
            
        # Sauvegarder nouvelles clés de traduction
        with open('new_translation_keys.py', 'w', encoding='utf-8') as f:
            f.write("# Nouvelles clés de traduction pour recommandations améliorées\\n\\n")
            f.write("# Français:\\n")
            for key, value in new_keys_fr.items():
                f.write(f"'{key}': '{value}',\\n")
            f.write("\\n# Anglais:\\n")
            for key, value in new_keys_en.items():
                f.write(f"'{key}': '{value}',\\n")
        
        print(f"\\n💾 Fichiers sauvegardés:")
        print(f"   • quality_improvements_patch.txt")
        print(f"   • new_translation_keys.py")
        
    except Exception as e:
        print(f"\\n⚠️ Erreur sauvegarde: {e}")
    
    print(f"\\n🎯 Bénéfices attendus:")
    print(f"   • Recommandations avec noms exacts des paramètres")
    print(f"   • Valeurs concrètes suggérées (ex: 0.8 → 0.6)")
    print(f"   • Conseils pratiques contextuels")
    print(f"   • Ajustements automatiques calculés")
    print(f"   • Workflow suggestions intelligentes")
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print(f"\\n✅ Intégration préparée avec succès")
    else:
        print(f"\\n❌ Erreur dans la préparation")
