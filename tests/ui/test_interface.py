#!/usr/bin/env python3
"""
Test script pour vérifier les nouvelles fonctionnalités d'interface
"""

import numpy as np
import cv2
from ui_components import InteractivePreviewPanel
import tkinter as tk
from tkinter import ttk

def create_test_image():
    """Créer une image de test simple"""
    # Créer une image colorée de test
    img = np.zeros((400, 600, 3), dtype=np.uint8)
    
    # Ajouter des formes colorées
    cv2.rectangle(img, (50, 50), (200, 150), (255, 0, 0), -1)    # Rectangle rouge
    cv2.rectangle(img, (250, 100), (400, 200), (0, 255, 0), -1)  # Rectangle vert
    cv2.rectangle(img, (450, 150), (550, 250), (0, 0, 255), -1)  # Rectangle bleu
    
    # Ajouter du texte
    cv2.putText(img, "Test Image", (200, 350), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
    
    return img

def main():
    """Test des nouvelles fonctionnalités"""
    root = tk.Tk()
    root.title("Test Interface Aqualix")
    root.geometry("800x600")
    
    # Créer le panneau d'aperçu interactif
    preview_panel = InteractivePreviewPanel(root)
    preview_panel.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Créer une image de test
    test_img = create_test_image()
    processed_img = cv2.GaussianBlur(test_img, (15, 15), 0)  # Image traitée avec flou
    
    # Mettre à jour les images
    preview_panel.update_images(test_img, processed_img)
    
    # Instructions
    info_frame = ttk.Frame(root)
    info_frame.pack(fill=tk.X, padx=10, pady=5)
    
    instructions = ttk.Label(
        info_frame, 
        text="Test des nouvelles fonctionnalités:\n• Bouton 'Ajuster' : Adapte l'image au canvas\n• Bouton '1:1' : Vue à l'échelle 1:1\n• Auto-fit : L'image devrait s'ajuster automatiquement au chargement",
        justify=tk.LEFT,
        font=('Arial', 9)
    )
    instructions.pack(pady=5)
    
    root.mainloop()

if __name__ == "__main__":
    main()
