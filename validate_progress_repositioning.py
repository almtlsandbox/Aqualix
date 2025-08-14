#!/usr/bin/env python3
"""
Test simple du nouveau positionnement de la barre de progression
"""

import sys
import os

# Ajouter le répertoire src au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

print("🚀 VALIDATION CHANGEMENT BARRE DE PROGRESSION")
print("=" * 60)

try:
    # Test 1: Vérifier que save_result() importe bien progress_bar
    print("📋 Test 1: Import de progress_bar dans save_result()")
    
    with open('src/main.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Rechercher la fonction save_result et vérifier qu'elle contient progress_bar
    save_result_found = 'def save_result(self):' in content
    progress_import_found = 'from .progress_bar import show_progress' in content
    
    print(f"   • Fonction save_result trouvée: {'✅' if save_result_found else '❌'}")
    
    # Analyser la fonction save_result
    lines = content.split('\n')
    in_save_result = False
    save_result_lines = []
    
    for line in lines:
        if 'def save_result(self):' in line:
            in_save_result = True
        elif in_save_result and line.strip().startswith('def ') and 'save_result' not in line:
            break
        
        if in_save_result:
            save_result_lines.append(line)
    
    save_result_code = '\n'.join(save_result_lines)
    
    # Vérifications dans save_result()
    has_progress_import = 'from .progress_bar import show_progress' in save_result_code
    has_show_progress = 'with show_progress(' in save_result_code
    has_full_res_call = 'get_full_resolution_processed_image()' in save_result_code
    has_progress_messages = 'progress.update_message(' in save_result_code
    
    print(f"   • Import progress_bar: {'✅' if has_progress_import else '❌'}")
    print(f"   • Context manager show_progress: {'✅' if has_show_progress else '❌'}")
    print(f"   • Appel get_full_resolution_processed_image: {'✅' if has_full_res_call else '❌'}")
    print(f"   • Messages de progression: {'✅' if has_progress_messages else '❌'}")
    
    # Test 2: Vérifier que save_image() n'a plus la barre de progression
    print("\n📋 Test 2: Suppression progress_bar de save_image()")
    
    # Analyser la fonction save_image
    in_save_image = False
    save_image_lines = []
    
    for line in lines:
        if 'def save_image(self):' in line:
            in_save_image = True
        elif in_save_image and line.strip().startswith('def ') and 'save_image' not in line:
            break
        
        if in_save_image:
            save_image_lines.append(line)
    
    save_image_code = '\n'.join(save_image_lines)
    
    # Vérifications dans save_image()
    save_image_no_progress_import = 'from .progress_bar import show_progress' not in save_image_code
    save_image_no_show_progress = 'with show_progress(' not in save_image_code
    save_image_no_progress_messages = 'progress.update_message(' not in save_image_code
    
    print(f"   • Pas d'import progress_bar: {'✅' if save_image_no_progress_import else '❌'}")
    print(f"   • Pas de show_progress: {'✅' if save_image_no_show_progress else '❌'}")
    print(f"   • Pas de progress messages: {'✅' if save_image_no_progress_messages else '❌'}")
    
    # Résumé
    print("\n📊 RÉSUMÉ:")
    
    save_result_ok = has_progress_import and has_show_progress and has_full_res_call and has_progress_messages
    save_image_ok = save_image_no_progress_import and save_image_no_show_progress and save_image_no_progress_messages
    
    print(f"   • save_result() avec progress bar: {'✅' if save_result_ok else '❌'}")
    print(f"   • save_image() sans progress bar: {'✅' if save_image_ok else '❌'}")
    
    if save_result_ok and save_image_ok:
        print("\n🎉 CHANGEMENT RÉUSSI!")
        print("   La barre de progression apparaît maintenant au clic 'Sauvegarder le résultat'")
        print("   Elle couvre les calculs lents (traitement pleine résolution)")
        print("   Plus de barre de progression pendant l'écriture du fichier")
    else:
        print("\n⚠️  CHANGEMENT INCOMPLET")
        if not save_result_ok:
            print("   - save_result() ne contient pas tous les éléments progress bar")
        if not save_image_ok:
            print("   - save_image() contient encore des éléments progress bar")

except Exception as e:
    print(f"❌ Erreur: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("📝 VALIDATION TERMINÉE")
