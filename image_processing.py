"""
Image Processing Module
Contains image processing algorithms and pipeline management.
"""

import cv2
import numpy as np
from typing import Dict, Any, List, Tuple

def create_preview_image(image: np.ndarray, max_size: int = 1024) -> Tuple[np.ndarray, float]:
    """
    Create a subsampled image for preview if the original is too large.
    
    Args:
        image: Input image as numpy array
        max_size: Maximum dimension size for preview
        
    Returns:
        Tuple of (preview_image, scale_factor)
    """
    height, width = image.shape[:2]
    max_dimension = max(height, width)
    
    if max_dimension <= max_size:
        return image.copy(), 1.0
    
    scale_factor = max_size / max_dimension
    new_width = int(width * scale_factor)
    new_height = int(height * scale_factor)
    
    # Use INTER_AREA for downsampling (better quality)
    preview_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
    
    return preview_image, scale_factor

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
            
            # Lake Green Water white balance parameters
            'lake_green_reduction': 0.3,        # Strength of green channel reduction (0.0-1.0)
            'lake_magenta_strength': 0.15,      # Magenta compensation strength (0.0-0.5)
            'lake_gray_world_influence': 0.7,   # Influence of gray-world correction (0.0-1.0)
            
            # UDCP (Underwater Dark Channel Prior) parameters
            'udcp_enabled': True,
            'udcp_omega': 0.95,           # Amount of haze to keep (0.95 = remove 95% of haze)
            'udcp_t0': 0.1,               # Minimum transmission value
            'udcp_window_size': 15,       # Window size for dark channel calculation
            'udcp_guided_radius': 60,     # Radius for guided filter
            'udcp_guided_eps': 0.001,     # Regularization parameter for guided filter
            'udcp_enhance_contrast': 1.2, # Contrast enhancement factor
            
            # Histogram equalization parameters
            'hist_eq_enabled': True,
            'hist_eq_clip_limit': 2.0,
            'hist_eq_tile_grid_size': 8,
        }
        
        # Processing pipeline order
        self.pipeline_order = [
            'white_balance',
            'udcp',
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
            elif operation == 'udcp' and self.parameters['udcp_enabled']:
                result = self.underwater_dark_channel_prior(result)
            elif operation == 'histogram_equalization' and self.parameters['hist_eq_enabled']:
                result = self.adaptive_histogram_equalization(result)
                
        return result
    
    def process_image_for_preview(self, image: np.ndarray, max_size: int = 1024) -> Tuple[np.ndarray, np.ndarray, float]:
        """
        Process an image for preview, using subsampling for large images.
        
        Args:
            image: Input image
            max_size: Maximum dimension for preview
            
        Returns:
            Tuple of (original_preview, processed_preview, scale_factor)
        """
        # Create preview version of original image
        original_preview, scale_factor = create_preview_image(image, max_size)
        
        # Process the preview image
        processed_preview = original_preview.copy()
        
        for operation in self.pipeline_order:
            if operation == 'white_balance' and self.parameters['white_balance_enabled']:
                processed_preview = self.apply_white_balance(processed_preview)
            elif operation == 'udcp' and self.parameters['udcp_enabled']:
                processed_preview = self.underwater_dark_channel_prior(processed_preview)
            elif operation == 'histogram_equalization' and self.parameters['hist_eq_enabled']:
                processed_preview = self.adaptive_histogram_equalization(processed_preview)
                
        return original_preview, processed_preview, scale_factor
    
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
        elif method == 'lake_green_water':
            return self.lake_green_water_white_balance(image)
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
    
    def lake_green_water_white_balance(self, image: np.ndarray) -> np.ndarray:
        """
        Specialized white balance for green lake/freshwater environments.
        Combines targeted green reduction (magenta compensation) with Gray-World balancing.
        
        This method is designed specifically for underwater photography in lakes and
        freshwater environments where green algae and vegetation create a strong
        green color cast that standard methods struggle to correct.
        
        Returns:
            np.ndarray: White balanced image
        """
        try:
            # Get parameters
            green_reduction = self.parameters.get('lake_green_reduction', 0.3)
            magenta_strength = self.parameters.get('lake_magenta_strength', 0.15)
            gray_world_influence = self.parameters.get('lake_gray_world_influence', 0.7)
            
            # Convert to float
            img_float = image.astype(np.float32) / 255.0
            height, width = img_float.shape[:2]
            
            # Step 1: Targeted green reduction
            # Create magenta compensation by reducing green channel relative to red/blue
            b_channel, g_channel, r_channel = cv2.split(img_float)
            
            # Calculate green dominance relative to red and blue
            rg_ratio = np.divide(r_channel, g_channel + 1e-6)
            bg_ratio = np.divide(b_channel, g_channel + 1e-6)
            
            # Create adaptive green reduction mask
            # More reduction where green is dominant (low red/blue ratios)
            green_dominance = 1.0 / (1.0 + rg_ratio + bg_ratio)
            green_reduction_mask = green_dominance * green_reduction
            
            # Apply adaptive green reduction
            g_channel_corrected = g_channel * (1.0 - green_reduction_mask)
            
            # Step 2: Magenta compensation
            # Boost red and blue channels proportionally to counteract green cast
            magenta_boost = magenta_strength * green_dominance
            r_channel_boosted = r_channel * (1.0 + magenta_boost)
            b_channel_boosted = b_channel * (1.0 + magenta_boost)
            
            # Reconstruct image with corrections
            img_corrected = cv2.merge([b_channel_boosted, g_channel_corrected, r_channel_boosted])
            
            # Step 3: Apply Gray-World balancing to the corrected image
            # Calculate mean values for each channel
            r_mean = np.mean(img_corrected[:, :, 2])
            g_mean = np.mean(img_corrected[:, :, 1])
            b_mean = np.mean(img_corrected[:, :, 0])
            
            # Calculate overall mean
            gray_mean = (r_mean + g_mean + b_mean) / 3.0
            
            if gray_mean > 0:
                # Calculate Gray-World scaling factors
                r_scale_gw = gray_mean / (r_mean + 1e-6)
                g_scale_gw = gray_mean / (g_mean + 1e-6)
                b_scale_gw = gray_mean / (b_mean + 1e-6)
                
                # Limit Gray-World adjustment to prevent overcorrection
                max_gw_adjustment = 2.0
                r_scale_gw = np.clip(r_scale_gw, 1/max_gw_adjustment, max_gw_adjustment)
                g_scale_gw = np.clip(g_scale_gw, 1/max_gw_adjustment, max_gw_adjustment)
                b_scale_gw = np.clip(b_scale_gw, 1/max_gw_adjustment, max_gw_adjustment)
                
                # Blend Gray-World correction with current state
                influence = gray_world_influence
                r_scale_final = 1.0 + influence * (r_scale_gw - 1.0)
                g_scale_final = 1.0 + influence * (g_scale_gw - 1.0)
                b_scale_final = 1.0 + influence * (b_scale_gw - 1.0)
                
                # Apply final scaling
                img_corrected[:, :, 2] *= r_scale_final
                img_corrected[:, :, 1] *= g_scale_final
                img_corrected[:, :, 0] *= b_scale_final
            
            # Convert back to uint8
            result = np.clip(img_corrected * 255.0, 0, 255).astype(np.uint8)
            return result
            
        except Exception as e:
            print(f"Error in lake green water white balance: {e}")
            # Fallback to standard gray-world method
            return self.gray_world_white_balance(image)
            
    def underwater_dark_channel_prior(self, image: np.ndarray) -> np.ndarray:
        """
        Apply Underwater Dark Channel Prior (UDCP) for underwater image enhancement.
        
        This method removes haze and improves visibility in underwater images by:
        1. Computing the dark channel of the image
        2. Estimating atmospheric light (background light in water)
        3. Estimating transmission map
        4. Recovering the scene radiance (dehazed image)
        """
        try:
            # Convert to float for processing
            img_float = image.astype(np.float32) / 255.0
            
            # Get parameters
            omega = self.parameters['udcp_omega']
            t0 = self.parameters['udcp_t0']
            window_size = self.parameters['udcp_window_size']
            guided_radius = self.parameters['udcp_guided_radius']
            guided_eps = self.parameters['udcp_guided_eps']
            enhance_contrast = self.parameters['udcp_enhance_contrast']
            
            # Step 1: Compute dark channel
            dark_channel = self._compute_dark_channel(img_float, window_size)
            
            # Step 2: Estimate atmospheric light (background light)
            atmospheric_light = self._estimate_atmospheric_light(img_float, dark_channel)
            
            # Step 3: Estimate transmission map
            transmission = self._estimate_transmission(img_float, atmospheric_light, omega, window_size)
            
            # Step 4: Refine transmission using guided filter
            transmission_refined = self._guided_filter(img_float[:, :, 0], transmission, guided_radius, guided_eps)
            
            # Ensure minimum transmission
            transmission_refined = np.maximum(transmission_refined, t0)
            
            # Step 5: Recover scene radiance
            recovered = np.zeros_like(img_float)
            for i in range(3):  # For each color channel
                recovered[:, :, i] = (img_float[:, :, i] - atmospheric_light[i]) / transmission_refined + atmospheric_light[i]
            
            # Clip values to valid range
            recovered = np.clip(recovered, 0, 1)
            
            # Optional: Enhance contrast
            if enhance_contrast != 1.0:
                recovered = self._enhance_contrast(recovered, enhance_contrast)
            
            # Convert back to uint8
            result = (recovered * 255).astype(np.uint8)
            
            return result
            
        except Exception as e:
            print(f"Error in UDCP processing: {e}")
            return image
    
    def _compute_dark_channel(self, image: np.ndarray, window_size: int) -> np.ndarray:
        """Compute the dark channel of the image"""
        # Take minimum across color channels
        min_channel = np.min(image, axis=2)
        
        # Apply minimum filter with specified window size
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (window_size, window_size))
        dark_channel = cv2.erode(min_channel, kernel)
        
        return dark_channel
    
    def _estimate_atmospheric_light(self, image: np.ndarray, dark_channel: np.ndarray) -> np.ndarray:
        """Estimate atmospheric light from the brightest pixels in the dark channel"""
        # Get the top 0.1% brightest pixels in dark channel
        num_pixels = dark_channel.size
        num_brightest = max(int(num_pixels * 0.001), 1)
        
        # Find indices of brightest pixels
        flat_dark = dark_channel.flatten()
        indices = np.argpartition(flat_dark, -num_brightest)[-num_brightest:]
        
        # Get atmospheric light as the mean of these brightest pixels
        atmospheric_light = np.zeros(3)
        flat_image = image.reshape(-1, 3)
        
        for i in range(3):
            atmospheric_light[i] = np.mean(flat_image[indices, i])
        
        return atmospheric_light
    
    def _estimate_transmission(self, image: np.ndarray, atmospheric_light: np.ndarray, omega: float, window_size: int) -> np.ndarray:
        """Estimate transmission map"""
        # Normalize by atmospheric light
        normalized = np.zeros_like(image)
        for i in range(3):
            normalized[:, :, i] = image[:, :, i] / max(atmospheric_light[i], 1e-6)
        
        # Compute dark channel of normalized image
        transmission = 1 - omega * self._compute_dark_channel(normalized, window_size)
        
        return transmission
    
    def _guided_filter(self, guide: np.ndarray, input_img: np.ndarray, radius: int, eps: float) -> np.ndarray:
        """Apply guided filter to refine the transmission map"""
        try:
            # Convert to float32 if needed
            I = guide.astype(np.float32)
            p = input_img.astype(np.float32)
            
            # Box filter
            kernel = np.ones((2*radius+1, 2*radius+1), np.float32) / ((2*radius+1)**2)
            
            mean_I = cv2.filter2D(I, -1, kernel)
            mean_p = cv2.filter2D(p, -1, kernel)
            corr_Ip = cv2.filter2D(I * p, -1, kernel)
            corr_II = cv2.filter2D(I * I, -1, kernel)
            
            cov_Ip = corr_Ip - mean_I * mean_p
            var_I = corr_II - mean_I * mean_I
            
            a = cov_Ip / (var_I + eps)
            b = mean_p - a * mean_I
            
            mean_a = cv2.filter2D(a, -1, kernel)
            mean_b = cv2.filter2D(b, -1, kernel)
            
            q = mean_a * I + mean_b
            
            return q
            
        except Exception as e:
            print(f"Error in guided filter: {e}")
            return input_img
    
    def _enhance_contrast(self, image: np.ndarray, factor: float) -> np.ndarray:
        """Enhance contrast of the image"""
        # Simple contrast enhancement: (image - 0.5) * factor + 0.5
        enhanced = (image - 0.5) * factor + 0.5
        return np.clip(enhanced, 0, 1)
            
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
                
            elif operation == 'udcp' and self.parameters['udcp_enabled']:
                pipeline_steps.append({
                    'name': 'UDCP (Underwater Dark Channel Prior)',
                    'description': 'Supprime le voile et améliore la visibilité des images sous-marines en utilisant '
                                 'l\'hypothèse du canal sombre. Estime et retire les effets de diffusion et d\'absorption de la lumière dans l\'eau.',
                    'parameters': f'Omega: {self.parameters["udcp_omega"]:.2f}, '
                                f'Transmission min: {self.parameters["udcp_t0"]:.2f}, '
                                f'Taille fenêtre: {self.parameters["udcp_window_size"]}, '
                                f'Rayon guidé: {self.parameters["udcp_guided_radius"]}, '
                                f'Contraste: {self.parameters["udcp_enhance_contrast"]:.1f}'
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
        elif method == 'lake_green_water':
            return f"Réduction vert: {self.parameters['lake_green_reduction']:.2f}, Magenta: {self.parameters['lake_magenta_strength']:.2f}, Gray-World: {self.parameters['lake_gray_world_influence']:.2f}"
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
                    ('grey_edge', 'Grey-Edge'),
                    ('lake_green_water', 'Eau Verte (Lac)')
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
            
            # Lake Green Water white balance parameters
            'lake_green_reduction': {
                'type': 'float',
                'label': 'Réduction du vert',
                'description': 'Intensité de la réduction du canal vert (0.0 = aucune, 1.0 = maximum)',
                'min': 0.0,
                'max': 1.0,
                'step': 0.05,
                'visible_when': {'white_balance_method': 'lake_green_water'}
            },
            'lake_magenta_strength': {
                'type': 'float',
                'label': 'Force magenta',
                'description': 'Intensité de la compensation magenta (rouge+bleu vs vert)',
                'min': 0.0,
                'max': 0.5,
                'step': 0.02,
                'visible_when': {'white_balance_method': 'lake_green_water'}
            },
            'lake_gray_world_influence': {
                'type': 'float',
                'label': 'Influence Gray-World',
                'description': 'Influence de la correction Gray-World finale (0.0 = aucune, 1.0 = maximum)',
                'min': 0.0,
                'max': 1.0,
                'step': 0.1,
                'visible_when': {'white_balance_method': 'lake_green_water'}
            },
            
            # UDCP (Underwater Dark Channel Prior) parameters
            'udcp_enabled': {
                'type': 'boolean',
                'label': 'UDCP (Underwater Dark Channel Prior)',
                'description': 'Active l\'amélioration des images sous-marines par suppression du voile'
            },
            'udcp_omega': {
                'type': 'float',
                'label': 'Omega (Conservation du voile)',
                'description': 'Fraction du voile à conserver (0.95 = supprime 95% du voile)',
                'min': 0.1,
                'max': 1.0,
                'step': 0.05
            },
            'udcp_t0': {
                'type': 'float',
                'label': 'Transmission minimale',
                'description': 'Valeur minimale de transmission pour éviter les artefacts',
                'min': 0.01,
                'max': 0.5,
                'step': 0.01
            },
            'udcp_window_size': {
                'type': 'int',
                'label': 'Taille de fenêtre',
                'description': 'Taille de la fenêtre pour le calcul du canal sombre',
                'min': 3,
                'max': 31,
                'step': 2
            },
            'udcp_guided_radius': {
                'type': 'int',
                'label': 'Rayon du filtre guidé',
                'description': 'Rayon pour le filtrage guidé de la carte de transmission',
                'min': 10,
                'max': 100,
                'step': 10
            },
            'udcp_guided_eps': {
                'type': 'float',
                'label': 'Epsilon du filtre guidé',
                'description': 'Paramètre de régularisation pour le filtre guidé',
                'min': 0.0001,
                'max': 0.01,
                'step': 0.0001
            },
            'udcp_enhance_contrast': {
                'type': 'float',
                'label': 'Amélioration du contraste',
                'description': 'Facteur d\'amélioration du contraste final',
                'min': 0.5,
                'max': 2.0,
                'step': 0.1
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
