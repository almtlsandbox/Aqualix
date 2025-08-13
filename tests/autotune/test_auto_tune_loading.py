#!/usr/bin/env python3
"""
Test rapide pour vérifier que l'auto-tune se déclenche au chargement
"""

import sys
import os
import cv2
import numpy as np

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
sys.path.append(os.path.dirname(__file__))

from src.image_processing import ImageProcessor

def test_auto_tune_on_load():
    """Test que l'auto-tune se déclenche correctement au chargement d'image"""
    print("🧪 TEST AUTO-TUNE AU CHARGEMENT")
    print("=" * 50)
    
    # Créer un processeur d'image
    processor = ImageProcessor()
    
    # Créer une image de test
    test_image = np.random.randint(0, 255, (300, 400, 3), dtype=np.uint8)
    
    # Récupérer les paramètres par défaut
    default_params = processor.get_all_parameters().copy()
    print(f"📊 Paramètres par défaut (quelques exemples):")
    print(f"   • gray_world_percentile: {default_params['gray_world_percentile']}")
    print(f"   • udcp_omega: {default_params['udcp_omega']}")
    print(f"   • beer_lambert_red_coeff: {default_params['beer_lambert_red_coeff']}")
    
    # Simuler l'auto-tune (comme le ferait trigger_auto_tune_for_new_image)
    print(f"\n🔧 SIMULATION AUTO-TUNE...")
    steps_to_tune = ['white_balance', 'udcp', 'beer_lambert']
    
    for step in steps_to_tune:
        print(f"\n   Running auto-tune for {step}...")
        try:
            optimized = processor.auto_tune_step(step, test_image)
            if optimized:
                print(f"   ✅ {step}: {len(optimized)} paramètres optimisés")
                for param, value in optimized.items():
                    if param in default_params and default_params[param] != value:
                        print(f"      • {param}: {default_params[param]} → {value}")
            else:
                print(f"   ⚠️  {step}: Aucun paramètre optimisé")
        except Exception as e:
            print(f"   ❌ {step}: Erreur - {e}")
    
    # Vérifier les paramètres après auto-tune
    final_params = processor.get_all_parameters()
    changes_count = 0
    for param, default_value in default_params.items():
        if final_params[param] != default_value:
            changes_count += 1
    
    print(f"📈 RÉSULTATS:")
    print(f"   • Paramètres modifiés: {changes_count}")
    status = "✅ FONCTIONNE" if changes_count > 0 else "❌ N'A PAS FONCTIONNÉ"
    print(f"   • Auto-tune {status}")
    
    return changes_count > 0

if __name__ == "__main__":
    test_auto_tune_on_load()
