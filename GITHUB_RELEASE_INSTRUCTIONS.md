# Instructions pour Créer une GitHub Release avec l'Exécutable

## 🎯 Objectif
Distribuer l'exécutable Windows Aqualix via une GitHub Release officielle.

## 📋 Étapes à Suivre

### 1. Accéder aux Releases GitHub
1. Aller sur: **https://github.com/almtlsandbox/Aqualix**
2. Cliquer sur l'onglet **"Releases"** (à droite des onglets Code/Issues/Pull requests)
3. Cliquer sur **"Create a new release"**

### 2. Configurer la Release

#### Tag Information:
- **Tag version**: `v1.0.0-windows` (déjà créé)
- **Target**: `main` branch
- **Release title**: `Aqualix v1.0.0 - Version Exécutable Windows`

#### Description de la Release:
```markdown
# 🌊 Aqualix v1.0.0 - Première Release Windows

## 🎉 Nouvelle Version Exécutable!

Aqualix est maintenant disponible sous forme d'exécutable Windows autonome - **aucune installation requise**!

### ✨ Fonctionnalités

#### Traitement d'Images Sous-Marines
- **Correction automatique** des couleurs aquatiques
- **White Balance** adaptatif pour milieux sous-marins
- **UDCP** (Underwater Dark Channel Prior)
- **Égalisation d'histogramme** CLAHE optimisée
- **Fusion multi-échelle** pour résultats parfaits

#### Interface Utilisateur
- **Design aquatique** avec couleurs douces inspirées de l'océan
- **Prévisualisation interactive** avec zoom et panoramique
- **Navigation intuitive** par onglets
- **Contrôle qualité intelligent** avec recommandations
- **Boutons optimisés** avec contraste parfait

### 📦 Installation

1. **Télécharger** `Aqualix-v1.0.0-Windows.zip`
2. **Extraire** l'archive dans un dossier
3. **Double-cliquer** sur `Aqualix.exe`
4. **Profiter** du traitement d'images sous-marines!

### 💻 Compatibilité

- **OS**: Windows 10/11 (64-bit)
- **RAM**: 4 GB minimum, 8 GB recommandé
- **Espace**: 500 MB libre
- **Installation**: Aucune - Prêt à l'emploi!

### 🎨 Formats Supportés

- **Images**: JPG, PNG, TIFF, BMP, WEBP
- **Vidéos**: MP4, AVI, MOV, MKV
- **Export**: Haute qualité configurable

### 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/almtlsandbox/Aqualix/issues)
- **Email**: arnauddominique.lina@gmail.com
- **Site**: https://www.ridinaroundmtl.ca/

---
🌊 **Bon traitement de vos photos sous-marines!** 🌊
```

### 3. Attacher l'Archive

1. Dans la section **"Attach binaries by dropping them here or selecting them"**
2. **Faire glisser** le fichier `Aqualix-v1.0.0-Windows-.zip` depuis votre explorateur
3. **OU** cliquer sur la zone et sélectionner le fichier

### 4. Publier

1. **Cocher** "Set as the latest release" si c'est la version principale
2. **Cliquer** sur **"Publish release"**

## 📍 Localisation du Fichier

Le fichier ZIP à attacher se trouve ici:
```
d:\OneDrive\DOCS\BATEAU-SCUBA\SCUBA\PHOTOS\COLOR CORRECTION\UI_Template\Aqualix-v1.0.0-Windows-.zip
```

Taille: **98.53 MB**

## ✅ Résultat Final

Après publication, les utilisateurs pourront:
1. Visiter la page Releases
2. Télécharger directement l'exécutable
3. L'installer en un clic
4. Utiliser Aqualix immédiatement

## 🔄 Mises à Jour Futures

Pour les prochaines versions:
1. Modifier le code source
2. Exécuter `build_executable.bat`
3. Créer une nouvelle release avec nouveau tag
4. Attacher la nouvelle archive
