"""
Post-Processing Quality Checks for Aqualix
Implements advanced quality control based on academic research in underwater image processing
"""

import numpy as np
import cv2
from typing import Dict, List, Tuple, Any, Optional
import logging


class PostProcessingQualityChecker:
    """Analyzes processed underwater images for quality issues and provides recommendations"""
    
    def __init__(self):
        self.analysis_results = {}
        self.recommendations = []
        self.logger = logging.getLogger(__name__)
        
    def run_all_checks(self, original_image: np.ndarray, processed_image: np.ndarray) -> Dict[str, Any]:
        """
        Run comprehensive quality analysis on processed image
        
        Args:
            original_image: Original image in BGR format
            processed_image: Processed image in BGR format
            
        Returns:
            Dictionary containing all analysis results
        """
        self.analysis_results = {}
        self.recommendations = []
        
        try:
            # Convert images to different color spaces for analysis
            processed_rgb = cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB)
            processed_hsv = cv2.cvtColor(processed_image, cv2.COLOR_BGR2HSV)
            processed_lab = cv2.cvtColor(processed_image, cv2.COLOR_BGR2LAB)
            
            original_rgb = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
            
            # Run individual checks
            self._check_unrealistic_colors(processed_rgb)
            self._check_red_channel_analysis(processed_rgb)
            self._check_saturation_clipping(processed_hsv)
            self._check_color_noise_amplification(original_rgb, processed_rgb)
            self._check_halo_artifacts(processed_image)
            self._check_midtone_balance(processed_lab)
            
            # Calculate quality improvements
            self._calculate_quality_improvements(original_image, processed_image)
            
            # Compile final results
            results = {
                'unrealistic_colors': self.analysis_results.get('unrealistic_colors', {}),
                'red_channel_analysis': self.analysis_results.get('red_channel_analysis', {}),
                'saturation_analysis': self.analysis_results.get('saturation_analysis', {}),
                'color_noise_analysis': self.analysis_results.get('color_noise_analysis', {}),
                'halo_artifacts': self.analysis_results.get('halo_artifacts', {}),
                'midtone_balance': self.analysis_results.get('midtone_balance', {}),
                'quality_improvements': self.analysis_results.get('quality_improvements', {}),
                'overall_recommendations': [rec for rec in self.recommendations]
            }
            
            return results
            
        except Exception as e:
            self.logger.error(f"Error in quality analysis: {str(e)}")
            return {
                'error': str(e),
                'partial_results': self.analysis_results
            }
    
    def _check_unrealistic_colors(self, img_rgb: np.ndarray):
        """
        Detect unrealistic colors that commonly result from over-correction
        Based on Berman et al. research on underwater color restoration artifacts
        """
        height, width = img_rgb.shape[:2]
        total_pixels = height * width
        
        # Convert to float for analysis
        img_float = img_rgb.astype(np.float32) / 255.0
        
        # Check for extreme red pixels (neon red artifacts)
        red_channel = img_float[:, :, 0]
        green_channel = img_float[:, :, 1]  
        blue_channel = img_float[:, :, 2]
        
        # Detect pixels with excessive red dominance
        red_dominant = (red_channel > 0.8) & (red_channel > green_channel + 0.3) & (red_channel > blue_channel + 0.4)
        extreme_red_pixels = np.sum(red_dominant) / total_pixels
        
        # Check for magenta shift (common Beer-Lambert over-correction artifact)
        magenta_mask = (red_channel > 0.7) & (blue_channel > 0.5) & (green_channel < 0.4)
        magenta_pixels = np.sum(magenta_mask) / total_pixels
        
        # Calculate red dominance ratio
        red_dominance_ratio = np.mean(red_channel) / max(np.mean(blue_channel), 0.1)
        
        # Store results
        self.analysis_results['unrealistic_colors'] = {
            'extreme_red_pixels': extreme_red_pixels,
            'magenta_pixels': magenta_pixels,
            'red_dominance_ratio': red_dominance_ratio,
            'recommendations': []
        }
        
        # Add recommendations based on thresholds
        if extreme_red_pixels > 0.02:  # More than 2% extreme red pixels
            self.analysis_results['unrealistic_colors']['recommendations'].append('qc_reduce_red_gain')
            
        if magenta_pixels > 0.01:  # More than 1% magenta pixels
            self.analysis_results['unrealistic_colors']['recommendations'].append('qc_reduce_red_compensation')
            
        if red_dominance_ratio > 1.5:  # Excessive red vs blue ratio
            self.analysis_results['unrealistic_colors']['recommendations'].append('qc_reduce_beer_lambert_red')
    
    def _check_red_channel_analysis(self, img_rgb: np.ndarray):
        """Analyze red channel dominance and distribution"""
        img_float = img_rgb.astype(np.float32) / 255.0
        
        red_channel = img_float[:, :, 0]
        green_channel = img_float[:, :, 1]
        blue_channel = img_float[:, :, 2]
        
        # Calculate channel statistics
        red_mean = np.mean(red_channel)
        green_mean = np.mean(green_channel)  
        blue_mean = np.mean(blue_channel)
        
        # Red vs blue ratio (important for underwater images)
        red_vs_blue_ratio = red_mean / max(blue_mean, 0.01)
        
        # Count red-dominant pixels
        red_dominant_pixels = np.sum(red_channel > np.maximum(green_channel, blue_channel)) / red_channel.size
        
        self.analysis_results['red_channel_analysis'] = {
            'red_vs_blue_ratio': red_vs_blue_ratio,
            'red_dominant_pixels': red_dominant_pixels,
            'channel_means': (red_mean, green_mean, blue_mean),
            'recommendations': []
        }
        
        if red_vs_blue_ratio > 1.8:
            self.analysis_results['red_channel_analysis']['recommendations'].append('qc_excessive_red_compensation')
    
    def _check_saturation_clipping(self, img_hsv: np.ndarray):
        """
        Check for saturation clipping that can lead to loss of detail
        Based on Ancuti et al. fusion method analysis
        """
        # Extract saturation channel (0-255)
        saturation = img_hsv[:, :, 1].astype(np.float32) / 255.0
        
        # Check for highly saturated pixels (potential clipping)
        highly_saturated = np.sum(saturation > 0.9) / saturation.size
        
        # Check for completely saturated pixels (definite clipping)
        clipped_saturation = np.sum(saturation >= 0.99) / saturation.size
        
        # Check for large areas of high saturation (unnatural)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        high_sat_mask = (saturation > 0.85).astype(np.uint8)
        dilated = cv2.dilate(high_sat_mask, kernel, iterations=2)
        large_saturated_areas = np.sum(dilated) / dilated.size
        
        # Calculate mean saturation
        mean_saturation = np.mean(saturation)
        
        self.analysis_results['saturation_analysis'] = {
            'highly_saturated_pixels': highly_saturated,
            'clipped_saturation': clipped_saturation,
            'large_saturated_areas': large_saturated_areas,
            'mean_saturation': mean_saturation,
            'recommendations': []
        }
        
        if clipped_saturation > 0.02:  # More than 2% clipped
            self.analysis_results['saturation_analysis']['recommendations'].append('qc_reduce_saturation')
            
        if highly_saturated > 0.1:  # More than 10% highly saturated
            self.analysis_results['saturation_analysis']['recommendations'].append('qc_reduce_saturation')
    
    def _check_color_noise_amplification(self, original_rgb: np.ndarray, processed_rgb: np.ndarray):
        """
        Detect color noise amplification in low-light areas
        Common issue with aggressive color correction
        """
        # Convert to float
        orig_float = original_rgb.astype(np.float32) / 255.0
        proc_float = processed_rgb.astype(np.float32) / 255.0
        
        # Focus on low-light areas where noise is most problematic
        orig_gray = cv2.cvtColor(original_rgb, cv2.COLOR_RGB2GRAY).astype(np.float32) / 255.0
        low_light_mask = orig_gray < 0.3
        
        if np.sum(low_light_mask) == 0:
            # No low-light areas to analyze
            self.analysis_results['color_noise_analysis'] = {
                'red_noise_amplification': 0.0,
                'green_noise_amplification': 0.0,
                'blue_noise_amplification': 0.0,
                'average_noise_ratio': 1.0,
                'recommendations': []
            }
            return
        
        # Calculate noise amplification per channel
        noise_ratios = []
        
        for i in range(3):
            orig_channel = orig_float[:, :, i]
            proc_channel = proc_float[:, :, i]
            
            # Calculate local variance (noise indicator)
            orig_var = cv2.Laplacian(orig_channel, cv2.CV_32F)
            proc_var = cv2.Laplacian(proc_channel, cv2.CV_32F)
            
            # Focus on low-light areas
            orig_noise = np.var(orig_var[low_light_mask])
            proc_noise = np.var(proc_var[low_light_mask])
            
            noise_ratio = proc_noise / max(orig_noise, 0.001)
            noise_ratios.append(noise_ratio)
        
        self.analysis_results['color_noise_analysis'] = {
            'red_noise_amplification': noise_ratios[0],
            'green_noise_amplification': noise_ratios[1],
            'blue_noise_amplification': noise_ratios[2],
            'average_noise_ratio': np.mean(noise_ratios),
            'recommendations': []
        }
        
        # Check for excessive noise amplification in red channel (most common)
        if noise_ratios[0] > 1.5:  # 50% increase in red noise
            self.analysis_results['color_noise_analysis']['recommendations'].append('qc_apply_noise_reduction')
    
    def _check_halo_artifacts(self, img_bgr: np.ndarray):
        """
        Detect halo artifacts around edges (common with CLAHE and fusion methods)
        Based on Chiang & Chen edge-preserving analysis
        """
        # Convert to grayscale for edge detection
        gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
        
        # Detect edges using Canny
        edges = cv2.Canny(gray, 50, 150)
        
        # Calculate edge gradient strength
        grad_x = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=3)
        grad_y = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=3)
        gradient_magnitude = np.sqrt(grad_x**2 + grad_y**2)
        
        # Dilate edges to create near-edge regions
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        dilated_edges = cv2.dilate(edges, kernel, iterations=1)
        
        # Calculate intensity statistics near edges
        edge_regions = dilated_edges > 0
        non_edge_regions = dilated_edges == 0
        
        if np.sum(edge_regions) == 0:
            halo_indicator = 0.0
            edge_gradient_mean = 0.0
        else:
            edge_intensity_mean = np.mean(gray[edge_regions])
            non_edge_intensity_mean = np.mean(gray[non_edge_regions]) if np.sum(non_edge_regions) > 0 else 0
            
            # Halo indicator: excessive brightness difference near edges
            halo_indicator = abs(edge_intensity_mean - non_edge_intensity_mean) / 255.0
            edge_gradient_mean = np.mean(gradient_magnitude[edge_regions])
        
        overall_gradient_mean = np.mean(gradient_magnitude)
        
        # Check for overshooting near edges
        edge_regions_mask = dilated_edges > 0
        edge_intensity_var = np.var(gray[edge_regions_mask]) if np.sum(edge_regions_mask) > 0 else 0
        
        self.analysis_results['halo_artifacts'] = {
            'halo_indicator': halo_indicator,
            'edge_intensity_variance': edge_intensity_var,
            'edge_gradient_ratio': edge_gradient_mean / max(overall_gradient_mean, 1),
            'recommendations': []
        }
        
        if halo_indicator > 0.15:  # Significant brightness difference near edges
            self.analysis_results['halo_artifacts']['recommendations'].append('qc_reduce_clahe_clip_limit')
    
    def _check_midtone_balance(self, img_lab: np.ndarray):
        """Check for proper midtone balance and shadow detail preservation"""
        L = img_lab[:, :, 0]  # Lightness channel (0-100)
        
        # Define tone ranges
        shadow_mask = L < 25
        midtone_mask = (L >= 25) & (L <= 75)
        highlight_mask = L > 75
        
        # Calculate ratios
        total_pixels = L.size
        shadow_ratio = np.sum(shadow_mask) / total_pixels
        midtone_ratio = np.sum(midtone_mask) / total_pixels
        highlight_ratio = np.sum(highlight_mask) / total_pixels
        
        # Check for shadow detail preservation
        shadow_detail_preserved = True
        if shadow_ratio > 0.1:  # Only check if significant shadow area exists
            shadow_std = np.std(L[shadow_mask])
            if shadow_std < 3.0:  # Very low variation in shadows indicates detail loss
                shadow_detail_preserved = False
        
        # Calculate mean lightness
        mean_lightness = np.mean(L)
        
        self.analysis_results['midtone_balance'] = {
            'shadow_ratio': shadow_ratio,
            'midtone_ratio': midtone_ratio,
            'highlight_ratio': highlight_ratio,
            'mean_lightness': mean_lightness,
            'shadow_detail_preserved': shadow_detail_preserved,
            'recommendations': []
        }
        
        if not shadow_detail_preserved:
            self.analysis_results['midtone_balance']['recommendations'].append('qc_adjust_gamma_shadows')
            
        if midtone_ratio < 0.3:  # Too much contrast, not enough midtones
            self.analysis_results['midtone_balance']['recommendations'].append('qc_reduce_contrast_enhancement')
    
    def _calculate_quality_improvements(self, original: np.ndarray, processed: np.ndarray):
        """Calculate quantitative quality improvements"""
        try:
            # Convert to grayscale for contrast analysis
            orig_gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
            proc_gray = cv2.cvtColor(processed, cv2.COLOR_BGR2GRAY)
            
            # Calculate contrast (standard deviation of pixel intensities)
            orig_contrast = np.std(orig_gray)
            proc_contrast = np.std(proc_gray)
            contrast_improvement = (proc_contrast - orig_contrast) / max(orig_contrast, 1)
            
            # Calculate entropy (measure of information content)
            orig_entropy = self._calculate_entropy(orig_gray)
            proc_entropy = self._calculate_entropy(proc_gray)
            entropy_improvement = (proc_entropy - orig_entropy) / max(orig_entropy, 1)
            
            # Calculate color enhancement (color variance in LAB space)
            orig_lab = cv2.cvtColor(original, cv2.COLOR_BGR2LAB)
            proc_lab = cv2.cvtColor(processed, cv2.COLOR_BGR2LAB)
            
            orig_color_var = np.var(orig_lab[:, :, 1]) + np.var(orig_lab[:, :, 2])  # a* and b* channels
            proc_color_var = np.var(proc_lab[:, :, 1]) + np.var(proc_lab[:, :, 2])
            color_enhancement = (proc_color_var - orig_color_var) / max(orig_color_var, 1)
            
            self.analysis_results['quality_improvements'] = {
                'contrast_improvement': contrast_improvement,
                'entropy_improvement': entropy_improvement,
                'color_enhancement': color_enhancement,
                'original_contrast': orig_contrast,
                'processed_contrast': proc_contrast,
                'recommendations': []
            }
            
            # Add recommendations based on improvements
            if contrast_improvement < 0.05:
                self.analysis_results['quality_improvements']['recommendations'].append('qc_increase_contrast')
            if entropy_improvement < 0.02:
                self.analysis_results['quality_improvements']['recommendations'].append('qc_enhance_detail_preservation')
                
        except Exception as e:
            self.logger.error(f"Error calculating quality improvements: {str(e)}")
            self.analysis_results['quality_improvements'] = {'error': str(e)}
    
    def _calculate_entropy(self, img: np.ndarray) -> float:
        """Calculate image entropy"""
        hist, _ = np.histogram(img, bins=256, range=(0, 256))
        hist = hist[hist > 0]  # Remove zero entries
        prob = hist / hist.sum()
        entropy = -np.sum(prob * np.log2(prob))
        return entropy
    
    def _calculate_overall_score(self, results: Dict[str, Any]) -> float:
        """Calculate overall quality score from 0-10"""
        if 'error' in results:
            return 0.0
        
        scores = []
        
        # Check unrealistic colors (weight: 0.25)
        if 'unrealistic_colors' in results:
            data = results['unrealistic_colors']
            extreme_red = data.get('extreme_red_pixels', 0)
            magenta = data.get('magenta_pixels', 0)
            score = max(0, 10 - extreme_red * 100 - magenta * 50)
            scores.append(score * 0.25)
        
        # Check saturation issues (weight: 0.20)
        if 'saturation_analysis' in results:
            data = results['saturation_analysis']
            clipped = data.get('clipped_saturation', 0)
            highly_sat = data.get('highly_saturated_pixels', 0)
            score = max(0, 10 - clipped * 200 - highly_sat * 50)
            scores.append(score * 0.20)
        
        # Check noise amplification (weight: 0.15)
        if 'color_noise_analysis' in results:
            data = results['color_noise_analysis']
            red_noise = data.get('red_noise_amplification', 0)
            score = max(0, 10 - red_noise * 5)
            scores.append(score * 0.15)
        
        # Check halo artifacts (weight: 0.15)
        if 'halo_artifacts' in results:
            data = results['halo_artifacts']
            halo = data.get('halo_indicator', 0)
            score = max(0, 10 - halo * 50)
            scores.append(score * 0.15)
        
        # Check midtone balance (weight: 0.15)
        if 'midtone_balance' in results:
            data = results['midtone_balance']
            shadow_preserved = data.get('shadow_detail_preserved', True)
            score = 8.0 if shadow_preserved else 3.0
            scores.append(score * 0.15)
        
        # Quality improvements bonus (weight: 0.10)
        if 'quality_improvements' in results:
            data = results['quality_improvements']
            improvements = (
                data.get('contrast_improvement', 0) +
                data.get('entropy_improvement', 0) +
                data.get('color_enhancement', 0)
            )
            score = min(10, max(0, 5 + improvements * 10))
            scores.append(score * 0.10)
        
        return sum(scores) if scores else 5.0
