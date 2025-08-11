#!/usr/bin/env python3
"""
Test pour vérifier que la correction du multiscale fusion fonctionne correctement.
Vérifie que les étapes précédentes influencent bien le résultat final quand fusion est activée.
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

def test_multiscale_fusion_respects_pipeline():
    """Test que la fusion multiscale respecte le pipeline précédent"""
    print("=== Test de la correction Multiscale Fusion ===")
    
    # Créer une image de test
    test_image = create_test_image()
    print(f"Image de test créée: {test_image.shape}")
    
    # Créer le processeur
    processor = ImageProcessor()
    
    # Test 1: Traitement SANS multiscale fusion
    print("\n1. Test SANS multiscale fusion:")
    processor.set_parameter('multiscale_fusion_enabled', False)
    processor.set_parameter('white_balance_enabled', True)
    processor.set_parameter('udcp_enabled', True)
    processor.set_parameter('beer_lambert_enabled', True)
    
    result_without_fusion = processor.process_image(test_image)
    print(f"   Résultat sans fusion - Moyenne R,G,B: {np.mean(result_without_fusion, axis=(0,1))}")
    
    # Test 2: Traitement AVEC multiscale fusion
    print("\n2. Test AVEC multiscale fusion:")
    processor.set_parameter('multiscale_fusion_enabled', True)
    # Les autres paramètres restent identiques
    
    result_with_fusion = processor.process_image(test_image)
    print(f"   Résultat avec fusion - Moyenne R,G,B: {np.mean(result_with_fusion, axis=(0,1))}")
    
    # Test 3: Vérifier la différence
    print("\n3. Analyse des différences:")
    
    # Calculer la différence entre les deux résultats
    diff = np.abs(result_with_fusion.astype(float) - result_without_fusion.astype(float))
    mean_diff = np.mean(diff)
    
    print(f"   Différence moyenne entre les résultats: {mean_diff:.2f}")
    
    # Test 4: Vérifier que la fusion utilise bien le pipeline
    print("\n4. Test avec changement de paramètres:")
    
    # Modifier fortement un paramètre de white balance
    processor.set_parameter('gray_world_percentile', 5)  # Valeur extrême
    processor.set_parameter('gray_world_max_adjustment', 3.0)  # Ajustement fort
    
    result_with_strong_params = processor.process_image(test_image)
    
    # Calculer la différence avec le résultat précédent
    diff_strong = np.abs(result_with_strong_params.astype(float) - result_with_fusion.astype(float))
    mean_diff_strong = np.mean(diff_strong)
    
    print(f"   Différence avec paramètres modifiés: {mean_diff_strong:.2f}")
    
    # Évaluation
    print("\n=== ÉVALUATION ===")
    
    if mean_diff_strong > 5.0:  # Différence significative
        print("✅ SUCCÈS: La multiscale fusion respecte maintenant les étapes du pipeline!")
        print("   Les changements de paramètres influencent le résultat final.")
        return True
    else:
        print("❌ ÉCHEC: La multiscale fusion ignore encore les étapes précédentes.")
        print("   Les changements de paramètres n'ont pas d'effet significatif.")
        return False

if __name__ == "__main__":
    success = test_multiscale_fusion_respects_pipeline()
    exit(0 if success else 1)
