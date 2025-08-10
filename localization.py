"""
Localization module for Aqualix
Supports French and English languages
"""

import json
import os
from pathlib import Path

class LocalizationManager:
    """Manages application localization"""
    
    def __init__(self, default_language='fr'):
        self.config_file = Path('aqualix_config.json')
        self.current_language = self.load_saved_language() or default_language
        self.translations = {}
        self.load_translations()
        
    def load_saved_language(self):
        """Load saved language preference"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.loads(f.read())
                    return config.get('language')
        except Exception:
            pass
        return None
        
    def save_language_preference(self, language):
        """Save language preference to config file"""
        try:
            config = {}
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.loads(f.read())
            
            config['language'] = language
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                f.write(json.dumps(config, indent=2))
        except Exception:
            pass  # Fail silently if can't save preferences
        
    def load_translations(self):
        """Load translation dictionaries"""
        # French translations (default)
        self.translations['fr'] = {
            # Main window
            'app_title': 'Aqualix - Traitement d\'Images et Vidéos',
            'select_file': 'Sélectionner un fichier',
            'select_folder': 'Sélectionner un dossier',
            'previous': 'Précédent',
            'next': 'Suivant',
            'save_result': 'Sauvegarder le résultat',
            'process_video': 'Traiter la vidéo',
            'no_files': 'Aucun fichier trouvé',
            'file_info': 'Fichier: {filename} ({index}/{total})',
            
            # Tabs
            'tab_parameters': 'Paramètres',
            'tab_operations': 'Opérations',
            'tab_info': 'Informations',
            'tab_about': 'À propos',
            
            # Panel titles
            'parameters_title': 'Paramètres de traitement',
            'pipeline_title': 'Pipeline des opérations', 
            'preview_title': 'Vue comparative interactive',
            'info_title': 'Informations de l\'image',
            
            # Info tabs
            'info_tab_file': 'Fichier',
            'info_tab_properties': 'Propriétés',
            'info_tab_analysis': 'Analyse',
            'info_tab_exif': 'EXIF',
            
            # Parameters
            'gray_world_wb': 'Balance des blancs Gray-World',
            'enable': 'Activer',
            'percentile': 'Percentile',
            'max_adjustment': 'Ajustement maximum',
            'hist_equalization': 'Égalisation d\'histogramme',
            'clip_limit': 'Limite de contraste',
            'tile_size': 'Taille des tuiles',
            
            # Operations panel
            'processing_pipeline': 'Pipeline de traitement',
            'no_operations': 'Aucune opération activée',
            'no_operations_desc': 'Toutes les étapes de traitement sont désactivées.',
            
            # White balance methods
            'white_balance_gray_world': 'Balance des blancs Gray-World',
            'white_balance_white_patch': 'Balance des blancs White-Patch',
            'white_balance_shades_of_gray': 'Balance des blancs Shades-of-Gray',
            'white_balance_grey_edge': 'Balance des blancs Grey-Edge',
            'white_balance_lake_green_water': 'Balance des blancs Eau Verte (Lac)',
            
            'operation_gw': 'Balance des blancs Gray-World',
            'operation_gw_desc': 'Corrige la température de couleur en assumant que la moyenne de la scène devrait être grise neutre.',
            'operation_wp': 'Balance des blancs White-Patch',
            'operation_wp_desc': 'Corrige la balance des blancs en assumant que les pixels les plus brillants devraient être blancs.',
            'operation_sog': 'Balance des blancs Shades-of-Gray',
            'operation_sog_desc': 'Généralisation de Gray-World utilisant la norme de Minkowski pour une meilleure robustesse.',
            'operation_ge': 'Balance des blancs Grey-Edge',
            'operation_ge_desc': 'Utilise les dérivées spatiales pour estimer l\'illumination de la scène.',
            'operation_lgw': 'Balance des blancs Eau Verte (Lac)',
            'operation_lgw_desc': 'Spécialisé pour les eaux vertes de lac avec réduction ciblée du vert et compensation magenta.',
            
            # Processing step titles
            'white_balance_step_title': 'Balance des blancs',
            'white_balance_step_desc': 'Correction de la température de couleur',
            'udcp_step_title': 'UDCP (Underwater Dark Channel Prior)',
            'udcp_step_desc': 'Amélioration spécialisée pour images sous-marines',
            'beer_lambert_step_title': 'Correction Beer-Lambert',
            'beer_lambert_step_desc': 'Correction de l\'atténuation en profondeur selon la loi de Beer-Lambert',
            'color_rebalance_step_title': 'Rééquilibrage des couleurs',
            'color_rebalance_step_desc': 'Matrice de transformation 3×3 avec garde-fous anti-magenta',
            'histogram_equalization_step_title': 'Égalisation d\'histogramme (CLAHE)',
            'histogram_equalization_step_desc': 'Amélioration du contraste local',
            'multiscale_fusion_step_title': 'Fusion Multi-échelles (Ancuti)',
            'multiscale_fusion_step_desc': 'Fusion robuste de 3 variantes (WB+contraste, WB+netteté, UDCP) pour optimiser le rendu',
            
            # UDCP method
            'udcp_title': 'UDCP (Underwater Dark Channel Prior)',
            'udcp_description': 'Amélioration spécialisée pour images sous-marines',
            'operation_udcp': 'UDCP (Underwater Dark Channel Prior)',
            'operation_udcp_desc': 'Supprime le voile et améliore la visibilité des images sous-marines en utilisant l\'hypothèse du canal sombre.',
            
            'operation_beer_lambert_desc': 'Corrige l\'atténuation dépendante de la profondeur en utilisant la loi de Beer-Lambert avec compensation par canal.',
            
            'operation_color_rebalance_desc': 'Applique une matrice de transformation 3×3 pour affiner l\'équilibre des couleurs avec limitation de saturation pour éviter les artefacts magenta.',
            
            'operation_he': 'Égalisation d\'histogramme adaptatif',
            'operation_he_desc': 'Améliore le contraste local en utilisant CLAHE (Contrast Limited Adaptive Histogram Equalization).',
            
            # Interactive preview
            'split_position': 'Division',
            'zoom': 'Zoom',
            'fit_image': 'Ajuster',
            'reset_view': '1:1',
            'rotation': 'Rotation',
            'collapse_all': 'Réduire tout',
            'expand_all': 'Développer tout',
            'reset_defaults': 'Réinitialiser',
            'reset_defaults_tooltip': 'Rétablir les paramètres par défaut de cette section',
            'auto_tune': 'Auto-Tune',
            'auto_tune_tooltip': 'Optimiser automatiquement les paramètres lors de l\'exécution de cette étape',
            'expand_all_sections': 'Développer toutes les sections',
            'reset_all_parameters': 'Réinitialiser Tout',
            'reset_all_parameters_tooltip': 'Remettre TOUS les paramètres à leurs valeurs par défaut',
            'no_image_loaded': 'Aucune image chargée',
            'preview_instructions': 'Contrôles: Clic gauche + glisser pour déplacer • Molette pour zoomer • Glisser la ligne de division',
            
            # Image info
            'image_info': 'Informations de l\'image',
            'file_tab': 'Fichier',
            'properties_tab': 'Propriétés',
            'analysis_tab': 'Analyse',
            'exif_tab': 'EXIF',
            'no_color_analysis': 'Aucune analyse de couleur disponible',
            'no_exif_data': 'Aucune donnée EXIF trouvée',
            
            # File info labels
            'name': 'Nom',
            'path': 'Chemin',
            'size': 'Taille',
            'modified': 'Modifié',
            'created': 'Créé',
            'extension': 'Extension',
            'hash_md5': 'Hash MD5',
            
            # Properties labels
            'width': 'Largeur',
            'height': 'Hauteur',
            'channels': 'Canaux',
            'total_pixels': 'Pixels totaux',
            'aspect_ratio': 'Ratio d\'aspect',
            'format': 'Format',
            'mode': 'Mode',
            'transparency': 'Transparence',
            'data_type': 'Type de données',
            'min_value': 'Valeur min',
            'max_value': 'Valeur max',
            'mean_value': 'Valeur moyenne',
            'fps': 'FPS',
            'total_frames': 'Frames totales',
            'duration': 'Durée',
            'codec': 'Codec',
            
            # Analysis labels
            'red_mean': 'Moyenne Rouge',
            'green_mean': 'Moyenne Vert',
            'blue_mean': 'Moyenne Bleu',
            'red_std': 'Écart-type Rouge',
            'green_std': 'Écart-type Vert',
            'blue_std': 'Écart-type Bleu',
            'brightness': 'Luminosité',
            'contrast': 'Contraste',
            'estimated_color_temp': 'Temp. couleur estimée',
            'unique_colors': 'Couleurs uniques',
            'min_intensity': 'Intensité min',
            'max_intensity': 'Intensité max',
            
            # Messages
            'yes': 'Oui',
            'no': 'Non',
            'error': 'Erreur',
            'success': 'Succès',
            'processing': 'Traitement en cours...',
            'saved_as': 'Sauvegardé sous: {path}',
            'could_not_load': 'Impossible de charger: {error}',
            'could_not_save': 'Impossible de sauvegarder: {error}',
            'video_saved_as': 'Vidéo sauvegardée sous: {path}',
            'processing_video_frames': 'Traitement des frames vidéo...',
            'frame_x_of_y': 'Frame {current} sur {total}',
            
            # Parameter labels and descriptions
            # White balance parameters
            'param_white_balance_enabled_label': 'Balance des blancs activée',
            'param_white_balance_enabled_desc': 'Applique la correction de la balance des blancs',
            'param_white_balance_method_label': 'Méthode de balance des blancs',
            'param_white_balance_method_desc': 'Algorithme utilisé pour la correction de la balance des blancs',
            'param_gray_world_percentile_label': 'Percentile Gray-World',
            'param_gray_world_percentile_desc': 'Percentile utilisé pour calculer la moyenne des canaux couleur',
            'param_gray_world_max_adjustment_label': 'Ajustement max (Gray-World)',
            'param_gray_world_max_adjustment_desc': 'Facteur maximum d\'échelle autorisé pour les canaux couleur',
            'param_white_patch_percentile_label': 'Percentile White-Patch',
            'param_white_patch_percentile_desc': 'Percentile pour identifier le patch le plus clair',
            'param_white_patch_max_adjustment_label': 'Ajustement max (White-Patch)',
            'param_white_patch_max_adjustment_desc': 'Facteur maximum d\'échelle autorisé pour les canaux couleur',
            'param_shades_of_gray_norm_label': 'Norme Minkowski (Shades of Gray)',
            'param_shades_of_gray_norm_desc': 'Ordre de la norme de Minkowski pour le calcul',
            'param_shades_of_gray_percentile_label': 'Percentile (Shades of Gray)',
            'param_shades_of_gray_percentile_desc': 'Percentile utilisé pour calculer la norme généralisée',
            'param_shades_of_gray_max_adjustment_label': 'Ajustement max (Shades of Gray)',
            'param_shades_of_gray_max_adjustment_desc': 'Facteur maximum d\'échelle autorisé pour les canaux couleur',
            'param_grey_edge_norm_label': 'Norme Minkowski (Grey-Edge)',
            'param_grey_edge_norm_desc': 'Ordre de la norme de Minkowski pour le calcul des dérivées',
            'param_grey_edge_sigma_label': 'Sigma gaussien (Grey-Edge)',
            'param_grey_edge_sigma_desc': 'Écart-type du filtre gaussien pour le calcul des dérivées',
            'param_grey_edge_max_adjustment_label': 'Ajustement max (Grey-Edge)',
            'param_grey_edge_max_adjustment_desc': 'Facteur maximum d\'échelle autorisé pour les canaux couleur',
            'param_lake_green_reduction_label': 'Réduction du vert',
            'param_lake_green_reduction_desc': 'Intensité de la réduction du canal vert (0.0 = aucune, 1.0 = maximum)',
            'param_lake_magenta_strength_label': 'Force du magenta',
            'param_lake_magenta_strength_desc': 'Intensité de la compensation magenta (rouge+bleu)',
            'param_lake_gray_world_influence_label': 'Influence Gray-World',
            'param_lake_gray_world_influence_desc': 'Influence de la correction Gray-World finale',
            
            # UDCP parameters
            'param_udcp_enabled_label': 'UDCP activé',
            'param_udcp_enabled_desc': 'Applique l\'algorithme Underwater Dark Channel Prior',
            'param_udcp_omega_label': 'Facteur Omega',
            'param_udcp_omega_desc': 'Facteur de préservation du voile atmosphérique (0.0 = suppression complète)',
            'param_udcp_t0_label': 'Transmission minimale (t0)',
            'param_udcp_t0_desc': 'Valeur minimale de transmission pour éviter la sur-correction',
            'param_udcp_window_size_label': 'Taille de fenêtre',
            'param_udcp_window_size_desc': 'Taille de la fenêtre pour le calcul du canal sombre',
            'param_udcp_guided_radius_label': 'Rayon du filtre guidé',
            'param_udcp_guided_radius_desc': 'Rayon du filtre guidé pour le raffinement de la carte de transmission',
            'param_udcp_guided_eps_label': 'Epsilon du filtre guidé',
            'param_udcp_guided_eps_desc': 'Paramètre de régularisation pour le filtre guidé',
            'param_udcp_enhance_contrast_label': 'Amélioration du contraste',
            'param_udcp_enhance_contrast_desc': 'Facteur d\'amélioration du contraste final',
            
            # Beer-Lambert parameters
            'param_beer_lambert_enabled_label': 'Correction Beer-Lambert',
            'param_beer_lambert_enabled_desc': 'Applique la correction de Beer-Lambert pour l\'atténuation en profondeur',
            'param_beer_lambert_depth_factor_label': 'Facteur de profondeur',
            'param_beer_lambert_depth_factor_desc': 'Facteur de correction basé sur la profondeur estimée',
            'param_beer_lambert_red_coeff_label': 'Coefficient rouge',
            'param_beer_lambert_red_coeff_desc': 'Coefficient d\'atténuation pour le canal rouge',
            'param_beer_lambert_green_coeff_label': 'Coefficient vert',
            'param_beer_lambert_green_coeff_desc': 'Coefficient d\'atténuation pour le canal vert',
            'param_beer_lambert_blue_coeff_label': 'Coefficient bleu',
            'param_beer_lambert_blue_coeff_desc': 'Coefficient d\'atténuation pour le canal bleu',
            'param_beer_lambert_enhance_factor_label': 'Facteur d\'amélioration',
            'param_beer_lambert_enhance_factor_desc': 'Facteur d\'amélioration finale pour la correction Beer-Lambert',
            
            # Color rebalancing parameters  
            'param_color_rebalance_enabled_label': 'Rééquilibrage des couleurs',
            'param_color_rebalance_enabled_desc': 'Active la matrice de transformation 3×3 pour l\'affinement des couleurs',
            'param_color_rebalance_rr_label': 'Rouge→Rouge (RR)',
            'param_color_rebalance_rr_desc': 'Coefficient de la matrice pour le canal rouge vers rouge',
            'param_color_rebalance_rg_label': 'Rouge→Vert (RG)', 
            'param_color_rebalance_rg_desc': 'Coefficient de mélange du canal rouge vers vert',
            'param_color_rebalance_rb_label': 'Rouge→Bleu (RB)',
            'param_color_rebalance_rb_desc': 'Coefficient de mélange du canal rouge vers bleu',
            'param_color_rebalance_gr_label': 'Vert→Rouge (GR)',
            'param_color_rebalance_gr_desc': 'Coefficient de mélange du canal vert vers rouge',
            'param_color_rebalance_gg_label': 'Vert→Vert (GG)',
            'param_color_rebalance_gg_desc': 'Coefficient de la matrice pour le canal vert vers vert',
            'param_color_rebalance_gb_label': 'Vert→Bleu (GB)',
            'param_color_rebalance_gb_desc': 'Coefficient de mélange du canal vert vers bleu',
            'param_color_rebalance_br_label': 'Bleu→Rouge (BR)',
            'param_color_rebalance_br_desc': 'Coefficient de mélange du canal bleu vers rouge',
            'param_color_rebalance_bg_label': 'Bleu→Vert (BG)',
            'param_color_rebalance_bg_desc': 'Coefficient de mélange du canal bleu vers vert',
            'param_color_rebalance_bb_label': 'Bleu→Bleu (BB)',
            'param_color_rebalance_bb_desc': 'Coefficient de la matrice pour le canal bleu vers bleu',
            'param_color_rebalance_saturation_limit_label': 'Limite de saturation',
            'param_color_rebalance_saturation_limit_desc': 'Plafond de saturation pour éviter les artefacts magenta (0.3-1.0)',
            'param_color_rebalance_preserve_luminance_label': 'Préserver la luminance',
            'param_color_rebalance_preserve_luminance_desc': 'Maintient la luminance originale lors du rééquilibrage',
            
            # Histogram equalization parameters
            'param_hist_eq_enabled_label': 'Égalisation d\'histogramme',
            'param_hist_eq_enabled_desc': 'Applique l\'égalisation adaptative d\'histogramme pour améliorer le contraste',
            'param_hist_eq_clip_limit_label': 'Limite de coupure CLAHE',
            'param_hist_eq_clip_limit_desc': 'Seuil pour la limitation du contraste dans l\'algorithme CLAHE',
            'param_hist_eq_tile_grid_size_label': 'Taille des tuiles CLAHE',
            'param_hist_eq_tile_grid_size_desc': 'Taille des tuiles pour l\'égalisation adaptative d\'histogramme',
            
            # Multi-scale Fusion Parameters
            'param_fusion_laplacian_levels_desc': 'Nombre de niveaux pour la pyramide laplacienne',
            'param_fusion_contrast_weight_desc': 'Poids pour la mesure de contraste',
            'param_fusion_saturation_weight_desc': 'Poids pour la mesure de saturation',
            'param_fusion_exposedness_weight_desc': 'Poids pour la mesure d\'exposition',
            'param_fusion_sigma_1_desc': 'Écart-type pour le premier filtre gaussien',
            'param_fusion_sigma_2_desc': 'Écart-type pour le deuxième filtre gaussien',
            'param_fusion_sigma_3_desc': 'Écart-type pour le troisième filtre gaussien',
            
            # White balance method names
            'method_gray_world': 'Gray-World',
            'method_white_patch': 'White-Patch', 
            'method_shades_of_gray': 'Shades-of-Gray',
            'method_grey_edge': 'Grey-Edge',
            'method_lake_green_water': 'Eau Verte (Lac)',
            
            # Language
            'language': 'Langue',
            'french': 'Français',
            'english': 'English',
            
            # About section
            'about_title': 'À propos d\'Aqualix',
            'about_app_name': 'Aqualix',
            'about_version': 'Version 1.0.0',
            'about_description': 'Application de traitement d\'images et vidéos sous-marines',
            'about_author': 'Auteur',
            'about_author_name': 'Votre Nom',
            'about_contact': 'Contact',
            'about_email': 'votre.email@example.com',
            'about_website': 'Site web',
            'about_website_url': 'https://github.com/almtlsandbox/Aqualix',
            'about_license': 'Licence',
            'about_license_type': 'MIT License',
            'about_copyright': 'Copyright © 2025 Tous droits réservés',
            'about_features_title': 'Fonctionnalités principales',
            'about_feature_1': '• Correction automatique de la balance des blancs (5 algorithmes)',
            'about_feature_2': '• Traitement UDCP pour images sous-marines',
            'about_feature_3': '• Correction Beer-Lambert pour l\'atténuation en profondeur',
            'about_feature_4': '• Égalisation d\'histogramme adaptatif (CLAHE)',
            'about_feature_5': '• Interface interactive avec zoom, panoramique et rotation',
            'about_feature_6': '• Support multilingue (Français/Anglais)',
            'about_feature_7': '• Traitement par lots pour les vidéos',
            'about_tech_title': 'Technologies utilisées',
            'about_tech_1': '• Python 3.9+ avec OpenCV et PIL/Pillow',
            'about_tech_2': '• Interface Tkinter avec composants ttk',
            'about_tech_3': '• Algorithmes de vision par ordinateur avancés',
            'about_acknowledgments': 'Remerciements',
            'about_thanks': 'Merci à la communauté OpenCV et aux chercheurs en vision sous-marine'
        }
        
        # English translations
        self.translations['en'] = {
            # Main window
            'app_title': 'Aqualix - Image and Video Processing',
            'select_file': 'Select File',
            'select_folder': 'Select Folder',
            'previous': 'Previous',
            'next': 'Next',
            'save_result': 'Save Result',
            'process_video': 'Process Video',
            'no_files': 'No files found',
            'file_info': 'File: {filename} ({index}/{total})',
            
            # Tabs
            'tab_parameters': 'Parameters',
            'tab_operations': 'Operations',
            'tab_info': 'Information',
            'tab_about': 'About',
            
            # Panel titles
            'parameters_title': 'Processing Parameters',
            'pipeline_title': 'Operations Pipeline', 
            'preview_title': 'Interactive Split View',
            'info_title': 'Image Information',
            
            # Info tabs
            'info_tab_file': 'File',
            'info_tab_properties': 'Properties',
            'info_tab_analysis': 'Analysis',
            'info_tab_exif': 'EXIF',
            
            # Parameters
            'gray_world_wb': 'Gray-World White Balance',
            'enable': 'Enable',
            'percentile': 'Percentile',
            'max_adjustment': 'Max Adjustment',
            'hist_equalization': 'Histogram Equalization',
            'clip_limit': 'Clip Limit',
            'tile_size': 'Tile Size',
            
            # Operations panel
            'processing_pipeline': 'Processing Pipeline',
            'no_operations': 'No operations enabled',
            'no_operations_desc': 'All processing steps are disabled.',
            
            # White balance methods
            'white_balance_gray_world': 'Gray-World White Balance',
            'white_balance_white_patch': 'White-Patch White Balance',
            'white_balance_shades_of_gray': 'Shades-of-Gray White Balance',
            'white_balance_grey_edge': 'Grey-Edge White Balance',
            'white_balance_lake_green_water': 'Lake Green Water White Balance',
            
            'operation_gw': 'Gray-World White Balance',
            'operation_gw_desc': 'Corrects color temperature by assuming the scene average should be neutral gray.',
            'operation_wp': 'White-Patch White Balance',
            'operation_wp_desc': 'Corrects white balance by assuming the brightest pixels should be white.',
            'operation_sog': 'Shades-of-Gray White Balance',
            'operation_sog_desc': 'Generalization of Gray-World using Minkowski norm for better robustness.',
            'operation_ge': 'Grey-Edge White Balance',
            'operation_ge_desc': 'Uses spatial derivatives to estimate scene illumination.',
            'operation_lgw': 'Lake Green Water White Balance',
            'operation_lgw_desc': 'Specialized for green lake water with targeted green reduction and magenta compensation.',
            
            # Processing step titles
            'white_balance_step_title': 'White Balance',
            'white_balance_step_desc': 'Color temperature correction',
            'udcp_step_title': 'UDCP (Underwater Dark Channel Prior)',
            'udcp_step_desc': 'Specialized enhancement for underwater images',
            'beer_lambert_step_title': 'Beer-Lambert Correction',
            'beer_lambert_step_desc': 'Depth-dependent attenuation correction using Beer-Lambert law',
            'color_rebalance_step_title': 'Color Rebalancing',
            'color_rebalance_step_desc': '3×3 transformation matrix with anti-magenta safeguards',
            'histogram_equalization_step_title': 'Histogram Equalization (CLAHE)',
            'histogram_equalization_step_desc': 'Local contrast enhancement',
            'multiscale_fusion_step_title': 'Multi-scale Fusion (Ancuti)',
            'multiscale_fusion_step_desc': 'Robust fusion of 3 variants (WB+contrast, WB+sharpness, UDCP) for optimal rendering',
            
            # UDCP method
            'udcp_title': 'UDCP (Underwater Dark Channel Prior)',
            'udcp_description': 'Specialized enhancement for underwater images',
            'operation_udcp': 'UDCP (Underwater Dark Channel Prior)',
            'operation_udcp_desc': 'Removes haze and improves visibility in underwater images using dark channel hypothesis.',
            
            'operation_beer_lambert_desc': 'Corrects depth-dependent attenuation using Beer-Lambert law with per-channel compensation.',
            
            'operation_color_rebalance_desc': 'Applies a 3×3 transformation matrix to fine-tune color balance with saturation limiting to prevent magenta artifacts.',
            
            'operation_he': 'Adaptive Histogram Equalization',
            'operation_he_desc': 'Enhances local contrast using CLAHE (Contrast Limited Adaptive Histogram Equalization).',
            
            # Interactive preview
            'split_position': 'Split',
            'zoom': 'Zoom',
            'fit_image': 'Fit',
            'reset_view': '1:1',
            'rotation': 'Rotation',
            'collapse_all': 'Collapse All',
            'expand_all': 'Expand All',
            'reset_defaults': 'Reset',
            'reset_defaults_tooltip': 'Reset this section parameters to default values',
            'auto_tune': 'Auto-Tune',
            'auto_tune_tooltip': 'Automatically optimize parameters during this step execution',
            'expand_all_sections': 'Expand all sections',
            'reset_all_parameters': 'Global Reset',
            'reset_all_parameters_tooltip': 'Reset ALL parameters to their default values',
            'no_image_loaded': 'No image loaded',
            'preview_instructions': 'Controls: Left click + drag to pan • Mouse wheel to zoom • Drag the split line',
            
            # Image info
            'image_info': 'Image Information',
            'file_tab': 'File',
            'properties_tab': 'Properties',
            'analysis_tab': 'Analysis',
            'exif_tab': 'EXIF',
            'no_color_analysis': 'No color analysis available',
            'no_exif_data': 'No EXIF data found',
            
            # File info labels
            'name': 'Name',
            'path': 'Path',
            'size': 'Size',
            'modified': 'Modified',
            'created': 'Created',
            'extension': 'Extension',
            'hash_md5': 'MD5 Hash',
            
            # Properties labels
            'width': 'Width',
            'height': 'Height',
            'channels': 'Channels',
            'total_pixels': 'Total Pixels',
            'aspect_ratio': 'Aspect Ratio',
            'format': 'Format',
            'mode': 'Mode',
            'transparency': 'Transparency',
            'data_type': 'Data Type',
            'min_value': 'Min Value',
            'max_value': 'Max Value',
            'mean_value': 'Mean Value',
            'fps': 'FPS',
            'total_frames': 'Total Frames',
            'duration': 'Duration',
            'codec': 'Codec',
            
            # Analysis labels
            'red_mean': 'Red Mean',
            'green_mean': 'Green Mean',
            'blue_mean': 'Blue Mean',
            'red_std': 'Red Std Dev',
            'green_std': 'Green Std Dev',
            'blue_std': 'Blue Std Dev',
            'brightness': 'Brightness',
            'contrast': 'Contrast',
            'estimated_color_temp': 'Est. Color Temp',
            'unique_colors': 'Unique Colors',
            'min_intensity': 'Min Intensity',
            'max_intensity': 'Max Intensity',
            
            # Messages
            'yes': 'Yes',
            'no': 'No',
            'error': 'Error',
            'success': 'Success',
            'processing': 'Processing...',
            'saved_as': 'Saved as: {path}',
            'could_not_load': 'Could not load: {error}',
            'could_not_save': 'Could not save: {error}',
            'video_saved_as': 'Video saved as: {path}',
            'processing_video_frames': 'Processing video frames...',
            'frame_x_of_y': 'Frame {current} of {total}',
            
            # Parameter labels and descriptions
            # White balance parameters
            'param_white_balance_enabled_label': 'White balance enabled',
            'param_white_balance_enabled_desc': 'Apply white balance correction',
            'param_white_balance_method_label': 'White balance method',
            'param_white_balance_method_desc': 'Algorithm used for white balance correction',
            'param_gray_world_percentile_label': 'Gray-World percentile',
            'param_gray_world_percentile_desc': 'Percentile used to calculate color channel averages',
            'param_gray_world_max_adjustment_label': 'Max adjustment (Gray-World)',
            'param_gray_world_max_adjustment_desc': 'Maximum allowed scaling factor for color channels',
            'param_white_patch_percentile_label': 'White-Patch percentile',
            'param_white_patch_percentile_desc': 'Percentile to identify the brightest patch',
            'param_white_patch_max_adjustment_label': 'Max adjustment (White-Patch)',
            'param_white_patch_max_adjustment_desc': 'Maximum allowed scaling factor for color channels',
            'param_shades_of_gray_norm_label': 'Minkowski norm (Shades of Gray)',
            'param_shades_of_gray_norm_desc': 'Order of the Minkowski norm for computation',
            'param_shades_of_gray_percentile_label': 'Percentile (Shades of Gray)',
            'param_shades_of_gray_percentile_desc': 'Percentile used to calculate the generalized norm',
            'param_shades_of_gray_max_adjustment_label': 'Max adjustment (Shades of Gray)',
            'param_shades_of_gray_max_adjustment_desc': 'Maximum allowed scaling factor for color channels',
            'param_grey_edge_norm_label': 'Minkowski norm (Grey-Edge)',
            'param_grey_edge_norm_desc': 'Order of the Minkowski norm for derivative computation',
            'param_grey_edge_sigma_label': 'Gaussian sigma (Grey-Edge)',
            'param_grey_edge_sigma_desc': 'Standard deviation of Gaussian filter for derivative computation',
            'param_grey_edge_max_adjustment_label': 'Max adjustment (Grey-Edge)',
            'param_grey_edge_max_adjustment_desc': 'Maximum allowed scaling factor for color channels',
            'param_lake_green_reduction_label': 'Green reduction',
            'param_lake_green_reduction_desc': 'Intensity of green channel reduction (0.0 = none, 1.0 = maximum)',
            'param_lake_magenta_strength_label': 'Magenta strength',
            'param_lake_magenta_strength_desc': 'Intensity of magenta compensation (red+blue boost)',
            'param_lake_gray_world_influence_label': 'Gray-World influence',
            'param_lake_gray_world_influence_desc': 'Influence of final Gray-World correction',
            
            # UDCP parameters
            'param_udcp_enabled_label': 'UDCP enabled',
            'param_udcp_enabled_desc': 'Apply Underwater Dark Channel Prior algorithm',
            'param_udcp_omega_label': 'Omega factor',
            'param_udcp_omega_desc': 'Atmospheric haze preservation factor (0.0 = complete removal)',
            'param_udcp_t0_label': 'Minimum transmission (t0)',
            'param_udcp_t0_desc': 'Minimum transmission value to avoid over-correction',
            'param_udcp_window_size_label': 'Window size',
            'param_udcp_window_size_desc': 'Window size for dark channel computation',
            'param_udcp_guided_radius_label': 'Guided filter radius',
            'param_udcp_guided_radius_desc': 'Radius of guided filter for transmission map refinement',
            'param_udcp_guided_eps_label': 'Guided filter epsilon',
            'param_udcp_guided_eps_desc': 'Regularization parameter for guided filter',
            'param_udcp_enhance_contrast_label': 'Contrast enhancement',
            'param_udcp_enhance_contrast_desc': 'Final contrast enhancement factor',
            
            # Beer-Lambert parameters
            'param_beer_lambert_enabled_label': 'Beer-Lambert correction',
            'param_beer_lambert_enabled_desc': 'Apply Beer-Lambert correction for depth-dependent attenuation',
            'param_beer_lambert_depth_factor_label': 'Depth factor',
            'param_beer_lambert_depth_factor_desc': 'Correction factor based on estimated depth',
            'param_beer_lambert_red_coeff_label': 'Red coefficient',
            'param_beer_lambert_red_coeff_desc': 'Attenuation coefficient for red channel',
            'param_beer_lambert_green_coeff_label': 'Green coefficient',
            'param_beer_lambert_green_coeff_desc': 'Attenuation coefficient for green channel',
            'param_beer_lambert_blue_coeff_label': 'Blue coefficient',
            'param_beer_lambert_blue_coeff_desc': 'Attenuation coefficient for blue channel',
            'param_beer_lambert_enhance_factor_label': 'Enhancement factor',
            'param_beer_lambert_enhance_factor_desc': 'Final enhancement factor for Beer-Lambert correction',
            
            # Color rebalancing parameters
            'param_color_rebalance_enabled_label': 'Color rebalancing',
            'param_color_rebalance_enabled_desc': 'Enable 3×3 transformation matrix for color fine-tuning',
            'param_color_rebalance_rr_label': 'Red→Red (RR)',
            'param_color_rebalance_rr_desc': 'Matrix coefficient for red channel to red output',
            'param_color_rebalance_rg_label': 'Red→Green (RG)',
            'param_color_rebalance_rg_desc': 'Cross-channel mixing coefficient from red to green',
            'param_color_rebalance_rb_label': 'Red→Blue (RB)',
            'param_color_rebalance_rb_desc': 'Cross-channel mixing coefficient from red to blue',
            'param_color_rebalance_gr_label': 'Green→Red (GR)',
            'param_color_rebalance_gr_desc': 'Cross-channel mixing coefficient from green to red',
            'param_color_rebalance_gg_label': 'Green→Green (GG)',
            'param_color_rebalance_gg_desc': 'Matrix coefficient for green channel to green output',
            'param_color_rebalance_gb_label': 'Green→Blue (GB)',
            'param_color_rebalance_gb_desc': 'Cross-channel mixing coefficient from green to blue',
            'param_color_rebalance_br_label': 'Blue→Red (BR)',
            'param_color_rebalance_br_desc': 'Cross-channel mixing coefficient from blue to red',
            'param_color_rebalance_bg_label': 'Blue→Green (BG)',
            'param_color_rebalance_bg_desc': 'Cross-channel mixing coefficient from blue to green',
            'param_color_rebalance_bb_label': 'Blue→Blue (BB)',
            'param_color_rebalance_bb_desc': 'Matrix coefficient for blue channel to blue output',
            'param_color_rebalance_saturation_limit_label': 'Saturation limit',
            'param_color_rebalance_saturation_limit_desc': 'Saturation ceiling to prevent magenta artifacts (0.3-1.0)',
            'param_color_rebalance_preserve_luminance_label': 'Preserve luminance',
            'param_color_rebalance_preserve_luminance_desc': 'Maintain original luminance during rebalancing',
            
            # Histogram equalization parameters
            'param_hist_eq_enabled_label': 'Histogram equalization',
            'param_hist_eq_enabled_desc': 'Apply adaptive histogram equalization to improve contrast',
            'param_hist_eq_clip_limit_label': 'CLAHE clip limit',
            'param_hist_eq_clip_limit_desc': 'Threshold for contrast limiting in CLAHE algorithm',
            'param_hist_eq_tile_grid_size_label': 'CLAHE tile size',
            'param_hist_eq_tile_grid_size_desc': 'Tile size for adaptive histogram equalization',
            
            # Multi-scale Fusion Parameters
            'param_fusion_laplacian_levels_desc': 'Number of levels for the Laplacian pyramid',
            'param_fusion_contrast_weight_desc': 'Weight for contrast measure',
            'param_fusion_saturation_weight_desc': 'Weight for saturation measure',
            'param_fusion_exposedness_weight_desc': 'Weight for exposedness measure',
            'param_fusion_sigma_1_desc': 'Standard deviation for first Gaussian filter',
            'param_fusion_sigma_2_desc': 'Standard deviation for second Gaussian filter',
            'param_fusion_sigma_3_desc': 'Standard deviation for third Gaussian filter',
            
            # White balance method names
            'method_gray_world': 'Gray-World',
            'method_white_patch': 'White-Patch',
            'method_shades_of_gray': 'Shades-of-Gray',
            'method_grey_edge': 'Grey-Edge',
            'method_lake_green_water': 'Lake Green Water',
            
            # Language
            'language': 'Language',
            'french': 'Français',
            'english': 'English',
            
            # About section
            'about_title': 'About Aqualix',
            'about_app_name': 'Aqualix',
            'about_version': 'Version 1.0.0',
            'about_description': 'Underwater image and video processing application',
            'about_author': 'Author',
            'about_author_name': 'Your Name',
            'about_contact': 'Contact',
            'about_email': 'your.email@example.com',
            'about_website': 'Website',
            'about_website_url': 'https://github.com/almtlsandbox/Aqualix',
            'about_license': 'License',
            'about_license_type': 'MIT License',
            'about_copyright': 'Copyright © 2025 All rights reserved',
            'about_features_title': 'Key Features',
            'about_feature_1': '• Automatic white balance correction (5 algorithms)',
            'about_feature_2': '• UDCP processing for underwater images',
            'about_feature_3': '• Beer-Lambert correction for depth attenuation',
            'about_feature_4': '• Adaptive histogram equalization (CLAHE)',
            'about_feature_5': '• Interactive interface with zoom, pan, and rotation',
            'about_feature_6': '• Multilingual support (French/English)',
            'about_feature_7': '• Batch processing for videos',
            'about_tech_title': 'Technologies Used',
            'about_tech_1': '• Python 3.9+ with OpenCV and PIL/Pillow',
            'about_tech_2': '• Tkinter interface with ttk components',
            'about_tech_3': '• Advanced computer vision algorithms',
            'about_acknowledgments': 'Acknowledgments',
            'about_thanks': 'Thanks to the OpenCV community and underwater vision researchers',
            
            # About section
            'about_title': 'About Aqualix',
            'about_app_name': 'Aqualix',
            'about_version': 'Version 1.0.0',
            'about_description': 'Underwater image and video processing application',
            'about_author': 'Author',
            'about_author_name': 'Your Name',
            'about_contact': 'Contact',
            'about_email': 'your.email@example.com',
            'about_website': 'Website',
            'about_website_url': 'https://github.com/almtlsandbox/Aqualix',
            'about_license': 'License',
            'about_license_type': 'MIT License',
            'about_copyright': 'Copyright © 2025 All rights reserved',
            'about_features_title': 'Key Features',
            'about_feature_1': '• Automatic white balance correction (5 algorithms)',
            'about_feature_2': '• UDCP processing for underwater images',
            'about_feature_3': '• Beer-Lambert correction for depth attenuation',
            'about_feature_4': '• Adaptive histogram equalization (CLAHE)',
            'about_feature_5': '• Interactive interface with zoom, pan, and rotation',
            'about_feature_6': '• Multilingual support (French/English)',
            'about_feature_7': '• Batch processing for videos',
            'about_tech_title': 'Technologies Used',
            'about_tech_1': '• Python 3.9+ with OpenCV and PIL/Pillow',
            'about_tech_2': '• Tkinter interface with ttk components',
            'about_tech_3': '• Advanced computer vision algorithms',
            'about_acknowledgments': 'Acknowledgments',
            'about_thanks': 'Thanks to the OpenCV community and underwater vision researchers'
        }
        
    def set_language(self, language):
        """Set the current language"""
        if language in self.translations:
            self.current_language = language
            self.save_language_preference(language)
            
    def get_language(self):
        """Get the current language"""
        return self.current_language
        
    def get_available_languages(self):
        """Get list of available languages"""
        return list(self.translations.keys())
        
    def t(self, key, **kwargs):
        """Translate a key to current language"""
        if self.current_language not in self.translations:
            return key
            
        translation = self.translations[self.current_language].get(key, key)
        
        # Format with provided arguments if any
        if kwargs:
            try:
                translation = translation.format(**kwargs)
            except (KeyError, ValueError):
                pass  # Return unformatted if formatting fails
                
        return translation
        
    def get_language_name(self, lang_code):
        """Get the display name for a language code"""
        names = {
            'fr': self.t('french'),
            'en': self.t('english')
        }
        return names.get(lang_code, lang_code)

# Global localization manager instance
_localization_manager = LocalizationManager()

def get_localization_manager():
    """Get the global localization manager instance"""
    return _localization_manager

def t(key, **kwargs):
    """Shortcut function for translation"""
    return _localization_manager.t(key, **kwargs)

def set_language(language):
    """Shortcut function to set language"""
    _localization_manager.set_language(language)
    
def get_language():
    """Shortcut function to get current language"""
    return _localization_manager.get_language()
