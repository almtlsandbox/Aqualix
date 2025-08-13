#!/usr/bin/env python3
"""
Auto-Tune Mapping System pour Aqualix
Système complet de mapping et d'intégration des méthodes auto-tune
Étape 3 du plan d'amélioration auto-tune
"""

from typing import Dict, List, Any, Optional, Callable
import inspect
import numpy as np

class AutoTuneMapper:
    """
    Système de mapping auto-tune unifié pour Aqualix
    Gère l'intégration entre méthodes standard et enhanced
    """
    
    def __init__(self, image_processor):
        """
        Initialise le mapper auto-tune
        
        Args:
            image_processor: Instance de ImageProcessor
        """
        self.processor = image_processor
        self.algorithm_registry = {}
        self.enhanced_mode = False
        self._initialize_mappings()
    
    def _initialize_mappings(self):
        """Initialise les mappings des algorithmes auto-tune"""
        
        # Mapping complet des algorithmes avec leurs méthodes
        self.algorithm_registry = {
            'white_balance': {
                'standard_method': '_auto_tune_white_balance',
                'enhanced_method': '_enhanced_auto_tune_white_balance',
                'display_name': 'White Balance',
                'priority': 1,
                'parameters': [
                    'white_balance_enabled', 'white_balance_method',
                    'gray_world_percentile', 'gray_world_max_adjustment',
                    'white_patch_percentile', 'white_patch_max_adjustment',
                    'shades_of_gray_norm', 'shades_of_gray_percentile', 
                    'shades_of_gray_max_adjustment', 'grey_edge_norm', 
                    'grey_edge_sigma', 'grey_edge_max_adjustment',
                    'lake_green_reduction', 'lake_magenta_strength', 
                    'lake_gray_world_influence'
                ],
                'enhanced_parameters': [
                    'gray_world_percentile', 'gray_world_max_adjustment',
                    'white_patch_percentile', 'grey_edge_norm', 'grey_edge_sigma'
                ],
                'description': 'Correction automatique de la balance des blancs selon le type d\'eau',
                'use_cases': ['underwater_photography', 'color_correction', 'blue_cast_removal']
            },
            
            'udcp': {
                'standard_method': '_auto_tune_udcp',
                'enhanced_method': '_enhanced_auto_tune_udcp',
                'display_name': 'Underwater Dark Channel Prior',
                'priority': 2,
                'parameters': [
                    'udcp_enabled', 'udcp_omega', 'udcp_t0', 'udcp_window_size',
                    'udcp_guided_radius', 'udcp_guided_epsilon', 'udcp_enhance_factor'
                ],
                'enhanced_parameters': [
                    'udcp_enabled', 'udcp_omega', 'udcp_t0', 'udcp_window_size',
                    'udcp_guided_radius', 'udcp_guided_epsilon', 'udcp_enhance_factor'
                ],
                'description': 'Débruitage et restauration basés sur recherche Drews et Carlevaris-Bianco',
                'use_cases': ['underwater_dehazing', 'visibility_enhancement', 'depth_restoration']
            },
            
            'beer_lambert': {
                'standard_method': '_auto_tune_beer_lambert',
                'enhanced_method': '_enhanced_auto_tune_beer_lambert',
                'display_name': 'Beer-Lambert Law Correction',
                'priority': 3,
                'parameters': [
                    'beer_lambert_enabled', 'beer_lambert_depth_factor',
                    'beer_lambert_red_coeff', 'beer_lambert_green_coeff',
                    'beer_lambert_blue_coeff', 'beer_lambert_enhance_factor'
                ],
                'enhanced_parameters': [
                    'beer_lambert_enabled', 'beer_lambert_depth_factor',
                    'beer_lambert_red_coeff', 'beer_lambert_green_coeff',
                    'beer_lambert_blue_coeff', 'beer_lambert_enhance_factor'
                ],
                'description': 'Correction spectrale basée sur loi Beer-Lambert et recherche McGlamery',
                'use_cases': ['spectral_correction', 'depth_compensation', 'water_type_adaptation']
            },
            
            'color_rebalance': {
                'standard_method': '_auto_tune_color_rebalance',
                'enhanced_method': '_enhanced_auto_tune_color_rebalancing',
                'display_name': 'Color Rebalancing',
                'priority': 4,
                'parameters': [
                    'color_rebalance_enabled', 'color_rebalance_rr', 'color_rebalance_rg', 
                    'color_rebalance_rb', 'color_rebalance_gr', 'color_rebalance_gg', 
                    'color_rebalance_gb', 'color_rebalance_br', 'color_rebalance_bg', 
                    'color_rebalance_bb', 'color_rebalance_saturation_limit', 
                    'color_rebalance_preserve_luminance'
                ],
                'enhanced_parameters': [
                    'color_rebalance_enabled', 'color_rebalance_red_factor',
                    'color_rebalance_green_factor', 'color_rebalance_blue_factor',
                    'color_rebalance_gamma', 'color_rebalance_saturation_factor'
                ],
                'description': 'Rééquilibrage adaptatif des couleurs selon environnement aquatique',
                'use_cases': ['color_cast_correction', 'saturation_enhancement', 'underwater_color_recovery']
            },
            
            'histogram_equalization': {
                'standard_method': '_auto_tune_histogram_equalization',
                'enhanced_method': '_enhanced_auto_tune_histogram_equalization',
                'display_name': 'Histogram Equalization',
                'priority': 5,
                'parameters': [
                    'hist_eq_enabled', 'hist_eq_method', 'hist_eq_clip_limit', 
                    'hist_eq_tile_grid_size'
                ],
                'enhanced_parameters': [
                    'hist_eq_enabled', 'hist_eq_method', 'hist_eq_clip_limit',
                    'hist_eq_grid_size'
                ],
                'description': 'Égalisation adaptative d\'histogramme avec analyse CLAHE intelligente',
                'use_cases': ['contrast_enhancement', 'detail_preservation', 'dynamic_range_expansion']
            },
            
            'multiscale_fusion': {
                'standard_method': '_auto_tune_multiscale_fusion',
                'enhanced_method': '_enhanced_auto_tune_multiscale_fusion',
                'display_name': 'Multiscale Fusion',
                'priority': 6,
                'parameters': [
                    'multiscale_fusion_enabled', 'fusion_laplacian_levels',
                    'fusion_contrast_weight', 'fusion_saturation_weight', 
                    'fusion_exposedness_weight', 'fusion_sigma_contrast',
                    'fusion_sigma_saturation', 'fusion_sigma_exposedness'
                ],
                'enhanced_parameters': [
                    'multiscale_fusion_enabled', 'multiscale_contrast_weight',
                    'multiscale_saturation_weight', 'multiscale_exposedness_weight',
                    'multiscale_levels', 'multiscale_sigma'
                ],
                'description': 'Fusion multi-échelle basée sur recherche Mertens et Ancuti',
                'use_cases': ['detail_enhancement', 'exposure_fusion', 'quality_preservation']
            }
        }
    
    def set_enhanced_mode(self, enabled: bool = True):
        """
        Active/désactive le mode enhanced auto-tune
        
        Args:
            enabled: True pour activer les méthodes enhanced
        """
        self.enhanced_mode = enabled
        if hasattr(self.processor, 'toggle_enhanced_autotune'):
            self.processor.toggle_enhanced_autotune(enabled)
        print(f"🔧 Auto-tune mode: {'Enhanced (Academic Research)' if enabled else 'Standard'}")
    
    def get_available_algorithms(self) -> List[str]:
        """Retourne la liste des algorithmes disponibles"""
        return list(self.algorithm_registry.keys())
    
    def get_algorithm_info(self, algorithm: str) -> Optional[Dict]:
        """
        Retourne les informations complètes d'un algorithme
        
        Args:
            algorithm: Nom de l'algorithme
            
        Returns:
            Dict avec informations complètes ou None si non trouvé
        """
        return self.algorithm_registry.get(algorithm)
    
    def get_method_for_algorithm(self, algorithm: str, enhanced: Optional[bool] = None) -> Optional[str]:
        """
        Retourne le nom de la méthode pour un algorithme donné
        
        Args:
            algorithm: Nom de l'algorithme
            enhanced: Force enhanced (True) ou standard (False), None = auto
            
        Returns:
            Nom de la méthode ou None si non trouvé
        """
        if algorithm not in self.algorithm_registry:
            return None
        
        algo_info = self.algorithm_registry[algorithm]
        use_enhanced = enhanced if enhanced is not None else self.enhanced_mode
        
        if use_enhanced and algo_info.get('enhanced_method'):
            return algo_info['enhanced_method']
        else:
            return algo_info['standard_method']
    
    def execute_auto_tune(self, algorithm: str, image: np.ndarray, enhanced: Optional[bool] = None) -> Dict[str, Any]:
        """
        Exécute l'auto-tune pour un algorithme spécifique
        
        Args:
            algorithm: Nom de l'algorithme
            image: Image numpy array
            enhanced: Force enhanced (True) ou standard (False), None = auto
            
        Returns:
            Paramètres optimisés ou dict vide en cas d'erreur
        """
        method_name = self.get_method_for_algorithm(algorithm, enhanced)
        
        if not method_name:
            print(f"❌ Algorithme '{algorithm}' non trouvé dans le registry")
            return {}
        
        if not hasattr(self.processor, method_name):
            print(f"❌ Méthode '{method_name}' non trouvée dans ImageProcessor")
            return {}
        
        method = getattr(self.processor, method_name)
        if not callable(method):
            print(f"❌ '{method_name}' n'est pas callable")
            return {}
        
        try:
            result = method(image)
            if result is None:
                result = {}
            elif not isinstance(result, dict):
                result = {}
            mode = "enhanced" if (enhanced or (enhanced is None and self.enhanced_mode)) else "standard"
            print(f"✅ Auto-tune {algorithm} ({mode}): {len(result)} paramètres optimisés")
            return result
        except Exception as e:
            print(f"❌ Erreur dans auto-tune {algorithm}: {e}")
            return {}
    
    def execute_pipeline_auto_tune(self, image: np.ndarray, algorithms: Optional[List[str]] = None, 
                                 enhanced: Optional[bool] = None) -> Dict[str, Dict[str, Any]]:
        """
        Exécute l'auto-tune pour un pipeline complet d'algorithmes
        
        Args:
            image: Image numpy array
            algorithms: Liste des algorithmes à exécuter (None = tous)
            enhanced: Force enhanced (True) ou standard (False), None = auto
            
        Returns:
            Dict {algorithm: parameters} avec résultats pour chaque algorithme
        """
        if algorithms is None:
            # Utiliser tous les algorithmes triés par priorité
            algorithms = sorted(self.algorithm_registry.keys(), 
                              key=lambda x: self.algorithm_registry[x]['priority'])
        
        results = {}
        mode = "enhanced" if (enhanced or (enhanced is None and self.enhanced_mode)) else "standard"
        
        print(f"\n🚀 PIPELINE AUTO-TUNE ({mode.upper()})")
        print("=" * 50)
        
        for algorithm in algorithms:
            if algorithm not in self.algorithm_registry:
                print(f"⚠️  Algorithme '{algorithm}' ignoré (non trouvé)")
                continue
            
            print(f"\n🔧 {self.algorithm_registry[algorithm]['display_name']}")
            print("-" * 30)
            
            result = self.execute_auto_tune(algorithm, image, enhanced)
            results[algorithm] = result
            
            if result:
                print(f"   📈 Paramètres optimisés: {list(result.keys())}")
            else:
                print(f"   ❌ Aucun paramètre optimisé")
        
        print(f"\n📊 RÉSUMÉ PIPELINE:")
        print(f"   • Algorithmes traités: {len([a for a in algorithms if a in self.algorithm_registry])}")
        print(f"   • Paramètres totaux: {sum(len(r) for r in results.values())}")
        print(f"   • Mode: {mode}")
        
        return results
    
    def get_parameters_mapping(self, algorithm: str, enhanced: Optional[bool] = None) -> List[str]:
        """
        Retourne la liste des paramètres utilisés par un algorithme
        
        Args:
            algorithm: Nom de l'algorithme
            enhanced: Force enhanced (True) ou standard (False), None = auto
            
        Returns:
            Liste des noms de paramètres
        """
        if algorithm not in self.algorithm_registry:
            return []
        
        algo_info = self.algorithm_registry[algorithm]
        use_enhanced = enhanced if enhanced is not None else self.enhanced_mode
        
        if use_enhanced and algo_info.get('enhanced_parameters'):
            return algo_info['enhanced_parameters']
        else:
            return algo_info['parameters']
    
    def validate_auto_tune_integration(self) -> Dict[str, Any]:
        """
        Valide l'intégration complète du système auto-tune
        
        Returns:
            Rapport de validation complet
        """
        validation_report = {
            'algorithms_count': len(self.algorithm_registry),
            'standard_methods': {},
            'enhanced_methods': {},
            'missing_methods': [],
            'integration_status': 'unknown'
        }
        
        print("\n🔍 VALIDATION INTÉGRATION AUTO-TUNE")
        print("=" * 50)
        
        for algo_name, algo_info in self.algorithm_registry.items():
            # Validation méthode standard
            std_method = algo_info['standard_method']
            std_exists = hasattr(self.processor, std_method)
            std_callable = callable(getattr(self.processor, std_method, None))
            
            validation_report['standard_methods'][algo_name] = {
                'method': std_method,
                'exists': std_exists,
                'callable': std_callable,
                'status': '✅' if (std_exists and std_callable) else '❌'
            }
            
            # Validation méthode enhanced
            enh_method = algo_info.get('enhanced_method')
            if enh_method:
                enh_exists = hasattr(self.processor, enh_method)
                enh_callable = callable(getattr(self.processor, enh_method, None))
                
                validation_report['enhanced_methods'][algo_name] = {
                    'method': enh_method,
                    'exists': enh_exists,
                    'callable': enh_callable,
                    'status': '✅' if (enh_exists and enh_callable) else '❌'
                }
            else:
                validation_report['enhanced_methods'][algo_name] = {
                    'method': None,
                    'exists': False,
                    'callable': False,
                    'status': '⚠️'
                }
            
            # Affichage détaillé
            print(f"\n🔧 {algo_info['display_name']}")
            print(f"   Standard: {validation_report['standard_methods'][algo_name]['status']} {std_method}")
            if enh_method:
                print(f"   Enhanced: {validation_report['enhanced_methods'][algo_name]['status']} {enh_method}")
            else:
                print(f"   Enhanced: ⚠️  Non implémenté")
        
        # Calcul statut global
        std_ok = all(m['exists'] and m['callable'] for m in validation_report['standard_methods'].values())
        enh_ok = all(m['exists'] and m['callable'] for m in validation_report['enhanced_methods'].values() if m['method'])
        
        if std_ok and enh_ok:
            validation_report['integration_status'] = 'excellent'
        elif std_ok:
            validation_report['integration_status'] = 'good'
        else:
            validation_report['integration_status'] = 'needs_work'
        
        print(f"\n🎯 STATUT GLOBAL: {validation_report['integration_status'].upper()}")
        
        return validation_report

def create_auto_tune_mapping_system(image_processor) -> AutoTuneMapper:
    """
    Factory function pour créer le système de mapping auto-tune
    
    Args:
        image_processor: Instance de ImageProcessor
        
    Returns:
        Instance configurée de AutoTuneMapper
    """
    return AutoTuneMapper(image_processor)
