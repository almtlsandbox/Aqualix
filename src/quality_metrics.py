#!/usr/bin/env python3
"""
Quality Metrics Integration pour Auto-Tune Aqualix
Système d'optimisation basé sur métriques de qualité d'image
Étape 4 du plan d'amélioration auto-tune
"""

import numpy as np
import cv2
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass
import math

@dataclass
class QualityMetrics:
    """Structure pour stocker les métriques de qualité d'image"""
    contrast: float = 0.0
    sharpness: float = 0.0
    saturation: float = 0.0
    brightness: float = 0.0
    noise_level: float = 0.0
    color_cast: float = 0.0
    underwater_visibility: float = 0.0
    detail_preservation: float = 0.0
    overall_quality: float = 0.0

@dataclass
class OptimizationResult:
    """Résultat d'optimisation auto-tune basé sur métriques"""
    original_metrics: QualityMetrics
    optimized_params: Dict[str, Any]
    predicted_improvement: float
    algorithm: str
    confidence: float

class QualityMetricsAnalyzer:
    """
    Analyseur de métriques de qualité pour l'optimisation auto-tune
    Basé sur recherche en traitement d'image sous-marine
    """
    
    def __init__(self):
        """Initialise l'analyseur de métriques"""
        self.weights = {
            'contrast': 0.20,
            'sharpness': 0.15,
            'saturation': 0.15,
            'brightness': 0.10,
            'noise_level': 0.10,
            'color_cast': 0.15,
            'underwater_visibility': 0.10,
            'detail_preservation': 0.05
        }
    
    def analyze_image_quality(self, img: np.ndarray) -> QualityMetrics:
        """
        Analyse complète de la qualité d'image
        
        Args:
            img: Image numpy array (BGR)
            
        Returns:
            QualityMetrics avec toutes les métriques calculées
        """
        try:
            if img is None or img.size == 0:
                return QualityMetrics()
            
            img_float = img.astype(np.float32) / 255.0
            h, w = img.shape[:2]
            
            metrics = QualityMetrics()
            
            # 1. Contrast Analysis (RMS Contrast)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255.0
            mean_luminance = np.mean(gray)
            metrics.contrast = np.sqrt(np.mean((gray - mean_luminance) ** 2))
            
            # 2. Sharpness Analysis (Variance of Laplacian)
            laplacian = cv2.Laplacian(gray, cv2.CV_64F)
            metrics.sharpness = laplacian.var()
            
            # 3. Saturation Analysis
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            saturation = hsv[:,:,1].astype(np.float32) / 255.0
            metrics.saturation = float(np.mean(saturation))
            
            # 4. Brightness Analysis
            metrics.brightness = float(mean_luminance)
            
            # 5. Noise Level Estimation (High-frequency content)
            try:
                kernel_high = np.array([[-1,-1,-1], [-1,8,-1], [-1,-1,-1]], dtype=np.float32)
                noise_map = cv2.filter2D(gray, cv2.CV_32F, kernel_high)
                metrics.noise_level = float(np.std(noise_map))
            except cv2.error:
                # Fallback simple pour estimation du bruit
                metrics.noise_level = float(np.std(gray))
            
            # 6. Color Cast Analysis (Underwater specific)
            b_channel = img_float[:,:,0]  # Blue
            g_channel = img_float[:,:,1]  # Green  
            r_channel = img_float[:,:,2]  # Red
            
            b_mean, g_mean, r_mean = np.mean(b_channel), np.mean(g_channel), np.mean(r_channel)
            
            # Color cast severity (deviation from neutral)
            neutral_target = (r_mean + g_mean + b_mean) / 3.0
            color_deviation = abs(b_mean - neutral_target) + abs(g_mean - neutral_target) + abs(r_mean - neutral_target)
            metrics.color_cast = float(color_deviation / 3.0)
            
            # 7. Underwater Visibility Metric
            # Based on overall clarity and blue/green dominance
            blue_dominance = b_mean / (r_mean + g_mean + b_mean + 1e-6)
            green_dominance = g_mean / (r_mean + g_mean + b_mean + 1e-6)
            
            # High blue/green = poor visibility, balanced = good visibility
            visibility_penalty = abs(blue_dominance - 0.33) + abs(green_dominance - 0.33)
            metrics.underwater_visibility = float(max(0, 1.0 - visibility_penalty * 3.0))
            
            # 8. Detail Preservation (Local standard deviation)
            try:
                kernel = np.ones((5,5), np.float32) / 25
                local_mean = cv2.filter2D(gray, cv2.CV_32F, kernel)
                local_variance = cv2.filter2D(gray**2, cv2.CV_32F, kernel) - local_mean**2
                metrics.detail_preservation = float(np.mean(np.sqrt(np.maximum(local_variance, 0))))
            except cv2.error:
                # Fallback si filter2D échoue
                metrics.detail_preservation = float(np.std(gray))
            
            # 9. Overall Quality Score (weighted combination)
            metrics.overall_quality = self._calculate_overall_quality(metrics)
            
            return metrics
            
        except Exception as e:
            print(f"Erreur analyse qualité: {e}")
            return QualityMetrics()
    
    def _calculate_overall_quality(self, metrics: QualityMetrics) -> float:
        """Calcule le score de qualité global pondéré"""
        
        # Normalisation des métriques (0-1)
        contrast_norm = min(1.0, metrics.contrast * 4.0)  # RMS contrast is typically 0-0.25
        sharpness_norm = min(1.0, metrics.sharpness / 100.0)  # Laplacian variance normalization
        saturation_norm = metrics.saturation  # Already 0-1
        brightness_norm = 1.0 - abs(metrics.brightness - 0.5) * 2.0  # Penalize extreme brightness
        noise_norm = max(0, 1.0 - metrics.noise_level * 10.0)  # Low noise = high score
        color_cast_norm = max(0, 1.0 - metrics.color_cast * 5.0)  # Low color cast = high score
        visibility_norm = metrics.underwater_visibility  # Already 0-1
        detail_norm = min(1.0, metrics.detail_preservation * 5.0)
        
        # Score pondéré
        overall = (
            self.weights['contrast'] * contrast_norm +
            self.weights['sharpness'] * sharpness_norm +
            self.weights['saturation'] * saturation_norm +
            self.weights['brightness'] * brightness_norm +
            self.weights['noise_level'] * noise_norm +
            self.weights['color_cast'] * color_cast_norm +
            self.weights['underwater_visibility'] * visibility_norm +
            self.weights['detail_preservation'] * detail_norm
        )
        
        return max(0.0, min(1.0, overall))

