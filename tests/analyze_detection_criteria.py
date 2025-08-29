"""
Analyse détaillée des critères de détection
"""

import sys
sys.path.insert(0, '.')

import numpy as np

def analyze_detection_criteria():
    """Analyse précise des critères de détection"""
    print("🔬 ANALYSE DÉTAILLÉE DES CRITÈRES DE DÉTECTION")
    print("=" * 60)
    
    # Cas test: Rouge intense [200, 40, 50] sur fond [60, 35, 45]
    print("\n📊 CAS TEST: Rouge intense sur fond avec dominante rouge")
    
    # Convertir en float normalisé
    rouge_test = np.array([200, 40, 50], dtype=np.float32) / 255.0
    fond_test = np.array([60, 35, 45], dtype=np.float32) / 255.0
    
    print(f"   Rouge test normalisé: [{rouge_test[0]:.2f}, {rouge_test[1]:.2f}, {rouge_test[2]:.2f}]")
    print(f"   Fond test normalisé:  [{fond_test[0]:.2f}, {fond_test[1]:.2f}, {fond_test[2]:.2f}]")
    
    # Critères actuels: (red > 0.5) & (red > green + 0.1) & (red > blue + 0.1)
    print(f"\n🔍 VÉRIFICATION CRITÈRES ACTUELS:")
    
    # Pour rouge test
    crit1_rouge = rouge_test[0] > 0.5
    crit2_rouge = rouge_test[0] > rouge_test[1] + 0.1
    crit3_rouge = rouge_test[0] > rouge_test[2] + 0.1
    
    print(f"   Rouge test:")
    print(f"      red > 0.5? {rouge_test[0]:.2f} > 0.5 = {crit1_rouge}")
    print(f"      red > green + 0.1? {rouge_test[0]:.2f} > {rouge_test[1]:.2f} + 0.1 = {rouge_test[0]:.2f} > {rouge_test[1] + 0.1:.2f} = {crit2_rouge}")
    print(f"      red > blue + 0.1? {rouge_test[0]:.2f} > {rouge_test[2]:.2f} + 0.1 = {rouge_test[0]:.2f} > {rouge_test[2] + 0.1:.2f} = {crit3_rouge}")
    print(f"      DÉTECTÉ? {crit1_rouge and crit2_rouge and crit3_rouge}")
    
    # Pour fond test  
    crit1_fond = fond_test[0] > 0.5
    crit2_fond = fond_test[0] > fond_test[1] + 0.1
    crit3_fond = fond_test[0] > fond_test[2] + 0.1
    
    print(f"\n   Fond test:")
    print(f"      red > 0.5? {fond_test[0]:.2f} > 0.5 = {crit1_fond}")
    print(f"      red > green + 0.1? {fond_test[0]:.2f} > {fond_test[1]:.2f} + 0.1 = {fond_test[0]:.2f} > {fond_test[1] + 0.1:.2f} = {crit2_fond}")
    print(f"      red > blue + 0.1? {fond_test[0]:.2f} > {fond_test[2]:.2f} + 0.1 = {fond_test[0]:.2f} > {fond_test[2] + 0.1:.2f} = {crit3_fond}")
    print(f"      DÉTECTÉ? {crit1_fond and crit2_fond and crit3_fond}")
    
    # Test avec critères plus sensibles
    print(f"\n🎯 TEST CRITÈRES PLUS SENSIBLES:")
    print(f"   Proposition: (red > 0.4) & (red > green + 0.05) & (red > blue + 0.05)")
    
    # Rouge test avec critères sensibles
    sens1_rouge = rouge_test[0] > 0.4
    sens2_rouge = rouge_test[0] > rouge_test[1] + 0.05
    sens3_rouge = rouge_test[0] > rouge_test[2] + 0.05
    
    print(f"   Rouge test (critères sensibles):")
    print(f"      red > 0.4? {rouge_test[0]:.2f} > 0.4 = {sens1_rouge}")
    print(f"      red > green + 0.05? {rouge_test[0]:.2f} > {rouge_test[1] + 0.05:.2f} = {sens2_rouge}")
    print(f"      red > blue + 0.05? {rouge_test[0]:.2f} > {rouge_test[2] + 0.05:.2f} = {sens3_rouge}")
    print(f"      DÉTECTÉ? {sens1_rouge and sens2_rouge and sens3_rouge}")
    
    # Fond test avec critères sensibles
    sens1_fond = fond_test[0] > 0.4
    sens2_fond = fond_test[0] > fond_test[1] + 0.05
    sens3_fond = fond_test[0] > fond_test[2] + 0.05
    
    print(f"\n   Fond test (critères sensibles):")
    print(f"      red > 0.4? {fond_test[0]:.2f} > 0.4 = {sens1_fond}")
    print(f"      red > green + 0.05? {fond_test[0]:.2f} > {fond_test[1] + 0.05:.2f} = {sens2_fond}")
    print(f"      red > blue + 0.05? {fond_test[0]:.2f} > {fond_test[2] + 0.05:.2f} = {sens3_fond}")
    print(f"      DÉTECTÉ? {sens1_fond and sens2_fond and sens3_fond}")
    
    # Recommandation
    rouge_detecte = sens1_rouge and sens2_rouge and sens3_rouge
    fond_detecte = sens1_fond and sens2_fond and sens3_fond
    
    print(f"\n💡 RECOMMANDATION:")
    if rouge_detecte and not fond_detecte:
        print(f"   ✅ Critères sensibles fonctionnent bien!")
        print(f"   ✅ Détectent le rouge problématique mais pas le fond")
        return True
    elif rouge_detecte and fond_detecte:
        print(f"   ⚠️ Critères sensibles détectent aussi le fond (faux positifs)")
        print(f"   ⚠️ Besoin de critères intermédiaires")
        return False
    else:
        print(f"   ❌ Critères sensibles ne détectent pas le rouge problématique")
        print(f"   ❌ Critères encore trop restrictifs")
        return False

if __name__ == "__main__":
    analyze_detection_criteria()
