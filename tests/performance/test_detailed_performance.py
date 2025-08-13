#!/usr/bin/env python3
"""
Test détaillé de performance des composants d'information image
"""
import time
import sys
import os

# Ajout du répertoire src au PYTHONPATH
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import numpy as np
from src.image_info import ImageInfoExtractor
import cv2
from pathlib import Path

def create_realistic_test_image(filepath, width=2000, height=1500):
    """Crée une image de test réaliste mais plus petite"""
    print(f"Création d'une image de test {width}x{height} pixels...")
    
    # Créer une image colorée réaliste (plus petite pour test rapide)
    image = np.random.randint(0, 256, (height, width, 3), dtype=np.uint8)
    
    # Ajouter des patterns réalistes avec des valeurs sécurisées
    for y in range(0, height, 10):  # Échantillonnage pour accélérer
        for x in range(0, width, 10):
            # Gradient bleu-vert sous-marin avec valeurs bornées
            blue_base = max(0, min(255, int(60 + (y / height) * 80)))
            green_base = max(0, min(255, int(40 + (x / width) * 60)))
            red_base = max(0, min(255, int(10 + abs(np.sin(x * 0.01)) * 20)))
            
            # Appliquer à un bloc 10x10
            image[y:y+10, x:x+10] = [red_base, green_base, blue_base]
    
    # Sauvegarder l'image
    cv2.imwrite(filepath, image)
    print(f"Image créée: {filepath}")
    return image

def test_individual_components():
    """Test chaque composant individuellement"""
    
    test_image_path = "test_components.jpg"
    
    try:
        # Créer une image de test plus petite mais réaliste
        test_image = create_realistic_test_image(test_image_path, width=2000, height=1500)
        
        extractor = ImageInfoExtractor()
        image_path = Path(test_image_path)
        
        print(f"\n=== TEST COMPOSANTS INDIVIDUELS ===")
        print(f"Image: {test_image_path} (2000x1500 = 3M pixels)")
        
        # Test 1: Informations fichier (sans hash)
        print("\n1. 📁 Informations fichier:")
        start_time = time.time()
        file_info = extractor._get_file_info(image_path, include_hash=False)
        duration = time.time() - start_time
        print(f"   Durée: {duration * 1000:.1f}ms")
        print(f"   Taille: {file_info['size']}")
        
        # Test 2: Hash MD5
        print("\n2. 🔒 Hash MD5:")
        start_time = time.time()
        hash_value = extractor._get_file_hash(image_path)
        duration = time.time() - start_time
        print(f"   Durée: {duration * 1000:.1f}ms")
        print(f"   Hash: {hash_value}")
        
        # Test 3: Propriétés image (dimensions, format)
        print("\n3. 📐 Propriétés image:")
        start_time = time.time()
        props = extractor._get_image_properties(image_path)
        duration = time.time() - start_time
        print(f"   Durée: {duration * 1000:.1f}ms")
        print(f"   Dimensions: {props.get('width')}x{props.get('height')}")
        
        # Test 4: Données EXIF
        print("\n4. 📷 Données EXIF:")
        start_time = time.time()
        exif_data = extractor._get_exif_data(image_path)
        duration = time.time() - start_time
        print(f"   Durée: {duration * 1000:.1f}ms")
        print(f"   EXIF brut: {len(exif_data.get('raw_exif', {}))} entrées")
        
        # Test 5: Analyse couleur (LE SUSPECT PRINCIPAL)
        print("\n5. 🎨 Analyse couleur (SUSPECT):")
        start_time = time.time()
        color_analysis = extractor._analyze_colors(test_image)
        duration = time.time() - start_time
        print(f"   Durée: {duration * 1000:.1f}ms ⚠️")
        print(f"   Luminosité: {color_analysis.get('brightness')}")
        print(f"   Contraste: {color_analysis.get('contrast')}")
        
        # Test 6: Rechargement image pour analyse couleur
        print("\n6. 🖼️ Rechargement image (cv2.imread):")
        start_time = time.time()
        img = cv2.imread(str(image_path))
        img_rgb = None
        if img is not None:
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        duration = time.time() - start_time
        print(f"   Durée: {duration * 1000:.1f}ms")
        print(f"   Image rechargée: {img.shape if img is not None else 'Échec'}")
        
        # Test 7: Analyse couleur sur image rechargée
        print("\n7. 🎨 Analyse couleur (sur image rechargée):")
        if img is not None and img_rgb is not None:
            start_time = time.time()
            color_analysis2 = extractor._analyze_colors(img_rgb)
            duration = time.time() - start_time
            print(f"   Durée: {duration * 1000:.1f}ms ⚠️")
            print(f"   Luminosité: {color_analysis2.get('brightness')}")
        
        print(f"\n📊 DIAGNOSTIC:")
        print(f"   • Si 'Analyse couleur' > 1000ms → C'EST LE PROBLÈME")
        print(f"   • Si 'Hash MD5' > 500ms → Problème secondaire")
        print(f"   • Si 'EXIF' > 200ms → Optimisable")
        
    finally:
        # Nettoyer
        if os.path.exists(test_image_path):
            os.remove(test_image_path)
            print(f"\nFichier de test supprimé: {test_image_path}")

def test_color_analysis_detail():
    """Test détaillé de l'analyse couleur pour identifier les opérations lentes"""
    print(f"\n=== ANALYSE DÉTAILLÉE - ANALYSE COULEUR ===")
    
    # Créer différentes tailles d'image pour voir l'impact
    sizes = [
        (500, 375),    # Petite - 0.2M pixels
        (1000, 750),   # Moyenne - 0.75M pixels 
        (2000, 1500),  # Grande - 3M pixels
        (4000, 3000)   # Très grande - 12M pixels
    ]
    
    for width, height in sizes:
        pixels = width * height
        print(f"\n📏 Test {width}x{height} ({pixels/1000000:.1f}M pixels):")
        
        # Créer image test
        test_image = np.random.randint(0, 256, (height, width, 3), dtype=np.uint8)
        
        extractor = ImageInfoExtractor()
        
        start_time = time.time()
        color_analysis = extractor._analyze_colors(test_image)
        duration = time.time() - start_time
        
        print(f"   Analyse couleur: {duration * 1000:.1f}ms")
        print(f"   Performance: {pixels / duration / 1000000:.1f}M pixels/sec")
        
        if duration > 1.0:
            print(f"   ⚠️ TROP LENT pour UX réactive!")
        elif duration > 0.1:
            print(f"   ⚡ Acceptable mais optimisable")
        else:
            print(f"   ✅ Rapide")

if __name__ == "__main__":
    print("🧪 DIAGNOSTIC DÉTAILLÉ - COMPOSANTS PANNEAU INFOS")
    print("=" * 60)
    
    print("\n1️⃣ Test des composants individuels...")
    test_individual_components()
    
    print("\n2️⃣ Test d'impact taille image sur analyse couleur...")
    test_color_analysis_detail()