class QualityBasedAutoTuneOptimizer:
    """
    Optimiseur auto-tune basé sur métriques de qualité
    Intègre analyse qualité avec optimisation paramètres
    """
    
    def __init__(self, image_processor, quality_analyzer: QualityMetricsAnalyzer):
        """
        Initialise l'optimiseur qualité-basé
        
        Args:
            image_processor: Instance ImageProcessor
            quality_analyzer: Analyseur de métriques
        """
        self.processor = image_processor
        self.quality_analyzer = quality_analyzer
        self.optimization_history = []
    
    def optimize_algorithm_parameters(self, img: np.ndarray, algorithm: str, 
                                    target_improvements: Optional[Dict[str, float]] = None) -> OptimizationResult:
        """
        Optimise les paramètres d'un algorithme basé sur métriques de qualité
        
        Args:
            img: Image numpy array
            algorithm: Nom de l'algorithme à optimiser
            target_improvements: Améliorations cibles par métrique
            
        Returns:
            Résultat d'optimisation avec paramètres optimisés
        """
        if target_improvements is None:
            target_improvements = {
                'contrast': 0.1,
                'saturation': 0.15,
                'underwater_visibility': 0.2,
                'color_cast': -0.1  # Réduction souhaitée
            }
        
        # Analyse qualité initiale
        original_metrics = self.quality_analyzer.analyze_image_quality(img)
        
        # Obtenir le mapper auto-tune
        mapper = self.processor.get_autotune_mapper()
        if mapper is None:
            return OptimizationResult(
                original_metrics=original_metrics,
                optimized_params={},
                predicted_improvement=0.0,
                algorithm=algorithm,
                confidence=0.0
            )
        
        # Exécuter auto-tune standard pour base
        base_params = mapper.execute_auto_tune(algorithm, img, enhanced=False)
        enhanced_params = mapper.execute_auto_tune(algorithm, img, enhanced=True)
        
        # Analyser quel mode donne de meilleurs résultats prédits
        predicted_improvement_std = self._predict_improvement(original_metrics, base_params, algorithm)
        predicted_improvement_enh = self._predict_improvement(original_metrics, enhanced_params, algorithm)
        
        if predicted_improvement_enh > predicted_improvement_std:
            optimized_params = enhanced_params
            predicted_improvement = predicted_improvement_enh
            confidence = 0.8
        else:
            optimized_params = base_params
            predicted_improvement = predicted_improvement_std
            confidence = 0.6
        
        # Ajustements spécifiques basés sur métriques
        optimized_params = self._refine_parameters_by_metrics(
            optimized_params, original_metrics, algorithm, target_improvements
        )
        
        # Recalcul de l'amélioration prédite après ajustements
        final_predicted_improvement = self._predict_improvement(original_metrics, optimized_params, algorithm)
        
        result = OptimizationResult(
            original_metrics=original_metrics,
            optimized_params=optimized_params,
            predicted_improvement=final_predicted_improvement,
            algorithm=algorithm,
            confidence=min(1.0, confidence + 0.1)
        )
        
        self.optimization_history.append(result)
        return result
    
    def _predict_improvement(self, metrics: QualityMetrics, params: Dict[str, Any], algorithm: str) -> float:
        """Prédit l'amélioration de qualité basée sur les paramètres"""
        
        if not params:
            return 0.0
        
        improvement = 0.0
        
        # Prédictions spécifiques par algorithme
        if algorithm == 'white_balance':
            # White balance améliore color_cast et saturation
            if metrics.color_cast > 0.2:
                improvement += 0.15 * min(1.0, metrics.color_cast * 2.0)
            if metrics.saturation < 0.4:
                improvement += 0.1 * (0.4 - metrics.saturation) * 2.0
                
        elif algorithm == 'udcp':
            # UDCP améliore contrast et underwater_visibility
            if metrics.contrast < 0.3:
                improvement += 0.2 * (0.3 - metrics.contrast) * 3.0
            if metrics.underwater_visibility < 0.6:
                improvement += 0.15 * (0.6 - metrics.underwater_visibility) * 2.0
                
        elif algorithm == 'beer_lambert':
            # Beer-Lambert améliore color_cast et brightness
            if metrics.color_cast > 0.15:
                improvement += 0.12 * metrics.color_cast * 2.0
            if abs(metrics.brightness - 0.5) > 0.2:
                improvement += 0.08 * abs(metrics.brightness - 0.5) * 2.0
                
        elif algorithm == 'color_rebalance':
            # Color rebalancing améliore saturation et color_cast
            if metrics.saturation < 0.5:
                improvement += 0.18 * (0.5 - metrics.saturation) * 2.0
            improvement += 0.1 * metrics.color_cast
            
        elif algorithm == 'histogram_equalization':
            # Hist EQ améliore contrast et detail_preservation
            if metrics.contrast < 0.25:
                improvement += 0.15 * (0.25 - metrics.contrast) * 4.0
            improvement += 0.05 * (1.0 - metrics.detail_preservation)
            
        elif algorithm == 'multiscale_fusion':
            # Multiscale fusion améliore sharpness et detail_preservation
            improvement += 0.1 * max(0, 0.5 - metrics.sharpness / 100.0)
            improvement += 0.08 * (1.0 - metrics.detail_preservation)
        
        return min(0.5, improvement)  # Cap à 50% d'amélioration prédite
    
    def _refine_parameters_by_metrics(self, params: Dict[str, Any], metrics: QualityMetrics, 
                                    algorithm: str, targets: Dict[str, float]) -> Dict[str, Any]:
        """Affine les paramètres basés sur les métriques actuelles"""
        
        refined_params = params.copy()
        
        # Ajustements spécifiques par algorithme
        if algorithm == 'white_balance' and params:
            # Ajuster l'intensité selon le color_cast
            if metrics.color_cast > 0.3:  # Fort color cast
                if 'gray_world_max_adjustment' in refined_params:
                    refined_params['gray_world_max_adjustment'] = min(3.0, 
                        refined_params.get('gray_world_max_adjustment', 1.5) * 1.3)
                        
        elif algorithm == 'udcp' and params:
            # Ajuster omega selon visibility
            if metrics.underwater_visibility < 0.4:  # Faible visibilité
                if 'udcp_omega' in refined_params:
                    refined_params['udcp_omega'] = min(0.95, 
                        refined_params.get('udcp_omega', 0.8) + 0.1)
                        
        elif algorithm == 'beer_lambert' and params:
            # Ajuster coefficients selon color dominance
            b_r_ratio = getattr(metrics, 'blue_red_ratio', 1.0)  # Would need to calculate this
            if 'beer_lambert_red_coeff' in refined_params and b_r_ratio > 1.5:
                refined_params['beer_lambert_red_coeff'] = min(2.0,
                    refined_params.get('beer_lambert_red_coeff', 0.6) * 1.2)
                    
        elif algorithm == 'histogram_equalization' and params:
            # Ajuster clip_limit selon noise
            if metrics.noise_level > 0.15:  # Image bruitée
                if 'hist_eq_clip_limit' in refined_params:
                    refined_params['hist_eq_clip_limit'] = max(1.0,
                        refined_params.get('hist_eq_clip_limit', 2.0) * 0.8)
        
        return refined_params
    
    def optimize_full_pipeline(self, img: np.ndarray, 
                             algorithms: Optional[List[str]] = None) -> Dict[str, OptimizationResult]:
        """
        Optimise un pipeline complet d'algorithmes basé sur métriques
        
        Args:
            img: Image numpy array
            algorithms: Liste des algorithmes (None = tous)
            
        Returns:
            Dict {algorithm: OptimizationResult}
        """
        if algorithms is None:
            algorithms = ['white_balance', 'udcp', 'beer_lambert', 'color_rebalance', 
                         'histogram_equalization', 'multiscale_fusion']
        
        results = {}
        
        print(f"\n🎯 OPTIMISATION QUALITY-BASED PIPELINE")
        print("=" * 50)
        
        # Analyse qualité initiale
        initial_metrics = self.quality_analyzer.analyze_image_quality(img)
        print(f"📊 Qualité initiale: {initial_metrics.overall_quality:.3f}")
        print(f"   • Contrast: {initial_metrics.contrast:.3f}")
        print(f"   • Saturation: {initial_metrics.saturation:.3f}")
        print(f"   • Color Cast: {initial_metrics.color_cast:.3f}")
        print(f"   • Visibility: {initial_metrics.underwater_visibility:.3f}")
        
        for algorithm in algorithms:
            print(f"\n🔧 Optimisation {algorithm}")
            print("-" * 30)
            
            result = self.optimize_algorithm_parameters(img, algorithm)
            results[algorithm] = result
            
            print(f"   📈 Amélioration prédite: +{result.predicted_improvement:.2%}")
            print(f"   🎯 Confiance: {result.confidence:.2%}")
            print(f"   ⚙️  Paramètres: {len(result.optimized_params)}")
        
        # Résumé global
        total_improvement = sum(r.predicted_improvement for r in results.values())
        avg_confidence = np.mean([r.confidence for r in results.values()])
        
        print(f"\n📊 RÉSUMÉ OPTIMISATION:")
        print(f"   • Amélioration totale prédite: +{total_improvement:.2%}")
        print(f"   • Confiance moyenne: {avg_confidence:.2%}")
        print(f"   • Algorithmes optimisés: {len(results)}")
        
        return results

def create_quality_metrics_system(image_processor):
    """
    Factory function pour créer le système de métriques de qualité
    
    Args:
        image_processor: Instance ImageProcessor
        
    Returns:
        Tuple (QualityMetricsAnalyzer, QualityBasedAutoTuneOptimizer)
    """
    analyzer = QualityMetricsAnalyzer()
    optimizer = QualityBasedAutoTuneOptimizer(image_processor, analyzer)
    return analyzer, optimizer
