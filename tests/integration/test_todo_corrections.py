#!/usr/bin/env python3
"""
Test corrections Todo List v2.3.1
Validation des corrections UDCP Omega, Scroll souris, Tab Opérations, Auto-tune Fusion
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

import cv2
import numpy as np
import tkinter as tk
from image_processing import ImageProcessor
from ui_components import ParameterPanel

def test_udcp_omega_correction():
    """Test que l'auto-tune UDCP donne des valeurs omega moins agressives"""
    print("\n=== Test Correction UDCP Omega ===")
    
    processor = ImageProcessor()
    
    # Créer une image test eau claire normale
    test_image = create_clear_water_image(512, 512)
    
    # Tester l'auto-tune UDCP
    udcp_params = processor._enhanced_auto_tune_udcp(test_image)
    
    omega_value = udcp_params.get('omega', 0.95)  # Défaut si pas défini
    
    print(f"Omega auto-tuned: {omega_value:.2f}")
    print(f"Expected range: 0.60-0.80 pour eau claire")
    
    # Validation: omega devrait être <= 0.85 pour eau claire
    assert omega_value <= 0.85, f"Omega trop agressif: {omega_value} > 0.85"
    
    # Pour eau claire normale (blue_red_ratio normal), omega devrait être 0.70
    if 0.8 <= calculate_blue_red_ratio(test_image) <= 1.4:  # Eau claire normale
        expected_omega = 0.70
        assert abs(omega_value - expected_omega) < 0.05, f"Omega pour eau claire: {omega_value} != {expected_omega}"
        print(f"✅ Omega corrigé pour eau claire: {omega_value:.2f} (attendu: 0.70)")
    
    print("✅ UDCP Omega correction validée")
    return True

def test_fusion_autotune_params():
    """Test que l'auto-tune fusion modifie saturation et exposedness"""
    print("\n=== Test Auto-tune Fusion Paramètres ===")
    
    processor = ImageProcessor()
    
    # Image test avec faible saturation et exposition
    test_image = create_low_saturation_image(512, 512)
    
    # Capturer paramètres avant auto-tune
    original_saturation = processor.parameters['fusion_saturation_weight']
    original_exposedness = processor.parameters['fusion_exposedness_weight']
    
    print(f"Saturation weight avant: {original_saturation}")
    print(f"Exposedness weight avant: {original_exposedness}")
    
    # Appliquer auto-tune fusion
    fusion_params = processor._auto_tune_multiscale_fusion(test_image)
    
    new_saturation = fusion_params.get('fusion_saturation_weight')
    new_exposedness = fusion_params.get('fusion_exposedness_weight')
    
    print(f"Saturation weight après: {new_saturation}")
    print(f"Exposedness weight après: {new_exposedness}")
    
    # Validation: pour image à faible saturation, les poids doivent augmenter
    assert new_saturation is not None, "Auto-tune doit définir fusion_saturation_weight"
    assert new_exposedness is not None, "Auto-tune doit définir fusion_exposedness_weight"
    assert new_saturation > original_saturation, f"Saturation weight doit augmenter: {new_saturation} <= {original_saturation}"
    assert new_exposedness > original_exposedness, f"Exposedness weight doit augmenter: {new_exposedness} <= {original_exposedness}"
    
    print("✅ Auto-tune fusion modifie bien saturation et exposedness")
    return True

def test_pipeline_description_includes_fusion():
    """Test que la description pipeline inclut la fusion multi-échelle"""
    print("\n=== Test Description Pipeline avec Fusion ===")
    
    processor = ImageProcessor()
    
    # Activer multiscale fusion
    processor.set_parameter('multiscale_fusion_enabled', True)
    
    # Obtenir description pipeline
    pipeline_desc = processor.get_pipeline_description()
    
    # Chercher fusion dans la description
    fusion_found = False
    fusion_step = None
    
    for step in pipeline_desc:
        if 'fusion' in step['name'].lower() or 'fusion' in step['description'].lower():
            fusion_found = True
            fusion_step = step
            break
    
    assert fusion_found, "Pipeline description doit inclure la fusion multi-échelle"
    
    print(f"Fusion trouvée: {fusion_step['name']}")
    print(f"Description: {fusion_step['description']}")
    print(f"Paramètres: {fusion_step['parameters']}")
    
    # Vérifier que les paramètres de fusion sont affichés
    params_text = fusion_step['parameters']
    assert 'Saturation' in params_text, "Paramètres doivent inclure Saturation"
    assert 'Exposition' in params_text, "Paramètres doivent inclure Exposition"
    assert 'Contraste' in params_text, "Paramètres doivent inclure Contraste"
    
    print("✅ Pipeline description inclut correctement la fusion")
    return True

