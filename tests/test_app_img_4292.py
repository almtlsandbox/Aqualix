"""
Test direct dans l'application avec IMG_4292.JPG
Pour vérifier si le bug de détection persiste
"""

import sys
sys.path.insert(0, '.')

import tkinter as tk
from src.main import ImageVideoProcessorApp
from src.quality_check import PostProcessingQualityChecker
import cv2
import os

def test_in_app():
    """Test direct dans l'application"""
    print("🎯 TEST DIRECT DANS L'APPLICATION - IMG_4292.JPG")
    print("=" * 60)
    
    image_path = r"D:\OneDrive\DOCS\BATEAU-SCUBA\SCUBA\PHOTOS\COLOR CORRECTION\test\IMG_4292.JPG"
    
    if not os.path.exists(image_path):
        print(f"❌ Image non trouvée: {image_path}")
        return
    
    try:
        # Créer l'application
        root = tk.Tk()
        root.withdraw()  # Cacher la fenêtre
        app = ImageVideoProcessorApp(root)
        
        print("📸 Chargement de l'image dans l'application...")
        
        # Charger l'image comme le ferait l'application
        img_bgr = cv2.imread(image_path)
        if img_bgr is None:
            print("❌ Impossible de charger l'image")
            return
            
        # Simuler le chargement dans l'app
        app.original_image = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        app.current_file = image_path
        
        print(f"   Image chargée: {app.original_image.shape}")
        
        # Test 1: Image originale (sans traitement)
        print(f"\n🔍 TEST 1: Analyse de l'image ORIGINALE (sans traitement)")
        checker = PostProcessingQualityChecker()
        
        # Attention: l'app stocke en RGB, mais quality_check attend BGR
        img_for_analysis = cv2.cvtColor(app.original_image, cv2.COLOR_RGB2BGR)
        results_orig = checker.run_all_checks(img_for_analysis, img_for_analysis)
        
        red_data_orig = results_orig.get('unrealistic_colors', {})
        red_pixels_orig = red_data_orig.get('extreme_red_pixels', 0)
        score_orig = checker._calculate_overall_score(results_orig)
        
        print(f"   Pixels rouges détectés: {red_pixels_orig*100:.2f}%")
        print(f"   Score: {score_orig:.2f}/10")
        
        if red_pixels_orig > 0.02:
            print(f"   🚨 L'APPLICATION DÉTECTE un problème rouge!")
        else:
            print(f"   ✅ L'APPLICATION NE DÉTECTE PAS de problème rouge")
        
        # Test 2: Image après traitement par l'app
        print(f"\n🔍 TEST 2: Analyse après TRAITEMENT par l'application")
        processed_img = app.get_full_resolution_processed_image()
        
        if processed_img is not None:
            # Convertir pour l'analyse
            img_processed_for_analysis = cv2.cvtColor(processed_img, cv2.COLOR_RGB2BGR)
            results_processed = checker.run_all_checks(img_processed_for_analysis, img_for_analysis)
            
            red_data_processed = results_processed.get('unrealistic_colors', {})
            red_pixels_processed = red_data_processed.get('extreme_red_pixels', 0)
            score_processed = checker._calculate_overall_score(results_processed)
            
            print(f"   Pixels rouges après traitement: {red_pixels_processed*100:.2f}%")
            print(f"   Score après traitement: {score_processed:.2f}/10")
            print(f"   Évolution: {red_pixels_processed - red_pixels_orig:+.3f} ({(red_pixels_processed - red_pixels_orig)*100:+.1f}%)")
            
            if red_pixels_processed < red_pixels_orig:
                print(f"   ✅ Le traitement RÉDUIT les problèmes de rouge")
            elif red_pixels_processed > red_pixels_orig:
                print(f"   ⚠️  Le traitement AUGMENTE les problèmes de rouge")
            else:
                print(f"   ➡️  Le traitement n'affecte pas les problèmes de rouge")
        else:
            print(f"   ❌ Impossible de traiter l'image")
        
        # Comparaison avec notre analyse précédente
        print(f"\n📊 COMPARAISON:")
        print(f"   Analyse optimisée précédente: 0.00% rouge")
        print(f"   Application (image originale): {red_pixels_orig*100:.2f}% rouge")
        
        if red_pixels_orig > 0.01:
            print(f"   ❓ CONTRADICTION détectée!")
            print(f"      L'application détecte du rouge là où l'analyse optimisée n'en trouve pas")
            print(f"      Cela peut être dû à:")
            print(f"         • Différence de résolution (analyse vs image complète)")
            print(f"         • Zones locales non échantillonnées")
            print(f"         • Bug de conversion d'image")
        else:
            print(f"   ✅ COHÉRENCE: Les deux analyses concordent")
        
        root.destroy()
        
        return red_pixels_orig > 0.02
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_in_app()
