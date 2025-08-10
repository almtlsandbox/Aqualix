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
            # Gray-world white balance parameters
            'gray_world_enabled': True,
            'gray_world_percentile': 50,
            'gray_world_max_adjustment': 2.0,
            
            # Histogram equalization parameters
            'hist_eq_enabled': True,
            'hist_eq_clip_limit': 2.0,
            'hist_eq_tile_grid_size': 8,
        }
        
        # Processing pipeline order
        self.pipeline_order = [
            'gray_world_white_balance',
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
            if operation == 'gray_world_white_balance' and self.parameters['gray_world_enabled']:
                result = self.gray_world_white_balance(result)
            elif operation == 'histogram_equalization' and self.parameters['hist_eq_enabled']:
                result = self.adaptive_histogram_equalization(result)
                
        return result
        
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
            if operation == 'gray_world_white_balance' and self.parameters['gray_world_enabled']:
                pipeline_steps.append({
                    'name': 'Balance des blancs (Gray-World)',
                    'description': f'Ajuste la température de couleur en supposant que la moyenne de la scène doit être grise neutre. '
                                 f'Utilise le {self.parameters["gray_world_percentile"]}e percentile avec un ajustement maximum de '
                                 f'{self.parameters["gray_world_max_adjustment"]}x.',
                    'parameters': f'Percentile: {self.parameters["gray_world_percentile"]}, '
                                f'Ajustement max: {self.parameters["gray_world_max_adjustment"]}'
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
        
    def get_parameter_info(self) -> Dict[str, Dict[str, Any]]:
        """Get parameter information for UI generation"""
        return {
            'gray_world_enabled': {
                'type': 'boolean',
                'label': 'Balance des blancs (Gray-World)',
                'description': 'Applique l\'algorithme gray-world pour corriger la balance des blancs'
            },
            'gray_world_percentile': {
                'type': 'float',
                'label': 'Percentile Gray-World',
                'description': 'Percentile utilisé pour calculer les moyennes des canaux (plus robuste que la moyenne)',
                'min': 10,
                'max': 90,
                'step': 5
            },
            'gray_world_max_adjustment': {
                'type': 'float',
                'label': 'Facteur d\'ajustement max',
                'description': 'Facteur maximum d\'échelle autorisé pour les canaux couleur',
                'min': 1.0,
                'max': 5.0,
                'step': 0.1
            },
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
