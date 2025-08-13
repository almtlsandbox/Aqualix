# Changelog - Aqualix

Toutes les modifications importantes du projet Aqualix seront documentées dans ce fichier.

## [2.2.2] - 2025-08-13

### 🔧 Corrections d'Interface
- **Traduction des boutons de barre d'outils** : Correction du problème où les boutons "Sauvegarder les résultats" et "Contrôle de la qualité" ne changeaient pas de langue
  - Ajout du bouton `quality_check` manquant dans `update_toolbar_texts()`
  - Les boutons de la barre d'outils se mettent maintenant correctement à jour lors du changement de langue
  - Synchronisation parfaite entre sélection de langue et affichage des boutons

## [2.2.1] - 2025-08-11

### 🌊 Nouvelles Fonctionnalités
- **Détection du Type d'Eau** : Affichage automatique du type d'environnement aquatique détecté
  - Classification intelligente : Lac/Eau douce, Océan/Eau profonde, Eaux tropicales, Eau claire/Contraste élevé, Environnement standard
  - Recommandation de méthode de correction optimale selon l'environnement
  - Affichage intégré dans l'onglet Operations avec traductions FR/EN

### 🔧 Améliorations Techniques
- **Méthode `get_water_type()`** : Nouvelle méthode publique dans `ImageProcessor` pour la détection d'environnement
- **Interface utilisateur enrichie** : Le panneau Pipeline affiche maintenant les informations d'environnement détecté
- **Logique de détection basée sur l'auto-tune** : Utilise la même analyse que le système d'optimisation automatique

## [2.2.0] - 2025-08-11

### 🎉 Nouvelles Fonctionnalités
- **Bouton Global Auto-Tune** : Ajout d'un bouton pour activer/désactiver tous les auto-tune d'un seul clic
- **Correction Multiscale Fusion** : La fusion multiscale respecte maintenant le pipeline de traitement précédent

### 🔧 Corrections Importantes
- **Multiscale Fusion Bug** : Résolution du problème où la fusion ignorait les étapes précédentes du pipeline
- **Pipeline Intégrité** : Les changements de paramètres influencent maintenant correctement le résultat final même avec la fusion activée

### ⚡ Améliorations de Performance
- **Nouvelles Variantes de Fusion** : Implémentation de variantes optimisées pour traitement post-pipeline
  - `_enhance_contrast_on_processed()` : Contraste doux sur image déjà traitée
  - `_enhance_sharpening_on_processed()` : Sharpening doux sur image déjà traitée

### 🌍 Interface Utilisateur
- **Contrôle Global** : Interface améliorée avec bouton Auto-Tune Global
- **Traductions Complètes** : Support français/anglais pour le nouveau bouton global
  - FR : "Auto-Tune Global" 
  - EN : "Global Auto-Tune"

### 🧪 Tests et Validation
- **Tests de Regression** : Nouveaux tests pour valider la correction multiscale fusion
- **Tests d'Intégration** : Validation que les changements de paramètres affectent le résultat final
- **Tests Réalistes** : Validation avec images synthétiques représentatives

### 📋 Détails Techniques
- **Workflow Corrigé** : `multiscale_fusion(original, processed)` utilise maintenant `processed` correctement
- **Variants Logic** : Les variantes partent maintenant de l'image traitée au lieu de l'image originale
- **Pipeline Respect** : Chaque étape du pipeline (White Balance, UDCP, Beer-Lambert, etc.) influence le résultat final

## [2.1.0] - 2025-08-10

### 🚀 Enhanced Auto-Tune Methods
- **Méthodes Auto-Tune Améliorées** : Implémentation basée sur la littérature scientifique
- **3 Méthodes Spécialisées** : 
  - White Balance Auto-Tune (Iqbal et al., 2007)
  - UDCP Auto-Tune (Ancuti et al., 2018)  
  - Beer-Lambert Auto-Tune (Chiang & Chen, 2012)

### 🏗️ Organisation du Projet
- **Restructuration Tests** : Organisation professionnelle des tests sous `tests/`
- **Structure Modulaire** : Séparation claire des responsabilités
- **Documentation** : README et documentation technique améliorés

### 📦 Repository Management
- **Git Workflow** : Tags de version et commits organisés
- **Version Tracking** : Système de versioning sémantique
- **Branch Management** : Stratégie de branches pour développement