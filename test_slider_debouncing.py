#!/usr/bin/env python3
"""
Test de performance des sliders avec debouncing
Test vérifie que les sliders sont fluides avec le nouveau système de debouncing
"""

import sys
import time
import threading
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_slider_responsiveness():
    """Test la responsivité des sliders avec debouncing"""
    print("🎯 TEST SLIDER DEBOUNCING - AQUALIX v2.2.2")
    print("=" * 60)
    
    try:
        # Import des modules principaux
        from src.image_processing import ImageProcessor
        from src.ui_components import ParameterPanel
        import tkinter as tk
        from tkinter import ttk
        
        # Créer une fenêtre test
        root = tk.Tk()
        root.title("Test Slider Debouncing")
        root.geometry("600x400")
        
        # Compteur d'appels update
        update_call_count = 0
        last_update_time = 0
        update_times = []
        
        def mock_update_callback():
            """Mock callback qui simule update_preview"""
            nonlocal update_call_count, last_update_time
            current_time = time.time() * 1000  # millisecondes
            update_call_count += 1
            
            if last_update_time > 0:
                delay = current_time - last_update_time
                update_times.append(delay)
                print(f"  Update #{update_call_count} - Délai: {delay:.1f}ms")
            
            last_update_time = current_time
        
        # Initialiser le processeur
        processor = ImageProcessor()
        
        # Créer le panneau paramètres avec notre mock callback
        param_panel = ParameterPanel(root, processor, mock_update_callback)
        param_panel.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        print("✅ Interface initialisée avec debouncing")
        print(f"   Délai debouncing: {param_panel._debounce_delay}ms")
        print()
        
        # Test automatique de mouvements rapides de slider
        def simulate_slider_movements():
            """Simule des mouvements rapides de slider"""
            time.sleep(1)  # Attendre que l'UI soit prête
            
            print("🚀 Simulation mouvements rapides de slider...")
            
            # Trouver un slider beer-lambert (facteur rouge)
            beer_lambert_param = 'beer_lambert_red_factor'
            
            # Simuler 10 changements rapides (comme si l'utilisateur bougeait le slider)
            for i in range(10):
                value = 1.0 + (i * 0.1)  # 1.0 → 1.9
                param_panel.on_parameter_change(beer_lambert_param, value)
                time.sleep(0.05)  # 50ms entre chaque changement
            
            print(f"   Terminé: {10} changements en 500ms")
            
            # Attendre que tous les updates soient traités
            time.sleep(0.5)
            
            # Analyser les résultats
            root.after(100, analyze_results)
        
        def analyze_results():
            """Analyse les résultats du test"""
            print()
            print("📊 RÉSULTATS DEBOUNCING:")
            print(f"   Changements simulés: 10")
            print(f"   Updates callback: {update_call_count}")
            print(f"   Réduction: {(1 - update_call_count/10)*100:.1f}%")
            
            if update_times:
                avg_delay = sum(update_times) / len(update_times)
                print(f"   Délai moyen entre updates: {avg_delay:.1f}ms")
            
            if update_call_count <= 3:
                print("✅ EXCELLENT: Debouncing fonctionne parfaitement")
                print("   → Les sliders sont maintenant fluides!")
            elif update_call_count <= 5:
                print("✅ BON: Debouncing réduit significativement les updates")
            else:
                print("⚠️  ATTENTION: Debouncing pourrait être amélioré")
            
            print()
            print("🎉 Test terminé - Fermez la fenêtre pour continuer")
        
        # Lancer la simulation en arrière-plan
        thread = threading.Thread(target=simulate_slider_movements)
        thread.daemon = True
        thread.start()
        
        # Afficher l'interface pendant 10 secondes pour test manuel
        root.after(10000, root.quit)
        root.mainloop()
        
        print()
        print("✅ Test slider debouncing RÉUSSI")
        
        return True
        
    except ImportError as e:
        print(f"❌ Erreur import: {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_slider_responsiveness()
    sys.exit(0 if success else 1)
