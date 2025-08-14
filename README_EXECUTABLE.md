# Aqualix - Exécutable Windows

## 📦 Version Exécutable Prête à Utiliser

Ceci est la version exécutable autonome d'Aqualix pour Windows. Aucune installation de Python n'est requise.

### 🚀 Utilisation Rapide

1. **Téléchargez** le dossier `Aqualix` complet
2. **Double-cliquez** sur `Aqualix.exe` pour lancer l'application
3. **Commencez** à traiter vos images sous-marines !

### 📂 Contenu du Package

```
Aqualix/
├── Aqualix.exe          # Application principale
├── _internal/           # Bibliothèques et dépendances (NE PAS MODIFIER)
├── src/                 # Code source inclus
├── config/              # Fichiers de configuration
├── docs/                # Documentation
├── LICENSE              # Licence MIT
├── CHANGELOG.md         # Historique des versions
└── requirements.txt     # Dépendances (référence)
```

### 💻 Configuration Système Requise

- **OS**: Windows 10/11 (64-bit recommandé)
- **RAM**: 4 GB minimum, 8 GB recommandé
- **Espace**: 500 MB d'espace libre
- **Processeur**: Compatible x86/x64

### 🎯 Fonctionnalités Principales

#### Traitement d'Images Sous-Marines
- **Correction automatique** des couleurs en milieu aquatique
- **White Balance** adaptatif pour conditions sous-marines
- **UDCP** (Underwater Dark Channel Prior)
- **Égalisation d'histogramme** CLAHE
- **Fusion multi-échelle** pour optimisation finale

#### Interface Utilisateur
- **Design aquatique** avec couleurs douces
- **Prévisualisation interactive** avec zoom et panoramique
- **Navigation facile** entre les fichiers
- **Contrôle qualité** intégré avec recommandations
- **Traitement par lots** pour vidéos

#### Formats Supportés
- **Images**: JPG, PNG, TIFF, BMP, WEBP
- **Vidéos**: MP4, AVI, MOV, MKV
- **Export**: JPG, PNG avec qualité configurable

### 🔧 Première Utilisation

1. **Lancez** Aqualix.exe
2. **Cliquez** sur "Parcourir" pour sélectionner une image
3. **Ajustez** les paramètres dans l'onglet "Paramètres"
4. **Visualisez** le résultat en temps réel
5. **Sauvegardez** votre image traitée

### 📊 Contrôle Qualité

L'onglet "Contrôle Qualité" analyse automatiquement vos images et fournit :
- **Score de qualité** global
- **Recommandations** d'amélioration
- **Ajustements suggérés** pour chaque paramètre
- **Comparaison** avant/après

### 🎨 Interface Aquatique

L'application utilise une palette de couleurs inspirée du monde aquatique :
- **Bleu océan** pour les sections principales
- **Corail rose** pour les accents
- **Vert algue** pour les informations
- **Beige sableux** pour les zones neutres

### 🛠️ Dépannage

#### L'application ne se lance pas
- Vérifiez que Windows Defender n'a pas bloqué le fichier
- Clic droit > Propriétés > Débloquer si nécessaire
- Exécutez en tant qu'administrateur si requis

#### Performance lente
- Fermez les autres applications gourmandes en mémoire
- Utilisez des images de taille raisonnable (< 20 MP)
- Activez le mode "Aperçu rapide" pour les grandes images

#### Erreur au traitement
- Vérifiez que l'image n'est pas corrompue
- Essayez avec une autre image
- Consultez les logs dans le dossier `logs/`

### 📝 Support et Contact

- **GitHub**: https://github.com/almtlsandbox/Aqualix
- **Email**: arnauddominique.lina@gmail.com
- **Website**: https://www.ridinaroundmtl.ca/

### 🔄 Mises à Jour

Cette version exécutable est autonome. Pour les mises à jour :
1. Téléchargez la nouvelle version depuis GitHub
2. Remplacez l'ancien dossier par le nouveau
3. Vos paramètres et configurations seront préservés

### 📜 Licence

Aqualix est distribué sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

---

**Version**: 1.0.0  
**Date**: 2025  
**Auteur**: Arnaud Dominique Lina  
**Développé avec**: Python, OpenCV, Tkinter, PyInstaller

🌊 **Bon traitement de vos images sous-marines !** 🌊
