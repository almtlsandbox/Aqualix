"""Test simple de la détection de type d'eau - exécuter avec main.py"""

import numpy as np
import cv2

def test_water_detection_logic():
    """Test direct de la logique de détection"""
    
    def detect_water_type(img):
        """Version simplifiée de la logique de détection"""
        if img is None or img.size == 0:
            return ("unknown", "Type inconnu", "Unknown type", "gray_world")
            
        try:
            # Conversion en float et normalisation 
            img_float = img.astype(np.float32) / 255.0
            
            # Calcul des ratios RGB moyens
            mean_bgr = np.mean(img_float, axis=(0, 1))
            total_intensity = np.sum(mean_bgr)
            
            if total_intensity > 0:
                B_ratio = mean_bgr[0] / total_intensity  # Bleu
                G_ratio = mean_bgr[1] / total_intensity  # Vert  
                R_ratio = mean_bgr[2] / total_intensity  # Rouge
            else:
                B_ratio = G_ratio = R_ratio = 1/3
            
            # Calcul de l'intensité des contours
            gray = cv2.cvtColor((img_float * 255).astype(np.uint8), cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 50, 150)
            edge_strength = np.mean(edges) / 255.0
            
            print(f"Ratios - B: {B_ratio:.3f}, G: {G_ratio:.3f}, R: {R_ratio:.3f}, Contours: {edge_strength:.3f}")
            
            # Classification selon la logique d'auto-tune
            if G_ratio > 0.4:
                return ("lake", "Lac / Eau douce", "Lake / Freshwater", "lake_green_water")
            elif B_ratio < 0.25:
                return ("ocean", "Océan / Eau profonde", "Ocean / Deep water", "gray_world")
            elif R_ratio < 0.2:
                return ("tropical", "Eaux tropicales", "Tropical waters", "shades_of_gray")
            elif edge_strength > 0.1:
                return ("clear", "Eau claire / Contraste élevé", "Clear water / High contrast", "grey_edge")
            else:
                return ("standard", "Environnement standard", "Standard environment", "white_patch")
                
        except Exception as e:
            print(f"⚠️ Erreur détection type d'eau: {e}")
            return ("error", "Erreur de détection", "Detection error", "gray_world")
    
    def create_test_image(dominant_color):
        """Crée une image de test avec une couleur dominante"""
        img = np.zeros((100, 100, 3), dtype=np.uint8)
        img[:] = dominant_color
        
        # Ajouter un peu de texture pour les contours
        for i in range(10, 90, 20):
            cv2.rectangle(img, (i, i), (i+10, i+10), (255, 255, 255), 2)
        
        return img

    test_cases = [
        ("Dominance verte (lac)", (20, 150, 50)),    # BGR : forte composante verte
        ("Dominance bleue (océan)", (150, 50, 20)),  # BGR : forte composante bleue  
        ("Faible rouge (tropical)", (100, 100, 20)), # BGR : faible composante rouge
        ("Image équilibrée (standard)", (80, 80, 80)), # BGR : équilibré
        ("Image claire avec contours", (200, 200, 200)), # BGR : clair
    ]
    
    print("🧪 Test de détection du type d'eau")
    print("=" * 50)
    
    for desc, color in test_cases:
        print(f"\n📊 {desc} (BGR: {color})")
        img = create_test_image(color)
        water_type_info = detect_water_type(img)
        
        type_tech, desc_fr, desc_en, method = water_type_info
        
        print(f"   ✅ Type détecté: {type_tech}")
        print(f"   📝 Description: {desc_fr}")
        print(f"   🔧 Méthode recommandée: {method}")

if __name__ == "__main__":
    test_water_detection_logic()
