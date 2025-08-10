# Changelog

Toutes les modifications notables de ce projet seront documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Versioning Sémantique](https://semver.org/lang/fr/).

## [1.0.0] - 2025-08-10

### Ajouté
- Application de traitement d'images et vidéos avec interface Tkinter
- Vue comparative interactive avec division ajustable
- Support complet des images (JPEG, PNG, BMP, TIFF)
- Support complet des vidéos (MP4, AVI, MOV, MKV)
- Interface à onglets :
  - Onglet "Paramètres" pour ajuster les réglages
  - Onglet "Opérations" pour voir la description du pipeline
- Fonctionnalités interactives :
  - Zoom avant/arrière (molette de souris ou boutons)
  - Déplacement/pan (clic-glisser)
  - Rotation par incréments de 90°
  - Réinitialisation de la vue
- Pipeline de traitement d'image :
  - Balance des blancs Gray-World avec paramètres ajustables
  - Égalisation adaptative d'histogramme (CLAHE)
- Navigation dans les collections de fichiers
- Curseur de navigation pour les frames vidéo
- Sauvegarde des résultats traités
- Traitement en lot pour les vidéos
- Interface entièrement en français
- Documentation complète avec README détaillé

### Technique
- Architecture modulaire (main.py, image_processing.py, ui_components.py)
- Gestion des erreurs robuste
- Threading pour le traitement vidéo
- Optimisations de performance pour l'affichage temps réel
- Support des environnements virtuels Python
