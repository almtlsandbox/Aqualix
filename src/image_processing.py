"""
Image Processing Module
Contains image processing algorithms and pipeline management.
"""

import cv2
import numpy as np
from typing import Dict, Any, List, Tuple
from .localization import t

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
            'gray_world_percentile': 15,         # Improved: 15% more robust than 50% (Iqbal et al., 2007)
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
            'lake_green_reduction': 0.4,        # Improved: More aggressive green reduction (was 0.3)
            'lake_magenta_strength': 0.15,      # Magenta compensation strength (0.0-0.5)
            'lake_gray_world_influence': 0.7,   # Influence of gray-world correction (0.0-1.0)
            
            # UDCP (Underwater Dark Channel Prior) parameters
            'udcp_enabled': True,
            'udcp_omega': 0.95,           # Amount of haze to keep (0.95 = remove 95% of haze)
            'udcp_t0': 0.1,               # Minimum transmission value
            'udcp_window_size': 11,       # Improved: Finer detail preservation (was 15, Ancuti et al., 2018)
            'udcp_guided_radius': 60,     # Radius for guided filter
            'udcp_guided_eps': 0.001,     # Regularization parameter for guided filter
            'udcp_enhance_contrast': 1.2, # Contrast enhancement factor
            
            # Beer-Lambert correction parameters
            'beer_lambert_enabled': True,
            'beer_lambert_depth_factor': 0.15,     # Improved: More effective correction (was 0.1, Chiang & Chen, 2012)
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
            'color_rebalance_saturation_limit': 0.8, # Improved: Anti-magenta protection (was 1.0, Ancuti et al., 2012)
            'color_rebalance_preserve_luminance': False, # Preserve luminance during rebalancing - disabled by default
            
            # Histogram equalization parameters
            'hist_eq_enabled': True,
            'hist_eq_clip_limit': 2.0,
            'hist_eq_tile_grid_size': 8,
            
            # Multi-scale fusion parameters (Ancuti method)
            'multiscale_fusion_enabled': True,      # Improved: Enabled by default (Ancuti et al., 2017 shows significant benefits)
            'fusion_laplacian_levels': 5,            # Number of Laplacian pyramid levels (3-7)
            'fusion_contrast_weight': 1.0,          # Weight for contrast measure (0.0-2.0)
            'fusion_saturation_weight': 1.0,        # Weight for saturation measure (0.0-2.0)
            'fusion_exposedness_weight': 1.0,       # Weight for well-exposedness measure (0.0-2.0)
            'fusion_sigma_contrast': 0.2,           # Gaussian sigma for contrast (0.1-0.5)
            'fusion_sigma_saturation': 0.3,         # Gaussian sigma for saturation (0.1-0.5)
            'fusion_sigma_exposedness': 0.2,        # Gaussian sigma for exposedness (0.1-0.5)
        }
        
        # Processing pipeline order
        self.pipeline_order = [
            'white_balance',
            'udcp',
            'beer_lambert',
            'color_rebalance',
            'histogram_equalization',
            'multiscale_fusion'
        ]
        
        # Auto-tune callback function
        self.auto_tune_callback = None
        
    def set_parameter(self, name: str, value: Any):
        """Set a processing parameter"""
        if name in self.parameters:
            self.parameters[name] = value
    
    def set_auto_tune_callback(self, callback):
        """Set the auto-tune callback function"""
        self.auto_tune_callback = callback
            
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
            'gray_world_percentile': 15,        # Updated: Literature-based improvement
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
            
            # Lake green water parameters
            'lake_green_reduction': 0.4,        # Updated: More aggressive green reduction
            'lake_magenta_strength': 0.15,
            'lake_gray_world_influence': 0.7,
            
            # UDCP parameters
            'udcp_enabled': True,
            'udcp_omega': 0.95,
            'udcp_t0': 0.1,
            'udcp_window_size': 11,             # Updated: Better detail preservation
            'udcp_guided_radius': 60,
            'udcp_guided_epsilon': 0.001,
            'udcp_enhance_factor': 1.2,
            
            # Beer-Lambert correction parameters
            'beer_lambert_enabled': True,
            'beer_lambert_depth_factor': 0.15,  # Updated: More effective correction
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
            'color_rebalance_saturation_limit': 0.8,  # Updated: Anti-magenta protection
            'color_rebalance_preserve_luminance': False,
            
            # Histogram equalization parameters
            'hist_eq_enabled': True,
            'hist_eq_clip_limit': 2.0,             # Corrected: Should be 2.0, not 3.0
            'hist_eq_tile_grid_size': 8,
            
            # Multi-scale fusion parameters
            'multiscale_fusion_enabled': True,      # Updated: Enabled by default
            'fusion_laplacian_levels': 5,
            'fusion_contrast_weight': 1.0,
            'fusion_saturation_weight': 1.0,
            'fusion_exposedness_weight': 1.0,
            'fusion_sigma_contrast': 0.2,
            'fusion_sigma_saturation': 0.3,
            'fusion_sigma_exposedness': 0.2
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
            'histogram_equalization': ['hist_eq_'],
            'multiscale_fusion': ['multiscale_fusion_', 'fusion_']
        }
        
        if step_key not in step_prefixes:
            return
            
        # Reset parameters that match the step prefixes
        for prefix in step_prefixes[step_key]:
            for param_name, default_value in defaults.items():
                if param_name.startswith(prefix):
                    self.set_parameter(param_name, default_value)
    
    def auto_tune_step(self, step_key: str, reference_image: np.ndarray) -> dict:
        """Auto-tune parameters for a specific processing step based on image analysis"""
        if reference_image is None:
            return {}
        
        # Route to specific auto-tune method based on step
        auto_tune_methods = {
            'white_balance': self._auto_tune_white_balance,
            'udcp': self._auto_tune_udcp,
            'beer_lambert': self._auto_tune_beer_lambert,
            'color_rebalance': self._auto_tune_color_rebalance,
            'histogram_equalization': self._auto_tune_histogram_equalization,
            'multiscale_fusion': self._auto_tune_multiscale_fusion
        }
        
        if step_key in auto_tune_methods:
            return auto_tune_methods[step_key](reference_image)
        
        return {}
        
    def process_image(self, image: np.ndarray) -> np.ndarray:
        """Process an image through the complete pipeline"""
        result = image.copy()
        
        for operation in self.pipeline_order:
            # Check if auto-tune is enabled for this step and perform it
            if self.auto_tune_callback and self.auto_tune_callback(operation):
                optimized_params = self.auto_tune_step(operation, image)
                # Apply optimized parameters directly to the processor
                if optimized_params:
                    for param_name, value in optimized_params.items():
                        self.set_parameter(param_name, value)
            
            # Execute the processing step
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
            elif operation == 'multiscale_fusion' and self.parameters['multiscale_fusion_enabled']:
                result = self.multiscale_fusion(image, result)
                
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
            elif operation == 'multiscale_fusion' and self.parameters['multiscale_fusion_enabled']:
                processed_preview = self.multiscale_fusion(original_preview, processed_preview)
                
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
            
    def multiscale_fusion(self, original: np.ndarray, processed: np.ndarray) -> np.ndarray:
        """
        Multi-scale fusion based on Ancuti method.
        Fuses the processed image with additional enhancement variants for improved robustness.
        
        Args:
            original: Original image (for reference)
            processed: Current processed image (result of previous pipeline steps)
            
        Returns:
            Fused result image
        """
        try:
            # Convert images to float32 for processing
            processed_f = processed.astype(np.float32) / 255.0
            
            # Create three variants:
            # 1. The processed image as-is (respects pipeline)
            variant1 = processed_f.copy()
            
            # 2. Processed image with additional contrast enhancement
            variant2 = self._enhance_contrast_on_processed(processed_f)
            
            # 3. Processed image with additional sharpening
            variant3 = self._enhance_sharpening_on_processed(processed_f)
            
            # Normalize variants to [0,1]
            variant1 = np.clip(variant1, 0, 1)
            variant2 = np.clip(variant2, 0, 1)
            variant3 = np.clip(variant3, 0, 1)
            
            # Create Laplacian pyramids for each variant
            levels = self.parameters['fusion_laplacian_levels']
            
            pyr1 = self._build_laplacian_pyramid(variant1, levels)
            pyr2 = self._build_laplacian_pyramid(variant2, levels)
            pyr3 = self._build_laplacian_pyramid(variant3, levels)
            
            # Compute quality measures for each variant
            weights1 = self._compute_quality_measures(variant1)
            weights2 = self._compute_quality_measures(variant2)  
            weights3 = self._compute_quality_measures(variant3)
            
            # Build Gaussian pyramids for weights
            w_pyr1 = self._build_gaussian_pyramid(weights1, levels)
            w_pyr2 = self._build_gaussian_pyramid(weights2, levels)
            w_pyr3 = self._build_gaussian_pyramid(weights3, levels)
            
            # Normalize weights at each level
            fused_pyramid = []
            for level in range(levels):
                # Normalize weights
                total_weight = w_pyr1[level] + w_pyr2[level] + w_pyr3[level] + 1e-12
                norm_w1 = w_pyr1[level] / total_weight
                norm_w2 = w_pyr2[level] / total_weight
                norm_w3 = w_pyr3[level] / total_weight
                
                # Fuse pyramids at this level
                fused_level = (norm_w1[..., np.newaxis] * pyr1[level] + 
                              norm_w2[..., np.newaxis] * pyr2[level] + 
                              norm_w3[..., np.newaxis] * pyr3[level])
                fused_pyramid.append(fused_level)
            
            # Reconstruct image from Laplacian pyramid
            result = self._reconstruct_from_laplacian_pyramid(fused_pyramid)
            
            # Convert back to uint8
            result = np.clip(result * 255, 0, 255).astype(np.uint8)
            
            return result
            
        except Exception as e:
            print(f"Multi-scale fusion error: {e}")
            return processed  # Return original processed image on error
    
    def _create_wb_contrast_variant(self, image: np.ndarray) -> np.ndarray:
        """Create white balance + contrast enhancement variant"""
        # Apply white balance
        variant = self._apply_white_balance_to_float(image)
        
        # Apply contrast enhancement using CLAHE
        variant_uint8 = (variant * 255).astype(np.uint8)
        lab = cv2.cvtColor(variant_uint8, cv2.COLOR_RGB2LAB)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(16, 16))
        lab[:, :, 0] = clahe.apply(lab[:, :, 0])
        variant_uint8 = cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)
        
        return variant_uint8.astype(np.float32) / 255.0
    
    def _create_wb_sharp_variant(self, image: np.ndarray) -> np.ndarray:
        """Create white balance + sharpening variant"""
        # Apply white balance
        variant = self._apply_white_balance_to_float(image)
        
        # Apply unsharp masking for sharpening
        variant_uint8 = (variant * 255).astype(np.uint8)
        blurred = cv2.GaussianBlur(variant_uint8, (0, 0), 1.0)
        sharpened = cv2.addWeighted(variant_uint8, 1.5, blurred, -0.5, 0)
        
        return np.clip(sharpened.astype(np.float32) / 255.0, 0, 1)
    
    def _create_udcp_variant(self, image: np.ndarray) -> np.ndarray:
        """Create UDCP-based variant"""
        # Apply UDCP processing
        variant_uint8 = (image * 255).astype(np.uint8)
        variant = self.underwater_dark_channel_prior(variant_uint8)
        
        return variant.astype(np.float32) / 255.0
    
    def _create_additional_contrast_variant(self, image: np.ndarray) -> np.ndarray:
        """Create additional contrast enhancement variant from processed image"""
        # Apply additional contrast enhancement using CLAHE
        variant_uint8 = (image * 255).astype(np.uint8)
        lab = cv2.cvtColor(variant_uint8, cv2.COLOR_RGB2LAB)
        clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(16, 16))
        lab[:, :, 0] = clahe.apply(lab[:, :, 0])
        variant_uint8 = cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)
        
        return variant_uint8.astype(np.float32) / 255.0
    
    def _create_additional_sharp_variant(self, image: np.ndarray) -> np.ndarray:
        """Create additional sharpening variant from processed image"""
        # Apply additional unsharp masking for sharpening
        variant_uint8 = (image * 255).astype(np.uint8)
        blurred = cv2.GaussianBlur(variant_uint8, (0, 0), 1.2)
        sharpened = cv2.addWeighted(variant_uint8, 1.3, blurred, -0.3, 0)
        
        return np.clip(sharpened.astype(np.float32) / 255.0, 0, 1)
    
    def _enhance_contrast_on_processed(self, processed_image: np.ndarray) -> np.ndarray:
        """Apply gentle contrast enhancement to already processed image"""
        # Convert to uint8 for CLAHE
        image_uint8 = (processed_image * 255).astype(np.uint8)
        
        # Apply gentle CLAHE in LAB space
        lab = cv2.cvtColor(image_uint8, cv2.COLOR_RGB2LAB)
        clahe = cv2.createCLAHE(clipLimit=1.5, tileGridSize=(16, 16))
        lab[:, :, 0] = clahe.apply(lab[:, :, 0])
        enhanced = cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)
        
        return enhanced.astype(np.float32) / 255.0
    
    def _enhance_sharpening_on_processed(self, processed_image: np.ndarray) -> np.ndarray:
        """Apply gentle sharpening to already processed image"""
        # Convert to uint8 for processing
        image_uint8 = (processed_image * 255).astype(np.uint8)
        
        # Apply gentle unsharp mask
        blurred = cv2.GaussianBlur(image_uint8, (0, 0), 0.8)
        sharpened = cv2.addWeighted(image_uint8, 1.2, blurred, -0.2, 0)
        
        return np.clip(sharpened.astype(np.float32) / 255.0, 0, 1)
    
    def _apply_white_balance_to_float(self, image: np.ndarray) -> np.ndarray:
        """Apply white balance to float image"""
        image_uint8 = (image * 255).astype(np.uint8)
        balanced = self.apply_white_balance(image_uint8)
        return balanced.astype(np.float32) / 255.0
    
    def _build_laplacian_pyramid(self, image: np.ndarray, levels: int) -> List[np.ndarray]:
        """Build Laplacian pyramid"""
        gaussian_pyramid = [image]
        
        # Build Gaussian pyramid
        for i in range(levels - 1):
            gaussian_pyramid.append(cv2.pyrDown(gaussian_pyramid[-1]))
        
        # Build Laplacian pyramid
        laplacian_pyramid = [gaussian_pyramid[-1]]  # Top level is Gaussian
        
        for i in range(levels - 1, 0, -1):
            size = (gaussian_pyramid[i-1].shape[1], gaussian_pyramid[i-1].shape[0])
            upsampled = cv2.pyrUp(gaussian_pyramid[i], dstsize=size)
            laplacian = gaussian_pyramid[i-1] - upsampled
            laplacian_pyramid.insert(0, laplacian)
        
        return laplacian_pyramid
    
    def _build_gaussian_pyramid(self, image: np.ndarray, levels: int) -> List[np.ndarray]:
        """Build Gaussian pyramid"""
        pyramid = [image]
        for i in range(levels - 1):
            pyramid.append(cv2.pyrDown(pyramid[-1]))
        return pyramid
    
    def _reconstruct_from_laplacian_pyramid(self, pyramid: List[np.ndarray]) -> np.ndarray:
        """Reconstruct image from Laplacian pyramid"""
        result = pyramid[-1]  # Start with top level
        
        for i in range(len(pyramid) - 2, -1, -1):
            size = (pyramid[i].shape[1], pyramid[i].shape[0])
            result = cv2.pyrUp(result, dstsize=size) + pyramid[i]
        
        return result
    
    def _compute_quality_measures(self, image: np.ndarray) -> np.ndarray:
        """Compute quality measures (contrast, saturation, well-exposedness)"""
        # Convert to grayscale for some measures
        if len(image.shape) == 3:
            gray = cv2.cvtColor((image * 255).astype(np.uint8), cv2.COLOR_RGB2GRAY).astype(np.float32) / 255.0
        else:
            gray = image
        
        # Contrast measure using Laplacian
        laplacian = cv2.Laplacian(gray, cv2.CV_32F)
        contrast = np.abs(laplacian)
        
        # Saturation measure
        if len(image.shape) == 3:
            saturation = np.std(image, axis=2)
        else:
            saturation = np.zeros_like(gray)
        
        # Well-exposedness measure (Gaussian around 0.5)
        exposedness = np.exp(-0.5 * ((gray - 0.5) / self.parameters['fusion_sigma_exposedness']) ** 2)
        
        # Apply Gaussian smoothing to measures
        contrast = cv2.GaussianBlur(contrast, (5, 5), self.parameters['fusion_sigma_contrast'])
        saturation = cv2.GaussianBlur(saturation, (5, 5), self.parameters['fusion_sigma_saturation'])
        exposedness = cv2.GaussianBlur(exposedness, (5, 5), self.parameters['fusion_sigma_exposedness'])
        
        # Combine measures with weights
        weight = (contrast ** self.parameters['fusion_contrast_weight'] * 
                 saturation ** self.parameters['fusion_saturation_weight'] *
                 exposedness ** self.parameters['fusion_exposedness_weight'])
        
        # Avoid division by zero
        weight = weight + 1e-12
        
        return weight
        
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
            },
            
            # Multi-scale fusion parameters
            'fusion_laplacian_levels': {
                'type': 'int',
                'label': t('param_fusion_laplacian_levels_label'),
                'description': t('param_fusion_laplacian_levels_desc'),
                'min': 3,
                'max': 7,
                'step': 1
            },
            'fusion_contrast_weight': {
                'type': 'float',
                'label': t('param_fusion_contrast_weight_label'),
                'description': t('param_fusion_contrast_weight_desc'),
                'min': 0.0,
                'max': 2.0,
                'step': 0.1
            },
            'fusion_saturation_weight': {
                'type': 'float', 
                'label': t('param_fusion_saturation_weight_label'),
                'description': t('param_fusion_saturation_weight_desc'),
                'min': 0.0,
                'max': 2.0,
                'step': 0.1
            },
            'fusion_exposedness_weight': {
                'type': 'float',
                'label': t('param_fusion_exposedness_weight_label'),
                'description': t('param_fusion_exposedness_weight_desc'),
                'min': 0.0,
                'max': 2.0,
                'step': 0.1
            },
            'fusion_sigma_contrast': {
                'type': 'float',
                'label': t('param_fusion_sigma_contrast_label'),
                'description': t('param_fusion_sigma_contrast_desc'),
                'min': 0.1,
                'max': 0.5,
                'step': 0.05
            },
            'fusion_sigma_saturation': {
                'type': 'float',
                'label': t('param_fusion_sigma_saturation_label'),
                'description': t('param_fusion_sigma_saturation_desc'),
                'min': 0.1,
                'max': 0.5,
                'step': 0.05
            },
            'fusion_sigma_exposedness': {
                'type': 'float',
                'label': t('param_fusion_sigma_exposedness_label'),
                'description': t('param_fusion_sigma_exposedness_desc'),
                'min': 0.1,
                'max': 0.5,
                'step': 0.05
            }
        }
    
    # ===============================
    # AUTO-TUNE METHODS
    # ===============================
    
    def _auto_tune_white_balance(self, img: np.ndarray) -> dict:
        """Auto-tune white balance parameters based on image characteristics"""
        try:
            if img is None:
                return {}
            
            # Analyze image color characteristics
            img_float = img.astype(np.float32) / 255.0
            h, s, v = cv2.split(cv2.cvtColor(img_float, cv2.COLOR_BGR2HSV))
            
            # Calculate color statistics
            r_mean = np.mean(img_float[:,:,2])  # Red channel (BGR)
            g_mean = np.mean(img_float[:,:,1])  # Green channel
            b_mean = np.mean(img_float[:,:,0])  # Blue channel
            
            # Detect dominant color cast
            r_ratio = r_mean / (r_mean + g_mean + b_mean + 1e-6)
            g_ratio = g_mean / (r_mean + g_mean + b_mean + 1e-6)
            b_ratio = b_mean / (r_mean + g_mean + b_mean + 1e-6)
            
            optimized_params = {}
            
            # Choose optimal white balance method based on color characteristics
            if g_ratio > 0.4:  # Strong green cast (lake/freshwater)
                optimized_params['white_balance_method'] = 'lake_green_water'
                optimized_params['lake_green_reduction'] = min(0.8, (g_ratio - 0.33) * 2.0)
                optimized_params['lake_magenta_strength'] = min(0.3, (g_ratio - 0.35) * 1.5)
                optimized_params['lake_gray_world_influence'] = 0.6
            elif b_ratio < 0.25:  # Blue loss (deep water)
                optimized_params['white_balance_method'] = 'gray_world'
                optimized_params['gray_world_percentile'] = 50
                optimized_params['gray_world_max_adjustment'] = min(2.0, 1.5 + (0.33 - b_ratio) * 2.0)
            elif r_ratio < 0.2:  # Red loss (typical underwater)
                optimized_params['white_balance_method'] = 'shades_of_gray'
                optimized_params['shades_of_gray_norm'] = 6
                optimized_params['shades_of_gray_percentile'] = 95
                optimized_params['shades_of_gray_max_adjustment'] = min(3.0, 2.0 + (0.33 - r_ratio) * 3.0)
            else:  # Balanced colors
                optimized_params['white_balance_method'] = 'white_patch'
                optimized_params['white_patch_percentile'] = 99
                optimized_params['white_patch_max_adjustment'] = 1.5
            
            return optimized_params
            
        except Exception as e:
            print(f"Auto-tune white balance error: {e}")
            return {}
    
    def _auto_tune_udcp(self, img: np.ndarray) -> dict:
        """Auto-tune UDCP parameters based on image turbidity and contrast"""
        try:
            if img is None:
                return {}
            
            # Analyze image characteristics
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Calculate contrast using standard deviation
            contrast = np.std(img_gray) / 255.0
            
            # Calculate darkness (dark channel prior approximation)
            dark_channel = np.min(img, axis=2)
            darkness_level = np.mean(dark_channel) / 255.0
            
            # Calculate turbidity estimation (variance in local patches)
            kernel = np.ones((15,15), np.float32) / 225
            mean_filtered = cv2.filter2D(img_gray.astype(np.float32), -1, kernel)
            turbidity = np.mean(np.abs(img_gray.astype(np.float32) - mean_filtered)) / 255.0
            
            optimized_params = {}
            
            # Adjust omega based on water clarity
            if turbidity > 0.15:  # Murky water
                optimized_params['udcp_omega'] = 0.7  # Less haze removal
            elif turbidity > 0.08:  # Medium clarity
                optimized_params['udcp_omega'] = 0.85
            else:  # Clear water
                optimized_params['udcp_omega'] = 0.95
            
            # Adjust t0 based on darkness level
            optimized_params['udcp_t0'] = max(0.05, min(0.2, 0.1 + darkness_level * 0.5))
            
            # Adjust window size based on image resolution and turbidity
            height, width = img_gray.shape
            base_window = 7 if width < 800 else 15
            if turbidity > 0.1:
                optimized_params['udcp_window_size'] = max(7, base_window - 4)
            else:
                optimized_params['udcp_window_size'] = base_window
            
            # Adjust guided filter parameters
            optimized_params['udcp_guided_radius'] = 30 if turbidity > 0.1 else 60
            optimized_params['udcp_guided_eps'] = 0.01 if contrast > 0.3 else 0.001
            
            # Enhance contrast for low-contrast images
            if contrast < 0.15:
                optimized_params['udcp_enhance_contrast'] = min(1.5, 1.0 + (0.2 - contrast) * 2.0)
            else:
                optimized_params['udcp_enhance_contrast'] = 1.0
                
            return optimized_params
            
        except Exception as e:
            print(f"Auto-tune UDCP error: {e}")
            return {}
    
    def _auto_tune_beer_lambert(self, img: np.ndarray) -> dict:
        """Auto-tune Beer-Lambert parameters based on color loss analysis"""
        try:
            if img is None:
                return {}
            
            # Analyze color channel distributions
            img_float = img.astype(np.float32) / 255.0
            r_channel = img_float[:,:,2]  # Red (BGR)
            g_channel = img_float[:,:,1]  # Green
            b_channel = img_float[:,:,0]  # Blue
            
            # Calculate average intensities
            r_mean = np.mean(r_channel)
            g_mean = np.mean(g_channel)
            b_mean = np.mean(b_channel)
            
            # Calculate color loss ratios (compared to expected balanced image)
            expected_mean = 0.4  # Expected mean for balanced underwater image
            r_loss = max(0, expected_mean - r_mean)
            g_loss = max(0, expected_mean - g_mean)
            b_loss = max(0, expected_mean - b_mean)
            
            # Estimate depth factor from overall darkness
            overall_darkness = 1.0 - np.mean([r_mean, g_mean, b_mean])
            
            optimized_params = {}
            
            # Depth factor based on overall image darkness
            optimized_params['beer_lambert_depth_factor'] = min(2.0, 0.5 + overall_darkness * 2.0)
            
            # Red coefficient (high for typical underwater red loss)
            optimized_params['beer_lambert_red_coeff'] = min(0.8, 0.4 + r_loss * 1.5)
            
            # Green coefficient (moderate, varies with water type)
            optimized_params['beer_lambert_green_coeff'] = min(0.6, 0.2 + g_loss * 1.2)
            
            # Blue coefficient (usually low, blue travels furthest)
            optimized_params['beer_lambert_blue_coeff'] = min(0.4, 0.1 + b_loss * 1.0)
            
            # Enhancement factor based on overall color loss
            total_loss = r_loss + g_loss + b_loss
            optimized_params['beer_lambert_enhance_factor'] = min(2.5, 1.0 + total_loss * 2.0)
            
            return optimized_params
            
        except Exception as e:
            print(f"Auto-tune Beer-Lambert error: {e}")
            return {}
    
    def _auto_tune_color_rebalance(self, img: np.ndarray) -> dict:
        """Auto-tune color rebalancing matrix based on color distribution analysis"""
        try:
            if img is None:
                return {}
            
            # Analyze color relationships in HSV space
            img_float = img.astype(np.float32) / 255.0
            hsv = cv2.cvtColor(img_float, cv2.COLOR_BGR2HSV)
            h, s, v = cv2.split(hsv)
            
            # Calculate color channel correlations
            r_channel = img_float[:,:,2]
            g_channel = img_float[:,:,1]
            b_channel = img_float[:,:,0]
            
            # Calculate cross-channel correlations
            rg_corr = np.corrcoef(r_channel.flat, g_channel.flat)[0,1]
            rb_corr = np.corrcoef(r_channel.flat, b_channel.flat)[0,1]
            gb_corr = np.corrcoef(g_channel.flat, b_channel.flat)[0,1]
            
            # Calculate saturation statistics
            sat_mean = np.mean(s)
            sat_std = np.std(s)
            
            optimized_params = {}
            
            # Adjust diagonal elements (main channel gains)
            optimized_params['color_rebalance_rr'] = min(2.0, 1.0 + (1.0 - sat_mean) * 0.5)
            optimized_params['color_rebalance_gg'] = 1.0
            optimized_params['color_rebalance_bb'] = min(2.0, 1.0 + (1.0 - sat_mean) * 0.3)
            
            # Adjust cross-channel mixing based on correlations
            # Reduce green influence on red if highly correlated (reduce green cast)
            if rg_corr > 0.8:
                optimized_params['color_rebalance_rg'] = max(-0.3, -0.1 * (rg_corr - 0.7))
            else:
                optimized_params['color_rebalance_rg'] = 0.0
                
            # Blue-red mixing for warm/cool balance
            if rb_corr < 0.5:
                optimized_params['color_rebalance_rb'] = min(0.2, 0.1 * (0.6 - rb_corr))
            else:
                optimized_params['color_rebalance_rb'] = 0.0
            
            # Green adjustments
            optimized_params['color_rebalance_gr'] = 0.0
            optimized_params['color_rebalance_gb'] = 0.0
            
            # Blue adjustments
            optimized_params['color_rebalance_br'] = 0.0
            optimized_params['color_rebalance_bg'] = 0.0
            
            # Saturation limiting based on current saturation distribution
            if sat_std > 0.2:  # High saturation variance
                optimized_params['color_rebalance_saturation_limit'] = min(0.8, 0.5 + sat_mean * 0.5)
            else:  # Low saturation variance
                optimized_params['color_rebalance_saturation_limit'] = min(1.0, 0.7 + sat_mean * 0.3)
            
            # Preserve luminance for natural look
            optimized_params['color_rebalance_preserve_luminance'] = True
            
            return optimized_params
            
        except Exception as e:
            print(f"Auto-tune color rebalance error: {e}")
            return {}
    
    def _auto_tune_histogram_equalization(self, img: np.ndarray) -> dict:
        """Auto-tune histogram equalization based on contrast analysis"""
        try:
            if img is None:
                return {}
            
            # Analyze image contrast and histogram distribution
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Calculate histogram
            hist = cv2.calcHist([img_gray], [0], None, [256], [0, 256])
            hist_norm = hist / (img_gray.shape[0] * img_gray.shape[1])
            
            # Calculate contrast metrics
            contrast_std = np.std(img_gray) / 255.0
            
            # Find histogram concentration (how much is in middle values)
            middle_range = np.sum(hist_norm[64:192])  # Middle 50% of intensity range
            
            # Calculate local contrast variation
            kernel = np.ones((9,9), np.float32) / 81
            mean_filtered = cv2.filter2D(img_gray.astype(np.float32), -1, kernel)
            local_contrast = np.mean(np.abs(img_gray.astype(np.float32) - mean_filtered)) / 255.0
            
            optimized_params = {}
            
            # Adjust clip limit based on contrast characteristics
            if contrast_std < 0.15:  # Low contrast image
                optimized_params['hist_eq_clip_limit'] = min(4.0, 2.0 + (0.2 - contrast_std) * 10.0)
            elif local_contrast > 0.1:  # High local contrast
                optimized_params['hist_eq_clip_limit'] = max(1.0, 2.0 - local_contrast * 5.0)
            else:  # Normal contrast
                optimized_params['hist_eq_clip_limit'] = 2.0
            
            # Adjust tile size based on image characteristics
            height, width = img_gray.shape
            
            # For high local variation, use smaller tiles
            if local_contrast > 0.08:
                base_size = 6 if min(width, height) < 600 else 8
            else:
                base_size = 8 if min(width, height) < 600 else 12
            
            # If histogram is concentrated in middle, use larger tiles
            if middle_range > 0.7:
                base_size += 2
            
            optimized_params['hist_eq_tile_grid_size'] = min(16, max(4, base_size))
            
            return optimized_params
            
        except Exception as e:
            print(f"Auto-tune histogram equalization error: {e}")
            return {}
    
    def _auto_tune_multiscale_fusion(self, img: np.ndarray) -> dict:
        """Auto-tune multiscale fusion based on image quality metrics"""
        try:
            if img is None:
                return {}
            
            # Analyze image characteristics for fusion optimization
            img_float = img.astype(np.float32) / 255.0
            
            # Calculate quality metrics
            # Contrast analysis
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            contrast_std = np.std(img_gray) / 255.0
            
            # Saturation analysis
            hsv = cv2.cvtColor(img_float, cv2.COLOR_BGR2HSV)
            saturation = hsv[:,:,1]
            sat_mean = np.mean(saturation)
            
            # Exposedness analysis (how well exposed the image is)
            luminance = 0.299 * img_float[:,:,2] + 0.587 * img_float[:,:,1] + 0.114 * img_float[:,:,0]
            # Well-exposed regions are around 0.5 luminance
            exposedness_map = np.exp(-0.5 * ((luminance - 0.5) / 0.25) ** 2)
            exposedness_mean = np.mean(exposedness_map)
            
            # Edge/detail analysis
            edges = cv2.Canny(img_gray, 50, 150)
            edge_density = np.sum(edges > 0) / (edges.shape[0] * edges.shape[1])
            
            optimized_params = {}
            
            # Adjust pyramid levels based on image size and detail
            height, width = img_gray.shape
            base_levels = 4 if min(width, height) > 800 else 3
            if edge_density > 0.1:  # High detail image
                optimized_params['fusion_laplacian_levels'] = min(6, base_levels + 1)
            else:
                optimized_params['fusion_laplacian_levels'] = base_levels
            
            # Weight optimization based on image characteristics
            
            # Contrast weight: higher for low-contrast images
            if contrast_std < 0.15:
                optimized_params['fusion_contrast_weight'] = min(2.0, 1.0 + (0.2 - contrast_std) * 5.0)
            else:
                optimized_params['fusion_contrast_weight'] = 1.0
            
            # Saturation weight: higher for low-saturation images
            if sat_mean < 0.3:
                optimized_params['fusion_saturation_weight'] = min(2.0, 1.0 + (0.4 - sat_mean) * 2.0)
            else:
                optimized_params['fusion_saturation_weight'] = 1.0
            
            # Exposedness weight: higher for poorly exposed images
            if exposedness_mean < 0.5:
                optimized_params['fusion_exposedness_weight'] = min(2.0, 1.0 + (0.6 - exposedness_mean) * 2.0)
            else:
                optimized_params['fusion_exposedness_weight'] = 1.0
            
            # Sigma parameters based on image characteristics
            # Smaller sigma for more detailed images
            if edge_density > 0.08:
                optimized_params['fusion_sigma_1'] = 0.15
                optimized_params['fusion_sigma_2'] = 0.20
                optimized_params['fusion_sigma_3'] = 0.15
            else:
                optimized_params['fusion_sigma_1'] = 0.20
                optimized_params['fusion_sigma_2'] = 0.30
                optimized_params['fusion_sigma_3'] = 0.20
            
            return optimized_params
            
        except Exception as e:
            print(f"Auto-tune multiscale fusion error: {e}")
            return {}

    # =============================
    # ENHANCED AUTO-TUNE METHODS (Literature-based improvements)
    # =============================

    def _enhanced_auto_tune_white_balance(self, img: np.ndarray) -> dict:
        """
        Enhanced auto-tune White Balance basé sur:
        - Iqbal et al. (2007): "Underwater Image Enhancement"
        - Ancuti et al. (2012): "Color Balance and Fusion"
        """
        try:
            if img is None or img.size == 0:
                return {}
            
            # 1. Conversion et analyse préliminaire
            img_float = img.astype(np.float32) / 255.0
            h, w = img.shape[:2]
            
            # 2. Analyse histogram spread (Iqbal method)
            hist_r = cv2.calcHist([img], [2], None, [256], [0, 256]).flatten()
            hist_g = cv2.calcHist([img], [1], None, [256], [0, 256]).flatten()
            hist_b = cv2.calcHist([img], [0], None, [256], [0, 256]).flatten()
            
            # Calcul du spread pour chaque canal
            spread_r = np.std(hist_r)
            spread_g = np.std(hist_g)
            spread_b = np.std(hist_b)
            max_spread = max(spread_r, spread_g, spread_b)
            
            # 3. Distance euclidienne des canaux (Ancuti method)
            r_mean = np.mean(img_float[:,:,2])
            g_mean = np.mean(img_float[:,:,1])
            b_mean = np.mean(img_float[:,:,0])
            
            euclidean_distance = np.sqrt(
                (r_mean - g_mean)**2 + 
                (g_mean - b_mean)**2 + 
                (b_mean - r_mean)**2
            )
            
            # 4. Détection pixels saturés et sous-exposés
            saturated_pixels = np.sum((img > 250).any(axis=2)) / (h * w)
            underexposed_pixels = np.sum((img < 5).any(axis=2)) / (h * w)
            
            # 5. Analyse de dominante couleur avancée
            color_cast_strength = max(abs(r_mean - g_mean), 
                                    abs(g_mean - b_mean), 
                                    abs(b_mean - r_mean))
            
            # 6. Paramètres optimisés selon littérature
            optimized_params = {}
            
            # Percentile adaptatif basé sur spread histogram
            base_percentile = 15  # Optimal selon Iqbal et al.
            if max_spread > 1200:  # Very high spread - image très contrastée
                optimized_params['gray_world_percentile'] = max(8, base_percentile - 7)
            elif max_spread > 800:   # High spread - image contrastée
                optimized_params['gray_world_percentile'] = max(10, base_percentile - 5)
            elif max_spread < 400:   # Low spread - image plate
                optimized_params['gray_world_percentile'] = min(25, base_percentile + 10)
            else:  # Normal spread
                optimized_params['gray_world_percentile'] = base_percentile
            
            # Max adjustment basé sur pixels saturés et distance euclidienne
            base_max_adj = 2.2  # Nouveau défaut littérature-basé
            if saturated_pixels > 0.08:  # >8% pixels saturés
                optimized_params['gray_world_max_adjustment'] = min(1.4, base_max_adj - saturated_pixels * 8)
            elif underexposed_pixels > 0.15:  # >15% sous-exposés
                optimized_params['gray_world_max_adjustment'] = min(3.0, base_max_adj + underexposed_pixels * 2)
            else:
                # Ajustement basé sur distance euclidienne (Ancuti method)
                optimized_params['gray_world_max_adjustment'] = min(2.8, base_max_adj + euclidean_distance * 3)
            
            # Choix méthode intelligent selon caractéristiques
            if color_cast_strength > 0.15 and euclidean_distance > 0.12:
                # Forte dominante couleur - préférer Gray World
                if 'gray_world_percentile' not in optimized_params:
                    optimized_params['gray_world_percentile'] = 12
                optimized_params['method'] = 'gray_world'
            elif saturated_pixels > 0.05:
                # Beaucoup de pixels saturés - préférer White Patch
                optimized_params['method'] = 'white_patch'
                optimized_params['white_patch_percentile'] = min(98, 95 + saturated_pixels * 20)
            
            # Logging pour debug
            print(f"Enhanced WB Auto-tune: spread={max_spread:.1f}, "
                  f"eucl_dist={euclidean_distance:.3f}, "
                  f"saturated={saturated_pixels:.3f}, "
                  f"params={optimized_params}")
            
            return optimized_params
            
        except Exception as e:
            print(f"Enhanced auto-tune white balance error: {e}")
            return {}

    def _enhanced_auto_tune_udcp(self, img: np.ndarray) -> dict:
        """
        Enhanced auto-tune UDCP basé sur:
        - Drews et al. (2013): "Transmission Estimation in Underwater Images"
        - Carlevaris-Bianco et al. (2010): "Initial Results in Underwater Single Image Dehazing"
        """
        try:
            if img is None or img.size == 0:
                return {}
            
            img_float = img.astype(np.float32) / 255.0
            h, w = img.shape[:2]
            
            # 1. Estimation de profondeur relative (Drews method)
            # Dark channel simple pour estimation grossière
            min_channel = np.min(img_float, axis=2)
            dark_channel_global = np.mean(min_channel)
            
            # Gradient d'intensité pour estimation locale de clarté
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            grad_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
            grad_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
            gradient_magnitude = np.sqrt(grad_x**2 + grad_y**2)
            avg_gradient = np.mean(gradient_magnitude)
            
            # 2. Analyse spectrale pour omega (Drews method)
            # Analyse de la distribution des couleurs
            b_channel, g_channel, r_channel = cv2.split(img_float)
            
            # Ratio blue/red pour estimer l'atténuation spectrale
            safe_r = np.maximum(r_channel, 0.01)  # Éviter division par 0
            blue_red_ratio = np.mean(b_channel / safe_r)
            
            # Variance des canaux pour mesurer la turbidité
            r_var = np.var(r_channel)
            g_var = np.var(g_channel)
            b_var = np.var(b_channel)
            color_variance = np.mean([r_var, g_var, b_var])
            
            # 3. Noise level estimation pour epsilon (Carlevaris-Bianco method)
            # Utilisation du Laplacian pour estimer le bruit
            laplacian = cv2.Laplacian(gray, cv2.CV_64F)
            noise_estimate = np.var(laplacian)
            
            # 4. Paramètres optimisés
            optimized_params = {}
            
            # Omega adaptatif basé sur analyse spectrale
            base_omega = 0.85  # Nouveau défaut littérature-basé (Drews)
            if blue_red_ratio > 1.4:  # Eau très bleue - forte atténuation rouge
                optimized_params['omega'] = min(0.95, base_omega + 0.1)
            elif blue_red_ratio < 0.8:  # Eau verte/trouble - moins d'atténuation
                optimized_params['omega'] = max(0.7, base_omega - 0.15)
            else:  # Eau claire normale
                optimized_params['omega'] = base_omega
            
            # t0 basé sur estimation de profondeur
            base_t0 = 0.15  # Nouveau défaut littérature-basé
            depth_factor = 1 - dark_channel_global  # Plus sombre = plus profond
            if depth_factor > 0.8:  # Image très sombre - probablement profonde
                optimized_params['t0'] = min(0.25, base_t0 + 0.1)
            elif depth_factor < 0.4:  # Image claire - probablement peu profonde
                optimized_params['t0'] = max(0.08, base_t0 - 0.07)
            else:
                optimized_params['t0'] = base_t0
            
            # Window size adaptatif selon résolution ET gradient
            base_window = max(15, min(h, w) // 40)  # Adapté à la résolution
            if avg_gradient > 30:  # Beaucoup de détails fins
                optimized_params['window_size'] = max(9, base_window - 6)
            elif avg_gradient < 15:  # Peu de détails
                optimized_params['window_size'] = min(25, base_window + 8)
            else:
                optimized_params['window_size'] = base_window
            
            # Epsilon pour guided filter basé sur noise estimation
            base_epsilon = 0.001  # Nouveau défaut littérature-basé
            if noise_estimate > 100:  # Image très bruitée
                optimized_params['guided_filter_epsilon'] = min(0.01, base_epsilon * 10)
            elif noise_estimate < 20:  # Image peu bruitée
                optimized_params['guided_filter_epsilon'] = max(0.0001, base_epsilon / 2)
            else:
                optimized_params['guided_filter_epsilon'] = base_epsilon
            
            # Logging
            print(f"Enhanced UDCP Auto-tune: depth_factor={depth_factor:.3f}, "
                  f"blue_red_ratio={blue_red_ratio:.3f}, "
                  f"noise_est={noise_estimate:.1f}, "
                  f"params={optimized_params}")
            
            return optimized_params
            
        except Exception as e:
            print(f"Enhanced auto-tune UDCP error: {e}")
            return {}

    def _enhanced_auto_tune_beer_lambert(self, img: np.ndarray) -> dict:
        """
        Enhanced auto-tune Beer-Lambert basé sur:
        - Chiang & Chen (2012): "Wavelength Compensation and Dehazing"
        - McGlamery (1980): "Computer Model for Underwater Camera Systems"
        """
        try:
            if img is None or img.size == 0:
                return {}
            
            img_float = img.astype(np.float32) / 255.0
            
            # 1. Coefficients d'absorption spectrale réels de l'eau (McGlamery)
            # Longueurs d'onde approximatives: R=650nm, G=550nm, B=450nm
            # Coefficients en m^-1 (eau pure + particules typiques)
            absorption_coeffs = {
                'red': 0.45,    # Fort absorption du rouge
                'green': 0.12,  # Absorption modérée du vert  
                'blue': 0.05    # Faible absorption du bleu
            }
            
            # 2. Analyse de la perte couleur par canal
            b_channel, g_channel, r_channel = cv2.split(img_float)
            
            # Moyennes des canaux pour estimer l'atténuation
            r_mean = np.mean(r_channel)
            g_mean = np.mean(g_channel)  
            b_mean = np.mean(b_channel)
            
            # 3. Estimation de distance relative (Chiang & Chen method)
            # Plus l'image est sombre, plus la distance est importante
            overall_brightness = (r_mean + g_mean + b_mean) / 3.0
            darkness_factor = 1.0 - overall_brightness
            
            # Analyse du ratio spectral pour raffiner l'estimation
            safe_b_mean = max(b_mean, 0.01)
            red_blue_ratio = r_mean / safe_b_mean
            green_blue_ratio = g_mean / safe_b_mean
            
            # 4. Modélisation du scattering (McGlamery)
            # Estimation du scattering via analyse de la variance locale
            kernel = np.ones((15,15), np.float32) / 225
            r_smooth = cv2.filter2D(r_channel, -1, kernel)
            g_smooth = cv2.filter2D(g_channel, -1, kernel) 
            b_smooth = cv2.filter2D(b_channel, -1, kernel)
            
            # Différence entre original et lissé = scattering approximatif
            r_scatter = np.mean(np.abs(r_channel - r_smooth))
            g_scatter = np.mean(np.abs(g_channel - g_smooth))
            b_scatter = np.mean(np.abs(b_channel - b_smooth))
            
            # 5. Paramètres optimisés
            optimized_params = {}
            
            # Depth factor basé sur darkness ET analyse spectrale
            base_depth = 0.7  # Nouveau défaut littérature-basé
            spectral_depth_indicator = 1.0 - red_blue_ratio  # Plus faible = plus profond
            combined_depth = (darkness_factor + spectral_depth_indicator) / 2.0
            
            if combined_depth > 0.8:  # Très profond/lointain
                optimized_params['depth_factor'] = min(1.2, base_depth + 0.5)
            elif combined_depth < 0.3:  # Peu profond/proche  
                optimized_params['depth_factor'] = max(0.3, base_depth - 0.4)
            else:
                optimized_params['depth_factor'] = base_depth + (combined_depth - 0.5) * 0.6
            
            # Coefficients d'atténuation basés sur coefficients réels
            # Ajustés selon les conditions observées de l'image
            attenuation_scale = 1.0 + darkness_factor  # Plus sombre = plus d'atténuation
            
            optimized_params['red_loss'] = min(0.95, 
                absorption_coeffs['red'] * attenuation_scale + r_scatter * 2.0)
            optimized_params['green_loss'] = min(0.6, 
                absorption_coeffs['green'] * attenuation_scale + g_scatter * 2.0) 
            optimized_params['blue_loss'] = min(0.3,
                absorption_coeffs['blue'] * attenuation_scale + b_scatter * 2.0)
            
            # Facteur de compensation global
            compensation_strength = min(2.5, 1.0 + combined_depth * 1.5)
            if 'red_loss' in optimized_params:
                optimized_params['red_loss'] *= compensation_strength
                optimized_params['green_loss'] *= compensation_strength  
                optimized_params['blue_loss'] *= compensation_strength
            
            # Logging
            print(f"Enhanced Beer-Lambert Auto-tune: "
                  f"depth={combined_depth:.3f}, "
                  f"spectral_ratios=R/B:{red_blue_ratio:.3f}, G/B:{green_blue_ratio:.3f}, "
                  f"params={optimized_params}")
            
            return optimized_params
            
        except Exception as e:
            print(f"Enhanced auto-tune Beer-Lambert error: {e}")
            return {}

    def toggle_enhanced_autotune(self, enabled: bool = True):
        """Active/désactive les auto-tune améliorés basés sur la littérature"""
        self.use_enhanced_autotune = enabled
        print(f"Enhanced auto-tune: {'ENABLED' if enabled else 'DISABLED'}")

    def enhanced_auto_tune_step(self, img: np.ndarray, step_name: str) -> dict:
        """
        Auto-tune unifié avec choix classique/amélioré
        """
        if hasattr(self, 'use_enhanced_autotune') and self.use_enhanced_autotune:
            # Utiliser les méthodes améliorées
            if step_name == 'white_balance':
                return self._enhanced_auto_tune_white_balance(img)
            elif step_name == 'udcp':
                return self._enhanced_auto_tune_udcp(img) 
            elif step_name == 'beer_lambert':
                return self._enhanced_auto_tune_beer_lambert(img)
            # Fallback vers méthodes classiques pour les autres étapes
            elif step_name == 'color_rebalance':
                return self._auto_tune_color_rebalance(img)
            elif step_name == 'histogram_equalization':
                return self._auto_tune_histogram_equalization(img)
            elif step_name == 'multiscale_fusion':
                return self._auto_tune_multiscale_fusion(img)
        
        # Utiliser méthodes classiques par défaut
        if step_name == 'white_balance':
            return self._auto_tune_white_balance(img)
        elif step_name == 'udcp':
            return self._auto_tune_udcp(img)
        elif step_name == 'beer_lambert':
            return self._auto_tune_beer_lambert(img)
        elif step_name == 'color_rebalance':
            return self._auto_tune_color_rebalance(img)
        elif step_name == 'histogram_equalization':
            return self._auto_tune_histogram_equalization(img)
        elif step_name == 'multiscale_fusion':
            return self._auto_tune_multiscale_fusion(img)
        
        return {}
