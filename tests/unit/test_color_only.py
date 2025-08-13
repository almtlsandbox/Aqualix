#!/usr/bin/env python3
"""
Test ultra-simple pour mesurer juste l'analyse couleur
"""
import time
import sys
import os

# Ajout du répertoire src au PYTHONPATH
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import numpy as np
from src.image_info import ImageInfoExtractor

def test_color_analysis_only():
    """Test SEULEMENT l'analyse couleur avec différentes tailles"""
    
    print("🎨 TEST ANALYSE COULEUR SEULE")
    print("=" * 50)
    
    extractor = ImageInfoExtractor()
    
    # Différentes tailles pour voir l'impact
    test_sizes = [
        (100, 75, "Très petit"),
        (500, 375, "Petit"),  
        (1000, 750, "Moyen"),
        (2000, 1500, "Grand"),
        (3000, 2250, "Très grand")
    ]
    
    for width, height, description in test_sizes:
        pixels = width * height
        print(f"\n📏 {description}: {width}x{height} ({pixels/1000000:.1f}M pixels)")
        
        # Créer une image test simple
        test_image = np.random.randint(0, 256, (height, width, 3), dtype=np.uint8)
        
        # Mesurer SEULEMENT l'analyse couleur
        start_time = time.time()
        try:
            color_analysis = extractor._analyze_colors(test_image)
            duration = time.time() - start_time
            
            print(f"   ⏱️ Temps: {duration * 1000:.1f}ms")
            if duration > 0:
                print(f"   📊 Perf: {pixels / duration / 1000000:.1f}M pixels/sec")
            else:
                print(f"   📊 Perf: Instantané")
            
            if duration > 5.0:
                print(f"   🔴 INACCEPTABLE (>5s)")
                break  # Arrêter si trop lent
            elif duration > 1.0:
                print(f"   🟠 LENT (>1s)")
            elif duration > 0.1:
                print(f"   🟡 Acceptable (<1s)")
            else:
                print(f"   🟢 Rapide (<100ms)")
                
        except Exception as e:
            print(f"   ❌ Erreur: {e}")
            break

if __name__ == "__main__":
    test_color_analysis_only()
