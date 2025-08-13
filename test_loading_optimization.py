#!/usr/bin/env python3
"""
Test pour vérifier l'optimisation du délai de chargement
"""

import sys
import time
from pathlib import Path

# Assurer le chemin
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_image_info_speed():
    """Test la vitesse d'extraction d'info avec et sans hash"""
    print("🚀 TEST OPTIMISATION CHARGEMENT - ÉLIMINATION DÉLAI MD5")
    print("=" * 65)
    
    try:
        from image_info import ImageInfoExtractor
        
        extractor = ImageInfoExtractor()
        test_image = "test_images/underwater_test.jpg"
        
        if not Path(test_image).exists():
            print(f"❌ Image de test non trouvée: {test_image}")
            return
            
        print(f"📸 Test avec: {test_image}")
        print(f"   Taille: {Path(test_image).stat().st_size / 1024 / 1024:.1f} MB")
        
        # Test mode rapide (sans hash)
        print("\n🚀 Mode RAPIDE (sans MD5 hash):")
        start_time = time.time()
        info_fast = extractor.get_image_info(test_image, include_hash=False)
        fast_time = time.time() - start_time
        print(f"   ⏱️  Temps: {fast_time:.3f} secondes")
        print(f"   📋 Hash MD5: {info_fast['file']['hash_md5']}")
        
        # Test mode complet (avec hash)
        print("\n🐌 Mode COMPLET (avec MD5 hash):")
        start_time = time.time()
        info_full = extractor.get_image_info(test_image, include_hash=True)
        full_time = time.time() - start_time
        print(f"   ⏱️  Temps: {full_time:.3f} secondes")
        print(f"   📋 Hash MD5: {info_full['file']['hash_md5']}")
        
        # Analyse des résultats
        print(f"\n📊 RÉSULTATS:")
        improvement = ((full_time - fast_time) / full_time * 100) if full_time > 0 else 0
        print(f"   🎯 Amélioration: {improvement:.1f}% plus rapide")
        print(f"   ⚡ Gain de temps: {full_time - fast_time:.3f} secondes")
        
        if fast_time < 0.5:
            print("   ✅ Mode rapide < 0.5s - Excellent!")
        elif fast_time < 1.0:
            print("   ⚠️  Mode rapide < 1s - Acceptable")
        else:
            print("   ❌ Mode rapide > 1s - Optimisation nécessaire")
            
        if improvement > 50:
            print("   🎉 OPTIMISATION RÉUSSIE!")
        else:
            print("   🔧 Optimisation partielle")
        
    except Exception as e:
        print(f"❌ Erreur durant le test: {e}")
        import traceback
        traceback.print_exc()

def test_ui_components_integration():
    """Test l'intégration avec ui_components"""
    print(f"\n🔍 TEST INTÉGRATION UI COMPONENTS")
    print("-" * 40)
    
    try:
        import tkinter as tk
        from ui_components import ImageInfoPanel
        
        root = tk.Tk()
        root.withdraw()
        
        # Test création panneau info
        info_panel = ImageInfoPanel(root)
        print("✅ Panneau info créé")
        
        # Test update rapide
        test_image = "test_images/underwater_test.jpg"
        if Path(test_image).exists():
            start_time = time.time()
            info_panel.update_info(test_image, fast_mode=True)
            fast_update_time = time.time() - start_time
            print(f"✅ Update rapide: {fast_update_time:.3f}s")
            
            if fast_update_time < 0.2:
                print("   🎯 UI response < 0.2s - Parfait!")
            else:
                print("   ⚠️  UI response > 0.2s - À améliorer")
        
        root.destroy()
        
    except Exception as e:
        print(f"❌ Erreur test UI: {e}")

if __name__ == "__main__":
    test_image_info_speed()
    test_ui_components_integration()
    
    print("\n" + "=" * 65)
    print("💡 SOLUTION IMPLÉMENTÉE:")
    print("   1. 🚀 Chargement initial RAPIDE (sans MD5)")
    print("   2. 🐌 Calcul MD5 en arrière-plan (après 2s)")
    print("   3. ⚡ Barre progression s'affiche immédiatement")
    print("   4. 👤 Expérience utilisateur optimale")
