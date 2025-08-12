#!/usr/bin/env python3
"""
Test simple du système de localisation
"""

from src.localization import get_localization_manager, t, set_language

def test_localization():
    """Test des traductions"""
    print("Test du système de localisation")
    print("="*50)
    
    # Test en français (par défaut)
    print(f"Langue courante: {get_localization_manager().get_language()}")
    print(f"Titre de l'application: {t('app_title')}")
    print(f"Sélectionner un fichier: {t('select_file')}")
    print(f"Paramètres: {t('tab_parameters')}")
    print()
    
    # Test en anglais
    set_language('en')
    print(f"Langue courante: {get_localization_manager().get_language()}")
    print(f"Titre de l'application: {t('app_title')}")
    print(f"Sélectionner un fichier: {t('select_file')}")
    print(f"Paramètres: {t('tab_parameters')}")
    print()
    
    # Test de clé inexistante
    print(f"Clé inexistante: {t('inexistant_key')}")
    
    # Test avec formatage
    print(f"Formatage: {t('file_info', filename='test.jpg', index=1, total=5)}")

if __name__ == "__main__":
    test_localization()

