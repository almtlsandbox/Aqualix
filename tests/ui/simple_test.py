#!/usr/bin/env python3
"""Test simple pour barres de progression"""

import tkinter as tk
import sys
import os
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))

# Assurer le chemin vers src
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

def test_simple():
    """Test simple des barres de progression"""
    print("🔍 Test simple des barres de progression...")
    
    try:
        # Test import
        from progress_bar import show_progress
        print("✅ Import réussi")
        
        # Test création
        root = tk.Tk()
        root.withdraw()
        
        # Test context manager
        print("📊 Test context manager...")
        with show_progress(root, "Test", "Initialisation...") as progress:
            import time
            progress.update_message("Étape 1...")
            time.sleep(0.5)
            progress.update_message("Étape 2...")
            time.sleep(0.5)
            progress.update_message("Finalisation...")
            time.sleep(0.2)
        
        print("✅ Test réussi!")
        root.destroy()
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_simple()
