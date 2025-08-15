@echo off
REM Script pour ouvrir la page GitHub Releases et guider vers la création

echo ========================================
echo  AQUALIX - CRÉATION GITHUB RELEASE
echo ========================================
echo.
echo Ce script va ouvrir GitHub pour créer une release officielle
echo avec l'exécutable Aqualix.
echo.

REM Vérifier si l'archive existe
if not exist "Aqualix-v1.0.2-Windows-.zip" (
    echo ❌ ERREUR: Archive non trouvée!
        echo    Exécutez d'abord create_distribution.bat
    pause
    exit /b 1
)

echo ✅ Archive trouvée: Aqualix-v1.0.2-Windows-.zip
for %%A in ("Aqualix-v1.0.2-Windows-.zip") do echo    Taille: %%~zA bytes

echo.
echo 📋 ÉTAPES À SUIVRE:
echo.
echo 1. GitHub va s'ouvrir dans votre navigateur
echo 2. Connectez-vous si nécessaire
echo 3. Cliquez sur "Create a new release"
echo 4. Utilisez le tag: v1.0.2-windows
echo 5. Ajoutez le titre: "Aqualix v1.0.2 - Version Exécutable Windows"
echo 6. GLISSEZ l'archive ZIP dans la zone "Attach binaries"
echo 7. Cliquez "Publish release"
echo.

pause

REM Ouvrir GitHub Releases
echo Ouverture de GitHub Releases...
start "GitHub" "https://github.com/almtlsandbox/Aqualix/releases/new?tag=v1.0.2-windows&title=Aqualix%%20v1.0.2%%20-%%20Version%%20Exécutable%%20Windows"

echo.
echo 🌐 GitHub ouvert dans votre navigateur!
echo.
echo 📁 L'archive à attacher se trouve dans ce dossier:
echo    %CD%\Aqualix-v1.0.2-Windows-.zip
echo.
echo 💡 ASTUCE: Ouvrez l'explorateur de fichiers et glissez
echo    l'archive directement dans la zone GitHub!

pause
