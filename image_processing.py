"""
Image Processing Module
Contains image processing algorithms and pipeline management.
"""

import cv2
import numpy as np
from typing import Dict, Any, List, Tuple
from localization import t

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
            
            # Beer-Lambert correction parameters
            'beer_lambert_enabled': True,
            'beer_lambert_depth_factor': 0.1,      # Depth attenuation factor (0.01-1.0)
            'beer_lambert_red_coeff': 0.6,         # Red attenuation coefficient (0.1-2.0)
            'beer_lambert_green_coeff': 0.3,       # Green attenuation coefficient (0.1-1.5)
            'beer_lambert_blue_coeff': 0.1,        # Blue attenuation coefficient (0.05-1.0)
            'beer_lambert_enhance_factor': 1.5,    # Enhancement factor (1.0-3.0)
            
            # Color Rebalancing (3x3 matrix) parameters
            'color_rebalance_enabled': True,
            'color_rebalance_rr': 1.0,              # Red to Red coefficient (0.5-2.0)
            'color_rebalance_rg': 0.0,              # Red to Green coefficient (-0.5-0.5)
            'color_rebalance_rb': 0.0,              # Red to Blue coefficient (-0.5-0.5)
            'color_rebalance_gr': 0.0,              # Green to Red coefficient (-0.5-0.5)
            'color_rebalance_gg': 1.0,              # Green to Green coefficient (0.5-2.0)
            'color_rebalance_gb': 0.0,              # Green to Blue coefficient (-0.5-0.5)
            'color_rebalance_br': 0.0,              # Blue to Red coefficient (-0.5-0.5)
            'color_rebalance_bg': 0.0,              # Blue to Green coefficient (-0.5-0.5)
            'color_rebalance_bb': 1.0,              # Blue to Blue coefficient (0.5-2.0)
            'color_rebalance_saturation_limit': 1.0, # Saturation clamp to avoid magenta (0.3-1.0) - 1.0 = no limit
            'color_rebalance_preserve_luminance': False, # Preserve luminance during rebalancing - disabled by default
            
            # Histogram equalization parameters
            'hist_eq_enabled': True,
            'hist_eq_clip_limit': 2.0,
            'hist_eq_tile_grid_size': 8,
        }
        
        # Processing pipeline order
        self.pipeline_order = [
            'white_balance',
            'udcp',
            'beer_lambert',
            'color_rebalance',
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
        
    def get_default_parameters(self) -> Dict[str, Any]:
        """Get default parameters (copy of initial values)"""
        # Return the default parameters defined at class level
        return {
            # White balance parameters
            'white_balance_enabled': True,
            'white_balance_method': 'gray_world',
            
            # Gray-world parameters
            'gray_world_threshold': 0.3,
            'gray_world_max_adjustment': 2.5,
            
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
            
            # Lake green water parameters
            'lake_green_reduction': 0.7,
            'lake_magenta_strength': 0.2,
            'lake_gray_world_influence': 0.8,
            
            # UDCP parameters
            'udcp_enabled': True,
            'udcp_omega': 0.95,
            'udcp_t0': 0.1,
            'udcp_window_size': 15,
            'udcp_guided_radius': 60,
            'udcp_guided_epsilon': 0.001,
            'udcp_enhance_factor': 1.0,
            
            # Beer-Lambert correction parameters
            'beer_lambert_enabled': True,
            'beer_lambert_depth_factor': 10.0,
            'beer_lambert_red_coeff': 0.6,
            'beer_lambert_green_coeff': 0.3,
            'beer_lambert_blue_coeff': 0.1,
            'beer_lambert_enhance_factor': 1.5,
            
            # Color Rebalancing parameters
            'color_rebalance_enabled': True,
            'color_rebalance_rr': 1.0,
            'color_rebalance_rg': 0.0,
            'color_rebalance_rb': 0.0,
            'color_rebalance_gr': 0.0,
            'color_rebalance_gg': 1.0,
            'color_rebalance_gb': 0.0,
            'color_rebalance_br': 0.0,
            'color_rebalance_bg': 0.0,
            'color_rebalance_bb': 1.0,
            'color_rebalance_saturation_limit': 1.0,
            'color_rebalance_preserve_luminance': False,
            
            # Histogram equalization parameters
            'hist_eq_enabled': True,
            'hist_eq_clip_limit': 3.0,
            'hist_eq_tile_grid_size': 8,
            'hist_eq_tile_grid_adaptive': True
        }
    
    def reset_step_parameters(self, step_key: str):
        """Reset parameters for a specific processing step to defaults"""
        defaults = self.get_default_parameters()
        
        # Define parameter prefixes for each step
        step_prefixes = {
            'white_balance': ['white_balance_', 'gray_world_', 'white_patch_', 'shades_of_gray_', 'grey_edge_', 'lake_'],
            'udcp': ['udcp_'],
            'beer_lambert': ['beer_lambert_'],
            'color_rebalance': ['color_rebalance_'],
            'histogram_equalization': ['hist_eq_']
        }
        
        if step_key not in step_prefixes:
            return
            
        # Reset parameters that match the step prefixes
        for prefix in step_prefixes[step_key]:
            for param_name, default_value in defaults.items():
                if param_name.startswith(prefix):
                    self.set_parameter(param_name, default_value)
        
    def process_image(self, image: np.ndarray) -> np.ndarray:
        """Process an image through the complete pipeline"""
        result = image.copy()
        
        for operation in self.pipeline_order:
            if operation == 'white_balance' and self.parameters['white_balance_enabled']:
                result = self.apply_white_balance(result)
            elif operation == 'udcp' and self.parameters['udcp_enabled']:
                result = self.underwater_dark_channel_prior(result)
            elif operation == 'beer_lambert' and self.parameters['beer_lambert_enabled']:
                result = self.beer_lambert_correction(result)
            elif operation == 'color_rebalance' and self.parameters['color_rebalance_enabled']:
                result = self.color_rebalance(result)
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
            elif operation == 'beer_lambert' and self.parameters['beer_lambert_enabled']:
                processed_preview = self.beer_lambert_correction(processed_preview)
            elif operation == 'color_rebalance' and self.parameters['color_rebalance_enabled']:
                processed_preview = self.color_rebalance(processed_preview)
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
    
    def beer_lambert_correction(self, image: np.ndarray) -> np.ndarray:
        """
        Apply Beer-Lambert law correction for underwater images.
        
        Beer-Lambert law describes the attenuation of light through water:
        I = I0 * exp(-k * d)
        where I0 is incident light, k is attenuation coefficient, d is distance
        
        This correction compensates for depth-dependent color loss in underwater photography.
        
        Returns:
            np.ndarray: Color-corrected image
        """
        try:
            # Get parameters
            depth_factor = self.parameters['beer_lambert_depth_factor']
            red_coeff = self.parameters['beer_lambert_red_coeff']
            green_coeff = self.parameters['beer_lambert_green_coeff']
            blue_coeff = self.parameters['beer_lambert_blue_coeff']
            enhance_factor = self.parameters['beer_lambert_enhance_factor']
            
            # Convert to float
            img_float = image.astype(np.float32) / 255.0
            height, width = img_float.shape[:2]
            
            # Create depth map estimation based on image brightness
            # Darker regions are assumed to be further/deeper
            gray = cv2.cvtColor(img_float, cv2.COLOR_BGR2GRAY)
            
            # Invert brightness to create depth approximation
            # Brighter areas = shallower, darker areas = deeper
            depth_map = 1.0 - gray
            depth_map = depth_map * depth_factor
            
            # Apply Beer-Lambert correction for each channel
            b_channel, g_channel, r_channel = cv2.split(img_float)
            
            # Calculate compensation factors based on attenuation coefficients
            # Higher attenuation coefficient = more correction needed
            r_compensation = np.exp(red_coeff * depth_map)
            g_compensation = np.exp(green_coeff * depth_map)
            b_compensation = np.exp(blue_coeff * depth_map)
            
            # Apply compensation (inverse of Beer-Lambert attenuation)
            r_corrected = r_channel * r_compensation
            g_corrected = g_channel * g_compensation
            b_corrected = b_channel * b_compensation
            
            # Combine channels
            corrected_image = cv2.merge([b_corrected, g_corrected, r_corrected])
            
            # Apply enhancement factor
            if enhance_factor != 1.0:
                corrected_image = corrected_image * enhance_factor
            
            # Normalize to prevent oversaturation while preserving dynamic range
            # Adaptive normalization per channel
            for i in range(3):
                channel = corrected_image[:, :, i]
                max_val = np.percentile(channel, 99)  # Use 99th percentile to avoid outliers
                if max_val > 1.0:
                    corrected_image[:, :, i] = channel / max_val
            
            # Convert back to uint8
            result = np.clip(corrected_image * 255.0, 0, 255).astype(np.uint8)
            return result
            
        except Exception as e:
            print(f"Error in Beer-Lambert correction: {e}")
            return image
    
    def color_rebalance(self, image: np.ndarray) -> np.ndarray:
        """
        Apply color rebalancing using a 3x3 transformation matrix with saturation guards.
        
        This correction allows fine-tuning of color balance after other corrections,
        with built-in protection against oversaturation (particularly magenta artifacts).
        
        Args:
            image: Input image as numpy array (RGB)
            
        Returns:
            np.ndarray: Color-rebalanced image with saturation protection
        """
        try:
            # Get transformation matrix parameters
            rr = self.parameters['color_rebalance_rr']
            rg = self.parameters['color_rebalance_rg'] 
            rb = self.parameters['color_rebalance_rb']
            gr = self.parameters['color_rebalance_gr']
            gg = self.parameters['color_rebalance_gg']
            gb = self.parameters['color_rebalance_gb']
            br = self.parameters['color_rebalance_br']
            bg = self.parameters['color_rebalance_bg']
            bb = self.parameters['color_rebalance_bb']
            saturation_limit = self.parameters['color_rebalance_saturation_limit']
            preserve_luminance = self.parameters['color_rebalance_preserve_luminance']
            
            # Convert to float [0, 1]
            img_float = image.astype(np.float32) / 255.0
            
            # Store original luminance if preservation is enabled
            original_luminance = None
            if preserve_luminance:
                # Calculate luminance using standard weights
                original_luminance = 0.299 * img_float[:, :, 0] + 0.587 * img_float[:, :, 1] + 0.114 * img_float[:, :, 2]
            
            # Create 3x3 transformation matrix
            transform_matrix = np.array([
                [rr, rg, rb],  # Red output coefficients
                [gr, gg, gb],  # Green output coefficients  
                [br, bg, bb]   # Blue output coefficients
            ], dtype=np.float32)
            
            # Reshape image for matrix multiplication
            height, width, channels = img_float.shape
            img_reshaped = img_float.reshape(-1, 3).T  # (3, H*W)
            
            # Apply transformation matrix
            transformed = np.dot(transform_matrix, img_reshaped)
            
            # Reshape back to image format
            result = transformed.T.reshape(height, width, 3)
            
            # Apply saturation limiting to prevent magenta artifacts
            if saturation_limit < 1.0:
                # Convert to HSV for saturation control
                result_hsv = cv2.cvtColor(np.clip(result, 0, 1), cv2.COLOR_RGB2HSV)
                
                # Limit saturation channel
                result_hsv[:, :, 1] = np.clip(result_hsv[:, :, 1], 0, saturation_limit)
                
                # Convert back to RGB
                result = cv2.cvtColor(result_hsv, cv2.COLOR_HSV2RGB)
            
            # Restore original luminance if requested
            if preserve_luminance and original_luminance is not None:
                # Calculate new luminance
                new_luminance = 0.299 * result[:, :, 0] + 0.587 * result[:, :, 1] + 0.114 * result[:, :, 2]
                
                # Avoid division by zero
                luminance_ratio = np.divide(original_luminance, new_luminance, 
                                          out=np.ones_like(original_luminance), 
                                          where=new_luminance > 1e-6)  # More robust threshold
                
                # Apply luminance correction to each channel
                for i in range(3):
                    result[:, :, i] = result[:, :, i] * luminance_ratio
            
            # Final clipping and conversion
            result = np.clip(result, 0, 1)
            return (result * 255.0).astype(np.uint8)
            
        except Exception as e:
            print(f"Error in color rebalancing: {e}")
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
                    'grey_edge': 'Grey-Edge',
                    'lake_green_water': t('white_balance_lake_green_water')
                }
                
                method_descriptions = {
                    'gray_world': t('operation_gw_desc'),
                    'white_patch': t('operation_wp_desc'),
                    'shades_of_gray': t('operation_sog_desc'),
                    'grey_edge': t('operation_ge_desc'),
                    'lake_green_water': t('operation_lgw_desc')
                }
                
                pipeline_steps.append({
                    'name': f'{t("white_balance_step_title")} ({method_names.get(method, method)})',
                    'description': method_descriptions.get(method, t('white_balance_step_desc')),
                    'parameters': self._format_wb_parameters()
                })
                
            elif operation == 'udcp' and self.parameters['udcp_enabled']:
                pipeline_steps.append({
                    'name': t('udcp_step_title'),
                    'description': t('operation_udcp_desc'),
                    'parameters': f'Omega: {self.parameters["udcp_omega"]:.2f}, '
                                f'Transmission min: {self.parameters["udcp_t0"]:.2f}, '
                                f'Taille fenêtre: {self.parameters["udcp_window_size"]}, '
                                f'Rayon guidé: {self.parameters["udcp_guided_radius"]}, '
                                f'Contraste: {self.parameters["udcp_enhance_contrast"]:.1f}'
                })
                
            elif operation == 'beer_lambert' and self.parameters['beer_lambert_enabled']:
                pipeline_steps.append({
                    'name': t('beer_lambert_step_title'),
                    'description': t('operation_beer_lambert_desc'),
                    'parameters': f'Facteur profondeur: {self.parameters["beer_lambert_depth_factor"]:.2f}, '
                                f'Coeff. rouge: {self.parameters["beer_lambert_red_coeff"]:.2f}, '
                                f'Coeff. vert: {self.parameters["beer_lambert_green_coeff"]:.2f}, '
                                f'Coeff. bleu: {self.parameters["beer_lambert_blue_coeff"]:.2f}, '
                                f'Enhancement: {self.parameters["beer_lambert_enhance_factor"]:.1f}'
                })
                
            elif operation == 'color_rebalance' and self.parameters['color_rebalance_enabled']:
                # Format matrix diagonal (main color channels)
                matrix_diag = f'R:{self.parameters["color_rebalance_rr"]:.2f}, ' \
                             f'G:{self.parameters["color_rebalance_gg"]:.2f}, ' \
                             f'B:{self.parameters["color_rebalance_bb"]:.2f}'
                
                # Show saturation limit
                sat_limit = f'Sat.Limite: {self.parameters["color_rebalance_saturation_limit"]:.2f}'
                
                pipeline_steps.append({
                    'name': t('color_rebalance_step_title'),
                    'description': t('operation_color_rebalance_desc'),
                    'parameters': f'{matrix_diag}, {sat_limit}'
                })
                
            elif operation == 'histogram_equalization' and self.parameters['hist_eq_enabled']:
                pipeline_steps.append({
                    'name': t('histogram_equalization_step_title'),
                    'description': t('operation_he_desc'),
                    'parameters': f'Limite de coupure: {self.parameters["hist_eq_clip_limit"]}, '
                                f'Taille des tuiles: {self.parameters["hist_eq_tile_grid_size"]}x{self.parameters["hist_eq_tile_grid_size"]}'
                })
                
        if not pipeline_steps:
            pipeline_steps.append({
                'name': t('no_operations'),
                'description': t('no_operations_desc'),
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
                'label': t('param_white_balance_method_label'),
                'description': t('param_white_balance_method_desc'),
                'choices': [
                    ('gray_world', t('method_gray_world')),
                    ('white_patch', t('method_white_patch')),
                    ('shades_of_gray', t('method_shades_of_gray')),
                    ('grey_edge', t('method_grey_edge')),
                    ('lake_green_water', t('method_lake_green_water'))
                ]
            },
            'white_balance_enabled': {
                'type': 'boolean',
                'label': t('param_white_balance_enabled_label'),
                'description': t('param_white_balance_enabled_desc')
            },
            
            # Gray-world parameters
            'gray_world_percentile': {
                'type': 'float',
                'label': t('param_gray_world_percentile_label'),
                'description': t('param_gray_world_percentile_desc'),
                'min': 10,
                'max': 90,
                'step': 5,
                'visible_when': {'white_balance_method': 'gray_world'}
            },
            'gray_world_max_adjustment': {
                'type': 'float',
                'label': t('param_gray_world_max_adjustment_label'),
                'description': t('param_gray_world_max_adjustment_desc'),
                'min': 1.0,
                'max': 5.0,
                'step': 0.1,
                'visible_when': {'white_balance_method': 'gray_world'}
            },
            
            # White-patch parameters
            'white_patch_percentile': {
                'type': 'float',
                'label': t('param_white_patch_percentile_label'),
                'description': t('param_white_patch_percentile_desc'),
                'min': 90,
                'max': 99.9,
                'step': 0.5,
                'visible_when': {'white_balance_method': 'white_patch'}
            },
            'white_patch_max_adjustment': {
                'type': 'float',
                'label': t('param_white_patch_max_adjustment_label'),
                'description': t('param_white_patch_max_adjustment_desc'),
                'min': 1.0,
                'max': 5.0,
                'step': 0.1,
                'visible_when': {'white_balance_method': 'white_patch'}
            },
            
            # Shades-of-gray parameters
            'shades_of_gray_norm': {
                'type': 'int',
                'label': t('param_shades_of_gray_norm_label'),
                'description': t('param_shades_of_gray_norm_desc'),
                'min': 1,
                'max': 10,
                'step': 1,
                'visible_when': {'white_balance_method': 'shades_of_gray'}
            },
            'shades_of_gray_percentile': {
                'type': 'float',
                'label': t('param_shades_of_gray_percentile_label'),
                'description': t('param_shades_of_gray_percentile_desc'),
                'min': 10,
                'max': 90,
                'step': 5,
                'visible_when': {'white_balance_method': 'shades_of_gray'}
            },
            'shades_of_gray_max_adjustment': {
                'type': 'float',
                'label': t('param_shades_of_gray_max_adjustment_label'),
                'description': t('param_shades_of_gray_max_adjustment_desc'),
                'min': 1.0,
                'max': 5.0,
                'step': 0.1,
                'visible_when': {'white_balance_method': 'shades_of_gray'}
            },
            
            # Grey-edge parameters
            'grey_edge_norm': {
                'type': 'int',
                'label': t('param_grey_edge_norm_label'),
                'description': t('param_grey_edge_norm_desc'),
                'min': 1,
                'max': 10,
                'step': 1,
                'visible_when': {'white_balance_method': 'grey_edge'}
            },
            'grey_edge_sigma': {
                'type': 'float',
                'label': t('param_grey_edge_sigma_label'),
                'description': t('param_grey_edge_sigma_desc'),
                'min': 0.0,
                'max': 3.0,
                'step': 0.1,
                'visible_when': {'white_balance_method': 'grey_edge'}
            },
            'grey_edge_max_adjustment': {
                'type': 'float',
                'label': t('param_grey_edge_max_adjustment_label'),
                'description': t('param_grey_edge_max_adjustment_desc'),
                'min': 1.0,
                'max': 5.0,
                'step': 0.1,
                'visible_when': {'white_balance_method': 'grey_edge'}
            },
            
            # Lake Green Water white balance parameters
            'lake_green_reduction': {
                'type': 'float',
                'label': t('param_lake_green_reduction_label'),
                'description': t('param_lake_green_reduction_desc'),
                'min': 0.0,
                'max': 1.0,
                'step': 0.05,
                'visible_when': {'white_balance_method': 'lake_green_water'}
            },
            'lake_magenta_strength': {
                'type': 'float',
                'label': t('param_lake_magenta_strength_label'),
                'description': t('param_lake_magenta_strength_desc'),
                'min': 0.0,
                'max': 0.5,
                'step': 0.02,
                'visible_when': {'white_balance_method': 'lake_green_water'}
            },
            'lake_gray_world_influence': {
                'type': 'float',
                'label': t('param_lake_gray_world_influence_label'),
                'description': t('param_lake_gray_world_influence_desc'),
                'min': 0.0,
                'max': 1.0,
                'step': 0.1,
                'visible_when': {'white_balance_method': 'lake_green_water'}
            },
            
            # UDCP (Underwater Dark Channel Prior) parameters
            'udcp_enabled': {
                'type': 'boolean',
                'label': t('param_udcp_enabled_label'),
                'description': t('param_udcp_enabled_desc')
            },
            'udcp_omega': {
                'type': 'float',
                'label': t('param_udcp_omega_label'),
                'description': t('param_udcp_omega_desc'),
                'min': 0.1,
                'max': 1.0,
                'step': 0.05
            },
            'udcp_t0': {
                'type': 'float',
                'label': t('param_udcp_t0_label'),
                'description': t('param_udcp_t0_desc'),
                'min': 0.01,
                'max': 0.5,
                'step': 0.01
            },
            'udcp_window_size': {
                'type': 'int',
                'label': t('param_udcp_window_size_label'),
                'description': t('param_udcp_window_size_desc'),
                'min': 3,
                'max': 31,
                'step': 2
            },
            'udcp_guided_radius': {
                'type': 'int',
                'label': t('param_udcp_guided_radius_label'),
                'description': t('param_udcp_guided_radius_desc'),
                'min': 10,
                'max': 100,
                'step': 10
            },
            'udcp_guided_eps': {
                'type': 'float',
                'label': t('param_udcp_guided_eps_label'),
                'description': t('param_udcp_guided_eps_desc'),
                'min': 0.0001,
                'max': 0.01,
                'step': 0.0001
            },
            'udcp_enhance_contrast': {
                'type': 'float',
                'label': t('param_udcp_enhance_contrast_label'),
                'description': t('param_udcp_enhance_contrast_desc'),
                'min': 0.5,
                'max': 2.0,
                'step': 0.1
            },
            
            # Beer-Lambert law correction parameters
            'beer_lambert_enabled': {
                'type': 'boolean',
                'label': t('param_beer_lambert_enabled_label'),
                'description': t('param_beer_lambert_enabled_desc')
            },
            'beer_lambert_depth_factor': {
                'type': 'float',
                'label': t('param_beer_lambert_depth_factor_label'),
                'description': t('param_beer_lambert_depth_factor_desc'),
                'min': 0.01,
                'max': 1.0,
                'step': 0.01
            },
            'beer_lambert_red_coeff': {
                'type': 'float',
                'label': t('param_beer_lambert_red_coeff_label'),
                'description': t('param_beer_lambert_red_coeff_desc'),
                'min': 0.1,
                'max': 2.0,
                'step': 0.1
            },
            'beer_lambert_green_coeff': {
                'type': 'float',
                'label': t('param_beer_lambert_green_coeff_label'),
                'description': t('param_beer_lambert_green_coeff_desc'),
                'min': 0.1,
                'max': 2.0,
                'step': 0.1
            },
            'beer_lambert_blue_coeff': {
                'type': 'float',
                'label': t('param_beer_lambert_blue_coeff_label'),
                'description': t('param_beer_lambert_blue_coeff_desc'),
                'min': 0.01,
                'max': 1.0,
                'step': 0.01
            },
            'beer_lambert_enhance_factor': {
                'type': 'float',
                'label': t('param_beer_lambert_enhance_factor_label'),
                'description': t('param_beer_lambert_enhance_factor_desc'),
                'min': 0.5,
                'max': 3.0,
                'step': 0.1
            },
            
            # Color Rebalancing parameters
            'color_rebalance_enabled': {
                'type': 'boolean',
                'label': t('param_color_rebalance_enabled_label'),
                'description': t('param_color_rebalance_enabled_desc')
            },
            'color_rebalance_rr': {
                'type': 'float',
                'label': t('param_color_rebalance_rr_label'),
                'description': t('param_color_rebalance_rr_desc'),
                'min': 0.5,
                'max': 2.0,
                'step': 0.05
            },
            'color_rebalance_rg': {
                'type': 'float',
                'label': t('param_color_rebalance_rg_label'),
                'description': t('param_color_rebalance_rg_desc'),
                'min': -0.5,
                'max': 0.5,
                'step': 0.05
            },
            'color_rebalance_rb': {
                'type': 'float',
                'label': t('param_color_rebalance_rb_label'),
                'description': t('param_color_rebalance_rb_desc'),
                'min': -0.5,
                'max': 0.5,
                'step': 0.05
            },
            'color_rebalance_gr': {
                'type': 'float',
                'label': t('param_color_rebalance_gr_label'),
                'description': t('param_color_rebalance_gr_desc'),
                'min': -0.5,
                'max': 0.5,
                'step': 0.05
            },
            'color_rebalance_gg': {
                'type': 'float',
                'label': t('param_color_rebalance_gg_label'),
                'description': t('param_color_rebalance_gg_desc'),
                'min': 0.5,
                'max': 2.0,
                'step': 0.05
            },
            'color_rebalance_gb': {
                'type': 'float',
                'label': t('param_color_rebalance_gb_label'),
                'description': t('param_color_rebalance_gb_desc'),
                'min': -0.5,
                'max': 0.5,
                'step': 0.05
            },
            'color_rebalance_br': {
                'type': 'float',
                'label': t('param_color_rebalance_br_label'),
                'description': t('param_color_rebalance_br_desc'),
                'min': -0.5,
                'max': 0.5,
                'step': 0.05
            },
            'color_rebalance_bg': {
                'type': 'float',
                'label': t('param_color_rebalance_bg_label'),
                'description': t('param_color_rebalance_bg_desc'),
                'min': -0.5,
                'max': 0.5,
                'step': 0.05
            },
            'color_rebalance_bb': {
                'type': 'float',
                'label': t('param_color_rebalance_bb_label'),
                'description': t('param_color_rebalance_bb_desc'),
                'min': 0.5,
                'max': 2.0,
                'step': 0.05
            },
            'color_rebalance_saturation_limit': {
                'type': 'float',
                'label': t('param_color_rebalance_saturation_limit_label'),
                'description': t('param_color_rebalance_saturation_limit_desc'),
                'min': 0.3,
                'max': 1.0,
                'step': 0.05
            },
            'color_rebalance_preserve_luminance': {
                'type': 'boolean',
                'label': t('param_color_rebalance_preserve_luminance_label'),
                'description': t('param_color_rebalance_preserve_luminance_desc')
            },
            
            # Histogram equalization parameters
            'hist_eq_enabled': {
                'type': 'boolean',
                'label': t('param_hist_eq_enabled_label'),
                'description': t('param_hist_eq_enabled_desc')
            },
            'hist_eq_clip_limit': {
                'type': 'float',
                'label': t('param_hist_eq_clip_limit_label'),
                'description': t('param_hist_eq_clip_limit_desc'),
                'min': 1.0,
                'max': 10.0,
                'step': 0.5
            },
            'hist_eq_tile_grid_size': {
                'type': 'int',
                'label': t('param_hist_eq_tile_grid_size_label'),
                'description': t('param_hist_eq_tile_grid_size_desc'),
                'min': 4,
                'max': 16,
                'step': 2
            }
        }
