@echo off
REM Script pour créer l'archive de distribution Aqualix v2.0.0

echo ========================================
echo  AQUALIX v2.0.0 - CRÉATION DISTRIBUTION
echo ========================================

REM Vérifier si l'exécutable existe
if not exist "dist\Aqualix\Aqualix.exe" (
    echo ❌ ERREUR: Exécutable non trouvé!
    echo    Exécutez d'abord build_executable.bat
    pause
    exit /b 1
)

echo ✅ Exécutable trouvé: dist\Aqualix\Aqualix.exe

REM Supprimer l'ancienne archive si elle existe
if exist "Aqualix-v2.0.0-Windows.zip" (
    echo 🗑️  Suppression de l'ancienne archive...
    del "Aqualix-v2.0.0-Windows.zip"
)

echo 📦 Création de l'archive de distribution...

REM Créer l'archive ZIP avec PowerShell
powershell -Command "Compress-Archive -Path 'dist\Aqualix\*' -DestinationPath 'Aqualix-v2.0.0-Windows.zip' -Force"

REM Vérifier la création
if exist "Aqualix-v2.0.0-Windows.zip" (
    echo.
    echo ========================================
    echo  ✅ DISTRIBUTION CRÉÉE AVEC SUCCÈS!
    echo ========================================
    echo.
    echo 📁 Archive: Aqualix-v2.0.0-Windows.zip
    
    REM Afficher la taille de l'archive
    for %%A in ("Aqualix-v2.0.0-Windows.zip") do (
        echo 📏 Taille: %%~zA bytes
        set /a sizeMB=%%~zA/1024/1024
    )
    
    echo.
    echo 🎯 L'archive est prête pour la release GitHub v2.0.0!
    echo.
    echo 📋 CONTENU DE L'ARCHIVE:
    echo    • Aqualix.exe (application principale)
    echo    • _internal\ (dépendances bundlées)
    echo    • src\ (code source pour référence)
    echo    • config\ (fichiers de configuration)
    echo    • docs\ (documentation)
    echo    • LICENSE, CHANGELOG.md, requirements.txt
    echo.
    echo 🚀 PROCHAINES ÉTAPES:
    echo    1. Ouvrir GitHub.com/almtlsandbox/Aqualix/releases
    echo    2. Cliquer "Create a new release"
    echo    3. Tag: v2.0.0
    echo    4. Titre: "Aqualix v2.0.0 - Standalone Windows Executable"
    echo    5. Glisser cette archive dans les assets
    echo    6. Publier la release
    echo.
) else (
    echo.
    echo ❌ ERREUR: Échec de création de l'archive!
    echo.
)

pause