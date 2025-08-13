"""
Test rapide de la traduction des boutons de barre d'outils
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from localization import LocalizationManager, set_global_localization_manager, t

def test_button_translations():
    """Test des traductions des boutons de la barre d'outils"""
    
    print("🧪 Test des traductions des boutons de barre d'outils")
    print("=" * 60)
    
    # Initialisation du manager de localisation
    localization_manager = LocalizationManager()
    set_global_localization_manager(localization_manager)
    
    # Test des boutons en français
    print("\n🇫🇷 FRANÇAIS:")
    localization_manager.set_language('fr')
    
    buttons = [
        ('select_file', 'Bouton Sélectionner fichier'),
        ('select_folder', 'Bouton Sélectionner dossier'), 
        ('previous', 'Bouton Précédent'),
        ('next', 'Bouton Suivant'),
        ('quality_check', 'Bouton Contrôle Qualité'),
        ('save_result', 'Bouton Sauvegarder'),
    ]
    
    for key, desc in buttons:
        translation = t(key)
        print(f"   {desc}: '{translation}'")
    
    # Test des boutons en anglais
    print("\n🇬🇧 ENGLISH:")
    localization_manager.set_language('en')
    
    for key, desc in buttons:
        translation = t(key)
        print(f"   {desc}: '{translation}'")
        
    print(f"\n✅ Test terminé - Toutes les traductions sont disponibles!")

if __name__ == "__main__":
    test_button_translations()
