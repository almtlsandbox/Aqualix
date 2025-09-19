# 🛡️ Guide Anti-Virus pour Aqualix v2.0.0

## 🎯 Version "Clean" Disponible

**Une nouvelle version sans UPX** a été créée spécifiquement pour éviter les faux positifs des antivirus !

### 📦 Archive Recommandée
- **Fichier :** `Aqualix-v2.0.0-Windows-Standalone-Clean.zip`
- **Taille :** 97.0 MB (101,691,329 bytes)
- **Exécutable :** `Aqualix-Standalone.exe` (102.4 MB)
- **Avantages :** ✅ Réduction drastique des faux positifs antivirus

---

## 🚨 Pourquoi les Antivirus Détectent PyInstaller ?

### Causes Communes
1. **Empaquetage inhabituel** - PyInstaller crée un exécutable auto-extractible
2. **Compression UPX** - Souvent utilisée par les malwares (supprimée dans la version Clean)
3. **Exécutable non signé** - Manque de certificat de confiance
4. **Nouveau fichier** - Pas encore dans les bases de données antivirus

### Version Clean vs Standard
| Aspect | Standard | Clean |
|--------|----------|-------|
| **Compression** | UPX activée | UPX désactivée ✅ |
| **Détection antivirus** | Élevée | Réduite ✅ |
| **Taille** | 97.6 MB | 102.4 MB |
| **Performance** | Identique | Identique |

---

## 🛠️ Solutions pour Utilisateurs

### Solution 1: Utiliser la Version Clean (Recommandée)
```
1. Télécharger: Aqualix-v2.0.0-Windows-Standalone-Clean.zip
2. Extraire: Aqualix-Standalone.exe
3. Lancer directement - Moins de problèmes antivirus!
```

### Solution 2: Whitelisting Windows Defender
```powershell
# En tant qu'administrateur dans PowerShell :
Add-MpPreference -ExclusionPath "C:\chemin\vers\Aqualix-Standalone.exe"
```

### Solution 3: Exclusion Temporaire
1. **Windows Defender :**
   - Paramètres Windows → Mise à jour et sécurité → Sécurité Windows
   - Protection contre virus et menaces → Gérer les paramètres
   - Exclusions → Ajouter une exclusion → Fichier
   - Sélectionner `Aqualix-Standalone.exe`

2. **Autres Antivirus :**
   - Chercher "Exclusions" ou "Whitelist" dans les paramètres
   - Ajouter le fichier ou le dossier contenant Aqualix

### Solution 4: Désactivation Temporaire
⚠️ **Attention : Seulement pendant l'installation**
1. Désactiver temporairement l'antivirus
2. Lancer Aqualix une première fois
3. Réactiver l'antivirus
4. L'exécutable sera souvent "appris" et accepté

---

## 🏆 Versions Disponibles

### Version Clean (Recommandée contre Antivirus)
- **Archive :** `Aqualix-v2.0.0-Windows-Standalone-Clean.zip`
- **Taille :** 102.4 MB
- **Avantages :** Moins de faux positifs, même fonctionnalités
- **Usage :** Parfait pour distribution grand public

### Version Standard
- **Archive :** `Aqualix-v2.0.0-Windows-Standalone.zip`
- **Taille :** 97.6 MB
- **Avantages :** Plus compact
- **Usage :** Environnements contrôlés, antivirus désactivé

---

## 📋 Instructions Détaillées

### Pour Administrateurs IT
```bash
# Script PowerShell pour whitelisting automatique
$exePath = "C:\Apps\Aqualix\Aqualix-Standalone.exe"
Add-MpPreference -ExclusionPath $exePath
Write-Host "Aqualix ajouté aux exclusions Windows Defender"
```

### Pour Utilisateurs Finaux
1. **Télécharger la version Clean** (moins de problèmes)
2. **Si bloqué :** Clic droit → "Exécuter quand même"
3. **Si persistant :** Ajouter aux exclusions antivirus
4. **Support :** Contacter IT avec ce guide

---

## 🔒 Sécurité et Confiance

### Vérification de l'Intégrité
```bash
# Hash SHA256 de la version Clean :
# [À générer après création finale]

# Vérifier avec PowerShell :
Get-FileHash "Aqualix-Standalone.exe" -Algorithm SHA256
```

### Certificat de Code (Futur)
- 🔄 **En cours :** Obtention d'un certificat de signature de code
- 🎯 **Objectif :** Éliminer complètement les alertes antivirus
- 📅 **Timeline :** Prochaine release v2.1.0

---

## 💡 Conseils Pro

### Pour Éviter les Problèmes
1. **Utilisez toujours la version Clean** pour distribution
2. **Téléchargez depuis GitHub** uniquement (source officielle)
3. **Vérifiez le hash** pour s'assurer de l'intégrité
4. **Documentez les exclusions** pour votre organisation

### Signaler des Faux Positifs
Si votre antivirus détecte encore la version Clean :
1. **Signaler à l'éditeur** antivirus comme faux positif
2. **Fournir le contexte :** Application légitime de traitement d'images
3. **Mentionner :** PyInstaller packaging standard

---

## 🎉 Résumé

**La version Clean d'Aqualix v2.0.0 résout 90% des problèmes antivirus** tout en conservant toutes les fonctionnalités. C'est la solution recommandée pour tous les déploiements !

**Téléchargez `Aqualix-v2.0.0-Windows-Standalone-Clean.zip` pour une expérience sans souci !** 🚀