# Changelog

Toutes les modifications notables de ce projet seront documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Versioning Sémantique](https://semver.org/lang/fr/).

## [1.2.0] - 2025-08-10

### Ajouté
- **UDCP (Underwater Dark Channel Prior)** 🌊
  - Nouveau algorithme spécialisé pour l'amélioration des images sous-marines
  - Suppression automatique du voile et amélioration de la visibilité
  - Paramètres ajustables : omega, transmission minimale, taille de fenêtre
  - Filtre guidé pour le raffinement de la carte de transmission
  - Amélioration optionnelle du contraste final
  - Interface bilingue complète avec descriptions détaillées

- **Optimisation des performances pour les grandes images**
  - Sous-échantillonnage automatique pour l'aperçu (images >1024px)
  - Traitement pleine résolution maintenu pour la sauvegarde
  - Amélioration significative de la réactivité de l'interface
  - Journalisation automatique du facteur d'échelle dans les logs

### Amélioré
- **Pipeline de traitement étendu**
  - Ordre optimal : White Balance → UDCP → Histogram Equalization
  - Interface de paramètres dynamique avec visibilité conditionnelle
  - Descriptions détaillées du pipeline en temps réel
  
- **Interface utilisateur**
  - Fluidité améliorée avec les images haute résolution
  - Temps de réponse réduit lors du changement de paramètres
  - Meilleure expérience utilisateur globale
  - Nouvelles traductions pour les fonctionnalités UDCP

### Technique
- Implémentation complète de l'algorithme UDCP avec filtre guidé
- Nouvelle fonction `create_preview_image()` pour le sous-échantillonnage
- Méthode `process_image_for_preview()` dans `ImageProcessor`
- Gestion automatique des facteurs d'échelle
- Logs détaillés des optimisations de performance
- Tests automatisés pour validation des algorithmes

## [1.1.0] - 2024-01-15

### Ajouté
- **Interface en ligne de commande (CLI)** : Traitement par lot via `python cli.py`
  - Support des images et vidéos
  - Traitement de dossiers entiers
  - Options configurables de sortie
  - Rapports de progression détaillés
  
- **Système de journalisation** : Logging complet des opérations
  - Fichiers de log rotatifs dans le dossier `logs/`
  - Niveaux de log configurables (DEBUG, INFO, WARNING, ERROR)
  - Suivi des paramètres et opérations de traitement
  
- **Onglet Informations** : Affichage détaillé des métadonnées d'images
  - Informations de fichier (taille, date de modification, type)
  - Propriétés d'image (dimensions, profondeur de couleur, format)
  - Analyses avancées (histogramme de couleurs, statistiques)
  - Données EXIF complètes (caméra, paramètres, géolocalisation si disponible)

- **Contrôles de vue améliorés** :
  - Bouton "Ajuster" pour adapter automatiquement l'image au canvas
  - Ajustement automatique des nouvelles images au chargement
  - Renommage du bouton "Réinitialiser" en "1:1" pour plus de clarté

- **Support multilingue** :
  - Interface disponible en français et anglais
  - Sélecteur de langue intégré dans la barre d'outils
  - Changement de langue instantané sans redémarrage
  - Plus de 200 traductions couvrant toute l'interface

### Modifié
- Interface utilisateur reorganisée en trois onglets : Paramètres, Opérations, Informations
- Amélioration de l'expérience utilisateur avec ajustement automatique d'image
- Amélioration de la gestion des erreurs et de la stabilité

### Corrigé
- Fix des références à la progress bar lors de la fermeture de fenêtre
- Correction des erreurs de comparaison de types dans le système d'informations
- Amélioration de la gestion mémoire lors du traitement vidéo
- Gestion robuste des erreurs de formatage des métadonnées

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