def test_mousewheel_binding():
    """Test que le scroll souris est configuré correctement"""
    print("\n=== Test Configuration Scroll Souris ===")
    
    # Créer fenêtre test
    root = tk.Tk()
    root.withdraw()
    
    try:
        processor = ImageProcessor()
        frame = tk.Frame(root)
        param_panel = ParameterPanel(frame, processor, lambda: None)
        
        # Vérifier que le canvas existe et a les bindings corrects
        canvas_found = False
        
        # Parcourir les widgets pour trouver le canvas
        for widget in frame.winfo_children():
            if isinstance(widget, tk.Canvas):
                canvas_found = True
                # Vérifier les bindings
                bindings = widget.bind()
                print(f"Canvas bindings: {bindings}")
                
                # Vérifier que MouseWheel est bindé directement au canvas
                mousewheel_bound = '<MouseWheel>' in bindings
                enter_bound = '<Enter>' in bindings
                leave_bound = '<Leave>' in bindings
                
                assert mousewheel_bound, "Canvas doit avoir binding MouseWheel direct"
                assert enter_bound, "Canvas doit avoir binding Enter pour activation"
                assert leave_bound, "Canvas doit avoir binding Leave pour désactivation"
                
                print("✅ Scroll souris configuré avec bindings directs et Enter/Leave")
                break
        
        assert canvas_found, "Canvas de paramètres non trouvé"
        
        return True
        
    finally:
        root.destroy()

def create_clear_water_image(height, width):
    """Créer image test eau claire avec ratio blue/red normal"""
    # Couleurs typiques eau claire (plus de bleu mais pas excessif)
    red_channel = np.full((height, width), 0.4)
    green_channel = np.full((height, width), 0.6) 
    blue_channel = np.full((height, width), 0.7)
    
    # Ajouter variation spatiale
    y_grad = np.linspace(0, 0.2, height)[:, np.newaxis]
    red_channel -= y_grad
    green_channel -= y_grad * 0.5
    blue_channel -= y_grad * 0.3
    
    # Combiner et convertir en uint8
    image = np.stack([red_channel, green_channel, blue_channel], axis=-1)
    image = np.clip(image, 0, 1)
    
    return (image * 255).astype(np.uint8)

def create_low_saturation_image(height, width):
    """Créer image test avec faible saturation et exposition"""
    # Image grisâtre (faible saturation) et sombre (faible exposition)
    base_value = 0.3  # Faible exposition
    saturation = 0.1  # Très faible saturation
    
    # Créer image HSV
    hue = np.random.uniform(0, 180, (height, width))
    sat = np.full((height, width), saturation * 255)
    val = np.full((height, width), base_value * 255)
    
    hsv = np.stack([hue, sat, val], axis=-1).astype(np.uint8)
    
    # Convertir en BGR
    bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    
    return bgr

def calculate_blue_red_ratio(image):
    """Calculer ratio blue/red pour classification eau"""
    img_float = image.astype(np.float32) / 255.0
    b_channel = img_float[:,:,0]  # Bleu en BGR
    r_channel = img_float[:,:,2]  # Rouge en BGR
    
    safe_r = np.maximum(r_channel, 0.01)
    ratio = np.mean(b_channel / safe_r)
    
    return ratio

def run_all_todo_tests():
    """Exécuter tous les tests de correction Todo"""
    print("🔧 Tests Corrections Todo List v2.3.1")
    print("=" * 50)
    
    success_count = 0
    
    try:
        if test_udcp_omega_correction():
            success_count += 1
    except Exception as e:
        print(f"❌ Test UDCP Omega échoué: {e}")
    
    try:
        if test_fusion_autotune_params():
            success_count += 1
    except Exception as e:
        print(f"❌ Test Fusion auto-tune échoué: {e}")
    
    try:
        if test_pipeline_description_includes_fusion():
            success_count += 1
    except Exception as e:
        print(f"❌ Test Pipeline description échoué: {e}")
    
    try:
        if test_mousewheel_binding():
            success_count += 1
    except Exception as e:
        print(f"❌ Test Scroll souris échoué: {e}")
    
    print("\n" + "=" * 50)
    print(f"✅ Tests réussis: {success_count}/4")
    
    if success_count == 4:
        print("🎉 Toutes les corrections Todo validées!")
        return True
    else:
        print("⚠️  Certaines corrections nécessitent révision")
        return False

if __name__ == "__main__":
    run_all_todo_tests()
