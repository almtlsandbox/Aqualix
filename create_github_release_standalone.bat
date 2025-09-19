@echo off
REM Script pour créer la GitHub Release v2.0.0 d'Aqualix STANDALONE

echo ========================================
echo  AQUALIX v2.0.0 - STANDALONE RELEASE
echo ========================================
echo.

REM Vérifier si l'exécutable standalone existe
if not exist "standalone\Aqualix-Standalone.exe" (
    echo ❌ ERREUR: Exécutable standalone non trouvé!
    echo    Exécutez d'abord: pyinstaller --onefile --windowed main.py
    pause
    exit /b 1
)

REM Vérifier si l'archive standalone existe
if not exist "Aqualix-v2.0.0-Windows-Standalone.zip" (
    echo ❌ ERREUR: Archive standalone non trouvée!
    echo    Création de l'archive...
    powershell -Command "Compress-Archive -Path 'standalone\Aqualix-Standalone.exe' -DestinationPath 'Aqualix-v2.0.0-Windows-Standalone.zip' -Force"
)

echo ✅ Exécutable standalone trouvé: standalone\Aqualix-Standalone.exe
for %%A in ("standalone\Aqualix-Standalone.exe") do (
    echo    📏 Taille: %%~zA bytes (~97.6 MB)
    echo    📅 Créé: %%~tA
)

echo ✅ Archive standalone trouvée: Aqualix-v2.0.0-Windows-Standalone.zip
for %%A in ("Aqualix-v2.0.0-Windows-Standalone.zip") do (
    echo    📏 Taille: %%~zA bytes (~97.0 MB)
    echo    📅 Créée: %%~tA
)

echo.
echo 🎯 INFORMATIONS DE RELEASE STANDALONE:
echo    • Version: v2.0.0
echo    • Type: STANDALONE EXECUTABLE - UN SEUL FICHIER
echo    • Plateforme: Windows 64-bit
echo    • Taille: ~97.6 MB (tout inclus)
echo    • Dépendances: AUCUNE - Complètement autonome
echo.

echo 📋 ÉTAPES POUR CRÉER LA RELEASE:
echo.
echo 1. 🌐 GitHub va s'ouvrir dans votre navigateur
echo 2. 🔐 Connectez-vous si nécessaire  
echo 3. 🏷️  Tag version: v2.0.0
echo 4. 📝 Titre: "Aqualix v2.0.0 - True Standalone Windows Executable"
echo 5. 📦 Glissez l'archive dans "Attach binaries"
echo 6. 📄 Copiez la description suggérée ci-dessous
echo 7. ✅ Cliquez "Publish release"
echo.

echo 📄 DESCRIPTION SUGGÉRÉE POUR LA RELEASE:
echo ----------------------------------------
echo.
echo ## 🚀 Aqualix v2.0.0 - True Standalone Windows Executable
echo.
echo **Version majeure** avec exécutable Windows 100%% autonome - UN SEUL FICHIER!
echo.
echo ### ✨ Nouveautés STANDALONE
echo - 📦 **UN SEUL FICHIER EXE** - Aucune dépendance externe
echo - 🚀 **ZERO INSTALLATION** requise sur la machine cible
echo - 💾 **PORTABLE COMPLET** - Fonctionne depuis USB/réseau  
echo - 🎯 **97.6 MB TOTAL** - Toutes librairies incluses
echo - 🖥️  **Interface optimisée** et refactorisée
echo.
echo ### 💻 Avantages STANDALONE
echo - **Windows 10/11** (64-bit) uniquement
echo - **Taille:** 97.6 MB (tout inclus)
echo - **Dépendances:** AUCUNE - Python, OpenCV, NumPy, SciPy, PIL inclus
echo - **Installation:** Télécharger, extraire, double-cliquer
echo.
echo ### 🎯 Utilisation Ultra-Simple
echo 1. Télécharger `Aqualix-v2.0.0-Windows-Standalone.zip`
echo 2. Extraire `Aqualix-Standalone.exe`
echo 3. Double-cliquer pour lancer - C'EST TOUT!
echo.
echo ### 🛠️ Fonctionnalités Complètes
echo - Traitement d'images sous-marines professionnelles
echo - Correction automatique des couleurs
echo - Interface intuitive avec aperçu temps réel
echo - Support vidéo et traitement par lots
echo - Exportation haute qualité
echo - Pas de configuration nécessaire
echo.
echo **Le plus simple possible - UN FICHIER, TOUT INCLUS!** 🎉
echo.
echo ----------------------------------------

pause

echo.
echo 🌐 Ouverture de GitHub Releases...

REM Ouvrir GitHub avec les paramètres pré-remplis
start "GitHub Release" "https://github.com/almtlsandbox/Aqualix/releases/new?tag=v2.0.0&title=Aqualix%%20v2.0.0%%20-%%20True%%20Standalone%%20Windows%%20Executable"

echo.
echo ✅ GitHub ouvert dans votre navigateur!
echo.
echo 📁 Archive à glisser: %CD%\Aqualix-v2.0.0-Windows-Standalone.zip
echo.
echo 💡 AVANTAGES DU STANDALONE:
echo    • UN SEUL FICHIER - Pas de dossier de dépendances
echo    • ZERO INSTALLATION - Aucune configuration requise
echo    • PORTABLE TOTAL - Fonctionne partout immédiatement
echo    • SIMPLE À DISTRIBUER - Un seul fichier à partager
echo.

pause