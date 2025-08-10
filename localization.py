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
            'operation_gw': 'Balance des blancs Gray-World',
            'operation_gw_desc': 'Corrige la température de couleur en assumant que la moyenne de la scène devrait être grise neutre.',
            'operation_he': 'Égalisation d\'histogramme adaptatif',
            'operation_he_desc': 'Améliore le contraste local en utilisant CLAHE (Contrast Limited Adaptive Histogram Equalization).',
            
            # Interactive preview
            'split_position': 'Division',
            'zoom': 'Zoom',
            'fit_image': 'Ajuster',
            'reset_view': '1:1',
            'rotation': 'Rotation',
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
            
            # Language
            'language': 'Langue',
            'french': 'Français',
            'english': 'English'
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
            'operation_gw': 'Gray-World White Balance',
            'operation_gw_desc': 'Corrects color temperature by assuming the scene average should be neutral gray.',
            'operation_he': 'Adaptive Histogram Equalization',
            'operation_he_desc': 'Enhances local contrast using CLAHE (Contrast Limited Adaptive Histogram Equalization).',
            
            # Interactive preview
            'split_position': 'Split',
            'zoom': 'Zoom',
            'fit_image': 'Fit',
            'reset_view': '1:1',
            'rotation': 'Rotation',
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
            
            # Language
            'language': 'Language',
            'french': 'Français',
            'english': 'English'
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
