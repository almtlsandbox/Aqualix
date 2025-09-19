@echo off
REM Script pour créer la GitHub Release v2.0.0 d'Aqualix

echo ========================================
echo  AQUALIX v2.0.0 - GITHUB RELEASE
echo ========================================
echo.

REM Vérifier si l'archive existe
if not exist "Aqualix-v2.0.0-Windows.zip" (
    echo ❌ ERREUR: Archive v2.0.0 non trouvée!
    echo    Exécutez d'abord create_distribution_v2.0.0.bat
    pause
    exit /b 1
)

echo ✅ Archive trouvée: Aqualix-v2.0.0-Windows.zip
for %%A in ("Aqualix-v2.0.0-Windows.zip") do (
    echo    📏 Taille: %%~zA bytes (~98.5 MB)
    echo    📅 Créée: %%~tA
)

echo.
echo 🎯 INFORMATIONS DE RELEASE:
echo    • Version: v2.0.0
echo    • Type: Major Release - Standalone Executable
echo    • Plateforme: Windows 64-bit
echo    • Taille: ~98.5 MB
echo.

echo 📋 ÉTAPES POUR CRÉER LA RELEASE:
echo.
echo 1. 🌐 GitHub va s'ouvrir dans votre navigateur
echo 2. 🔐 Connectez-vous si nécessaire  
echo 3. 🏷️  Tag version: v2.0.0
echo 4. 📝 Titre: "Aqualix v2.0.0 - Standalone Windows Executable"
echo 5. 📦 Glissez l'archive dans "Attach binaries"
echo 6. 📄 Copiez la description suggérée ci-dessous
echo 7. ✅ Cliquez "Publish release"
echo.

echo 📄 DESCRIPTION SUGGÉRÉE POUR LA RELEASE:
echo ----------------------------------------
echo.
echo ## 🚀 Aqualix v2.0.0 - Standalone Windows Executable
echo.
echo **Version majeure** avec exécutable Windows autonome complet!
echo.
echo ### ✨ Nouveautés
echo - 📦 **Exécutable standalone** - Aucune installation Python requise
echo - 🎯 **Distribution complète** - Toutes dépendances incluses  
echo - 🖥️  **Interface utilisateur** optimisée et refactorisée
echo - 🔧 **Tests complets** et réorganisation du code
echo - 📚 **Documentation** mise à jour
echo.
echo ### 💻 Compatibilité
echo - **Windows 10/11** (64-bit)
echo - **Taille:** ~98.5 MB
echo - **Portable** - Fonctionne depuis USB/réseau
echo.
echo ### 🎯 Installation
echo 1. Télécharger `Aqualix-v2.0.0-Windows.zip`
echo 2. Extraire le contenu
echo 3. Lancer `Aqualix.exe` directement
echo.
echo ### 🛠️ Fonctionnalités
echo - Traitement d'images sous-marines
echo - Correction automatique des couleurs
echo - Interface intuitive avec aperçu en temps réel
echo - Support vidéo et traitement par lots
echo - Exportation haute qualité
echo.
echo **Prêt à utiliser sans configuration!** 🎉
echo.
echo ----------------------------------------

pause

echo.
echo 🌐 Ouverture de GitHub Releases...

REM Ouvrir GitHub avec les paramètres pré-remplis
start "GitHub Release" "https://github.com/almtlsandbox/Aqualix/releases/new?tag=v2.0.0&title=Aqualix%%20v2.0.0%%20-%%20Standalone%%20Windows%%20Executable"

echo.
echo ✅ GitHub ouvert dans votre navigateur!
echo.
echo 📁 Archive à glisser: %CD%\Aqualix-v2.0.0-Windows.zip
echo.
echo 💡 ASTUCE: 
echo    • Copiez-collez la description suggérée ci-dessus
echo    • Glissez l'archive ZIP dans la zone "Attach binaries"
echo    • Vérifiez que "Set as the latest release" est coché
echo.

pause