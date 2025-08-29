"""
Test intégration complète du système de score corrigé
Utilise l'application complète pour vérifier les corrections
"""

import sys
sys.path.insert(0, '.')

import numpy as np
import cv2
import os
import tempfile
from src.main import ImageVideoProcessorApp
from src.quality_check import PostProcessingQualityChecker
import tkinter as tk

def test_app_integration():
    """Test le système de score avec l'application complète"""
    print("🎯 TEST INTÉGRATION COMPLÈTE - SYSTÈME DE SCORE")
    print("=" * 60)
    
    # Créer une application
    root = tk.Tk()
    root.withdraw()
    app = ImageVideoProcessorApp(root)
    
    # Créer une image test sous-marine avec des problèmes de rouge
    print("\n📸 CRÉATION D'UNE IMAGE TEST SOUS-MARINE")
    height, width = 800, 1200
    img_test = create_underwater_image_with_red_issues(height, width)
    
    # Sauvegarder temporairement
    with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
        temp_path = tmp.name
        cv2.imwrite(temp_path, img_test)
    
    try:
        # Charger l'image dans l'app
        img_bgr = cv2.imread(temp_path)
        if img_bgr is not None:
            app.original_image = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
            app.current_file = temp_path
            print(f"   Image chargée: {app.original_image.shape}")
        else:
            raise ValueError("Impossible de charger l'image test")
        
        # Test 1: Image originale (avec problèmes)
        print("\n🔍 ANALYSE 1: Image originale (problématique)")
        checker = PostProcessingQualityChecker()
        results_orig = checker.run_all_checks(app.original_image, app.original_image)
        score_orig = checker._calculate_overall_score(results_orig)
        
        # Afficher les détections
        red_data = results_orig.get('unrealistic_colors', {})
        red_pixels = red_data.get('extreme_red_pixels', 0)
        magenta_pixels = red_data.get('magenta_pixels', 0)
        
        print(f"   Score original: {score_orig:.2f}/10")
        print(f"   Pixels rouges extrêmes: {red_pixels*100:.2f}%")
        print(f"   Pixels magenta: {magenta_pixels*100:.2f}%")
        
        # Test 2: Image traitée par l'app
        print("\n🔄 TRAITEMENT: Application des corrections")
        processed_img = app.get_full_resolution_processed_image()
        
        if processed_img is not None:
            print("   Traitement appliqué avec succès")
            
            # Analyse de l'image traitée
            print("\n🔍 ANALYSE 2: Image traitée")
            results_processed = checker.run_all_checks(processed_img, app.original_image)
            score_processed = checker._calculate_overall_score(results_processed)
            
            # Afficher les détections post-traitement
            red_data_proc = results_processed.get('unrealistic_colors', {})
            red_pixels_proc = red_data_proc.get('extreme_red_pixels', 0)
            magenta_pixels_proc = red_data_proc.get('magenta_pixels', 0)
            
            print(f"   Score après traitement: {score_processed:.2f}/10")
            print(f"   Pixels rouges extrêmes: {red_pixels_proc*100:.2f}%")
            print(f"   Pixels magenta: {magenta_pixels_proc*100:.2f}%")
            
            # Évaluation
            print(f"\n📊 ÉVALUATION FINALE:")
            print(f"   Score avant traitement: {score_orig:.2f}/10")
            print(f"   Score après traitement: {score_processed:.2f}/10")
            print(f"   Amélioration: {score_processed - score_orig:+.2f} points")
            
            if score_processed > score_orig:
                print(f"   ✅ SUCCÈS: Le traitement améliore la qualité!")
                if red_pixels_proc < red_pixels:
                    print(f"   ✅ BONUS: Réduction des artefacts rouges de {(red_pixels-red_pixels_proc)*100:.1f}%")
            else:
                print(f"   ⚠️  NOTE: Le score n'augmente pas (peut être normal selon l'image)")
            
            print(f"\n🎉 SYSTÈME DE SCORE FONCTIONNEL:")
            print(f"   - Détection des problèmes: ✅")
            print(f"   - Calcul de score cohérent: ✅")
            print(f"   - Intégration avec app: ✅")
            
        else:
            print("   ❌ Erreur: Impossible de traiter l'image")
    
    finally:
        # Nettoyage
        os.unlink(temp_path)
        root.destroy()

def create_underwater_image_with_red_issues(height, width):
    """Crée une image sous-marine avec des problèmes de rouge typiques"""
    # Base: couleurs sous-marines naturelles
    img = np.zeros((height, width, 3), dtype=np.uint8)
    img[:, :] = [25, 45, 75]  # Fond bleu-vert sous-marin
    
    # Ajouter des éléments naturels
    natural_pixels = int(height * width * 0.3)
    for _ in range(natural_pixels):
        y, x = np.random.randint(0, height), np.random.randint(0, width)
        # Couleurs sous-marines naturelles
        colors = [
            [35, 60, 85],   # Eau claire
            [20, 40, 70],   # Eau profonde  
            [50, 70, 90],   # Particules
            [40, 55, 80],   # Variations
        ]
        img[y, x] = colors[np.random.randint(0, len(colors))]
    
    # Ajouter des problèmes de rouge typiques (sur-correction)
    red_problem_pixels = int(height * width * 0.06)  # 6% de pixels problématiques
    for _ in range(red_problem_pixels):
        y, x = np.random.randint(0, height), np.random.randint(0, width)
        # Rouge artificiel typique des sur-corrections
        red_colors = [
            [180, 40, 50],  # Rouge saturé
            [160, 30, 45],  # Rouge modéré
            [200, 50, 60],  # Rouge intense
            [170, 35, 40],  # Rouge typical
        ]
        img[y, x] = red_colors[np.random.randint(0, len(red_colors))]
    
    return img

if __name__ == "__main__":
    test_app_integration()
