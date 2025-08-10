"""
Image Processing Module
Contains image processing algorithms and pipeline management.
"""

import cv2
import numpy as np
from typing import Dict, Any, List, Tuple

class ImageProcessor:
    def __init__(self):
        # Initialize parameters with default values
        self.parameters = {
            # White balance method selection
            'white_balance_method': 'gray_world',  # gray_world, white_patch, shades_of_gray, grey_edge
            'white_balance_enabled': True,
            
            # Gray-world white balance parameters
            'gray_world_percentile': 50,
            'gray_world_max_adjustment': 2.0,
            
            # White-patch parameters
            'white_patch_percentile': 99,
            'white_patch_max_adjustment': 2.0,
            
            # Shades-of-gray parameters
            'shades_of_gray_norm': 6,
            'shades_of_gray_percentile': 50,
            'shades_of_gray_max_adjustment': 2.0,
            
            # Grey-edge parameters
            'grey_edge_norm': 1,
            'grey_edge_sigma': 1,
            'grey_edge_max_adjustment': 2.0,
            
            # Histogram equalization parameters
            'hist_eq_enabled': True,
            'hist_eq_clip_limit': 2.0,
            'hist_eq_tile_grid_size': 8,
        }
        
        # Processing pipeline order
        self.pipeline_order = [
            'white_balance',
            'histogram_equalization'
        ]
        
    def set_parameter(self, name: str, value: Any):
        """Set a processing parameter"""
        if name in self.parameters:
            self.parameters[name] = value
            
    def get_parameter(self, name: str) -> Any:
        """Get a processing parameter"""
        return self.parameters.get(name)
        
    def get_all_parameters(self) -> Dict[str, Any]:
        """Get all parameters"""
        return self.parameters.copy()
        
    def process_image(self, image: np.ndarray) -> np.ndarray:
        """Process an image through the complete pipeline"""
        result = image.copy()
        
        for operation in self.pipeline_order:
            if operation == 'white_balance' and self.parameters['white_balance_enabled']:
                result = self.apply_white_balance(result)
            elif operation == 'histogram_equalization' and self.parameters['hist_eq_enabled']:
                result = self.adaptive_histogram_equalization(result)
                
        return result
    
    def apply_white_balance(self, image: np.ndarray) -> np.ndarray:
        """Apply the selected white balance method"""
        method = self.parameters['white_balance_method']
        
        if method == 'gray_world':
            return self.gray_world_white_balance(image)
        elif method == 'white_patch':
            return self.white_patch_white_balance(image)
        elif method == 'shades_of_gray':
            return self.shades_of_gray_white_balance(image)
        elif method == 'grey_edge':
            return self.grey_edge_white_balance(image)
        else:
            return image
        
    def gray_world_white_balance(self, image: np.ndarray) -> np.ndarray:
        """
        Apply gray-world white balance algorithm.
        Assumes the average color in the image should be gray.
        """
        try:
            # Convert to float for processing
            img_float = image.astype(np.float32) / 255.0
            
            # Calculate channel means
            percentile = self.parameters['gray_world_percentile']
            max_adjustment = self.parameters['gray_world_max_adjustment']
            
            # Use percentile instead of mean for more robust estimation
            r_mean = np.percentile(img_float[:, :, 0], percentile)
            g_mean = np.percentile(img_float[:, :, 1], percentile)
            b_mean = np.percentile(img_float[:, :, 2], percentile)
            
            # Calculate scaling factors
            gray_mean = (r_mean + g_mean + b_mean) / 3.0
            
            if gray_mean > 0:
                r_scale = gray_mean / (r_mean + 1e-6)
                g_scale = gray_mean / (g_mean + 1e-6)
                b_scale = gray_mean / (b_mean + 1e-6)
                
                # Limit adjustment to prevent overcorrection
                r_scale = np.clip(r_scale, 1/max_adjustment, max_adjustment)
                g_scale = np.clip(g_scale, 1/max_adjustment, max_adjustment)
                b_scale = np.clip(b_scale, 1/max_adjustment, max_adjustment)
                
                # Apply scaling
                img_float[:, :, 0] *= r_scale
                img_float[:, :, 1] *= g_scale
                img_float[:, :, 2] *= b_scale
                
            # Convert back to uint8
            result = np.clip(img_float * 255.0, 0, 255).astype(np.uint8)
            return result
            
        except Exception as e:
            print(f"Error in gray-world white balance: {e}")
            return image
    
    def white_patch_white_balance(self, image: np.ndarray) -> np.ndarray:
        """
        Apply white-patch white balance algorithm.
        Assumes the brightest pixels should be white.
        """
        try:
            # Convert to float for processing
            img_float = image.astype(np.float32) / 255.0
            
            percentile = self.parameters['white_patch_percentile']
            max_adjustment = self.parameters['white_patch_max_adjustment']
            
            # Find the brightest pixels for each channel
            r_white = np.percentile(img_float[:, :, 0], percentile)
            g_white = np.percentile(img_float[:, :, 1], percentile)
            b_white = np.percentile(img_float[:, :, 2], percentile)
            
            # Calculate scaling factors to make these white
            if r_white > 0 and g_white > 0 and b_white > 0:
                r_scale = 1.0 / r_white
                g_scale = 1.0 / g_white
                b_scale = 1.0 / b_white
                
                # Limit adjustment to prevent overcorrection
                r_scale = np.clip(r_scale, 1/max_adjustment, max_adjustment)
                g_scale = np.clip(g_scale, 1/max_adjustment, max_adjustment)
                b_scale = np.clip(b_scale, 1/max_adjustment, max_adjustment)
                
                # Apply scaling
                img_float[:, :, 0] *= r_scale
                img_float[:, :, 1] *= g_scale
                img_float[:, :, 2] *= b_scale
                
            # Convert back to uint8
            result = np.clip(img_float * 255.0, 0, 255).astype(np.uint8)
            return result
            
        except Exception as e:
            print(f"Error in white-patch white balance: {e}")
            return image
    
    def shades_of_gray_white_balance(self, image: np.ndarray) -> np.ndarray:
        """
        Apply shades-of-gray white balance algorithm.
        Generalization of gray-world using Minkowski norm.
        """
        try:
            # Convert to float for processing
            img_float = image.astype(np.float32) / 255.0
            
            norm = self.parameters['shades_of_gray_norm']
            percentile = self.parameters['shades_of_gray_percentile']
            max_adjustment = self.parameters['shades_of_gray_max_adjustment']
            
            # Calculate Minkowski norm for each channel
            def minkowski_norm(channel, p):
                if p == np.inf:
                    return np.max(channel)
                else:
                    return np.power(np.mean(np.power(channel + 1e-6, p)), 1.0/p)
            
            r_norm = minkowski_norm(img_float[:, :, 0], norm)
            g_norm = minkowski_norm(img_float[:, :, 1], norm)
            b_norm = minkowski_norm(img_float[:, :, 2], norm)
            
            # Calculate scaling factors
            gray_norm = (r_norm + g_norm + b_norm) / 3.0
            
            if gray_norm > 0:
                r_scale = gray_norm / (r_norm + 1e-6)
                g_scale = gray_norm / (g_norm + 1e-6)
                b_scale = gray_norm / (b_norm + 1e-6)
                
                # Limit adjustment to prevent overcorrection
                r_scale = np.clip(r_scale, 1/max_adjustment, max_adjustment)
                g_scale = np.clip(g_scale, 1/max_adjustment, max_adjustment)
                b_scale = np.clip(b_scale, 1/max_adjustment, max_adjustment)
                
                # Apply scaling
                img_float[:, :, 0] *= r_scale
                img_float[:, :, 1] *= g_scale
                img_float[:, :, 2] *= b_scale
                
            # Convert back to uint8
            result = np.clip(img_float * 255.0, 0, 255).astype(np.uint8)
            return result
            
        except Exception as e:
            print(f"Error in shades-of-gray white balance: {e}")
            return image
    
    def grey_edge_white_balance(self, image: np.ndarray) -> np.ndarray:
        """
        Apply grey-edge white balance algorithm.
        Uses derivatives to find illumination.
        """
        try:
            # Convert to float for processing
            img_float = image.astype(np.float32) / 255.0
            
            norm = self.parameters['grey_edge_norm']
            sigma = self.parameters['grey_edge_sigma']
            max_adjustment = self.parameters['grey_edge_max_adjustment']
            
            # Apply Gaussian smoothing if sigma > 0
            if sigma > 0:
                from scipy import ndimage
                img_smooth = ndimage.gaussian_filter(img_float, sigma)
            else:
                img_smooth = img_float
            
            # Calculate derivatives for each channel
            def calculate_derivatives(channel):
                dx = np.abs(np.gradient(channel, axis=1))
                dy = np.abs(np.gradient(channel, axis=0))
                return dx + dy
            
            r_deriv = calculate_derivatives(img_smooth[:, :, 0])
            g_deriv = calculate_derivatives(img_smooth[:, :, 1])
            b_deriv = calculate_derivatives(img_smooth[:, :, 2])
            
            # Calculate Minkowski norm of derivatives
            def minkowski_norm(channel, p):
                if p == np.inf:
                    return np.max(channel)
                else:
                    return np.power(np.mean(np.power(channel + 1e-6, p)), 1.0/p)
            
            r_norm = minkowski_norm(r_deriv, norm)
            g_norm = minkowski_norm(g_deriv, norm)
            b_norm = minkowski_norm(b_deriv, norm)
            
            # Calculate scaling factors
            gray_norm = (r_norm + g_norm + b_norm) / 3.0
            
            if gray_norm > 0:
                r_scale = gray_norm / (r_norm + 1e-6)
                g_scale = gray_norm / (g_norm + 1e-6)
                b_scale = gray_norm / (b_norm + 1e-6)
                
                # Limit adjustment to prevent overcorrection
                r_scale = np.clip(r_scale, 1/max_adjustment, max_adjustment)
                g_scale = np.clip(g_scale, 1/max_adjustment, max_adjustment)
                b_scale = np.clip(b_scale, 1/max_adjustment, max_adjustment)
                
                # Apply scaling
                img_float[:, :, 0] *= r_scale
                img_float[:, :, 1] *= g_scale
                img_float[:, :, 2] *= b_scale
                
            # Convert back to uint8
            result = np.clip(img_float * 255.0, 0, 255).astype(np.uint8)
            return result
            
        except Exception as e:
            print(f"Error in grey-edge white balance: {e}")
            # Fallback to gray-world if scipy is not available
            if "No module named 'scipy'" in str(e):
                print("Scipy not available, falling back to gray-world method")
                return self.gray_world_white_balance(image)
            return image
            
    def adaptive_histogram_equalization(self, image: np.ndarray) -> np.ndarray:
        """
        Apply Contrast Limited Adaptive Histogram Equalization (CLAHE).
        """
        try:
            # Convert to LAB color space for better results
            lab = cv2.cvtColor(image, cv2.COLOR_RGB2LAB)
            
            # Apply CLAHE to the L channel
            clip_limit = self.parameters['hist_eq_clip_limit']
            tile_grid_size = self.parameters['hist_eq_tile_grid_size']
            
            clahe = cv2.createCLAHE(
                clipLimit=clip_limit,
                tileGridSize=(tile_grid_size, tile_grid_size)
            )
            
            lab[:, :, 0] = clahe.apply(lab[:, :, 0])
            
            # Convert back to RGB
            result = cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)
            return result
            
        except Exception as e:
            print(f"Error in histogram equalization: {e}")
            return image
            
    def get_pipeline_description(self) -> List[Dict[str, str]]:
        """Get a description of the current processing pipeline"""
        pipeline_steps = []
        
        for operation in self.pipeline_order:
            if operation == 'white_balance' and self.parameters['white_balance_enabled']:
                method = self.parameters['white_balance_method']
                method_names = {
                    'gray_world': 'Gray-World',
                    'white_patch': 'White-Patch',
                    'shades_of_gray': 'Shades-of-Gray',
                    'grey_edge': 'Grey-Edge'
                }
                
                method_descriptions = {
                    'gray_world': 'Corrige la température couleur en supposant que la moyenne de la scène doit être gris neutre.',
                    'white_patch': 'Corrige la balance des blancs en supposant que les pixels les plus brillants doivent être blancs.',
                    'shades_of_gray': 'Généralisation de Gray-World utilisant la norme de Minkowski pour une meilleure robustesse.',
                    'grey_edge': 'Utilise les dérivées spatiales pour estimer l\'illumination de la scène.'
                }
                
                pipeline_steps.append({
                    'name': f'Balance des blancs ({method_names.get(method, method)})',
                    'description': method_descriptions.get(method, 'Méthode de balance des blancs'),
                    'parameters': self._format_wb_parameters()
                })
                
            elif operation == 'histogram_equalization' and self.parameters['hist_eq_enabled']:
                pipeline_steps.append({
                    'name': 'Égalisation adaptative d\'histogramme',
                    'description': f'Améliore le contraste local en utilisant CLAHE (Contrast Limited Adaptive Histogram Equalization). '
                                 f'Appliqué au canal de luminance dans l\'espace colorimétrique LAB.',
                    'parameters': f'Limite de coupure: {self.parameters["hist_eq_clip_limit"]}, '
                                f'Taille des tuiles: {self.parameters["hist_eq_tile_grid_size"]}x{self.parameters["hist_eq_tile_grid_size"]}'
                })
                
        if not pipeline_steps:
            pipeline_steps.append({
                'name': 'Aucun traitement',
                'description': 'Toutes les étapes de traitement sont désactivées.',
                'parameters': 'N/A'
            })
            
        return pipeline_steps
    
    def _format_wb_parameters(self) -> str:
        """Format white balance parameters for display"""
        method = self.parameters['white_balance_method']
        
        if method == 'gray_world':
            return f"Percentile: {self.parameters['gray_world_percentile']}%, Max ajustement: {self.parameters['gray_world_max_adjustment']}"
        elif method == 'white_patch':
            return f"Percentile: {self.parameters['white_patch_percentile']}%, Max ajustement: {self.parameters['white_patch_max_adjustment']}"
        elif method == 'shades_of_gray':
            return f"Norme: {self.parameters['shades_of_gray_norm']}, Percentile: {self.parameters['shades_of_gray_percentile']}%, Max ajustement: {self.parameters['shades_of_gray_max_adjustment']}"
        elif method == 'grey_edge':
            return f"Norme: {self.parameters['grey_edge_norm']}, Sigma: {self.parameters['grey_edge_sigma']}, Max ajustement: {self.parameters['grey_edge_max_adjustment']}"
        else:
            return ""
        
    def get_parameter_info(self) -> Dict[str, Dict[str, Any]]:
        """Get parameter information for UI generation"""
        return {
            # White balance method selection
            'white_balance_method': {
                'type': 'choice',
                'label': 'Méthode de balance des blancs',
                'description': 'Choisir la méthode de correction de la balance des blancs',
                'choices': [
                    ('gray_world', 'Gray-World'),
                    ('white_patch', 'White-Patch'),
                    ('shades_of_gray', 'Shades-of-Gray'),
                    ('grey_edge', 'Grey-Edge')
                ]
            },
            'white_balance_enabled': {
                'type': 'boolean',
                'label': 'Activer la balance des blancs',
                'description': 'Active ou désactive la correction de la balance des blancs'
            },
            
            # Gray-world parameters
            'gray_world_percentile': {
                'type': 'float',
                'label': 'Percentile Gray-World',
                'description': 'Percentile utilisé pour calculer les moyennes des canaux (plus robuste que la moyenne)',
                'min': 10,
                'max': 90,
                'step': 5,
                'visible_when': {'white_balance_method': 'gray_world'}
            },
            'gray_world_max_adjustment': {
                'type': 'float',
                'label': 'Facteur d\'ajustement max (Gray-World)',
                'description': 'Facteur maximum d\'échelle autorisé pour les canaux couleur',
                'min': 1.0,
                'max': 5.0,
                'step': 0.1,
                'visible_when': {'white_balance_method': 'gray_world'}
            },
            
            # White-patch parameters
            'white_patch_percentile': {
                'type': 'float',
                'label': 'Percentile White-Patch',
                'description': 'Percentile des pixels les plus brillants considérés comme blancs',
                'min': 90,
                'max': 99.9,
                'step': 0.5,
                'visible_when': {'white_balance_method': 'white_patch'}
            },
            'white_patch_max_adjustment': {
                'type': 'float',
                'label': 'Facteur d\'ajustement max (White-Patch)',
                'description': 'Facteur maximum d\'échelle autorisé pour les canaux couleur',
                'min': 1.0,
                'max': 5.0,
                'step': 0.1,
                'visible_when': {'white_balance_method': 'white_patch'}
            },
            
            # Shades-of-gray parameters
            'shades_of_gray_norm': {
                'type': 'int',
                'label': 'Norme Shades-of-Gray',
                'description': 'Ordre de la norme de Minkowski (1=moyenne, 2=euclidienne, inf=max)',
                'min': 1,
                'max': 10,
                'step': 1,
                'visible_when': {'white_balance_method': 'shades_of_gray'}
            },
            'shades_of_gray_percentile': {
                'type': 'float',
                'label': 'Percentile Shades-of-Gray',
                'description': 'Percentile utilisé si applicable',
                'min': 10,
                'max': 90,
                'step': 5,
                'visible_when': {'white_balance_method': 'shades_of_gray'}
            },
            'shades_of_gray_max_adjustment': {
                'type': 'float',
                'label': 'Facteur d\'ajustement max (Shades-of-Gray)',
                'description': 'Facteur maximum d\'échelle autorisé pour les canaux couleur',
                'min': 1.0,
                'max': 5.0,
                'step': 0.1,
                'visible_when': {'white_balance_method': 'shades_of_gray'}
            },
            
            # Grey-edge parameters
            'grey_edge_norm': {
                'type': 'int',
                'label': 'Norme Grey-Edge',
                'description': 'Ordre de la norme pour les dérivées (1=manhattan, 2=euclidienne)',
                'min': 1,
                'max': 10,
                'step': 1,
                'visible_when': {'white_balance_method': 'grey_edge'}
            },
            'grey_edge_sigma': {
                'type': 'float',
                'label': 'Sigma Grey-Edge',
                'description': 'Paramètre de lissage gaussien (0=pas de lissage)',
                'min': 0.0,
                'max': 3.0,
                'step': 0.1,
                'visible_when': {'white_balance_method': 'grey_edge'}
            },
            'grey_edge_max_adjustment': {
                'type': 'float',
                'label': 'Facteur d\'ajustement max (Grey-Edge)',
                'description': 'Facteur maximum d\'échelle autorisé pour les canaux couleur',
                'min': 1.0,
                'max': 5.0,
                'step': 0.1,
                'visible_when': {'white_balance_method': 'grey_edge'}
            },
            
            # Histogram equalization parameters
            'hist_eq_enabled': {
                'type': 'boolean',
                'label': 'Égalisation d\'histogramme',
                'description': 'Applique l\'égalisation adaptative d\'histogramme pour améliorer le contraste'
            },
            'hist_eq_clip_limit': {
                'type': 'float',
                'label': 'Limite de coupure CLAHE',
                'description': 'Seuil pour la limitation du contraste dans l\'algorithme CLAHE',
                'min': 1.0,
                'max': 10.0,
                'step': 0.5
            },
            'hist_eq_tile_grid_size': {
                'type': 'int',
                'label': 'Taille des tuiles CLAHE',
                'description': 'Taille des tuiles pour l\'égalisation adaptative d\'histogramme',
                'min': 4,
                'max': 16,
                'step': 2
            }
        }
