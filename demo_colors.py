#!/usr/bin/env python3
"""
Démonstration des couleurs Aqualix
Affiche un aperçu de toutes les couleurs de la palette aquatique
"""

import tkinter as tk
import sys
import os

# Ajouter src/ au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.ui_colors import AqualixColors, ColoredFrame, ColoredButton

def create_color_demo():
    """Créer une fenêtre de démonstration des couleurs"""
    
    root = tk.Tk()
    root.title("🎨 Démonstration Palette Aquatique Aqualix")
    root.geometry("800x700")
    root.configure(bg=AqualixColors.PEARL_WHITE)
    
    # Titre principal
    title = tk.Label(root,
                    text="🌊 Palette Aquatique Aqualix",
                    font=('Arial', 18, 'bold'),
                    bg=AqualixColors.PEARL_WHITE,
                    fg=AqualixColors.DEEP_NAVY)
    title.pack(pady=20)
    
    # Description
    desc = tk.Label(root,
                   text="Design doux et harmonieux inspiré des couleurs sous-marines",
                   font=('Arial', 12, 'italic'),
                   bg=AqualixColors.PEARL_WHITE,
                   fg=AqualixColors.MEDIUM_GRAY)
    desc.pack(pady=(0, 20))
    
    # Frame principal avec défilement
    main_frame = ColoredFrame(root, bg_color=AqualixColors.PEARL_WHITE)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    # === COULEURS PRIMAIRES ===
    primary_frame = ColoredFrame(main_frame, bg_color=AqualixColors.FOAM_WHITE, relief='solid', bd=2)
    primary_frame.pack(fill=tk.X, pady=(0, 15))
    
    tk.Label(primary_frame, 
            text="🌊 Couleurs Primaires Océaniques",
            font=('Arial', 14, 'bold'),
            bg=AqualixColors.FOAM_WHITE,
            fg=AqualixColors.DEEP_NAVY).pack(pady=10)
    
    colors_primary = [
        ("Océan Profond", AqualixColors.DEEP_OCEAN),
        ("Bleu Océan", AqualixColors.OCEAN_BLUE),
        ("Eau Claire", AqualixColors.SHALLOW_WATER),
    ]
    
    primary_colors_frame = ColoredFrame(primary_frame, bg_color=AqualixColors.FOAM_WHITE)
    primary_colors_frame.pack(pady=(0, 10))
    
    for i, (name, color) in enumerate(colors_primary):
        color_frame = tk.Frame(primary_colors_frame, bg=color, width=120, height=80, relief='raised', bd=2)
        color_frame.pack(side=tk.LEFT, padx=5, pady=5)
        color_frame.pack_propagate(False)
        
        tk.Label(color_frame, text=name, font=('Arial', 9, 'bold'), 
                bg=color, fg='white' if i < 2 else AqualixColors.DEEP_NAVY).pack(expand=True)
        tk.Label(color_frame, text=color, font=('Arial', 7),
                bg=color, fg='white' if i < 2 else AqualixColors.DEEP_NAVY).pack()
    
    # === COULEURS CORAIL ===
    coral_frame = ColoredFrame(main_frame, bg_color=AqualixColors.SANDY_BEIGE, relief='solid', bd=2)
    coral_frame.pack(fill=tk.X, pady=(0, 15))
    
    tk.Label(coral_frame,
            text="🪸 Couleurs Corail et Chaleureuses", 
            font=('Arial', 14, 'bold'),
            bg=AqualixColors.SANDY_BEIGE,
            fg=AqualixColors.DEEP_NAVY).pack(pady=10)
    
    colors_coral = [
        ("Rose Corail", AqualixColors.CORAL_PINK),
        ("Orange Corail", AqualixColors.CORAL_ORANGE),
        ("Beige Sablonneux", AqualixColors.SANDY_BEIGE),
    ]
    
    coral_colors_frame = ColoredFrame(coral_frame, bg_color=AqualixColors.SANDY_BEIGE)
    coral_colors_frame.pack(pady=(0, 10))
    
    for name, color in colors_coral:
        color_frame = tk.Frame(coral_colors_frame, bg=color, width=120, height=80, relief='raised', bd=2)
        color_frame.pack(side=tk.LEFT, padx=5, pady=5)
        color_frame.pack_propagate(False)
        
        tk.Label(color_frame, text=name, font=('Arial', 9, 'bold'), 
                bg=color, fg=AqualixColors.DEEP_NAVY).pack(expand=True)
        tk.Label(color_frame, text=color, font=('Arial', 7),
                bg=color, fg=AqualixColors.DEEP_NAVY).pack()
    
    # === COULEURS VÉGÉTALES ===
    plant_frame = ColoredFrame(main_frame, bg_color=AqualixColors.SECTION_COLOR_BALANCE, relief='solid', bd=2)
    plant_frame.pack(fill=tk.X, pady=(0, 15))
    
    tk.Label(plant_frame,
            text="🌱 Couleurs Végétales Marines",
            font=('Arial', 14, 'bold'),
            bg=AqualixColors.SECTION_COLOR_BALANCE,
            fg=AqualixColors.DEEP_NAVY).pack(pady=10)
    
    colors_plant = [
        ("Vert Marin", AqualixColors.SEA_GREEN),
        ("Vert Algue", AqualixColors.KELP_GREEN),
        ("Vert Profond", AqualixColors.DEEP_SEA_GREEN),
    ]
    
    plant_colors_frame = ColoredFrame(plant_frame, bg_color=AqualixColors.SECTION_COLOR_BALANCE)
    plant_colors_frame.pack(pady=(0, 10))
    
    for name, color in colors_plant:
        color_frame = tk.Frame(plant_colors_frame, bg=color, width=120, height=80, relief='raised', bd=2)
        color_frame.pack(side=tk.LEFT, padx=5, pady=5)
        color_frame.pack_propagate(False)
        
        tk.Label(color_frame, text=name, font=('Arial', 9, 'bold'), 
                bg=color, fg='white').pack(expand=True)
        tk.Label(color_frame, text=color, font=('Arial', 7),
                bg=color, fg='white').pack()
    
    # === DÉMONSTRATION DES BOUTONS ===
    buttons_frame = ColoredFrame(main_frame, bg_color=AqualixColors.MIST_BLUE, relief='solid', bd=2)
    buttons_frame.pack(fill=tk.X, pady=(0, 15))
    
    tk.Label(buttons_frame,
            text="🔘 Styles de Boutons",
            font=('Arial', 14, 'bold'),
            bg=AqualixColors.MIST_BLUE,
            fg=AqualixColors.DEEP_NAVY).pack(pady=10)
    
    buttons_demo_frame = ColoredFrame(buttons_frame, bg_color=AqualixColors.MIST_BLUE)
    buttons_demo_frame.pack(pady=(0, 10))
    
    ColoredButton(buttons_demo_frame, text="Bouton Principal", style_type='primary').pack(side=tk.LEFT, padx=5)
    ColoredButton(buttons_demo_frame, text="Bouton Secondaire", style_type='secondary').pack(side=tk.LEFT, padx=5) 
    ColoredButton(buttons_demo_frame, text="Bouton Accent", style_type='accent').pack(side=tk.LEFT, padx=5)
    
    # === SECTIONS UTILISÉES ===
    sections_frame = ColoredFrame(main_frame, bg_color=AqualixColors.FOAM_WHITE, relief='solid', bd=2)
    sections_frame.pack(fill=tk.X, pady=(0, 20))
    
    tk.Label(sections_frame,
            text="📊 Couleurs par Section de Paramètres",
            font=('Arial', 14, 'bold'),
            bg=AqualixColors.FOAM_WHITE,
            fg=AqualixColors.DEEP_NAVY).pack(pady=10)
    
    sections = [
        ("Balance des Blancs", "white_balance"),
        ("UDCP", "udcp"), 
        ("Beer-Lambert", "beer_lambert"),
        ("Rééquilibrage", "color_rebalance"),
        ("Histogramme", "histogram_equalization"),
        ("Fusion", "multiscale_fusion")
    ]
    
    sections_demo_frame = ColoredFrame(sections_frame, bg_color=AqualixColors.FOAM_WHITE)
    sections_demo_frame.pack(pady=(0, 10), padx=10)
    
    for i, (name, section_key) in enumerate(sections):
        color = AqualixColors.get_section_color(section_key)
        section_demo = tk.Frame(sections_demo_frame, bg=color, width=120, height=60, relief='raised', bd=1)
        section_demo.pack(side=tk.LEFT, padx=2, pady=2)
        section_demo.pack_propagate(False)
        
        tk.Label(section_demo, text=name, font=('Arial', 8, 'bold'),
                bg=color, fg=AqualixColors.DEEP_NAVY).pack(expand=True)
    
    # Bouton fermer
    ColoredButton(root, text="Fermer", command=root.destroy, style_type='accent').pack(pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    print("🎨 Démonstration de la palette aquatique Aqualix")
    print("=" * 60)
    create_color_demo()
