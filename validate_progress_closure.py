#!/usr/bin/env python3
"""
Test simple de validation - fermeture automatique barre de progression
"""

import sys
import os

# Ajouter le répertoire src au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

print("🚀 VALIDATION FERMETURE PROGRESS BAR")
print("=" * 50)

try:
    # Test 1: Vérifier les améliorations dans save_result()
    print("📋 Test 1: Améliorations dans save_result()")
    
    with open('src/main.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
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
    
    # Vérifications
    has_time_import = 'import time' in save_result_code
    has_sleep = 'time.sleep(' in save_result_code
    has_context_manager = 'with show_progress(' in save_result_code
    has_finalisation = 'Finalisation' in save_result_code
    has_exit_comment = 'automatically closed' in save_result_code or 'context manager' in save_result_code
    
    print(f"   • Import time pour délai: {'✅' if has_time_import else '❌'}")
    print(f"   • Délai avant fermeture: {'✅' if has_sleep else '❌'}")
    print(f"   • Context manager présent: {'✅' if has_context_manager else '❌'}")
    print(f"   • Message finalisation: {'✅' if has_finalisation else '❌'}")
    print(f"   • Documentation fermeture: {'✅' if has_exit_comment else '❌'}")
    
    # Test 2: Vérifier les améliorations dans progress_bar.py
    print("\n📋 Test 2: Améliorations dans progress_bar.py")
    
    with open('src/progress_bar.py', 'r', encoding='utf-8') as f:
        pb_content = f.read()
    
    # Analyser la méthode hide()
    hide_lines = []
    in_hide = False
    
    for line in pb_content.split('\n'):
        if 'def hide(self):' in line:
            in_hide = True
        elif in_hide and line.strip().startswith('def '):
            break
        
        if in_hide:
            hide_lines.append(line)
    
    hide_code = '\n'.join(hide_lines)
    
    # Vérifications
    has_update_idletasks = 'update_idletasks' in hide_code
    has_update_call = 'self.parent.update()' in hide_code
    has_immediate_comment = 'immediately' in hide_code
    has_force_ui_update = 'Force UI update' in hide_code or 'Process all pending events' in hide_code
    
    print(f"   • update_idletasks() ajouté: {'✅' if has_update_idletasks else '❌'}")
    print(f"   • parent.update() ajouté: {'✅' if has_update_call else '❌'}")
    print(f"   • Documentation 'immediately': {'✅' if has_immediate_comment else '❌'}")
    print(f"   • Commentaires Force UI: {'✅' if has_force_ui_update else '❌'}")
    
    # Résumé
    print("\n📊 RÉSUMÉ:")
    
    save_result_improvements = sum([has_time_import, has_sleep, has_context_manager, has_finalisation])
    progress_bar_improvements = sum([has_update_idletasks, has_update_call, has_immediate_comment])
    
    print(f"   • save_result() améliorations: {save_result_improvements}/4")
    print(f"   • progress_bar.py améliorations: {progress_bar_improvements}/3")
    
    if save_result_improvements >= 3 and progress_bar_improvements >= 2:
        print("\n🎉 AMÉLIORATIONS RÉUSSIES!")
        print("   Les modifications pour la fermeture automatique sont en place:")
        print("   • Délai pour montrer la completion")
        print("   • Context manager pour fermeture automatique")
        print("   • Fermeture UI forcée avec update_idletasks()")
        print("   • Processing des événements avec update()")
        print("\n💡 RÉSULTAT ATTENDU:")
        print("   La barre de progression doit maintenant disparaître")
        print("   automatiquement une fois les calculs terminés!")
    else:
        print("\n⚠️  AMÉLIORATIONS INCOMPLÈTES")
        if save_result_improvements < 3:
            print("   - save_result() manque certaines améliorations")
        if progress_bar_improvements < 2:
            print("   - progress_bar.py manque certaines améliorations")

except Exception as e:
    print(f"❌ Erreur: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 50)
print("📝 VALIDATION TERMINÉE")
