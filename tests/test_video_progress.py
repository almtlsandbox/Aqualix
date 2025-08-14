#!/usr/bin/env python3
"""
Test spécifique pour la progression granulaire des vidéos
Simule le traitement vidéo avec progression par frame et par étape
"""

import sys
sys.path.insert(0, '.')

def test_video_progress_simulation():
    """Simule le traitement vidéo avec progression granulaire"""
    print("🎬 TEST: Progression granulaire pour vidéos")
    print("=" * 60)
    
    try:
        from src.image_processing import ImageProcessor
        import numpy as np
        
        processor = ImageProcessor()
        
        # Simuler des frames de vidéo
        total_frames = 5  # Petit nombre pour test rapide
        print(f"🎥 Simulation traitement vidéo: {total_frames} frames")
        
        all_progress_updates = []
        
        for frame_num in range(total_frames):
            print(f"\n📊 Frame {frame_num + 1}/{total_frames}:")
            
            # Créer une frame test
            test_frame = np.random.randint(50, 200, (50, 50, 3), dtype=np.uint8)
            
            frame_progress_updates = []
            
            def frame_callback(message, percentage):
                # Calculer la progression globale comme dans save_video
                frame_start = 10 + (frame_num * 80 // total_frames)
                frame_end = 10 + ((frame_num + 1) * 80 // total_frames)
                frame_range = frame_end - frame_start
                adjusted_percentage = frame_start + (percentage * frame_range // 100)
                
                global_message = f"Frame {frame_num + 1}/{total_frames}: {message}"
                frame_progress_updates.append((global_message, adjusted_percentage))
                print(f"    📈 {adjusted_percentage:3.0f}% - {global_message}")
            
            # Traiter la frame
            processed_frame = processor.process_image(test_frame, progress_callback=frame_callback)
            
            print(f"    ✅ Frame traitée: {processed_frame is not None}")
            print(f"    📊 Steps pour cette frame: {len(frame_progress_updates)}")
            
            all_progress_updates.extend(frame_progress_updates)
        
        print(f"\n🎯 RÉSUMÉ VIDÉO:")
        print(f"   📊 Total updates reçues: {len(all_progress_updates)}")
        print(f"   🎬 Frames traitées: {total_frames}")
        print(f"   📈 Updates par frame (moyenne): {len(all_progress_updates) / total_frames:.1f}")
        
        # Vérifier progression globale
        coverage_ok = False
        if all_progress_updates:
            percentages = [update[1] for update in all_progress_updates]
            min_progress = min(percentages)
            max_progress = max(percentages)
            
            print(f"   📊 Progression globale: {min_progress:.0f}% → {max_progress:.0f}%")
            
            # Vérifier que la progression couvre bien la plage 10-90%
            expected_min = 10
            expected_max = 85  # Environ 90% moins les dernières étapes
            
            coverage_ok = min_progress <= expected_min + 5 and max_progress >= expected_max - 5
            print(f"   ✅ Couverture attendue (10-85%): {'✅' if coverage_ok else '❌'}")
        
        # Test progression frame par frame
        frame_ranges = {}
        for update in all_progress_updates:
            message = update[0]
            percentage = update[1]
            
            # Extraire le numéro de frame du message
            if "Frame " in message:
                try:
                    frame_part = message.split("Frame ")[1].split("/")[0]
                    frame_num = int(frame_part)
                    
                    if frame_num not in frame_ranges:
                        frame_ranges[frame_num] = []
                    frame_ranges[frame_num].append(percentage)
                except:
                    pass
        
        print(f"\n📈 PROGRESSION PAR FRAME:")
        for frame_num in sorted(frame_ranges.keys()):
            percentages = frame_ranges[frame_num]
            frame_min = min(percentages)
            frame_max = max(percentages)
            print(f"   Frame {frame_num}: {frame_min:.0f}% → {frame_max:.0f}% ({len(percentages)} étapes)")
        
        # Validation finale
        tests_passed = (
            len(all_progress_updates) > 0 and
            len(frame_ranges) == total_frames and
            coverage_ok
        )
        
        if tests_passed:
            print("\n🎉 TEST VIDÉO RÉUSSI - Progression granulaire par frame fonctionnelle!")
            return True
        else:
            print("\n⚠️  Test vidéo partiellement échoué")
            return False
            
    except Exception as e:
        print(f"❌ Erreur pendant test vidéo: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_video_progress_simulation()
    sys.exit(0 if success else 1)
