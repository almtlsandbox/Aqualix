"""
Image Information Module for Aqualix
Extracts and displays detailed information about images and videos.
"""

import cv2
import numpy as np
from PIL import Image
from PIL.ExifTags import TAGS
import os
from pathlib import Path
from datetime import datetime
import hashlib

class ImageInfoExtractor:
    def __init__(self):
        pass
        
    def get_image_info(self, image_path, image_array=None, include_hash=True):
        """Extract comprehensive information from an image"""
        info = {}
        
        try:
            image_path = Path(image_path)
            
            # File information (with optional hash for speed)
            info['file'] = self._get_file_info(image_path, include_hash=include_hash)
            
            # Image properties
            if image_array is not None:
                info['properties'] = self._get_array_properties(image_array)
            else:
                info['properties'] = self._get_image_properties(image_path)
                
            # EXIF data
            info['exif'] = self._get_exif_data(image_path)
            
            # Color analysis
            if image_array is not None:
                info['color_analysis'] = self._analyze_colors(image_array)
            else:
                # Load image for color analysis
                img = cv2.imread(str(image_path))
                if img is not None:
                    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    info['color_analysis'] = self._analyze_colors(img_rgb)
                    
        except Exception as e:
            info['error'] = str(e)
            
        return info
        
    def get_video_info(self, video_path, include_hash=True):
        """Extract comprehensive information from a video"""
        info = {}
        
        try:
            video_path = Path(video_path)
            
            # File information (with optional hash for speed)
            info['file'] = self._get_file_info(video_path, include_hash=include_hash)
            
            # Video properties
            info['properties'] = self._get_video_properties(video_path)
            
        except Exception as e:
            info['error'] = str(e)
            
        return info
        
    def _get_file_info(self, file_path, include_hash=True):
        """Get basic file information"""
        try:
            stat = file_path.stat()
            
            # Calculate hash only if requested (for performance)
            hash_value = self._get_file_hash(file_path) if include_hash else "Calculé en arrière-plan..."
            
            return {
                'name': file_path.name,
                'path': str(file_path.absolute()),
                'size': self._format_size(stat.st_size),
                'size_bytes': stat.st_size,
                'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
                'created': datetime.fromtimestamp(stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S'),
                'extension': file_path.suffix.lower(),
                'hash_md5': hash_value
            }
        except Exception as e:
            # Return basic info even if stat fails
            return {
                'name': file_path.name if hasattr(file_path, 'name') else 'N/A',
                'path': str(file_path) if file_path else 'N/A',
                'size': 'N/A',
                'size_bytes': 0,
                'modified': 'N/A',
                'created': 'N/A',
                'extension': file_path.suffix.lower() if hasattr(file_path, 'suffix') else 'N/A',
                'hash_md5': 'N/A'
            }
        
    def _get_image_properties(self, image_path):
        """Get image properties using OpenCV and PIL"""
        properties = {}
        
        # OpenCV properties
        img = cv2.imread(str(image_path))
        if img is not None:
            height, width, channels = img.shape
            properties.update({
                'width': width,
                'height': height,
                'channels': channels,
                'total_pixels': width * height,
                'aspect_ratio': round(width / height, 3),
                'color_space': 'BGR' if channels == 3 else 'Grayscale'
            })
            
        # PIL properties
        try:
            with Image.open(image_path) as pil_img:
                properties.update({
                    'format': pil_img.format,
                    'mode': pil_img.mode,
                    'has_transparency': pil_img.mode in ['RGBA', 'LA'] or 'transparency' in pil_img.info
                })
        except Exception:
            pass
            
        return properties
        
    def _get_array_properties(self, image_array):
        """Get properties from numpy array"""
        if len(image_array.shape) == 3:
            height, width, channels = image_array.shape
        else:
            height, width = image_array.shape
            channels = 1
            
        return {
            'width': width,
            'height': height,
            'channels': channels,
            'total_pixels': width * height,
            'aspect_ratio': round(width / height, 3),
            'dtype': str(image_array.dtype),
            'min_value': int(np.min(image_array)),
            'max_value': int(np.max(image_array)),
            'mean_value': round(float(np.mean(image_array)), 2)
        }
        
    def _get_video_properties(self, video_path):
        """Get video properties using OpenCV"""
        properties = {}
        
        cap = cv2.VideoCapture(str(video_path))
        if cap.isOpened():
            properties.update({
                'width': int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                'height': int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
                'fps': round(cap.get(cv2.CAP_PROP_FPS), 2),
                'total_frames': int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
                'duration': self._format_duration(cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS)),
                'fourcc': self._decode_fourcc(cap.get(cv2.CAP_PROP_FOURCC))
            })
            
            # Calculate additional properties
            if properties['total_frames'] > 0 and properties['fps'] > 0:
                properties['aspect_ratio'] = round(properties['width'] / properties['height'], 3)
                
            cap.release()
            
        return properties
        
    def _get_exif_data(self, image_path):
        """Extract EXIF data from image"""
        exif_data = {}
        
        try:
            with Image.open(image_path) as img:
                # Use getexif() method (modern approach)
                if hasattr(img, 'getexif'):
                    exif = img.getexif()
                    if exif is not None:
                        for tag_id, value in exif.items():
                            tag = TAGS.get(tag_id, tag_id)
                            exif_data[tag] = str(value)
                # Modern getexif is sufficient, no fallback needed
        except Exception:
            pass
            
        return exif_data
        
    def _analyze_colors(self, image_array):
        """Analyze color properties of image"""
        analysis = {}
        
        if len(image_array.shape) == 3:
            # RGB image
            r_channel = image_array[:, :, 0]
            g_channel = image_array[:, :, 1]
            b_channel = image_array[:, :, 2]
            
            analysis.update({
                'red_mean': round(float(np.mean(r_channel)), 2),
                'green_mean': round(float(np.mean(g_channel)), 2),
                'blue_mean': round(float(np.mean(b_channel)), 2),
                'red_std': round(float(np.std(r_channel)), 2),
                'green_std': round(float(np.std(g_channel)), 2),
                'blue_std': round(float(np.std(b_channel)), 2),
                'brightness': round(float(np.mean(image_array)), 2),
                'contrast': round(float(np.std(image_array)), 2)
            })
            
            # Color temperature estimation (simplified)
            r_mean, g_mean, b_mean = analysis['red_mean'], analysis['green_mean'], analysis['blue_mean']
            if b_mean > 0:
                color_temp_ratio = r_mean / b_mean
                # Rough estimation (not scientifically accurate)
                estimated_temp = 6500 - (color_temp_ratio - 1) * 1000
                analysis['estimated_color_temp'] = max(2000, min(10000, int(estimated_temp)))
                
            # Dominant colors (simplified)
            unique_colors = len(np.unique(image_array.reshape(-1, image_array.shape[-1]), axis=0))
            analysis['unique_colors'] = min(unique_colors, 1000000)  # Cap at 1M for display
            
        else:
            # Grayscale
            analysis.update({
                'brightness': round(float(np.mean(image_array)), 2),
                'contrast': round(float(np.std(image_array)), 2),
                'min_intensity': int(np.min(image_array)),
                'max_intensity': int(np.max(image_array))
            })
            
        return analysis
        
    def _format_size(self, size_bytes):
        """Format file size in human readable format"""
        try:
            # Ensure size_bytes is a number
            if not isinstance(size_bytes, (int, float)) or size_bytes < 0:
                return "N/A"
                
            size_bytes = int(size_bytes)
            
            if size_bytes < 1024:
                return f"{size_bytes} B"
            elif size_bytes < 1024 * 1024:
                return f"{size_bytes / 1024:.1f} KB"
            elif size_bytes < 1024 * 1024 * 1024:
                return f"{size_bytes / (1024 * 1024):.1f} MB"
            else:
                return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"
        except (TypeError, ValueError):
            return "N/A"
            
    def _format_duration(self, seconds):
        """Format duration in human readable format"""
        try:
            # Ensure seconds is a number
            if not isinstance(seconds, (int, float)) or seconds < 0:
                return "N/A"
                
            seconds = float(seconds)
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            secs = int(seconds % 60)
            
            if hours > 0:
                return f"{hours:02d}:{minutes:02d}:{secs:02d}"
            else:
                return f"{minutes:02d}:{secs:02d}"
        except (TypeError, ValueError):
            return "N/A"
            
    def _decode_fourcc(self, fourcc_int):
        """Decode FOURCC code to string"""
        try:
            fourcc_bytes = int(fourcc_int).to_bytes(4, byteorder='little')
            return fourcc_bytes.decode('ascii').rstrip('\x00')
        except:
            return "Unknown"
            
    def _get_file_hash(self, file_path):
        """Calculate MD5 hash of file"""
        try:
            hash_md5 = hashlib.md5()
            with open(file_path, "rb") as f:
                # Read in chunks to handle large files
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()[:8]  # First 8 characters
        except:
            return "N/A"
