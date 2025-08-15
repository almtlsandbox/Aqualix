@echo off
REM Script de création de l'archive de distribution Aqualix

echo ========================================
echo  AQUALIX - CRÉATION ARCHIVE DISTRIBUTION
echo ========================================

REM Vérifier si l'exécutable existe
if not exist "dist\Aqualix\Aqualix.exe" (
    echo Erreur: Exécutable non trouvé!
    echo Veuillez d'abord exécuter build_executable.bat
    pause
    exit /b 1
)

REM Nom de l'archive avec date et version
for /f "tokens=2-4 delims=/ " %%a in ('date /t') do set mydate=%%c-%%b-%%a
for /f "tokens=1-2 delims=: " %%a in ('time /t') do set mytime=%%a-%%b
set archive_name=Aqualix-v1.0.2-Windows-%mydate%

echo Création de l'archive: %archive_name%.zip
echo.

REM Créer l'archive avec PowerShell
powershell -command "Compress-Archive -Path 'dist\Aqualix\*' -DestinationPath '%archive_name%.zip' -Force"

if exist "%archive_name%.zip" (
    echo.
    echo ========================================
    echo  ARCHIVE CRÉÉE AVEC SUCCÈS!
    echo ========================================
    echo.
    echo Archive: %archive_name%.zip
    
    REM Obtenir la taille de l'archive
    for %%A in ("%archive_name%.zip") do echo Taille: %%~zA bytes
    
    echo.
    echo L'archive est prête pour distribution!
    echo Elle contient tout ce qui est nécessaire pour exécuter Aqualix.
    echo.
    echo Instructions pour l'utilisateur final:
    echo 1. Télécharger et extraire l'archive
    echo 2. Ouvrir le dossier extrait
    echo 3. Double-cliquer sur Aqualix.exe
    echo.
) else (
    echo.
    echo ========================================
    echo  ÉCHEC DE CRÉATION DE L'ARCHIVE!
    echo ========================================
    echo.
    echo Vérifiez que PowerShell est disponible.
    echo.
)

pause
