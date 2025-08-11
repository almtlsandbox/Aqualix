# Aqualix - Traitement d'Images Sous-Marines

[![GitHub](https://img.shields.io/github/license/almtlsandbox/Aqualix)](https://github.com/almtlsandbox/Aqualix/blob/main/LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![OpenCV](https://img.shields.io/badge/opencv-4.8+-green.svg)](https://opencv.org/)

Une application Python spécialisée pour le traitement interactif d'images et vidéos sous-marines avec une interface utilisateur intuitive et des algorithmes de correction couleur avancés.

![Aqualix Interface](https://img.shields.io/badge/Interface-Fran%C3%A7ais%2FEnglish-blue)
![Aqualix Language Support](https://img.shields.io/badge/Languages-FR%20%7C%20EN-green)
![Pipeline](https://img.shields.io/badge/Pipeline-6%20Steps-orange)

## 🌊 Caractéristiques Principales

### Pipeline de Traitement Spécialisé pour l'Imagerie Sous-Marine

1. **🎨 Balance des Blancs (5 Méthodes)**
   - **Gray-World** : Correction basée sur l'hypothèse de neutralité moyenne
   - **White-Patch** : Utilise les pixels les plus brillants comme référence blanche
   - **Shades-of-Gray** : Généralisation robuste utilisant la norme de Minkowski
   - **Grey-Edge** : Estimation d'illumination par dérivées spatiales
   - **Lake Green Water** : Méthode spécialisée pour la photographie en eau douce avec réduction du dominant vert

2. **🌊 UDCP (Underwater Dark Channel Prior)**
   - Algorithme spécialisé pour l'amélioration d'images sous-marines
   - Suppression du voile atmosphérique et amélioration de la visibilité
   - Estimation de la lumière atmosphérique et calcul de carte de transmission
   - Filtre guidé pour un rendu sans artifacts
   - Paramètres configurables : omega, transmission minimale, taille de fenêtre

3. **⚗️ Beer-Lambert (Correction d'Atténuation)**
   - Modélisation physique de l'absorption lumineuse dans l'eau
   - Correction différentielle par canal couleur (rouge, vert, bleu)
   - Paramètres ajustables : facteur de profondeur, coefficients d'atténuation
   - Amélioration du contraste intégrée

4. **🎛️ Rééquilibrage Couleur (Matrice 3x3)**
   - Transformation matricielle configurable pour ajustements fins
   - 9 coefficients ajustables pour mélange inter-canal
   - Protection anti-magenta avec limitation de saturation HSV
   - Préservation optionnelle de la luminance

5. **📊 Égalisation d'Histogramme Adaptatif (CLAHE)**
   - Amélioration du contraste local dans l'espace couleur LAB
   - Limitation de contraste configurable
   - Taille de grille adaptable

6. **🔬 Fusion Multi-Échelle**
   - Combinaison d'informations à différentes échelles
   - Préservation des détails fins et structures globales
   - Paramètres de fusion configurables

### 🚀 Interface Utilisateur Avancée

#### Vue Interactive en Temps Réel
- **Vue Divisée Ajustable** : Comparaison avant/après avec diviseur repositionnable
- **Contrôles de Zoom** : Molette souris ou boutons +/- pour zoom précis  
- **Panoramique** : Glisser-déposer pour navigation dans l'image
- **Rotation** : Boutons de rotation 90° (↺ ↻)
- **Réinitialisation** : Retour aux paramètres de vue par défaut
- **Aperçu Optimisé** : Sous-échantillonnage intelligent pour fluidité

#### Organisation Modulaire
- **Onglet Paramètres** : Sections repliables par étape de traitement
- **Onglet Pipeline** : Visualisation du pipeline de traitement actuel  
- **Onglet Informations** : Métadonnées détaillées et analyses d'image
- **Navigation Fichiers** : Parcours de collections d'images/vidéos
- **Contrôles Vidéo** : Slider de navigation frame par frame

### 🎯 Fonctionnalités Avancées

#### Auto-Tune Intelligent
- **Optimisation Automatique** : Chaque étape dispose d'un algorithme d'auto-optimisation
- **Déclenchement Immédiat** : Auto-tune activé dès la sélection de la checkbox
- **Analyse d'Image** : Paramètres optimisés selon le contenu de l'image
- **Boutons de Réinitialisation** : Reset propre avec désactivation de l'auto-tune

#### Support Multilingue Complet
- **Interface Bilingue** : Français et anglais avec commutation instantanée
- **200+ Traductions** : Couverture complète de l'interface utilisateur
- **Descriptions Contextuelles** : Paramètres et opérations traduits
- **Sauvegarde des Préférences** : Langue mémorisée entre les sessions

#### Gestion Fichiers et Médias
- **Formats Supportés** :
  - Images : JPEG, PNG, BMP, TIFF, WebP
  - Vidéos : MP4, AVI, MOV, MKV, WMV
- **Traitement par Lot** : Dossiers complets avec récursivité
- **Navigation Intuitive** : Boutons précédent/suivant
- **Sauvegarde Flexible** : Export avec qualité configurable

#### Système de Journalisation Professionnel
- **Logs Rotatifs** : Fichiers automatiquement archivés (10MB max)
- **Niveaux Configurables** : DEBUG, INFO, WARNING, ERROR
- **Traçabilité Complète** : Suivi de toutes les opérations et paramètres
- **Performance Tracking** : Mesure des temps de traitement

## 📦 Installation

### Prérequis
- Python 3.8 ou plus récent
- 4GB+ RAM recommandés pour le traitement vidéo
- Codecs vidéo compatibles OpenCV

### Installation Standard

1. **Cloner le repository** :
   ```bash
   git clone https://github.com/almtlsandbox/Aqualix.git
   cd Aqualix
   ```

2. **Créer un environnement virtuel** (recommandé) :
   ```bash
   python -m venv .venv
   
   # Windows:
   .venv\Scripts\activate
   
   # macOS/Linux:
   source .venv/bin/activate
   ```

3. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```

## 🎮 Utilisation

### Interface Graphique

1. **Lancer l'application** :
   ```bash
   python main.py
   ```

2. **Charger des médias** :
   - **Fichier unique** : "Sélectionner un fichier" pour image/vidéo individuelle
   - **Traitement par lot** : "Sélectionner un dossier" pour collections
   - **Navigation** : Boutons Précédent/Suivant pour parcourir

3. **Configuration des paramètres** :
   - **Sections repliables** : Cliquer sur ▼ pour développer chaque étape
   - **Auto-tune** : Cocher pour optimisation automatique des paramètres
   - **Réinitialisation** : Bouton "Réinitialiser" par étape ou global
   - **Temps réel** : Aperçu mis à jour instantanément

4. **Vue interactive** :
   - **Division ajustable** : Glisser la ligne blanche ou utiliser le slider
   - **Zoom précis** : Molette souris ou boutons +/- 
   - **Navigation** : Clic gauche + glisser pour panoramique
   - **Rotation** : Boutons ↺ ↻ pour rotation 90°
   - **Adaptation** : Bouton "Ajuster" pour adapter au canvas
   - **Échelle réelle** : Bouton "1:1" pour affichage natif

5. **Traitement vidéo** :
   - **Navigation frames** : Slider pour parcourir la vidéo
   - **Aperçu temps réel** : Effets appliqués à la frame courante
   - **Traitement complet** : Sauvegarde applique à toute la vidéo

6. **Sauvegarde et export** :
   - **Qualité configurable** : JPEG avec curseur de qualité
   - **Formats multiples** : Support PNG, TIFF, etc.
   - **Traitement haute résolution** : Image originale utilisée (pas l'aperçu)

### Interface Ligne de Commande (CLI)

```bash
# Traitement d'une image
python cli.py -i image.jpg -o processed.jpg

# Traitement d'un dossier complet  
python cli.py -i ./photos -o ./processed --recursive

# Vidéo avec paramètres personnalisés
python cli.py -i video.mp4 -o out.mp4 --wb-percentile 15 --clahe-clip 3.0

# Voir toutes les options
python cli.py --help
```

## ⚙️ Paramètres de Traitement

### Balance des Blancs
- **Méthode** : Sélection parmi 5 algorithmes spécialisés
- **Percentile** : Calcul de moyenne (10-90%)
- **Ajustement Max** : Limite de mise à l'échelle (1.0-5.0x)
- **Paramètres spécialisés** selon la méthode sélectionnée

### UDCP (Underwater Dark Channel Prior)
- **Omega** : Force de suppression du voile (0.85-0.99)
- **T0** : Transmission minimale (0.05-0.2)
- **Taille fenêtre** : Calcul dark channel (5-25px)
- **Rayon filtre guidé** : Lissage transmission (20-100px)
- **Epsilon** : Régularisation filtre (0.0001-0.01)
- **Amélioration contraste** : Boost final optionnel (1.0-2.0x)

### Beer-Lambert (Atténuation)
- **Facteur profondeur** : Simulation profondeur (0.01-1.0)
- **Coeff. rouge** : Atténuation canal rouge (0.1-2.0)
- **Coeff. vert** : Atténuation canal vert (0.1-1.5)
- **Coeff. bleu** : Atténuation canal bleu (0.05-1.0)
- **Facteur amélioration** : Boost final (1.0-3.0)

### Rééquilibrage Couleur (Matrice 3x3)
- **9 coefficients** : Transformation matricielle complète
- **Diagonale** : Coefficients principaux (0.5-2.0)
- **Hors-diagonale** : Mélange inter-canal (-0.5-0.5)
- **Limite saturation** : Protection anti-magenta (0.3-1.0)
- **Préservation luminance** : Conservation brightness optionnelle

### Égalisation d'Histogramme (CLAHE)
- **Limite clip** : Seuil limitation contraste (1.0-10.0)
- **Taille tuile** : Grille traitement adaptatif (4x4 à 16x16)

### Fusion Multi-Échelle
- **Échelles** : Nombre de niveaux décomposition (2-5)
- **Sigma base** : Flou gaussien initial (0.5-2.0)
- **Facteur échelle** : Progression entre niveaux (1.5-3.0)
- **Poids détails** : Balance détails/structure (0.3-0.8)

## 🔧 Architecture Technique

### Structure des Fichiers
```
Aqualix/
├── main.py                 # Application principale et coordination UI
├── src/
│   ├── image_processing.py # Algorithmes et pipeline de traitement
│   ├── ui_components.py    # Composants UI réutilisables
│   ├── localization.py     # Système de traduction i18n
│   └── logger.py          # Système de journalisation
├── config/                 # Configuration et paramètres
├── docs/                   # Documentation détaillée
├── logs/                   # Fichiers de log rotatifs
└── requirements.txt        # Dépendances Python
```

### Dépendances Principales
- **OpenCV** : Traitement d'image et vidéo
- **Pillow (PIL)** : Manipulation et affichage d'images
- **NumPy** : Opérations numériques optimisées
- **Tkinter** : Framework GUI (inclus avec Python)
- **JSON** : Configuration et traductions

### Optimisations Performance
- **Aperçu sous-échantillonné** : Images >1024px réduites pour fluidité
- **Traitement pleine résolution** : Sauvegarde utilise l'image originale
- **Threading vidéo** : Traitement en arrière-plan avec barre de progression
- **Rendu optimisé** : Transformations PIL efficaces pour vue interactive
- **Cache intelligent** : Évite les recalculs inutiles

## 🛠️ Développement et Extension

### Ajouter une Nouvelle Opération

1. **Paramètres** dans `ImageProcessor.__init__()` :
   ```python
   self.parameters['new_op_enabled'] = True
   self.parameters['new_op_param'] = 1.0
   ```

2. **Ordre pipeline** dans `pipeline_order` :
   ```python
   self.pipeline_order.append('new_operation')
   ```

3. **Fonction de traitement** :
   ```python
   def new_operation(self, image):
       if self.parameters['new_op_enabled']:
           # Implémentation du traitement
           return processed_image
       return image
   ```

4. **Métadonnées paramètres** dans `get_parameter_info()` :
   ```python
   'new_op_param': {
       'type': 'float', 'min': 0.1, 'max': 2.0,
       'description': 'Description du paramètre'
   }
   ```

### Ajouter un Algorithme d'Auto-Tune

1. **Méthode d'optimisation** :
   ```python
   def _auto_tune_new_operation(self, image):
       # Analyse de l'image
       # Calcul paramètres optimaux
       # Mise à jour self.parameters
       return optimized_params
   ```

2. **Enregistrement** dans `auto_tune_methods` :
   ```python
   'new_operation': self._auto_tune_new_operation
   ```

## 🐛 Résolution de Problèmes

### Problèmes Courants
- **Erreurs d'import** : Vérifier l'installation des dépendances
- **Codecs vidéo** : Installer codecs supplémentaires si nécessaire
- **Mémoire insuffisante** : Fermer autres applications, réduire taille vidéo
- **Performance** : Réduire résolution pour traitement plus rapide

### Configuration Système Recommandée
- Python 3.8+ (3.9+ recommandé)
- 8GB+ RAM pour traitement vidéo intensif
- Processeur multi-coeur pour meilleur threading
- Espace disque suffisant pour logs et caches temporaires

## 📚 Documentation Supplémentaire

- **[CHANGELOG.md](docs/CHANGELOG.md)** : Historique des versions et nouveautés
- **[Tests](docs/TEST_COLOR_REBALANCING.md)** : Procédures de test et validation
- **[Logs](logs/)** : Fichiers de journalisation détaillés

## 🤝 Contribution

Les contributions sont les bienvenues ! Processus recommandé :

1. **Fork** le projet
2. **Créer une branche** : `git checkout -b feature/NewFeature`
3. **Développer** avec tests appropriés
4. **Commit** : `git commit -m 'feat: Add NewFeature'`
5. **Push** : `git push origin feature/NewFeature`
6. **Pull Request** avec description détaillée

### Standards de Code
- Code documenté en français ou anglais
- Respect des conventions Python (PEP 8)
- Tests unitaires pour nouvelles fonctionnalités
- Messages de commit explicites

## 📄 Licence

Projet sous licence MIT. Voir [LICENSE](LICENSE) pour détails complets.

## 🙏 Remerciements

- **[OpenCV](https://opencv.org/)** : Algorithmes de traitement d'image
- **[Pillow](https://python-pillow.org/)** : Manipulation d'images Python
- **Communauté Python** : Outils et bibliothèques exceptionnels
- **Photographes sous-marins** : Retours et cas d'usage

## 📞 Support

- **Issues GitHub** : [Signaler un problème](https://github.com/almtlsandbox/Aqualix/issues)
- **Documentation** : Dossier `docs/` pour guides détaillés
- **Logs** : Dossier `logs/` pour diagnostic des problèmes

---

**Aqualix** - *Révélez la beauté cachée des profondeurs* 🌊
