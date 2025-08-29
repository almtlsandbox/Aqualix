"""
Analyse spécifique de l'image IMG_4292.JPG
Vérifie si la détection de rouge excessive est justifiée
"""

import sys
sys.path.insert(0, '.')

from src.quality_check import PostProcessingQualityChecker
import cv2
import numpy as np
import os

def analyze_specific_image():
    """Analyse l'image IMG_4292.JPG pour vérifier la détection de rouge"""
    print("🔍 ANALYSE SPÉCIFIQUE - IMG_4292.JPG")
    print("=" * 60)
    
    image_path = r"D:\OneDrive\DOCS\BATEAU-SCUBA\SCUBA\PHOTOS\COLOR CORRECTION\test\IMG_4292.JPG"
    
    # Vérifier si l'image existe
    if not os.path.exists(image_path):
        print(f"❌ Image non trouvée: {image_path}")
        return
    
    print(f"📸 Chargement de l'image: {os.path.basename(image_path)}")
    
    # Charger l'image
    try:
        img_bgr = cv2.imread(image_path)
        if img_bgr is None:
            print("❌ Impossible de charger l'image")
            return
        
        height, width = img_bgr.shape[:2]
        print(f"   Dimensions: {width}x{height} pixels")
        print(f"   Taille: {height * width:,} pixels au total")
        
        # Analyser avec notre système corrigé
        print(f"\n🔬 ANALYSE AVEC SYSTÈME CORRIGÉ:")
        checker = PostProcessingQualityChecker()
        results = checker.run_all_checks(img_bgr, img_bgr)  # Image originale sans traitement
        
        # Récupérer les résultats de détection de rouge
        red_data = results.get('unrealistic_colors', {})
        red_pixels = red_data.get('extreme_red_pixels', 0)
        magenta_pixels = red_data.get('magenta_pixels', 0)
        red_dominance = red_data.get('red_dominance_ratio', 1.0)
        
        # Score global
        overall_score = checker._calculate_overall_score(results)
        
        print(f"   Pixels rouges extrêmes détectés: {red_pixels*100:.2f}%")
        print(f"   Pixels magenta détectés: {magenta_pixels*100:.2f}%")
        print(f"   Ratio dominance rouge: {red_dominance:.2f}")
        print(f"   Score global: {overall_score:.2f}/10")
        
        # Analyse visuelle des couleurs
        print(f"\n🎨 ANALYSE VISUELLE DES COULEURS:")
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        img_float = img_rgb.astype(np.float32) / 255.0
        
        # Statistiques des canaux
        red_channel = img_float[:, :, 0]
        green_channel = img_float[:, :, 1]
        blue_channel = img_float[:, :, 2]
        
        red_mean = np.mean(red_channel)
        green_mean = np.mean(green_channel)
        blue_mean = np.mean(blue_channel)
        
        print(f"   Moyennes des canaux RGB: R={red_mean:.3f}, G={green_mean:.3f}, B={blue_mean:.3f}")
        
        # Balance des couleurs
        if red_mean > green_mean and red_mean > blue_mean:
            dominance = "Rouge dominant"
        elif green_mean > blue_mean:
            dominance = "Vert dominant"
        else:
            dominance = "Bleu dominant"
        
        print(f"   Balance générale: {dominance}")
        
        # Vérification manuelle des critères
        print(f"\n🔍 VÉRIFICATION MANUELLE DES CRITÈRES:")
        red_dominant_manual = (red_channel > 0.45) & (red_channel > green_channel + 0.08) & (red_channel > blue_channel + 0.08)
        manual_detection = np.sum(red_dominant_manual) / (height * width)
        
        print(f"   Détection manuelle: {manual_detection*100:.2f}%")
        
        # Échantillonnage de pixels
        print(f"\n🔍 ÉCHANTILLONS DE PIXELS:")
        sample_count = 10
        sample_indices = np.random.choice(height * width, sample_count, replace=False)
        
        for i, idx in enumerate(sample_indices[:5]):
            y, x = divmod(idx, width)
            pixel = img_float[y, x]
            
            # Vérifier si ce pixel serait détecté
            detected = (pixel[0] > 0.45) and (pixel[0] > pixel[1] + 0.08) and (pixel[0] > pixel[2] + 0.08)
            
            print(f"      Pixel {i+1}: RGB=[{pixel[0]:.2f}, {pixel[1]:.2f}, {pixel[2]:.2f}] {'🔴' if detected else '⚪'}")
        
        # Interprétation des résultats
        print(f"\n📊 INTERPRÉTATION:")
        
        if red_pixels > 0.05:  # Plus de 5%
            print(f"   🚨 DÉTECTION JUSTIFIÉE: {red_pixels*100:.1f}% de pixels rouges excessifs")
            print(f"      Cette image présente effectivement une dominance rouge problématique")
            print(f"      Recommandation: Réduire le gain du canal rouge ou ajuster la balance des blancs")
        elif red_pixels > 0.02:  # Entre 2% et 5%
            print(f"   ⚠️  DÉTECTION MODÉRÉE: {red_pixels*100:.1f}% de pixels rouges excessifs")
            print(f"      L'image présente quelques zones avec excès de rouge")
            print(f"      Peut nécessiter de légers ajustements")
        else:
            print(f"   ✅ PAS DE PROBLÈME MAJEUR: {red_pixels*100:.1f}% de pixels rouges excessifs")
            print(f"      L'image semble avoir une balance des couleurs acceptable")
            
        # Analyse du type d'image sous-marine
        if blue_mean > 0.4:
            environment = "Eau claire/peu profonde"
        elif blue_mean > 0.2:
            environment = "Eau moyennement profonde"
        else:
            environment = "Eau profonde/trouble"
            
        print(f"\n🌊 CONTEXTE SOUS-MARIN:")
        print(f"   Type d'environnement estimé: {environment}")
        print(f"   Canal bleu moyen: {blue_mean:.2f}")
        
        if red_mean / blue_mean > 1.2:
            print(f"   ⚠️  Ratio rouge/bleu élevé ({red_mean/blue_mean:.2f}) - typique des corrections excessives")
        
        return red_pixels > 0.02  # Retourne True si détection justifiée
        
    except Exception as e:
        print(f"❌ Erreur lors de l'analyse: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    analyze_specific_image()
