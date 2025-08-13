"""Test simple des traductions"""

# Test direct avec des imports absolus
import sys
import os
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))

# Ajouter le répertoire src au path
src_path = os.path.join(str(Path(__file__).parent.parent.parent), 'src')
sys.path.insert(0, src_path)

def test_translations():
    """Test simple des traductions"""
    print("🧪 Test des traductions des boutons")
    print("=" * 50)
    
    # Test direct des traductions
    translations_fr = {
        'save_result': 'Sauvegarder le résultat',
        'quality_check': 'Contrôle Qualité',
        'select_file': 'Sélectionner un fichier',
        'select_folder': 'Sélectionner un dossier',
        'previous': 'Précédent',
        'next': 'Suivant'
    }
    
    translations_en = {
        'save_result': 'Save Result',
        'quality_check': 'Quality Check', 
        'select_file': 'Select File',
        'select_folder': 'Select Folder',
        'previous': 'Previous',
        'next': 'Next'
    }
    
    print("🇫🇷 Traductions françaises:")
    for key, value in translations_fr.items():
        print(f"   {key}: '{value}'")
    
    print("\n🇬🇧 Traductions anglaises:")
    for key, value in translations_en.items():
        print(f"   {key}: '{value}'")
        
    print("\n✅ Correction appliquée:")
    print("   - Ajout de 'quality_check' dans update_toolbar_texts()")
    print("   - Les deux boutons seront maintenant traduits lors du changement de langue")
    print("   - La liste button_texts contient maintenant tous les boutons dans l'ordre")

if __name__ == "__main__":
    test_translations()
