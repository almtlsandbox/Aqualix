"""
Analyse optimisée pour grandes images - IMG_4292.JPG
Utilise un échantillonnage pour accélérer l'analyse
"""

import sys
sys.path.insert(0, '.')

from src.quality_check import PostProcessingQualityChecker
import cv2
import numpy as np
import os

def analyze_large_image_optimized():
    """Analyse optimisée pour les grandes images"""
    print("🔍 ANALYSE OPTIMISÉE - IMG_4292.JPG")
    print("=" * 60)
    
    image_path = r"D:\OneDrive\DOCS\BATEAU-SCUBA\SCUBA\PHOTOS\COLOR CORRECTION\test\IMG_4292.JPG"
    
    if not os.path.exists(image_path):
        print(f"❌ Image non trouvée: {image_path}")
        return
    
    print(f"📸 Chargement de l'image: {os.path.basename(image_path)}")
    
    try:
        # Charger l'image
        img_bgr = cv2.imread(image_path)
        if img_bgr is None:
            print("❌ Impossible de charger l'image")
            return
        
        height, width = img_bgr.shape[:2]
        print(f"   Dimensions originales: {width}x{height} pixels ({height * width:,} pixels)")
        
        # Redimensionner pour l'analyse (plus rapide, mais représentatif)
        max_size = 1200  # Taille maximale pour l'analyse
        if max(height, width) > max_size:
            scale = max_size / max(height, width)
            new_width = int(width * scale)
            new_height = int(height * scale)
            img_resized = cv2.resize(img_bgr, (new_width, new_height), interpolation=cv2.INTER_AREA)
            print(f"   Redimensionnée pour analyse: {new_width}x{new_height} pixels (facteur: {scale:.3f})")
        else:
            img_resized = img_bgr
            new_height, new_width = height, width
        
        # Analyse rapide des couleurs
        print(f"\n🎨 ANALYSE RAPIDE DES COULEURS:")
        img_rgb = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)
        img_float = img_rgb.astype(np.float32) / 255.0
        
        # Statistiques des canaux
        red_channel = img_float[:, :, 0]
        green_channel = img_float[:, :, 1]
        blue_channel = img_float[:, :, 2]
        
        red_mean = np.mean(red_channel)
        green_mean = np.mean(green_channel)
        blue_mean = np.mean(blue_channel)
        
        print(f"   Moyennes RGB: R={red_mean:.3f}, G={green_mean:.3f}, B={blue_mean:.3f}")
        
        # Ratios de balance
        red_green_ratio = red_mean / max(green_mean, 0.001)
        red_blue_ratio = red_mean / max(blue_mean, 0.001)
        
        print(f"   Ratio Rouge/Vert: {red_green_ratio:.2f}")
        print(f"   Ratio Rouge/Bleu: {red_blue_ratio:.2f}")
        
        # Détection manuelle rapide
        print(f"\n🔍 DÉTECTION RAPIDE DES PIXELS ROUGES:")
        red_dominant = (red_channel > 0.45) & (red_channel > green_channel + 0.08) & (red_channel > blue_channel + 0.08)
        red_pixels_ratio = np.sum(red_dominant) / (new_height * new_width)
        
        print(f"   Pixels rouges excessifs: {red_pixels_ratio*100:.2f}%")
        
        # Analyse de la distribution des couleurs
        print(f"\n📊 DISTRIBUTION DES COULEURS:")
        
        # Histogrammes simplifiés
        red_hist = np.histogram(red_channel.flatten(), bins=10, range=(0, 1))[0]
        green_hist = np.histogram(green_channel.flatten(), bins=10, range=(0, 1))[0]
        blue_hist = np.histogram(blue_channel.flatten(), bins=10, range=(0, 1))[0]
        
        # Pixels dans les hautes valeurs (> 0.7)
        high_red = np.sum(red_channel > 0.7) / red_channel.size
        high_green = np.sum(green_channel > 0.7) / green_channel.size
        high_blue = np.sum(blue_channel > 0.7) / blue_channel.size
        
        print(f"   Pixels à haute intensité (>0.7): R={high_red*100:.1f}%, G={high_green*100:.1f}%, B={high_blue*100:.1f}%")
        
        # Échantillons de pixels représentatifs
        print(f"\n🔍 ÉCHANTILLONS DE PIXELS:")
        sample_positions = [
            (new_height//4, new_width//4),      # Quart supérieur gauche
            (new_height//4, 3*new_width//4),    # Quart supérieur droit
            (new_height//2, new_width//2),      # Centre
            (3*new_height//4, new_width//4),    # Quart inférieur gauche
            (3*new_height//4, 3*new_width//4),  # Quart inférieur droit
        ]
        
        for i, (y, x) in enumerate(sample_positions):
            pixel = img_float[y, x]
            detected = (pixel[0] > 0.45) and (pixel[0] > pixel[1] + 0.08) and (pixel[0] > pixel[2] + 0.08)
            region = ["Sup.G", "Sup.D", "Centre", "Inf.G", "Inf.D"][i]
            print(f"      {region}: RGB=[{pixel[0]:.2f}, {pixel[1]:.2f}, {pixel[2]:.2f}] {'🔴' if detected else '⚪'}")
        
        # Interprétation finale
        print(f"\n📋 ÉVALUATION FINALE:")
        
        # Critères d'évaluation
        excessive_red = red_pixels_ratio > 0.05
        moderate_red = 0.02 < red_pixels_ratio <= 0.05
        high_red_dominance = red_blue_ratio > 1.3
        very_high_red_dominance = red_blue_ratio > 1.8
        
        if excessive_red:
            print(f"   🚨 ROUGE EXCESSIF DÉTECTÉ ({red_pixels_ratio*100:.1f}%)")
            print(f"      ✅ La détection est JUSTIFIÉE")
            print(f"      Cette image présente une dominance rouge problématique")
            
            if very_high_red_dominance:
                print(f"      ⚠️  Ratio rouge/bleu très élevé ({red_blue_ratio:.2f}) - correction forte recommandée")
            elif high_red_dominance:
                print(f"      ⚠️  Ratio rouge/bleu élevé ({red_blue_ratio:.2f}) - correction modérée recommandée")
                
        elif moderate_red:
            print(f"   ⚠️  ROUGE MODÉRÉ DÉTECTÉ ({red_pixels_ratio*100:.1f}%)")
            print(f"      ✅ La détection est PARTIELLEMENT justifiée")
            print(f"      L'image pourrait bénéficier d'ajustements légers")
            
        else:
            print(f"   ✅ PAS DE PROBLÈME ROUGE MAJEUR ({red_pixels_ratio*100:.1f}%)")
            print(f"      ❓ Si le système détecte un problème, il pourrait y avoir:")
            print(f"         - Des zones locales non échantillonnées")
            print(f"         - Une sensibilité différente sur l'image complète")
        
        # Contexte sous-marin
        print(f"\n🌊 CONTEXTE SOUS-MARIN:")
        if blue_mean > 0.3:
            env = "Eau relativement claire"
        elif blue_mean > 0.15:
            env = "Eau moyennement profonde"
        else:
            env = "Eau profonde/très colorée"
            
        print(f"   Environnement estimé: {env}")
        
        if red_mean > blue_mean:
            print(f"   ⚠️  Dominance rouge sur bleu - typique des images corrigées ou en eaux colorées")
        else:
            print(f"   ✅ Dominance bleue préservée - image plus naturelle")
            
        return excessive_red or moderate_red
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    analyze_large_image_optimized()
