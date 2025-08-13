#!/usr/bin/env python3
"""
Test de performance du calcul MD5 en threading
"""
import time
import sys
import os
import threading
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))

import numpy as np
import tkinter as tk
from tkinter import ttk
from src.image_info import ImageInfoExtractor

def create_large_test_file(filepath, size_mb=10):
    """Crée un gros fichier de test pour simuler une grosse image"""
    print(f"Création d'un fichier de test de {size_mb}MB...")
    with open(filepath, 'wb') as f:
        # Écrire des données aléatoirement pour simuler une grosse image
        chunk_size = 1024 * 1024  # 1MB chunks
        for i in range(size_mb):
            data = np.random.randint(0, 256, chunk_size, dtype=np.uint8).tobytes()
            f.write(data)
    print(f"Fichier créé: {filepath}")

def test_md5_threading():
    """Test du calcul MD5 avec et sans threading"""
    
    test_file = "test_large_image.bin"
    
    try:
        # Créer un gros fichier de test
        create_large_test_file(test_file, size_mb=50)  # 50MB pour un test significatif
        
        extractor = ImageInfoExtractor()
        
        print("\n=== TEST CALCUL MD5 ===")
        
        # Test 1: Calcul synchrone (bloquant)
        print("\n1. Test SYNCHRONE (bloquant):")
        start_time = time.time()
        hash_sync = extractor._get_file_hash(test_file)
        sync_duration = time.time() - start_time
        print(f"   Hash: {hash_sync}")
        print(f"   Durée: {sync_duration:.2f}s")
        
        # Test 2: Calcul asynchrone (non-bloquant)
        print("\n2. Test ASYNCHRONE (non-bloquant):")
        
        hash_result = {"value": None, "completed": False}
        
        def hash_callback(result):
            hash_result["value"] = result
            hash_result["completed"] = True
            print(f"   🎯 Hash calculé en arrière-plan: {result}")
        
        start_time = time.time()
        placeholder = extractor._get_file_hash_async(test_file, hash_callback)
        async_immediate = time.time() - start_time
        
        print(f"   Retour immédiat: '{placeholder}'")
        print(f"   Temps de retour: {async_immediate * 1000:.1f}ms (quasi-instantané)")
        
        # Attendre que le calcul se termine
        print("   Attente du calcul en arrière-plan...")
        wait_start = time.time()
        while not hash_result["completed"] and (time.time() - wait_start) < 30:
            time.sleep(0.1)
        
        total_async_time = time.time() - start_time
        
        if hash_result["completed"]:
            print(f"   Durée totale calcul: {total_async_time:.2f}s")
            print(f"   ✅ Hash identique: {hash_sync == hash_result['value']}")
        else:
            print("   ❌ Timeout - calcul trop long")
        
        print(f"\n📊 RÉSULTAT:")
        print(f"   • Synchrone:  {sync_duration:.2f}s (BLOQUE l'interface)")
        print(f"   • Asynchrone: {async_immediate * 1000:.1f}ms retour (N'BLOQUE PAS)")
        print(f"   • Gain UX: {((sync_duration - async_immediate) / sync_duration * 100):.1f}% plus réactif")
        
    finally:
        # Nettoyer le fichier de test
        if os.path.exists(test_file):
            os.remove(test_file)
            print(f"\nFichier de test supprimé: {test_file}")

def test_ui_responsiveness():
    """Test de réactivité de l'interface avec calcul MD5"""
    
    root = tk.Tk()
    root.title("Test Réactivité UI - Calcul MD5")
    root.geometry("400x300")
    
    # État du test
    test_state = {
        "start_time": None,
        "clicks": 0,
        "ui_blocked": False
    }
    
    # Interface de test
    title = ttk.Label(root, text="Test de Réactivité Interface", font=('Arial', 14, 'bold'))
    title.pack(pady=10)
    
    instructions = ttk.Label(root, text="Cliquez rapidement sur le bouton pendant le calcul MD5")
    instructions.pack(pady=5)
    
    click_counter = ttk.Label(root, text="Clics: 0", font=('Arial', 12))
    click_counter.pack(pady=5)
    
    status_label = ttk.Label(root, text="Prêt", font=('Arial', 10))
    status_label.pack(pady=5)
    
    def increment_click():
        test_state["clicks"] += 1
        click_counter.config(text=f"Clics: {test_state['clicks']}")
        
        if test_state["start_time"]:
            elapsed = time.time() - test_state["start_time"]
            if elapsed < 3.0:  # Dans les 3 premières secondes
                if not test_state["ui_blocked"]:
                    status_label.config(text="✅ Interface RÉACTIVE!", foreground="green")
            
    def start_md5_test():
        # Créer un gros fichier temporaire
        test_file = "ui_test_file.bin"
        create_large_test_file(test_file, size_mb=20)
        
        test_state["start_time"] = time.time()
        test_state["clicks"] = 0
        test_state["ui_blocked"] = True
        
        status_label.config(text="🔄 Calcul MD5 en cours... Testez les clics!", foreground="blue")
        
        extractor = ImageInfoExtractor()
        
        def hash_done(result):
            elapsed = time.time() - test_state["start_time"]
            status_label.config(
                text=f"✅ MD5 terminé! ({elapsed:.1f}s) Clics pendant calcul: {test_state['clicks']}", 
                foreground="green"
            )
            # Nettoyer
            if os.path.exists(test_file):
                os.remove(test_file)
        
        # Calcul asynchrone
        extractor._get_file_hash_async(test_file, hash_done)
        
        # Timer pour détecter si l'UI se bloque
        def check_responsiveness():
            if test_state["start_time"]:
                elapsed = time.time() - test_state["start_time"] 
                if elapsed > 1.0 and test_state["clicks"] == 0:
                    status_label.config(text="❌ Interface semble bloquée", foreground="red")
                    
        root.after(2000, check_responsiveness)
    
    test_button = ttk.Button(root, text="🧪 Commencer Test MD5", command=start_md5_test)
    test_button.pack(pady=10)
    
    click_button = ttk.Button(root, text="👆 Cliquez ici rapidement!", command=increment_click)
    click_button.pack(pady=10)
    
    close_button = ttk.Button(root, text="Fermer", command=root.destroy)
    close_button.pack(pady=10)
    
    print("\n🖼️ Fenêtre de test UI ouverte")
    print("Instructions:")
    print("1. Cliquez sur 'Commencer Test MD5'")
    print("2. Cliquez rapidement sur le bouton de test")
    print("3. Si l'interface reste réactive, le threading fonctionne!")
    
    root.mainloop()

if __name__ == "__main__":
    print("🧪 TEST DE PERFORMANCE MD5 AVEC THREADING")
    print("=" * 50)
    
    print("\n1. Test de performance comparative...")
    test_md5_threading()
    
    print(f"\n2. Test d'interface utilisateur...")
    test_ui_responsiveness()
