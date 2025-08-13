#!/usr/bin/env python3
"""
Test de performance du slider - diagnostic des optimisations
"""
import time
import sys
import os
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))

import numpy as np
import tkinter as tk
from tkinter import ttk
from src.ui_components import InteractivePreviewPanel

def create_test_image(width=800, height=600):
    """Crée une image de test colorée"""
    image = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Créer un gradient coloré
    for y in range(height):
        for x in range(width):
            image[y, x] = [
                (x * 255) // width,          # Rouge
                (y * 255) // height,         # Vert  
                ((x + y) * 255) // (width + height)  # Bleu
            ]
    
    return image

def test_slider_performance():
    """Test de performance du slider"""
    root = tk.Tk()
    root.title("Test Performance Slider")
    root.geometry("1000x700")
    
    # Créer le panel interactif
    panel = InteractivePreviewPanel(root)
    panel.pack(fill='both', expand=True)
    
    # Créer des images de test
    print("Création des images de test...")
    original = create_test_image(800, 600)
    processed = create_test_image(800, 600)
    
    # Modifier légèrement l'image traitée
    processed = processed * 0.8  # Plus sombre
    processed = processed.astype(np.uint8)
    
    print("Images créées, chargement dans le panel...")
    
    # Charger les images
    panel.update_images(original, processed, reset_view=True)
    
    # Fonction de test du slider
    def test_slider_movements():
        print("\n=== DÉBUT TEST SLIDER ===")
        
        positions = [0.0, 0.25, 0.5, 0.75, 1.0, 0.5]
        
        for i, pos in enumerate(positions):
            print(f"Test {i+1}/6: Position {pos}")
            start_time = time.time()
            
            # Simuler le mouvement du slider
            panel.on_split_change(pos)
            
            # Forcer l'affichage immédiat
            root.update()
            
            end_time = time.time()
            duration = (end_time - start_time) * 1000  # en ms
            
            print(f"  Temps: {duration:.1f}ms")
            
            # État du cache
            cache_size = len(panel.transformed_cache)
            print(f"  Cache: {cache_size} entrées")
            
            time.sleep(0.1)  # Petite pause entre les tests
        
        print("\n=== TEST ZOOM/ROTATION ===")
        
        # Test zoom
        start_time = time.time()
        panel.zoom_in()
        root.update()
        end_time = time.time()
        print(f"Zoom in: {(end_time - start_time) * 1000:.1f}ms")
        
        # Test rotation
        start_time = time.time()
        panel.rotate_left()
        root.update()
        end_time = time.time()
        print(f"Rotate: {(end_time - start_time) * 1000:.1f}ms")
        
        print(f"\nCache final: {len(panel.transformed_cache)} entrées")
        print("Test terminé - fermez la fenêtre")
    
    # Lancer le test après 1 seconde
    root.after(1000, test_slider_movements)
    
    print("Fenêtre de test ouverte - attendez le début du test...")
    root.mainloop()

if __name__ == "__main__":
    test_slider_performance()
