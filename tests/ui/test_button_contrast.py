#!/usr/bin/env python3
"""
Test de contraste du bouton Analyser
Démontre la différence entre l'ancien style TTK et le nouveau ColoredButton
"""

import tkinter as tk
from tkinter import ttk
import sys
import os

# Ajouter src/ au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.ui_colors import AqualixColors, ColoredButton
from src.localization import LocalizationManager

def create_contrast_demo():
    """Créer une fenêtre de démonstration des contrastes"""
    
    root = tk.Tk()
    root.title("🎨 Test Contraste Bouton Analyser - Aqualix")
    root.geometry("600x400")
    root.configure(bg=AqualixColors.PEARL_WHITE)
    
    # Titre principal
    title = tk.Label(root,
                    text="🔍 Comparaison Contraste Bouton Analyser",
                    font=('Arial', 16, 'bold'),
                    bg=AqualixColors.PEARL_WHITE,
                    fg=AqualixColors.DEEP_NAVY)
    title.pack(pady=20)
    
    # Description
    desc = tk.Label(root,
                   text="Comparaison entre l'ancien style TTK et le nouveau ColoredButton",
                   font=('Arial', 10, 'italic'),
                   bg=AqualixColors.PEARL_WHITE,
                   fg=AqualixColors.MEDIUM_GRAY)
    desc.pack(pady=(0, 30))
    
    # Frame pour les boutons
    buttons_frame = tk.Frame(root, bg=AqualixColors.PEARL_WHITE)
    buttons_frame.pack(pady=20)
    
    # === ANCIEN STYLE TTK ===
    old_frame = tk.LabelFrame(buttons_frame, 
                             text="❌ ANCIEN: Style TTK Accent (Contraste faible)",
                             font=('Arial', 11, 'bold'),
                             bg=AqualixColors.FOAM_WHITE,
                             fg=AqualixColors.DEEP_NAVY,
                             padx=20, pady=20)
    old_frame.pack(side=tk.LEFT, padx=(0, 20), fill=tk.BOTH, expand=True)
    
    # Configuration style TTK pour démonstration
    style = ttk.Style()
    style.configure("Demo.Accent.TButton", 
                   background=AqualixColors.CORAL_ORANGE,
                   foreground="white",
                   font=('Arial', 10))
    
    old_button = ttk.Button(old_frame,
                           text="Analyser (Ancien)",
                           style="Demo.Accent.TButton")
    old_button.pack(pady=10)
    
    old_info = tk.Label(old_frame,
                       text="• Couleur: Orange corail\n• Contraste: Faible\n• Lisibilité: ⚠️  Difficile",
                       justify=tk.LEFT,
                       font=('Arial', 9),
                       bg=AqualixColors.FOAM_WHITE,
                       fg=AqualixColors.DEEP_NAVY)
    old_info.pack(pady=(5, 0))
    
    # === NOUVEAU STYLE COLORED BUTTON ===
    new_frame = tk.LabelFrame(buttons_frame,
                             text="✅ NOUVEAU: ColoredButton Primary (Contraste optimal)",
                             font=('Arial', 11, 'bold'), 
                             bg=AqualixColors.FOAM_WHITE,
                             fg=AqualixColors.DEEP_NAVY,
                             padx=20, pady=20)
    new_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    new_button = ColoredButton(new_frame,
                              text="Analyser (Nouveau)",
                              style_type='primary')
    new_button.pack(pady=10)
    
    new_info = tk.Label(new_frame,
                       text="• Couleur: Bleu océan\n• Contraste: Optimal\n• Lisibilité: ✅ Excellente",
                       justify=tk.LEFT,
                       font=('Arial', 9),
                       bg=AqualixColors.FOAM_WHITE,
                       fg=AqualixColors.DEEP_NAVY)
    new_info.pack(pady=(5, 0))
    
    # === DÉTAILS TECHNIQUES ===
    tech_frame = tk.Frame(root, bg=AqualixColors.PEARL_WHITE)
    tech_frame.pack(fill=tk.X, padx=40, pady=20)
    
    tech_title = tk.Label(tech_frame,
                         text="🔧 Détails Techniques:",
                         font=('Arial', 12, 'bold'),
                         bg=AqualixColors.PEARL_WHITE,
                         fg=AqualixColors.DEEP_NAVY)
    tech_title.pack(anchor=tk.W)
    
    tech_details = tk.Text(tech_frame,
                          height=6,
                          wrap=tk.WORD,
                          font=('Arial', 9),
                          bg=AqualixColors.MIST_BLUE,
                          fg=AqualixColors.DEEP_NAVY,
                          relief=tk.FLAT,
                          padx=10,
                          pady=5)
    tech_details.pack(fill=tk.X, pady=(5, 0))
    
    tech_text = """PROBLÈME RÉSOLU: Le bouton "Analyser" était trop pâle avec le style TTK Accent
    
ANCIEN: ttk.Button avec style="Accent.TButton" 
    → Orange corail (#FF8A65) sur fond clair
    → Contraste insuffisant pour la lisibilité
    
NOUVEAU: ColoredButton avec style_type='primary'
    → Bleu océan (#4A7BA7) avec texte blanc
    → Hover: Océan profond (#2C5282)  
    → Contraste optimal selon standards d'accessibilité"""
    
    tech_details.insert(tk.END, tech_text)
    tech_details.config(state=tk.DISABLED)
    
    # Bouton fermer
    close_button = ColoredButton(root, text="Fermer", command=root.destroy, style_type='secondary')
    close_button.pack(pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    print("🎨 Test de contraste du bouton Analyser")
    print("=" * 50)
    create_contrast_demo()
