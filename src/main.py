"""
Image and Video Processing Application
A Tkinter-based GUI application for processing images and videos with various filters and corrections.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import cv2
import numpy as np
import os
import time
from PIL import Image, ImageTk
import threading
from pathlib import Path

from .image_processing import ImageProcessor
from .ui_components import ParameterPanel, PipelinePanel, InteractivePreviewPanel, ImageInfoPanel, AboutPanel
from .logger import AqualixLogger
from .localization import get_localization_manager, t

class ImageVideoProcessorApp:
    def __init__(self, root):
        self.root = root
        self.localization_manager = get_localization_manager()
        self.root.title(t('app_title'))
        self.root.geometry("1200x800")
        
        # Initialize variables
        self.current_file = None
        self.files_list = []
        self.current_index = 0
        self.original_image = None
        self.processed_image = None
        self.video_capture = None
        self.current_frame = 0
        self.total_frames = 0
        
        # Preview variables for performance optimization
        self.preview_scale_factor = 1.0
        self.original_preview = None
        self.processed_preview = None
        
        # Flag to indicate if we're loading a new image (vs parameter change)
        self.loading_new_image = False
        
        # Initialize image processor and logger
        self.processor = ImageProcessor()
        self.logger = AqualixLogger()
        
        # Log application startup
        self.logger.info("=== Aqualix Application Started ===")
        self.logger.info(f"Log file: {self.logger.get_log_file_path()}")
        
        # Setup UI
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the main UI components"""
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Top toolbar with language selector
        self.create_toolbar(main_frame)
        
        # Main content area
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        
        # Left panel - Parameters and Pipeline in tabs
        left_panel = ttk.Frame(content_frame)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5))
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(left_panel)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Parameters tab
        params_frame = ttk.Frame(self.notebook)
        self.notebook.add(params_frame, text=t('tab_parameters'))
        
        # Parameter panel
        self.param_panel = ParameterPanel(params_frame, self.processor, self.update_preview, lambda: self.original_image)
        self.param_panel.pack(fill=tk.BOTH, expand=True)
        
        # Setup auto-tune callback
        self.processor.set_auto_tune_callback(self.param_panel.is_auto_tune_enabled)
        
        # Pipeline tab
        pipeline_frame = ttk.Frame(self.notebook)
        self.notebook.add(pipeline_frame, text=t('tab_operations'))
        
        # Pipeline panel
        self.pipeline_panel = PipelinePanel(pipeline_frame)
        self.pipeline_panel.pack(fill=tk.BOTH, expand=True)
        
        # Image info tab
        info_frame = ttk.Frame(self.notebook)
        self.notebook.add(info_frame, text=t('tab_info'))
        
        # Image info panel
        self.info_panel = ImageInfoPanel(info_frame)
        self.info_panel.pack(fill=tk.BOTH, expand=True)
        
        # About tab
        about_frame = ttk.Frame(self.notebook)
        self.notebook.add(about_frame, text=t('tab_about'))
        
        # About panel
        self.about_panel = AboutPanel(about_frame)
        self.about_panel.pack(fill=tk.BOTH, expand=True)
        
        # Right panel - Preview
        right_panel = ttk.Frame(content_frame)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Preview panel
        self.preview_panel = InteractivePreviewPanel(right_panel)
        self.preview_panel.pack(fill=tk.BOTH, expand=True)
        
        # Video controls
        self.create_video_controls(right_panel)
        
    def create_toolbar(self, parent):
        """Create the top toolbar with file operations and navigation"""
        toolbar = ttk.Frame(parent)
        toolbar.pack(fill=tk.X, pady=(0, 5))
        
        # File operations
        ttk.Button(toolbar, text=t('select_file'), command=self.select_file).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(toolbar, text=t('select_folder'), command=self.select_folder).pack(side=tk.LEFT, padx=(0, 5))
        
        # Navigation
        ttk.Button(toolbar, text=t('previous'), command=self.previous_file).pack(side=tk.LEFT, padx=(10, 2))
        ttk.Button(toolbar, text=t('next'), command=self.next_file).pack(side=tk.LEFT, padx=(2, 5))
        
        # File info
        self.file_info_label = ttk.Label(toolbar, text=t('no_files'))
        self.file_info_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # Language selector (right side)
        lang_frame = ttk.Frame(toolbar)
        lang_frame.pack(side=tk.RIGHT, padx=(5, 10))
        
        ttk.Label(lang_frame, text=t('language') + ':').pack(side=tk.LEFT, padx=(0, 5))
        self.language_var = tk.StringVar(value=self.localization_manager.get_language())
        self.language_combo = ttk.Combobox(
            lang_frame, 
            textvariable=self.language_var, 
            values=['fr', 'en'], 
            state='readonly',
            width=8
        )
        self.language_combo.pack(side=tk.LEFT, padx=(0, 10))
        self.language_combo.bind('<<ComboboxSelected>>', self.on_language_change)
        
        # Quality Check button  
        ttk.Button(toolbar, text=t('quality_check'), command=self.run_quality_check).pack(side=tk.RIGHT, padx=(0, 5))
        
        # Save button
        ttk.Button(toolbar, text=t('save_result'), command=self.save_result).pack(side=tk.RIGHT)
        
    def create_video_controls(self, parent):
        """Create video-specific controls"""
        self.video_frame = ttk.Frame(parent)
        self.video_frame.pack(fill=tk.X, pady=(5, 0))
        
        # Frame slider
        ttk.Label(self.video_frame, text="Frame:").pack(side=tk.LEFT)
        self.frame_var = tk.IntVar()
        self.frame_slider = ttk.Scale(
            self.video_frame, 
            from_=0, 
            to=100, 
            orient=tk.HORIZONTAL, 
            variable=self.frame_var,
            command=self.on_frame_change
        )
        self.frame_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        
        # Frame info
        self.frame_info_label = ttk.Label(self.video_frame, text="0/0")
        self.frame_info_label.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Initially hide video controls
        self.video_frame.pack_forget()
        
    def select_file(self):
        """Select a single file"""
        file_path = filedialog.askopenfilename(
            title="Select Image or Video",
            filetypes=[
                ("All supported", "*.jpg *.jpeg *.png *.bmp *.tiff *.mp4 *.avi *.mov *.mkv"),
                ("Images", "*.jpg *.jpeg *.png *.bmp *.tiff"),
                ("Videos", "*.mp4 *.avi *.mov *.mkv"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            self.files_list = [file_path]
            self.current_index = 0
            self.load_current_file()
            
    def select_folder(self):
        """Select a folder containing images/videos"""
        folder_path = filedialog.askdirectory(title="Select Folder")
        
        if folder_path:
            # Get all supported files from the folder
            supported_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.mp4', '.avi', '.mov', '.mkv'}
            self.files_list = []
            
            for file_path in Path(folder_path).iterdir():
                if file_path.suffix.lower() in supported_extensions:
                    self.files_list.append(str(file_path))
                    
            if self.files_list:
                self.files_list.sort()
                self.current_index = 0
                self.load_current_file()
            else:
                messagebox.showwarning("Warning", "No supported files found in the selected folder.")
                
    def previous_file(self):
        """Navigate to previous file"""
        if self.files_list and self.current_index > 0:
            self.current_index -= 1
            self.load_current_file()
            
    def next_file(self):
        """Navigate to next file"""
        if self.files_list and self.current_index < len(self.files_list) - 1:
            self.current_index += 1
            self.load_current_file()
            
    def load_current_file(self):
        """Load the current file from the files list"""
        if not self.files_list or self.current_index >= len(self.files_list):
            return
            
        self.current_file = self.files_list[self.current_index]
        file_name = os.path.basename(self.current_file)
        
        # Update file info
        self.file_info_label.config(text=f"{file_name} ({self.current_index + 1}/{len(self.files_list)})")
        
        # Update image info panel
        if hasattr(self, 'info_panel'):
            self.info_panel.update_info(self.current_file)
        
        # Check if it's a video file
        video_extensions = {'.mp4', '.avi', '.mov', '.mkv'}
        is_video = Path(self.current_file).suffix.lower() in video_extensions
        
        if is_video:
            self.load_video()
        else:
            self.load_image()
            
    def load_image(self):
        """Load an image file"""
        # Hide video controls
        self.video_frame.pack_forget()
        
        try:
            if self.current_file is None:
                raise ValueError("No file selected")
                
            # Mark that we're loading a new image
            self.loading_new_image = True
            
            # Load image using OpenCV
            self.original_image = cv2.imread(self.current_file)
            if self.original_image is None:
                raise ValueError("Could not load image")
                
            # Convert BGR to RGB for display
            self.original_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2RGB)
            
            # Update preview
            self.update_preview()
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not load image: {str(e)}")
            self.loading_new_image = False  # Reset flag on error
            
    def load_video(self):
        """Load a video file"""
        # Show video controls
        self.video_frame.pack(fill=tk.X, pady=(5, 0))
        
        try:
            # Release previous video capture if exists
            if self.video_capture:
                self.video_capture.release()
            
            if self.current_file is None:
                raise ValueError("No file selected")
                
            self.video_capture = cv2.VideoCapture(self.current_file)
            if not self.video_capture.isOpened():
                raise ValueError("Could not open video file")
                
            self.total_frames = int(self.video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
            
            # Setup frame slider
            self.frame_slider.configure(to=self.total_frames - 1)
            self.frame_var.set(0)
            self.current_frame = 0
            
            # Load first frame
            self.load_video_frame(0)
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not load video: {str(e)}")
            
    def load_video_frame(self, frame_number):
        """Load a specific frame from the video"""
        if not self.video_capture:
            return
            
        try:
            # Mark that we're loading a new image
            self.loading_new_image = True
            
            self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
            ret, frame = self.video_capture.read()
            
            if ret:
                # Convert BGR to RGB for display
                self.original_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.current_frame = frame_number
                
                # Update frame info
                self.frame_info_label.config(text=f"{frame_number + 1}/{self.total_frames}")
                
                # Update preview
                self.update_preview()
            else:
                messagebox.showerror("Error", "Could not read video frame")
                self.loading_new_image = False
                
        except Exception as e:
            messagebox.showerror("Error", f"Could not load video frame: {str(e)}")
            self.loading_new_image = False  # Reset flag on error
            
    def on_frame_change(self, value):
        """Handle frame slider change"""
        frame_number = int(float(value))
        if frame_number != self.current_frame:
            self.load_video_frame(frame_number)
            
    def update_preview(self):
        """Update the preview with processed image using optimized subsampling for large images"""
        if self.original_image is None:
            return
            
        try:
            # Use optimized preview processing for large images
            self.original_preview, self.processed_preview, self.preview_scale_factor = self.processor.process_image_for_preview(
                self.original_image.copy(), max_size=1024
            )
            
            # Mark that full-size processed image needs to be updated when needed
            self.processed_image = None
            
            # Update preview panel with preview images
            # Pass reset_view=True if loading new image, False if just updating parameters
            self.preview_panel.update_images(
                self.original_preview, 
                self.processed_preview, 
                reset_view=self.loading_new_image
            )
            
            # Reset the flag after using it to ensure next parameter changes preserve rotation
            if self.loading_new_image:
                self.loading_new_image = False
            
            # Update pipeline description
            self.pipeline_panel.update_pipeline(self.processor.get_pipeline_description())
            
            # Log preview information for debugging
            if self.preview_scale_factor < 1.0:
                original_size = self.original_image.shape[:2]
                preview_size = self.original_preview.shape[:2]
                self.logger.info(f"Preview subsampling: {original_size[1]}x{original_size[0]} -> {preview_size[1]}x{preview_size[0]} (scale: {self.preview_scale_factor:.3f})")
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not process image: {str(e)}")
            self.logger.error(f"Preview update error: {str(e)}")
            
    def get_full_resolution_processed_image(self):
        """Get the full resolution processed image (process if needed)"""
        if self.original_image is None:
            return None
            
        # If we already have a full resolution processed image, return it
        if self.processed_image is not None:
            return self.processed_image
            
        # Otherwise, process the full resolution image
        try:
            self.logger.info("Processing full resolution image for saving...")
            original_size = self.original_image.shape[:2]
            self.logger.info(f"Full resolution: {original_size[1]}x{original_size[0]} pixels")
            
            # Process the full resolution image
            self.processed_image = self.processor.process_image(self.original_image.copy())
            
            self.logger.info("Full resolution processing completed")
            return self.processed_image
            
        except Exception as e:
            self.logger.error(f"Error processing full resolution image: {str(e)}")
            return None
    
    def run_quality_check(self):
        """Run quality analysis on the processed image - DISABLED FOR NOW"""
        messagebox.showinfo(
            "Contrôle Qualité", 
            "Système de contrôle qualité implémenté mais temporairement désactivé.\n"
            "Les modules d'analyse avancée sont prêts:\n"
            "- Détection couleurs irréalistes\n"
            "- Analyse saturation\n"
            "- Détection artefacts halo\n"
            "- Amplification bruit couleur\n"
            "- Équilibre tons moyens\n\n"
            "Activé dans la prochaine version."
        )
        
        # Original implementation commented out to avoid import issues
        # The quality check system is fully implemented in src/quality_check.py
        # but there are import conflicts when loading from the __init__.py
        """
        if self.original_image is None or self.processed_image is None:
            messagebox.showwarning(
                t('warning'),
                "Aucune image traitée disponible pour l'analyse qualité"
            )
            return
        
        try:
            # Show processing message
            progress_window = tk.Toplevel(self.root)
            progress_window.title(t('processing'))
            progress_window.geometry("300x100")
            progress_window.transient(self.root)
            progress_window.grab_set()
            
            # Center the window
            progress_window.update_idletasks()
            x = (progress_window.winfo_screenwidth() // 2) - (progress_window.winfo_width() // 2)
            y = (progress_window.winfo_screenheight() // 2) - (progress_window.winfo_height() // 2)
            progress_window.geometry(f"+{x}+{y}")
            
            progress_label = ttk.Label(progress_window, text="Analyse qualité en cours...", padding="20")
            progress_label.pack(expand=True)
            
            progress_bar = ttk.Progressbar(progress_window, mode='indeterminate', length=200)
            progress_bar.pack(pady=(0, 20))
            progress_bar.start()
            
            progress_window.update()
            
            # Get full resolution images for quality analysis
            original_full = self.original_image
            processed_full = self.get_full_resolution_processed_image()
            
            if processed_full is None:
                processed_full = self.processed_image
            
            # Initialize quality checker and run analysis
            from .quality_check import PostProcessingQualityChecker
            quality_checker = PostProcessingQualityChecker()
            quality_results = quality_checker.run_all_checks(original_full, processed_full)
            
            # Close progress window
            progress_window.destroy()
            
            # Show quality check dialog
            if quality_results and 'error' not in quality_results:
                # Get image name for the dialog
                image_name = "Unknown"
                if hasattr(self, 'current_file') and self.current_file:
                    image_name = os.path.basename(self.current_file)
                
                # For now, show results in a simple message box
                overall_score = quality_checker._calculate_overall_score(quality_results)
                messagebox.showinfo(
                    "Contrôle Qualité",
                    f"Analyse terminée pour {image_name}\\n"
                    f"Score global: {overall_score:.1f}/10\\n\\n"
                    f"Détails disponibles dans les logs."
                )
                
                # Log detailed results
                self.logger.info(f"Quality check completed for {image_name}: score {overall_score:.1f}/10")
                for category, data in quality_results.items():
                    if isinstance(data, dict) and 'recommendations' in data:
                        if data['recommendations']:
                            self.logger.info(f"{category} recommendations: {data['recommendations']}")
                
                self.logger.info("Quality check completed successfully")
            else:
                error_msg = quality_results.get('error', 'Unknown error') if quality_results else 'Analysis failed'
                messagebox.showerror(
                    t('error'),
                    f"Erreur lors de l'analyse qualité: {error_msg}"
                )
                self.logger.error(f"Quality check failed: {error_msg}")
                
        except Exception as e:
            error_msg = f"Erreur lors de l'analyse qualité: {str(e)}"
            messagebox.showerror(t('error'), error_msg)
            self.logger.error(error_msg)
        """
    
    def show_quality_placeholder(self):
        """Placeholder for quality check functionality"""
        messagebox.showinfo(
            "Contrôle Qualité",
            "Fonction de contrôle qualité en cours de développement.\n"
            "Cette fonctionnalité analysera automatiquement la qualité\n"
            "de l'image traitée et proposera des améliorations."
        )
            
    def save_result(self):
        """Save the processed result"""
        # Get full resolution processed image
        full_res_image = self.get_full_resolution_processed_image()
        
        if full_res_image is None:
            messagebox.showwarning("Warning", "No processed image to save")
            return
            
        # Check if it's a video
        if self.video_capture:
            self.save_video()
        else:
            self.save_image()
            
    def save_image(self):
        """Save processed image with advanced options"""
        from save_dialog import show_save_dialog
        
        # Determine initial filename and format
        initial_filename = ""
        initial_format = "jpg"
        
        if hasattr(self, 'current_file') and self.current_file:
            base_name = os.path.splitext(os.path.basename(self.current_file))[0]
            initial_filename = f"{base_name}_processed.jpg"
        
        # Show advanced save dialog
        save_options = show_save_dialog(self.root, initial_filename, initial_format)
        
        if not save_options:
            return  # User cancelled
            
        file_path = save_options['filename']
        
        try:
            # Show processing message for large images
            if self.processed_image is None and self.preview_scale_factor < 1.0:
                # Create a simple progress window
                progress_window = tk.Toplevel(self.root)
                progress_window.title("Processing...")
                progress_window.geometry("300x80")
                progress_window.transient(self.root)
                progress_window.grab_set()
                
                progress_label = ttk.Label(progress_window, text="Processing full resolution image...")
                progress_label.pack(pady=20)
                
                # Update the window to show it
                progress_window.update()
                
                # Get full resolution processed image
                full_res_image = self.get_full_resolution_processed_image()
                
                # Close progress window
                progress_window.destroy()
            else:
                full_res_image = self.get_full_resolution_processed_image()
                
            if full_res_image is None:
                raise ValueError("No processed image to save")
                
            # Convert RGB to BGR for saving
            image_bgr = cv2.cvtColor(full_res_image, cv2.COLOR_RGB2BGR)
            
            # Determine save parameters based on format and options
            save_params = []
            file_format = save_options['format']
            
            if file_format == 'jpg':
                quality = save_options.get('quality', 95)
                save_params = [cv2.IMWRITE_JPEG_QUALITY, quality]
                
                if save_options.get('progressive', False):
                    save_params.extend([cv2.IMWRITE_JPEG_PROGRESSIVE, 1])
                    
            elif file_format == 'png':
                compression = save_options.get('compression', 6)
                save_params = [cv2.IMWRITE_PNG_COMPRESSION, compression]
                
            elif file_format == 'tiff':
                compression_type = save_options.get('compression', 'lzw')
                if compression_type == 'none':
                    save_params = [cv2.IMWRITE_TIFF_COMPRESSION, 1]
                elif compression_type == 'lzw':
                    save_params = [cv2.IMWRITE_TIFF_COMPRESSION, 5]
                elif compression_type == 'zip':
                    save_params = [cv2.IMWRITE_TIFF_COMPRESSION, 8]
            
            # Save with advanced options
            success = cv2.imwrite(file_path, image_bgr, save_params)
            
            if success:
                # Handle metadata preservation if requested
                if save_options.get('preserve_metadata', False) and hasattr(self, 'current_file') and self.current_file:
                    self._preserve_metadata(self.current_file, file_path)
                
                messagebox.showinfo("Success", f"Image saved successfully!\nFile: {file_path}")
                self.logger.info(f"Image saved: {file_path} with format: {file_format}, options: {save_options}")
            else:
                raise ValueError("Failed to write image file")
                
        except Exception as e:
            messagebox.showerror("Error", f"Could not save image: {str(e)}")
            self.logger.error(f"Save image error: {str(e)}")
            
    def _preserve_metadata(self, source_path: str, target_path: str):
        """Preserve EXIF metadata from source to target image"""
        try:
            from PIL import Image
            from PIL.ExifTags import TAGS
            
            # Open source image to extract EXIF
            with Image.open(source_path) as source_img:
                exifdata = source_img.getexif()
                
            # Open target image and add EXIF
            if exifdata:
                with Image.open(target_path) as target_img:
                    # Convert to RGB if needed
                    if target_img.mode != 'RGB':
                        target_img = target_img.convert('RGB')
                    
                    # Save with EXIF data
                    target_img.save(target_path, exif=exifdata, quality=95, optimize=True)
                    
                self.logger.info(f"EXIF metadata preserved from {source_path} to {target_path}")
                
        except Exception as e:
            self.logger.warning(f"Could not preserve metadata: {str(e)}")
            # Continue without metadata preservation - not a critical error
                
    def save_video(self):
        """Save processed video"""
        file_path = filedialog.asksaveasfilename(
            title="Save Processed Video",
            defaultextension=".mp4",
            filetypes=[
                ("MP4", "*.mp4"),
                ("AVI", "*.avi"),
                ("MOV", "*.mov"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            # Show progress dialog
            progress_window = tk.Toplevel(self.root)
            progress_window.title("Processing Video")
            progress_window.geometry("400x100")
            progress_window.transient(self.root)
            progress_window.grab_set()
            
            progress_label = ttk.Label(progress_window, text="Processing video frames...")
            progress_label.pack(pady=10)
            
            progress_bar = ttk.Progressbar(progress_window, mode='determinate', maximum=self.total_frames)
            progress_bar.pack(fill=tk.X, padx=20, pady=10)
            
            # Process video in a separate thread
            def process_video():
                try:
                    if self.video_capture is None:
                        raise ValueError("No video loaded")
                        
                    # Get video properties
                    fps = int(self.video_capture.get(cv2.CAP_PROP_FPS))
                    width = int(self.video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
                    height = int(self.video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
                    
                    # Create video writer
                    fourcc = cv2.VideoWriter.fourcc(*'mp4v')
                    out = cv2.VideoWriter(file_path, fourcc, fps, (width, height))
                    
                    # Process each frame
                    self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    
                    for frame_num in range(self.total_frames):
                        ret, frame = self.video_capture.read()
                        if not ret:
                            break
                            
                        # Convert BGR to RGB
                        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        
                        # Process frame
                        processed_frame = self.processor.process_image(frame_rgb)
                        
                        # Convert back to BGR and write
                        processed_bgr = cv2.cvtColor(processed_frame, cv2.COLOR_RGB2BGR)
                        out.write(processed_bgr)
                        
                        # Update progress
                        try:
                            if progress_window.winfo_exists():
                                self.root.after(0, lambda f=frame_num: progress_bar.configure(value=f + 1) if progress_window.winfo_exists() else None)
                        except tk.TclError:
                            # Window was destroyed, ignore
                            pass
                        
                    out.release()
                    
                    # Close progress window and show success message
                    self.root.after(0, lambda: [
                        progress_window.destroy(),
                        messagebox.showinfo("Success", "Video saved successfully!")
                    ])
                    
                except Exception as e:
                    self.root.after(0, lambda: [
                        progress_window.destroy(),
                        messagebox.showerror("Error", f"Could not save video: {str(e)}")
                    ])
                    
            # Start processing thread
            thread = threading.Thread(target=process_video)
            thread.daemon = True
            thread.start()
            
    def __del__(self):
        """Cleanup resources"""
        if self.video_capture:
            self.video_capture.release()
            
    def on_language_change(self, event):
        """Handle language change"""
        new_language = self.language_var.get()
        self.localization_manager.set_language(new_language)
        self.refresh_ui()
        
    def refresh_ui(self):
        """Refresh the UI with new language"""
        # Update window title
        self.root.title(t('app_title'))
        
        # Update tab names
        self.notebook.tab(0, text=t('tab_parameters'))
        self.notebook.tab(1, text=t('tab_operations'))
        self.notebook.tab(2, text=t('tab_info'))
        self.notebook.tab(3, text=t('tab_about'))
        
        # Update toolbar button texts (without recreating)
        self.refresh_toolbar()
        
        # Update parameter panel
        if hasattr(self, 'param_panel'):
            self.param_panel.refresh_ui()
            
        # Update pipeline panel  
        if hasattr(self, 'pipeline_panel'):
            self.pipeline_panel.refresh_ui()
            
        # Update info panel
        if hasattr(self, 'info_panel'):
            self.info_panel.refresh_ui()
            
        # Update about panel
        if hasattr(self, 'about_panel'):
            self.about_panel.refresh_ui()
            
        # Update preview panel
        if hasattr(self, 'preview_panel'):
            self.preview_panel.refresh_ui()
    
    def refresh_toolbar(self):
        """Refresh toolbar texts without recreating widgets"""
        # Find the toolbar frame and update button texts
        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, ttk.Frame) and len(child.winfo_children()) > 5:  # This is likely the toolbar
                        self.update_toolbar_texts(child)
                        break
                break
    
    def update_toolbar_texts(self, toolbar):
        """Update toolbar button texts"""
        button_texts = [
            t('select_file'), t('select_folder'), t('previous'), t('next'), 
            None, None, None, t('save_result')  # None for labels and combobox
        ]
        
        button_index = 0
        for child in toolbar.winfo_children():
            if isinstance(child, ttk.Button):
                if button_index < len(button_texts) and button_texts[button_index]:
                    child.config(text=button_texts[button_index])
                button_index += 1
            elif isinstance(child, ttk.Label) and hasattr(self, 'file_info_label') and child == self.file_info_label:
                # Update file info label if no file is loaded
                current_text = child.cget('text')
                if 'No files' in current_text or 'Aucun fichier' in current_text:
                    child.config(text=t('no_files'))
            elif isinstance(child, ttk.Frame):  # Language selector frame
                for subchild in child.winfo_children():
                    if isinstance(subchild, ttk.Label):
                        subchild.config(text=t('language') + ':')

def main():
    root = tk.Tk()
    app = ImageVideoProcessorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
