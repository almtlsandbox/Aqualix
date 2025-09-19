# Aqualix v2.0.0 Release Notes

## 🚀 Aqualix v2.0.0 - Standalone Windows Executable

**Date de release:** 19 septembre 2025  
**Version majeure** avec exécutable Windows autonome complet!

---

## ✨ Nouveautés principales

### 📦 Exécutable Standalone
- **Aucune installation Python requise** sur la machine cible
- **Toutes les dépendances bundlées** (OpenCV, PIL, NumPy, SciPy, Tkinter)
- **Portable** - Fonctionne depuis USB, réseau ou dossier local
- **Taille optimisée** avec compression UPX

### 🎯 Interface Utilisateur Améliorée
- **Panel de paramètres refactorisé** avec alignement pixel-perfect
- **Boutons d'action** remplaçant les anciennes checkboxes
- **Navigation améliorée** avec contrôles intuitifs
- **Aperçu temps réel** des modifications

### 🔧 Code et Structure
- **Réorganisation complète** des tests sous `tests/`
- **Suppression** des fichiers obsolètes et legacy
- **Documentation** mise à jour et complète
- **Scripts de build** automatisés

---

## 💻 Informations Techniques

### Compatibilité
- **Plateformes:** Windows 10/11 (64-bit)
- **Taille archive:** ~98.5 MB
- **Taille installée:** ~265 MB
- **Nombre de fichiers:** 1,436

### Build Information
- **PyInstaller:** v6.16.0
- **Python:** 3.9.10
- **Compression:** UPX activée
- **Mode:** GUI (pas de console)

---

## 🎯 Installation et Utilisation

### Installation Simple
1. **Télécharger** `Aqualix-v2.0.0-Windows.zip`
2. **Extraire** le contenu dans un dossier
3. **Lancer** `Aqualix.exe` directement

### Aucune Configuration Requise
- ✅ Pas d'installation Python nécessaire
- ✅ Pas de dépendances à installer
- ✅ Fonctionne immédiatement après extraction
- ✅ Peut être déplacé/copié sur d'autres PC

---

## 🛠️ Fonctionnalités Complètes

### Traitement d'Images
- **Correction automatique** des couleurs sous-marines
- **Gray-world white balancing** pour équilibrage naturel
- **Égalisation d'histogramme** pour améliorer le contraste
- **Paramètres ajustables** en temps réel

### Interface Avancée
- **Navigateur de fichiers** intégré (images/vidéos/dossiers)
- **Contrôles de navigation** next/previous intuitifs
- **Slider vidéo** pour navigation frame par frame
- **Vue divisée interactive** avec zoom/pan/rotation
- **Aperçu temps réel** des modifications

### Export et Traitement par Lots
- **Sauvegarde haute qualité** des résultats
- **Traitement par lots** pour vidéos (application sur toutes les frames)
- **Formats supportés** : JPEG, PNG, MP4, AVI, etc.

---

## 📁 Contenu de la Distribution

```
Aqualix/
├── Aqualix.exe          # Application principale (6.92 MB)
├── _internal/           # Dépendances bundlées
├── src/                 # Code source (référence)
├── config/              # Fichiers de configuration
├── docs/                # Documentation
├── LICENSE              # Licence
├── CHANGELOG.md         # Historique des versions
└── requirements.txt     # Liste des dépendances
```

---

## 🔄 Migration depuis v1.x

### Pas de Migration Nécessaire
- **Nouvelle installation** recommandée
- **Aucun conflit** avec versions précédentes
- **Paramètres réinitialisés** aux valeurs optimales

### Avantages du Passage à v2.0.0
- 🚀 **Performance** améliorée (exécutable natif)
- 💾 **Portabilité** totale (pas d'environnement Python requis)  
- 🎯 **Interface** plus intuitive et responsive
- 📦 **Distribution** simplifiée (un seul fichier ZIP)

---

## 🐛 Corrections de Bugs

- ✅ **Imports relatifs** corrigés pour l'exécutable
- ✅ **Alignement UI** pixel-perfect dans tous les panels
- ✅ **Navigation vidéo** plus fluide et précise
- ✅ **Gestion mémoire** optimisée pour gros fichiers
- ✅ **Auto-tune paramètres** synchronisés correctement

---

## 🎉 Prêt pour la Production!

Cette version v2.0.0 marque une **étape majeure** dans l'évolution d'Aqualix :

- ✅ **Stabilité** validée par tests complets
- ✅ **Performance** optimisée pour usage intensif  
- ✅ **Portabilité** maximale pour déploiement facile
- ✅ **Expérience utilisateur** grandement améliorée

**Parfait pour les photographes sous-marins professionnels et amateurs!** 🌊📸

---

## 🔗 Liens Utiles

- **Repository:** [github.com/almtlsandbox/Aqualix](https://github.com/almtlsandbox/Aqualix)
- **Documentation:** [docs/README.md](docs/README.md)
- **Issues:** [GitHub Issues](https://github.com/almtlsandbox/Aqualix/issues)
- **Changelog:** [CHANGELOG.md](CHANGELOG.md)

---

**Téléchargez maintenant et transformez vos photos sous-marines !** 🚀