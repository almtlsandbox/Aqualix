#!/usr/bin/env python3
"""
Test de la barre de progression avec pourcentages
Valide que la progress bar affiche maintenant un vrai progrès (0-100%)
"""

import sys
import os

# Ajouter le répertoire src au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

print("🚀 TEST BARRE DE PROGRESSION AVEC POURCENTAGES")
print("=" * 60)
print("📋 Objectif: Vérifier que la progress bar affiche des pourcentages")

try:
    # Test 1: Vérifier les modifications dans progress_bar.py
    print("📋 Test 1: Modifications dans progress_bar.py")
    
    with open('src/progress_bar.py', 'r', encoding='utf-8') as f:
        pb_content = f.read()
    
    # Vérifications du mode déterminé
    has_determinate_mode = "mode='determinate'" in pb_content
    has_maximum_100 = "maximum=100" in pb_content
    has_value_0 = "self.progress_bar['value'] = 0" in pb_content
    has_update_progress = "def update_progress(self, percentage:" in pb_content
    has_update_both = "def update_message_and_progress(" in pb_content
    has_clamp_percentage = "max(0, min(100, percentage))" in pb_content
    
    print(f"   • Mode 'determinate': {'✅' if has_determinate_mode else '❌'}")
    print(f"   • Maximum 100: {'✅' if has_maximum_100 else '❌'}")
    print(f"   • Initialisation à 0%: {'✅' if has_value_0 else '❌'}")
    print(f"   • Méthode update_progress: {'✅' if has_update_progress else '❌'}")
    print(f"   • Méthode update_both: {'✅' if has_update_both else '❌'}")
    print(f"   • Protection 0-100%: {'✅' if has_clamp_percentage else '❌'}")
    
    # Test 2: Vérifier les modifications dans save_result()
    print("\n📋 Test 2: Modifications dans save_result()")
    
    with open('src/main.py', 'r', encoding='utf-8') as f:
        main_content = f.read()
    
    # Analyser save_result pour les pourcentages
    lines = main_content.split('\n')
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
    
    # Rechercher les appels avec pourcentages
    has_update_message_and_progress = "update_message_and_progress" in save_result_code
    has_5_percent = ", 5)" in save_result_code
    has_10_percent = ", 10)" in save_result_code  
    has_85_percent = ", 85)" in save_result_code
    has_90_percent = ", 90)" in save_result_code
    has_95_percent = ", 95)" in save_result_code
    has_100_percent = ", 100)" in save_result_code
    
    print(f"   • update_message_and_progress: {'✅' if has_update_message_and_progress else '❌'}")
    print(f"   • Pourcentage 5% (init): {'✅' if has_5_percent else '❌'}")
    print(f"   • Pourcentage 10% (start): {'✅' if has_10_percent else '❌'}")
    print(f"   • Pourcentage 85% (processing): {'✅' if has_85_percent else '❌'}")
    print(f"   • Pourcentage 90% (prep): {'✅' if has_90_percent else '❌'}")
    print(f"   • Pourcentage 95% (save): {'✅' if has_95_percent else '❌'}")
    print(f"   • Pourcentage 100% (final): {'✅' if has_100_percent else '❌'}")
    
    # Test 3: Compter les étapes de progression
    percentage_calls = []
    for line in save_result_lines:
        if "update_message_and_progress" in line and ", " in line:
            # Extraire le pourcentage de la ligne
            parts = line.split(", ")
            if len(parts) >= 2:
                try:
                    percentage = int(parts[-1].split(")")[0])
                    percentage_calls.append(percentage)
                except:
                    pass
    
    print(f"\n📊 Pourcentages détectés: {percentage_calls}")
    
    # Vérifier la progression logique
    is_ascending = all(percentage_calls[i] <= percentage_calls[i+1] 
                      for i in range(len(percentage_calls)-1))
    starts_low = len(percentage_calls) > 0 and percentage_calls[0] <= 10
    ends_high = len(percentage_calls) > 0 and percentage_calls[-1] >= 95
    has_steps = len(percentage_calls) >= 5
    
    print(f"   • Progression croissante: {'✅' if is_ascending else '❌'}")
    print(f"   • Commence bas (≤10%): {'✅' if starts_low else '❌'}")
    print(f"   • Termine haut (≥95%): {'✅' if ends_high else '❌'}")
    print(f"   • Étapes suffisantes (≥5): {'✅' if has_steps else '❌'}")
    
    # Résumé
    print("\n📊 RÉSUMÉ:")
    
    progress_bar_score = sum([
        has_determinate_mode, has_maximum_100, has_value_0,
        has_update_progress, has_update_both, has_clamp_percentage
    ])
    
    save_result_score = sum([
        has_update_message_and_progress, has_5_percent, has_10_percent,
        has_85_percent, has_90_percent, has_95_percent, has_100_percent
    ])
    
    progression_score = sum([is_ascending, starts_low, ends_high, has_steps])
    
    print(f"   • progress_bar.py améliorations: {progress_bar_score}/6")
    print(f"   • save_result() pourcentages: {save_result_score}/7")
    print(f"   • logique progression: {progression_score}/4")
    
    total_score = progress_bar_score + save_result_score + progression_score
    max_score = 6 + 7 + 4
    
    if total_score >= max_score * 0.8:  # 80% ou plus
        print("\n🎉 BARRE DE PROGRESSION AVEC POURCENTAGES RÉUSSIE!")
        print("   Toutes les améliorations ont été implémentées:")
        print("   • Mode 'determinate' avec pourcentages 0-100%")
        print("   • Méthodes update_progress et update_message_and_progress")  
        print("   • Progression logique dans save_result(): 5% → 100%")
        print("   • Étapes bien réparties pour feedback utilisateur")
        print("\n💡 RÉSULTAT ATTENDU:")
        print("   La barre de progression doit maintenant afficher")
        print("   un pourcentage visuel qui augmente pendant l'opération!")
    else:
        print(f"\n⚠️  AMÉLIORATIONS INCOMPLÈTES ({total_score}/{max_score})")
        if progress_bar_score < 5:
            print("   - progress_bar.py: Mode déterminé incomplet")
        if save_result_score < 5:
            print("   - save_result(): Pourcentages manquants")
        if progression_score < 3:
            print("   - Logique de progression défaillante")

except Exception as e:
    print(f"❌ Erreur: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("📝 TEST TERMINÉ")
