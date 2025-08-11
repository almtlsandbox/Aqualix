# Proposition de Réorganisation du Projet Aqualix

## Structure Actuelle
Le projet contient actuellement ~30 fichiers de test éparpillés à la racine, ce qui rend la navigation difficile.

## Structure Proposée

```
aqualix/
├── src/                          # Code source principal
│   ├── __init__.py
│   ├── main.py                   # Point d'entrée principal
│   ├── image_processing.py       # Moteur de traitement d'images
│   ├── ui_components.py          # Composants d'interface utilisateur
│   ├── localization.py          # Système de localisation
│   ├── logger.py                # Système de logging
│   └── image_info.py            # Utilitaires d'information d'images
├── tests/                       # Tous les tests regroupés
│   ├── __init__.py
│   ├── unit/                    # Tests unitaires
│   │   ├── __init__.py
│   │   ├── test_image_processing.py
│   │   ├── test_localization.py
│   │   └── test_ui_components.py
│   ├── integration/             # Tests d'intégration
│   │   ├── __init__.py
│   │   ├── test_pipeline.py
│   │   ├── test_full_workflow.py
│   │   └── test_auto_tune.py
│   ├── ui/                      # Tests d'interface utilisateur
│   │   ├── __init__.py
│   │   ├── test_interface.py
│   │   ├── test_manual_buttons.py
│   │   └── test_parameter_updates.py
│   ├── performance/             # Tests de performance
│   │   ├── __init__.py
│   │   ├── test_performance.py
│   │   └── test_multiscale_fusion.py
│   └── fixtures/                # Données de test (images, etc.)
│       ├── test_fusion_input.jpg
│       ├── test_fusion_output.jpg
│       ├── test_pipeline_input.jpg
│       └── test_pipeline_output.jpg
├── scripts/                     # Scripts utilitaires
│   ├── __init__.py
│   ├── cli.py                   # Interface en ligne de commande
│   ├── list_parameters.py       # Utilitaire de listage des paramètres
│   └── quick_test.py           # Script de test rapide
├── config/                      # Configuration
│   ├── __init__.py
│   ├── about_config.py         # Configuration "À propos"
│   └── aqualix_config.json     # Configuration JSON
├── docs/                       # Documentation
│   ├── README.md
│   ├── CHANGELOG.md
│   ├── TEST_COLOR_REBALANCING.md
│   └── api/                    # Documentation API
├── logs/                       # Fichiers de log (existant)
├── .venv/                      # Environnement virtuel (existant)
├── .github/                    # Configuration GitHub (existant)
├── .vscode/                    # Configuration VS Code (existant)
├── requirements.txt            # Dépendances
├── setup.py                    # Configuration du package
├── .gitignore                  # Git ignore
├── LICENSE                     # Licence
├── run_app.bat                 # Script de lancement Windows
└── demo_cli.bat               # Script de démo CLI
```

## Avantages de cette Structure

### 1. **Séparation des Préoccupations**
- Code source dans `src/`
- Tests organisés par catégorie dans `tests/`
- Scripts utilitaires dans `scripts/`
- Configuration dans `config/`

### 2. **Tests Mieux Organisés**
- **Unit tests** : Tests de composants individuels
- **Integration tests** : Tests de workflow complets
- **UI tests** : Tests d'interface utilisateur
- **Performance tests** : Tests de performance et benchmarks
- **Fixtures** : Données de test centralisées

### 3. **Meilleure Maintenabilité**
- Fichiers regroupés par fonction
- Navigation plus facile
- Import paths plus clairs
- Structure évolutive

### 4. **Conformité aux Standards Python**
- Structure de package Python standard
- Possibilité d'installer avec `pip install -e .`
- Compatible avec les outils de développement Python

## Plan de Migration

### Phase 1: Création de la Structure
1. Créer les répertoires `src/`, `tests/`, `scripts/`, `config/`, `docs/`
2. Ajouter les fichiers `__init__.py` appropriés

### Phase 2: Migration du Code Source
1. Déplacer les fichiers principaux vers `src/`
2. Mettre à jour les imports
3. Tester que l'application fonctionne

### Phase 3: Réorganisation des Tests
1. Catégoriser et déplacer les tests
2. Créer des fixtures partagées
3. Mettre à jour les chemins d'accès

### Phase 4: Scripts et Configuration
1. Déplacer les scripts utilitaires
2. Organiser la configuration
3. Déplacer la documentation

### Phase 5: Validation
1. Tests complets de l'application
2. Validation des imports
3. Mise à jour des scripts de lancement

## Fichiers `__init__.py` Nécessaires

Chaque package Python doit contenir un fichier `__init__.py` pour être reconnu comme un module importable.

Voulez-vous que je procède à cette réorganisation étape par étape ?
