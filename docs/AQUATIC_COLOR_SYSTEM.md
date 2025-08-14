# 🎨 Système de Couleurs Aquatique Aqualix

## Vue d'ensemble

Le système de couleurs Aqualix utilise une palette aquatique douce et harmonieuse inspirée des couleurs sous-marines. L'objectif est de créer une interface utilisateur apaisante et professionnelle qui améliore l'expérience utilisateur sans être distrayante.

## Philosophie de Design

- **Douceur** : Couleurs pastelles et tons apaisants
- **Harmonie** : Palette cohérente basée sur l'écosystème aquatique
- **Professionnalisme** : Design moderne et épuré
- **Accessibilité** : Contrastes suffisants pour la lisibilité

## Palette de Couleurs

### 🌊 Couleurs Primaires Océaniques
- **Océan Profond** (`#2C5282`) : Éléments principaux, headers
- **Bleu Océan** (`#4A7BA7`) : Boutons primaires, accents
- **Eau Claire** (`#BDE4FF`) : Arrière-plans doux

### 🪸 Couleurs Corail et Chaleureuses
- **Rose Corail** (`#E8A598`) : Éléments d'attention
- **Orange Corail** (`#FF8A65`) : Boutons d'action
- **Beige Sablonneux** (`#F5E6D3`) : Arrière-plans neutres

### 🌱 Couleurs Végétales Marines
- **Vert Marin** (`#8DB4A0`) : Boutons secondaires
- **Vert Algue** (`#A8D5A8`) : Éléments de nature
- **Vert Profond** (`#5A8A6B`) : Accents discrets

### 💎 Couleurs Neutres
- **Blanc Perle** (`#F8F9FA`) : Arrière-plan principal
- **Blanc Écume** (`#F0F4F8`) : Arrière-plans de section
- **Bleu Brume** (`#E2F1F8`) : Zones délimitées
- **Gris Moyen** (`#6B7C93`) : Texte secondaire
- **Marine Profond** (`#1A365D`) : Texte principal

## Utilisation des Couleurs par Section

### Sections de Paramètres
Chaque section d'algorithmes a sa propre couleur d'arrière-plan pour faciliter la navigation :

- **Balance des Blancs** : Blanc Écume (`#F0F4F8`)
- **UDCP** : Bleu Brume (`#E2F1F8`) 
- **Beer-Lambert** : Eau Claire (`#BDE4FF`)
- **Rééquilibrage Couleur** : Beige Sablonneux (`#F5E6D3`)
- **Égalisation Histogramme** : Vert Algue (`#A8D5A8`)
- **Fusion Multi-échelle** : Rose Corail (`#E8A598`)

### Styles de Boutons

#### Bouton Principal (Primary)
- **Couleur** : Bleu Océan (`#4A7BA7`)
- **Survol** : Océan Profond (`#2C5282`)
- **Usage** : Actions principales, traitement

#### Bouton Secondaire (Secondary)
- **Couleur** : Vert Marin (`#8DB4A0`)
- **Survol** : Vert Profond (`#5A8A6B`)
- **Usage** : Actions auxiliaires, navigation

#### Bouton Accent (Accent)
- **Couleur** : Orange Corail (`#FF8A65`)
- **Survol** : version assombrie
- **Usage** : Actions importantes, alertes

## Implémentation Technique

### Classes Principales

#### `AqualixColors`
Classe statique contenant toutes les couleurs de la palette.

```python
from src.ui_colors import AqualixColors

# Utilisation
bg_color = AqualixColors.PEARL_WHITE
button_color = AqualixColors.OCEAN_BLUE
```

#### `ColoredFrame`
Extension de `tk.Frame` avec support couleur d'arrière-plan.

```python
from src.ui_colors import ColoredFrame

# Création d'un frame coloré
frame = ColoredFrame(parent, bg_color=AqualixColors.FOAM_WHITE)
```

#### `ColoredButton`
Bouton avec styles prédéfinis et effets de survol.

```python
from src.ui_colors import ColoredButton

# Boutons avec styles
btn_primary = ColoredButton(parent, text="Traiter", style_type='primary')
btn_secondary = ColoredButton(parent, text="Annuler", style_type='secondary')
btn_accent = ColoredButton(parent, text="Important", style_type='accent')
```

### TTK Theming

Le système configure automatiquement les styles TTK pour une apparence cohérente :

- Notebooks avec onglets colorés
- Labels avec couleurs appropriées
- Frames avec arrière-plans harmonieux

## Avantages

1. **Expérience Utilisateur Améliorée** : Interface plus agréable et moins fatigante
2. **Navigation Facilitée** : Couleurs par section pour identification rapide
3. **Professionnalisme** : Apparence moderne et soignée
4. **Cohérence** : Palette unifiée dans toute l'application
5. **Maintenabilité** : Système centralisé et modulaire

## Évolutions Futures

- Mode sombre avec palette aquatique nocturne
- Personnalisation utilisateur des couleurs
- Thèmes saisonniers (été/hiver aquatique)
- Adaptation automatique selon le type d'image traitée

## Démonstration

Pour voir toutes les couleurs en action :

```bash
python demo_colors.py
```

Cette commande lance une fenêtre de démonstration montrant toute la palette et les différents styles de composants.
