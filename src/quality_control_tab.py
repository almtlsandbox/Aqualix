"""
Quality Control Tab Component for Aqualix
Integrated quality control panel that works as a tab in the main interface
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import threading
from pathlib import Path
import importlib.util
import numpy as np
from .ui_colors import ColoredButton


class QualityControlTab:
    """Quality control tab component integrated in main interface"""
    
    def __init__(self, parent, app_instance, loc_manager):
        self.parent = parent
        self.app = app_instance
        self.loc = loc_manager
        
        # Quality control state
        self.quality_results = None
        self.last_analysis_time = None
        self.is_running = False
        
        self.setup_ui()
    
    def refresh_ui(self):
        """Refresh UI elements when language changes"""
        if hasattr(self, 'analyze_button'):
            self.analyze_button.config(text=self.loc.t('qc_run_analysis'))
        
        # Update status display
        if hasattr(self, 'status_label'):
            if self.quality_results is None:
                self.status_label.config(text=self.loc.t('qc_no_analysis'))
            elif self.is_running:
                self.status_label.config(text=self.loc.t('qc_analysis_running'))
            elif self.last_analysis_time:
                self.status_label.config(text=f"{self.loc.t('qc_last_analysis')} {self.last_analysis_time}")
        
        # Refresh results display if present
        if self.quality_results is not None:
            self.display_results()
    
    def setup_ui(self):
        """Setup the quality control tab interface"""
        
        # Main container
        main_frame = ttk.Frame(self.parent)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header with analysis button
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Analysis button
        self.analyze_button = ColoredButton(
            header_frame, 
            text=self.loc.t('qc_run_analysis'),
            command=self.run_analysis,
            style_type='primary'  # Style primary pour meilleur contraste
        )
        self.analyze_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Status label
        self.status_label = ttk.Label(
            header_frame, 
            text=self.loc.t('qc_no_analysis'),
            foreground="gray"
        )
        self.status_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Results container
        self.results_frame = ttk.Frame(main_frame)
        self.results_frame.pack(fill=tk.BOTH, expand=True)
        
        # Initially show "no analysis" message
        self.show_no_analysis()
    
    def show_no_analysis(self):
        """Show message when no analysis has been run"""
        # Clear existing results
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        # Show message
        msg_frame = ttk.Frame(self.results_frame)
        msg_frame.pack(expand=True)
        
        ttk.Label(
            msg_frame,
            text=self.loc.t('qc_no_analysis'),
            foreground="gray",
            font=("TkDefaultFont", 10)
        ).pack(pady=50)
    
    def run_analysis(self):
        """Run quality analysis in background thread"""
        if self.is_running:
            return
        
        # Check if image is loaded - PROTECTION RENFORCÉE
        if not self.app.current_file or self.app.original_image is None:  # ✅ CORRIGÉ : current_file au lieu de current_image_path
            messagebox.showwarning(
                "Attention",
                "Veuillez d'abord charger une image avant de lancer l'analyse qualité."
            )
            return
        
        # Update UI
        self.is_running = True
        self.analyze_button.config(state='disabled', text=self.loc.t('qc_analysis_running'))
        self.status_label.config(text=self.loc.t('qc_analysis_running'), foreground="blue")
        
        # Run analysis in background
        def analyze_thread():
            try:
                # Force complete refresh of processing pipeline with current UI parameters
                # This ensures all parameter changes are applied before analysis
                self.app.processed_image = None
                self.app.processed_preview = None
                
                # Force a preview update to synchronize all parameters
                # This will process the image with the current UI parameter values
                if hasattr(self.app, 'update_preview'):
                    try:
                        self.app.update_preview()
                    except:
                        pass
                
                # OPTIMIZATION: Use subsampled preview images for faster quality analysis
                # Preview images are already processed with current parameters and are much smaller
                # This provides the same quality metrics while being significantly faster
                
                # Get preview images (already processed with current parameters)
                if not hasattr(self.app, 'original_preview') or self.app.original_preview is None:
                    raise Exception("Preview images not available - please wait for preview to update")
                
                if not hasattr(self.app, 'processed_preview') or self.app.processed_preview is None:
                    raise Exception("Processed preview not available")
                
                original_for_analysis = self.app.original_preview
                processed_for_analysis = self.app.processed_preview
                
                # Log the optimization being used
                original_size = self.app.original_image.shape[:2] if self.app.original_image is not None else (0, 0)
                preview_size = original_for_analysis.shape[:2]
                scale_factor = getattr(self.app, 'preview_scale_factor', 1.0)
                
                self.app.logger.info(f"Quality analysis using preview optimization: {original_size[1]}x{original_size[0]} -> {preview_size[1]}x{preview_size[0]} (scale: {scale_factor:.3f})")
                
                # Load quality check module
                quality_check_path = Path(__file__).parent / "quality_check.py"
                spec = importlib.util.spec_from_file_location("quality_check", quality_check_path)
                if spec is None:
                    raise ImportError("Cannot load quality_check module")
                
                quality_check_module = importlib.util.module_from_spec(spec)
                if spec.loader is not None:
                    spec.loader.exec_module(quality_check_module)
                
                # Run analysis
                quality_checker = quality_check_module.PostProcessingQualityChecker()
                quality_results = quality_checker.run_all_checks(original_for_analysis, processed_for_analysis)
                
                # Update UI in main thread
                self.app.root.after(0, self.analysis_completed, quality_results)
                
            except Exception as e:
                self.app.root.after(0, self.analysis_failed, str(e))
        
        thread = threading.Thread(target=analyze_thread, daemon=True)
        thread.start()
    
    def analysis_completed(self, quality_results):
        """Handle completed analysis"""
        self.is_running = False
        self.quality_results = quality_results
        self.last_analysis_time = datetime.now()
        
        # Update UI
        self.analyze_button.config(state='normal', text=self.loc.t('qc_run_analysis'))
        self.status_label.config(
            text=f"{self.loc.t('qc_last_analysis')} {self.last_analysis_time.strftime('%H:%M:%S')}",
            foreground="green"
        )
        
        # Display results
        self.display_results()
    
    def analysis_failed(self, error_message):
        """Handle failed analysis"""
        self.is_running = False
        
        # Update UI
        self.analyze_button.config(state='normal', text=self.loc.t('qc_run_analysis'))
        self.status_label.config(
            text=f"{self.loc.t('error')}: {error_message}",
            foreground="red"
        )
    
    def display_results(self):
        """Display quality analysis results"""
        # Clear existing results
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        if not self.quality_results:
            self.show_no_analysis()
            return
        
        # Calculate overall score
        overall_score = self.calculate_overall_score()
        
        # Create main results container
        results_container = ttk.Frame(self.results_frame)
        results_container.pack(fill=tk.BOTH, expand=True)
        
        # Overall score section
        score_frame = ttk.LabelFrame(results_container, text=self.loc.t('qc_overall_score'), padding=10)
        score_frame.pack(fill=tk.X, pady=(0, 10))
        
        score_color = self.get_score_color(overall_score)
        ttk.Label(
            score_frame,
            text=f"{overall_score:.1f}/10.0",
            font=("TkDefaultFont", 16, "bold"),
            foreground=score_color
        ).pack(side=tk.LEFT)
        
        ttk.Label(
            score_frame,
            text=self.get_status_text(overall_score),
            font=("TkDefaultFont", 12),
            foreground=score_color
        ).pack(side=tk.LEFT, padx=(20, 0))
        
        # Create notebook for detailed results
        self.results_notebook = ttk.Notebook(results_container)
        self.results_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Add tabs for each analysis section
        self.add_color_analysis_tab()
        self.add_saturation_tab()
        self.add_noise_artifacts_tab()
        self.add_tone_mapping_tab()
        self.add_quality_metrics_tab()
    
    def add_color_analysis_tab(self):
        """Add color analysis tab"""
        tab_frame = ttk.Frame(self.results_notebook)
        self.results_notebook.add(tab_frame, text=self.loc.t('qc_tab_color_analysis'))
        
        # Scrollable frame
        canvas = tk.Canvas(tab_frame)
        scrollbar = ttk.Scrollbar(tab_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Add content
        self.add_section_content(scrollable_frame, 'unrealistic_colors')
        self.add_section_content(scrollable_frame, 'red_channel_analysis')
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def add_saturation_tab(self):
        """Add saturation analysis tab"""
        tab_frame = ttk.Frame(self.results_notebook)
        self.results_notebook.add(tab_frame, text=self.loc.t('qc_tab_saturation'))
        
        # Scrollable frame
        canvas = tk.Canvas(tab_frame)
        scrollbar = ttk.Scrollbar(tab_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Add content
        self.add_section_content(scrollable_frame, 'saturation_analysis')
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def add_noise_artifacts_tab(self):
        """Add noise & artifacts analysis tab"""
        tab_frame = ttk.Frame(self.results_notebook)
        self.results_notebook.add(tab_frame, text=self.loc.t('qc_tab_noise_artifacts'))
        
        # Scrollable frame
        canvas = tk.Canvas(tab_frame)
        scrollbar = ttk.Scrollbar(tab_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Add content
        self.add_section_content(scrollable_frame, 'color_noise_analysis')
        self.add_section_content(scrollable_frame, 'halo_artifacts')
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def add_tone_mapping_tab(self):
        """Add tone mapping analysis tab"""
        tab_frame = ttk.Frame(self.results_notebook)
        self.results_notebook.add(tab_frame, text=self.loc.t('qc_tab_tone_mapping'))
        
        # Scrollable frame
        canvas = tk.Canvas(tab_frame)
        scrollbar = ttk.Scrollbar(tab_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Add content
        self.add_section_content(scrollable_frame, 'midtone_balance')
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def add_quality_metrics_tab(self):
        """Add quality metrics tab"""
        tab_frame = ttk.Frame(self.results_notebook)
        self.results_notebook.add(tab_frame, text=self.loc.t('qc_tab_quality_metrics'))
        
        # Scrollable frame
        canvas = tk.Canvas(tab_frame)
        scrollbar = ttk.Scrollbar(tab_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Add content
        self.add_section_content(scrollable_frame, 'quality_improvements')
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def add_section_content(self, parent, section_key):
        """Add content for a specific analysis section"""
        if not self.quality_results or section_key not in self.quality_results:
            return
        
        section_data = self.quality_results[section_key]
        section_title = self.loc.t(f'qc_{section_key}', default=section_key.title())
        
        # Section frame
        section_frame = ttk.LabelFrame(parent, text=section_title, padding=10)
        section_frame.pack(fill=tk.X, pady=5)
        
        # Handle different data types
        if isinstance(section_data, list):
            # Handle list of recommendations
            for item in section_data:
                item_text = self.loc.t(item, default=item)
                ttk.Label(section_frame, text=f"• {item_text}").pack(anchor=tk.W, pady=1)
        elif isinstance(section_data, dict):
            # Handle dictionary data
            for key, value in section_data.items():
                if key == 'recommendations':
                    continue
                
                label = self.loc.t(f'qc_{key}', default=key.replace('_', ' ').title())
                
                # Create metric frame
                metric_frame = ttk.Frame(section_frame)
                metric_frame.pack(fill=tk.X, pady=2)
                
                ttk.Label(metric_frame, text=f"{label}:", width=25, anchor=tk.W).pack(side=tk.LEFT)
                
                # Format value based on type
                if isinstance(value, float):
                    value_text = f"{value:.3f}"
                    color = self.get_metric_color(value, key)
                elif isinstance(value, (list, tuple)) and len(value) == 3:
                    value_text = f"R:{value[0]:.1f} G:{value[1]:.1f} B:{value[2]:.1f}"
                    color = "black"
                else:
                    value_text = str(value)
                    color = "black"
                
                ttk.Label(
                    metric_frame, 
                    text=value_text,
                    foreground=color,
                    font=("TkDefaultFont", 9, "bold" if color != "black" else "normal")
                ).pack(side=tk.LEFT, padx=(10, 0))
            
            # Add recommendations
            if 'recommendations' in section_data and section_data['recommendations']:
                rec_frame = ttk.LabelFrame(section_frame, text=self.loc.t('qc_recommendations'), padding=5)
                rec_frame.pack(fill=tk.X, pady=(10, 0))
                
                for rec in section_data['recommendations']:
                    rec_text = self.loc.t(rec, default=rec)
                    ttk.Label(
                        rec_frame, 
                        text=f"• {rec_text}",
                        wraplength=400,
                        justify=tk.LEFT
                    ).pack(anchor=tk.W, pady=1)
    
    def calculate_overall_score(self):
        """Calculate overall quality score"""
        if not self.quality_results:
            return 0.0
        
        scores = []
        
        # Weight different aspects
        weights = {
            'unrealistic_colors': 0.25,
            'saturation_analysis': 0.20,
            'color_noise_analysis': 0.15,
            'halo_artifacts': 0.15,
            'midtone_balance': 0.15,
            'quality_improvements': 0.10
        }
        
        for section, weight in weights.items():
            if section in self.quality_results:
                section_score = self.calculate_section_score(section)
                scores.append(section_score * weight)
        
        return min(10.0, sum(scores))
    
    def calculate_section_score(self, section):
        """Calculate score for a specific section"""
        if not self.quality_results:
            return 5.0
        
        data = self.quality_results.get(section, {})
        
        if section == 'unrealistic_colors':
            extreme_red = data.get('extreme_red_pixels', 0)
            magenta = data.get('magenta_pixels', 0) 
            red_dominance = data.get('red_dominance_ratio', 1)
            score = 10.0 - (extreme_red * 20 + magenta * 15 + max(0, red_dominance - 1.5) * 5)
            return max(0, score)
            
        elif section == 'saturation_analysis':
            highly_sat = data.get('highly_saturated_pixels', 0)
            clipped = data.get('clipped_saturation', 0)
            large_areas = data.get('large_saturated_areas', 0)
            score = 10.0 - (highly_sat * 10 + clipped * 15 + large_areas * 10)
            return max(0, score)
            
        elif section == 'color_noise_analysis':
            red_noise = data.get('red_noise_amplification', 0)
            avg_noise = data.get('average_noise_ratio', 1)
            score = 10.0 - (red_noise * 10 + max(0, avg_noise - 1.2) * 5)
            return max(0, score)
            
        elif section == 'halo_artifacts':
            halo = data.get('halo_indicator', 0)
            edge_var = data.get('edge_intensity_variance', 0)
            score = 10.0 - (halo * 15 + edge_var * 5)
            return max(0, score)
            
        elif section == 'midtone_balance':
            shadow_detail = data.get('shadow_detail_preserved', True)
            midtone_ratio = data.get('midtone_ratio', 0.3)
            score = 8.0 if shadow_detail else 4.0
            score += min(2.0, midtone_ratio * 5)
            return score
            
        elif section == 'quality_improvements':
            contrast_imp = data.get('contrast_improvement', 0)
            entropy_imp = data.get('entropy_improvement', 0)
            color_enh = data.get('color_enhancement', 0)
            score = (contrast_imp + entropy_imp + color_enh) * 2
            return min(10.0, score)
        
        return 5.0
    
    def get_score_color(self, score):
        """Get color for score display"""
        if score >= 8.0:
            return "green"
        elif score >= 6.0:
            return "orange" 
        else:
            return "red"
    
    def get_status_text(self, score):
        """Get status text for score"""
        if score >= 8.0:
            return self.loc.t('qc_status_excellent')
        elif score >= 6.0:
            return self.loc.t('qc_status_good')
        else:
            return self.loc.t('qc_status_needs_improvement')
    
    def get_metric_color(self, value, key):
        """Get color for metric value based on key"""
        # Define thresholds for different metrics
        thresholds = {
            'extreme_red_pixels': (0.02, 0.05),
            'magenta_pixels': (0.01, 0.03),
            'red_dominance_ratio': (1.5, 2.0),
            'highly_saturated_pixels': (0.1, 0.2),
            'clipped_saturation': (0.02, 0.05),
            'red_noise_amplification': (1.5, 2.0),
            'halo_indicator': (0.15, 0.25)
        }
        
        if key not in thresholds:
            return "black"
        
        warning, error = thresholds[key]
        
        if value >= error:
            return "red"
        elif value >= warning:
            return "orange"
        else:
            return "green"
