#!/usr/bin/env python3
"""
Test détaillé pour comprendre pourquoi la multiscale fusion ne respecte pas le pipeline
"""

import numpy as np
import cv2
from src.image_processing import ImageProcessor

def create_test_image():
    """Créer une image de test avec des couleurs distinctes"""
    # Image 100x100 avec des bandes de couleur
    image = np.zeros((100, 100, 3), dtype=np.uint8)
    
    # Bande rouge
    image[0:33, :, :] = [200, 50, 50]  # Rouge dominant
    
    # Bande verte
    image[33:66, :, :] = [50, 200, 50]  # Vert dominant
    
    # Bande bleue
    image[66:100, :, :] = [50, 50, 200]  # Bleu dominant
    
    return image

def test_pipeline_step_by_step():
    """Test chaque étape du pipeline individuellement"""
    print("=== Test détaillé du pipeline ===")
    
    # Créer une image de test
    test_image = create_test_image()
    print(f"Image originale - Moyenne R,G,B: {np.mean(test_image, axis=(0,1))}")
    
    # Créer le processeur avec paramètres par défaut
    processor = ImageProcessor()
    
    # Désactiver toutes les étapes sauf white balance
    processor.set_parameter('white_balance_enabled', True)
    processor.set_parameter('udcp_enabled', False)
    processor.set_parameter('beer_lambert_enabled', False)
    processor.set_parameter('color_rebalance_enabled', False)
    processor.set_parameter('hist_eq_enabled', False)
    processor.set_parameter('multiscale_fusion_enabled', False)
    
    # Test avec paramètres par défaut
    print("\n1. White balance avec paramètres par défaut:")
    result_default = processor.process_image(test_image)
    print(f"   Résultat - Moyenne R,G,B: {np.mean(result_default, axis=(0,1))}")
    
    # Test avec paramètres modifiés
    print("\n2. White balance avec paramètres modifiés:")
    processor.set_parameter('gray_world_percentile', 5)  # Très différent de 15
    processor.set_parameter('gray_world_max_adjustment', 3.0)  # Très différent de 2.0
    
    result_modified = processor.process_image(test_image)
    print(f"   Résultat - Moyenne R,G,B: {np.mean(result_modified, axis=(0,1))}")
    
    diff = np.abs(result_modified.astype(float) - result_default.astype(float))
    print(f"   Différence: {np.mean(diff):.2f}")
    
    # Maintenant activons la multiscale fusion AVEC les paramètres modifiés
    print("\n3. Même configuration AVEC multiscale fusion:")
    processor.set_parameter('multiscale_fusion_enabled', True)
    
    result_with_fusion = processor.process_image(test_image)
    print(f"   Résultat - Moyenne R,G,B: {np.mean(result_with_fusion, axis=(0,1))}")
    
    # Maintenant remettons les paramètres par défaut mais gardons la fusion
    print("\n4. Fusion AVEC paramètres par défaut (pour comparaison):")
    processor.set_parameter('gray_world_percentile', 15)  # Retour par défaut
    processor.set_parameter('gray_world_max_adjustment', 2.0)  # Retour par défaut
    
    result_fusion_default = processor.process_image(test_image)
    print(f"   Résultat - Moyenne R,G,B: {np.mean(result_fusion_default, axis=(0,1))}")
    
    # Calculer les différences
    diff_fusion = np.abs(result_with_fusion.astype(float) - result_fusion_default.astype(float))
    print(f"   Différence entre fusion avec params modifiés vs défaut: {np.mean(diff_fusion):.2f}")
    
    # Évaluation
    print("\n=== ÉVALUATION ===")
    
    if np.mean(diff_fusion) > 2.0:  # Différence significative
        print("✅ SUCCÈS: La multiscale fusion respecte les changements de paramètres!")
        return True
    else:
        print("❌ ÉCHEC: La multiscale fusion ignore les changements de paramètres.")
        print("   Vérification supplémentaire...")
        
        # Test direct de l'image processed vs variant1
        print("\n=== DÉBOGAGE APPROFONDI ===")
        
        # Créer manuellement une image "processed" différente
        test_processed = test_image.copy()
        test_processed = test_processed.astype(float)
        test_processed[:, :, 0] *= 1.5  # Modifier le rouge
        test_processed[:, :, 1] *= 0.8  # Modifier le vert
        test_processed = np.clip(test_processed, 0, 255).astype(np.uint8)
        
        print(f"Image processed modifiée - Moyenne R,G,B: {np.mean(test_processed, axis=(0,1))}")
        
        # Appeler directement la fusion avec cette image
        fusion_result = processor.multiscale_fusion(test_image, test_processed)
        print(f"Résultat fusion directe - Moyenne R,G,B: {np.mean(fusion_result, axis=(0,1))}")
        
        # Compare with the processed image
        diff_direct = np.abs(fusion_result.astype(float) - test_processed.astype(float))
        print(f"Différence fusion vs processed: {np.mean(diff_direct):.2f}")
        
        return False

if __name__ == "__main__":
    success = test_pipeline_step_by_step()
    exit(0 if success else 1)
