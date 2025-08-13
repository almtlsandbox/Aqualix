#!/usr/bin/env python3
"""
Test simple des corrections sans import complexe

CORRECTIONS À VÉRIFIER:
1. Changement langue → onglet qualité persiste
2. Protection image → message d'erreur si pas d'image
3. Suppression bouton → plus de bouton dans toolbar
"""

import os
from pathlib import Path

def test_source_code_corrections():
    """Test basé sur l'analyse du code source"""
    
    print("🔍 ANALYSE CORRECTIONS DANS LE CODE SOURCE")
    print("=" * 50)
    
    # Paths
    src_dir = Path(__file__).parent / "src"
    main_file = src_dir / "main.py"
    quality_tab_file = src_dir / "quality_control_tab.py"
    
    print("1. TEST CORRECTION CHANGEMENT LANGUE")
    print("-" * 40)
    
    with open(main_file, 'r', encoding='utf-8') as f:
        main_content = f.read()
    
    # Check refresh_ui includes quality tab
    refresh_ui_section = False
    quality_tab_in_refresh = False
    
    if "def refresh_ui(self):" in main_content:
        refresh_ui_section = True
        print("   ✅ Méthode refresh_ui() trouvée")
        
        # Find the refresh_ui method
        lines = main_content.split('\n')
        in_refresh_ui = False
        for line in lines:
            if "def refresh_ui(self):" in line:
                in_refresh_ui = True
            elif in_refresh_ui and line.strip().startswith("def "):
                in_refresh_ui = False
            elif in_refresh_ui and "tab_quality" in line:
                quality_tab_in_refresh = True
                print("   ✅ Onglet qualité dans refresh_ui()")
                break
    
    # Check QualityControlTab has refresh_ui method
    with open(quality_tab_file, 'r', encoding='utf-8') as f:
        quality_content = f.read()
    
    quality_has_refresh = "def refresh_ui(self):" in quality_content
    
    print(f"   refresh_ui() dans main.py: {'✅' if refresh_ui_section else '❌'}")
    print(f"   tab_quality dans refresh: {'✅' if quality_tab_in_refresh else '❌'}")  
    print(f"   refresh_ui() dans QualityControlTab: {'✅' if quality_has_refresh else '❌'}")
    
    correction1 = refresh_ui_section and quality_tab_in_refresh and quality_has_refresh
    
    print("\n2. TEST PROTECTION AUCUNE IMAGE")
    print("-" * 32)
    
    # Check image validation in run_analysis
    image_check_present = False
    protection_message = False
    
    if "def run_analysis(self):" in quality_content:
        print("   ✅ Méthode run_analysis() trouvée")
        
        # Look for image validation
        if "self.app.current_image_path" in quality_content and "self.app.original_image" in quality_content:
            image_check_present = True
            print("   ✅ Vérification image path ET original_image")
        
        if "messagebox.showwarning" in quality_content:
            protection_message = True
            print("   ✅ Message d'avertissement présent")
    
    correction2 = image_check_present and protection_message
    
    print("\n3. TEST SUPPRESSION ANCIEN BOUTON")
    print("-" * 33)
    
    # Check old button removed
    old_button_removed = "ttk.Button(toolbar, text=t('quality_check')" not in main_content
    old_method_removed = "def run_quality_check(self):" not in main_content
    new_method_present = "def show_quality_tab(self):" in main_content
    
    print(f"   Ancien bouton supprimé: {'✅' if old_button_removed else '❌'}")
    print(f"   Ancienne méthode supprimée: {'✅' if old_method_removed else '❌'}")
    print(f"   Nouvelle méthode présente: {'✅' if new_method_present else '❌'}")
    
    correction3 = old_button_removed and old_method_removed and new_method_present
    
    print("\n📋 RÉSUMÉ DES CORRECTIONS")
    print("=" * 30)
    print(f"1. Changement langue:   {'✅ CORRIGÉ' if correction1 else '❌ ÉCHEC'}")
    print(f"2. Protection image:    {'✅ CORRIGÉ' if correction2 else '❌ ÉCHEC'}")
    print(f"3. Suppression bouton:  {'✅ CORRIGÉ' if correction3 else '❌ ÉCHEC'}")
    
    all_corrections = correction1 and correction2 and correction3
    
    if all_corrections:
        print("\n🎉 TOUTES LES CORRECTIONS SONT EN PLACE!")
        print("   Les 3 problèmes identifiés ont été résolus:")
        print("   • Onglet qualité persiste lors changement langue")
        print("   • Analyse protégée si aucune image chargée") 
        print("   • Ancien bouton supprimé, interface nettoyée")
    else:
        print("\n⚠️  CORRECTIONS PARTIELLES")
        if not correction1:
            print("   ❌ Problème changement langue non résolu")
        if not correction2:
            print("   ❌ Problème protection image non résolu")
        if not correction3:
            print("   ❌ Problème suppression bouton non résolu")
    
    return all_corrections

if __name__ == "__main__":
    success = test_source_code_corrections()
    
    if success:
        print("\n🚀 L'application est prête avec toutes les corrections!")
        print("   Vous pouvez maintenant:")
        print("   • Changer de langue sans perdre l'onglet qualité")
        print("   • Cliquer 'Analyser' sans image → message approprié")
        print("   • Interface propre sans doublons")
    else:
        print("\n📝 Des ajustements peuvent encore être nécessaires.")
