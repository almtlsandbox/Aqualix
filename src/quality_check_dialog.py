"""
Quality Check Dialog for Post-Processing Analysis
Shows detailed quality analysis results with recommendations
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import Dict, Any, Optional
import webbrowser
from datetime import datetime
import json
import sys
import os
from pathlib import Path

# Add src directory to path for imports when loaded dynamically
current_dir = Path(__file__).parent
if str(current_dir) not in sys.path:
    sys.path.append(str(current_dir))

try:
    from localization import LocalizationManager
except ImportError:
    # Fallback for when running from different contexts
    from .localization import LocalizationManager


class QualityCheckDialog:
    """Dialog for displaying quality check results"""
    
    def __init__(self, parent: tk.Widget, quality_results: Dict[str, Any], 
                 image_name: str, localization: LocalizationManager):
        self.parent = parent
        self.quality_results = quality_results
        self.image_name = image_name
        self.loc = localization
        self.dialog = None
        self.create_dialog()
        
    def create_dialog(self):
        """Create the quality check dialog"""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title(self.loc.t('qc_dialog_title'))
        self.dialog.geometry("900x700")
        self.dialog.resizable(True, True)
        
        # Make dialog modal
        if self.parent and hasattr(self.parent, 'winfo_toplevel'):
            self.dialog.transient(self.parent.winfo_toplevel())
        self.dialog.grab_set()
        
        # Center on parent
        self.center_on_parent()
        
        # Main container with padding
        main_frame = ttk.Frame(self.dialog, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        self.dialog.grid_rowconfigure(0, weight=1)
        self.dialog.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Header with overall score
        self.create_header(main_frame)
        
        # Notebook for tabbed interface
        self.create_notebook(main_frame)
        
        # Bottom buttons
        self.create_buttons(main_frame)
        
    def center_on_parent(self):
        """Center dialog on parent window"""
        if self.dialog is None:
            return
            
        self.dialog.update_idletasks()
        
        if self.parent and hasattr(self.parent, 'winfo_rootx'):
            x = self.parent.winfo_rootx() + (self.parent.winfo_width() // 2) - (self.dialog.winfo_width() // 2)
            y = self.parent.winfo_rooty() + (self.parent.winfo_height() // 2) - (self.dialog.winfo_height() // 2)
        else:
            # Center on screen if no parent
            x = (self.dialog.winfo_screenwidth() // 2) - (self.dialog.winfo_width() // 2)
            y = (self.dialog.winfo_screenheight() // 2) - (self.dialog.winfo_height() // 2)
            
        self.dialog.geometry(f"+{x}+{y}")
        
    def create_header(self, parent):
        """Create header with overall quality score"""
        header_frame = ttk.LabelFrame(parent, text=self.loc.t('qc_overall_score'), padding="10")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        
        # Calculate overall score
        overall_score = self.calculate_overall_score()
        score_color = self.get_score_color(overall_score)
        status_text = self.get_status_text(overall_score)
        
        # Score display
        score_label = tk.Label(header_frame, text=f"{overall_score:.1f}/10", 
                             font=("Arial", 24, "bold"), fg=score_color)
        score_label.grid(row=0, column=0, padx=(0, 20))
        
        # Status text
        status_label = tk.Label(header_frame, text=status_text, 
                              font=("Arial", 12), fg=score_color)
        status_label.grid(row=0, column=1, sticky="w")
        
        # Image name
        name_label = tk.Label(header_frame, text=f"Image: {self.image_name}", 
                            font=("Arial", 10))
        name_label.grid(row=1, column=0, columnspan=2, sticky="w", pady=(10, 0))
        
    def create_notebook(self, parent):
        """Create tabbed notebook for different analysis categories"""
        self.notebook = ttk.Notebook(parent)
        self.notebook.grid(row=1, column=0, sticky="nsew", pady=(0, 10))
        
        # Color Analysis tab
        self.create_color_analysis_tab()
        
        # Saturation Analysis tab
        self.create_saturation_tab()
        
        # Noise & Artifacts tab
        self.create_noise_artifacts_tab()
        
        # Tone Mapping tab
        self.create_tone_mapping_tab()
        
        # Quality Metrics tab
        self.create_quality_metrics_tab()
        
    def create_color_analysis_tab(self):
        """Create color analysis tab"""
        tab_frame = ttk.Frame(self.notebook)
        self.notebook.add(tab_frame, text=self.loc.t('qc_tab_color_analysis'))
        
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
        
        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        tab_frame.grid_rowconfigure(0, weight=1)
        tab_frame.grid_columnconfigure(0, weight=1)
        
        # Content
        self.create_metrics_section(scrollable_frame, 'unrealistic_colors', 
                                   self.loc.t('qc_unrealistic_colors'))
        self.create_metrics_section(scrollable_frame, 'red_channel_analysis', 
                                   self.loc.t('qc_red_channel_analysis'))
        
    def create_saturation_tab(self):
        """Create saturation analysis tab"""
        tab_frame = ttk.Frame(self.notebook)
        self.notebook.add(tab_frame, text=self.loc.t('qc_tab_saturation'))
        
        # Scrollable frame setup (same as color analysis)
        canvas = tk.Canvas(tab_frame)
        scrollbar = ttk.Scrollbar(tab_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        tab_frame.grid_rowconfigure(0, weight=1)
        tab_frame.grid_columnconfigure(0, weight=1)
        
        # Content
        self.create_metrics_section(scrollable_frame, 'saturation_analysis', 
                                   self.loc.t('qc_saturation_analysis'))
        
    def create_noise_artifacts_tab(self):
        """Create noise & artifacts analysis tab"""
        tab_frame = ttk.Frame(self.notebook)
        self.notebook.add(tab_frame, text=self.loc.t('qc_tab_noise_artifacts'))
        
        # Scrollable frame setup
        canvas = tk.Canvas(tab_frame)
        scrollbar = ttk.Scrollbar(tab_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        tab_frame.grid_rowconfigure(0, weight=1)
        tab_frame.grid_columnconfigure(0, weight=1)
        
        # Content
        self.create_metrics_section(scrollable_frame, 'color_noise_analysis', 
                                   self.loc.t('qc_color_noise_analysis'))
        self.create_metrics_section(scrollable_frame, 'halo_artifacts', 
                                   self.loc.t('qc_halo_artifacts_analysis'))
        
    def create_tone_mapping_tab(self):
        """Create tone mapping analysis tab"""
        tab_frame = ttk.Frame(self.notebook)
        self.notebook.add(tab_frame, text=self.loc.t('qc_tab_tone_mapping'))
        
        # Scrollable frame setup
        canvas = tk.Canvas(tab_frame)
        scrollbar = ttk.Scrollbar(tab_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        tab_frame.grid_rowconfigure(0, weight=1)
        tab_frame.grid_columnconfigure(0, weight=1)
        
        # Content
        self.create_metrics_section(scrollable_frame, 'midtone_balance', 
                                   self.loc.t('qc_midtone_balance_analysis'))
        
    def create_quality_metrics_tab(self):
        """Create quality metrics overview tab"""
        tab_frame = ttk.Frame(self.notebook)
        self.notebook.add(tab_frame, text=self.loc.t('qc_tab_quality_metrics'))
        
        # Scrollable frame setup
        canvas = tk.Canvas(tab_frame)
        scrollbar = ttk.Scrollbar(tab_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        tab_frame.grid_rowconfigure(0, weight=1)
        tab_frame.grid_columnconfigure(0, weight=1)
        
        # Content
        self.create_metrics_section(scrollable_frame, 'quality_improvements', 
                                   self.loc.t('qc_quality_improvements'))
        
    def create_metrics_section(self, parent, section_key: str, section_title: str):
        """Create a section for specific metrics"""
        if section_key not in self.quality_results:
            return
            
        section_data = self.quality_results[section_key]
        
        # Section frame
        section_frame = ttk.LabelFrame(parent, text=section_title, padding="10")
        section_frame.grid(sticky="ew", padx=5, pady=5)
        parent.grid_columnconfigure(0, weight=1)
        
        row = 0
        
        # Display metrics
        for key, value in section_data.items():
            if key == 'recommendations':
                continue
                
            # Get localized label
            label_key = f"qc_{key}"
            label_text = self.loc.t(label_key, default=key.replace('_', ' ').title())
            
            # Create label
            label = ttk.Label(section_frame, text=f"{label_text}:")
            label.grid(row=row, column=0, sticky="w", padx=(0, 10))
            
            # Format and display value
            if isinstance(value, float):
                value_text = f"{value:.3f}"
                color = self.get_metric_color(value, key)
            elif isinstance(value, bool):
                value_text = self.loc.t('qc_detail_preserved' if value else 'qc_detail_lost')
                color = "green" if value else "red"
            elif isinstance(value, (list, tuple)) and len(value) == 3:
                # RGB values
                value_text = f"R:{value[0]:.1f} G:{value[1]:.1f} B:{value[2]:.1f}"
                color = "black"
            else:
                value_text = str(value)
                color = "black"
                
            value_label = tk.Label(section_frame, text=value_text, fg=color, font=("Arial", 9, "bold"))
            value_label.grid(row=row, column=1, sticky="w")
            
            # Add status indicator for problematic values
            if isinstance(value, float):
                status = self.get_metric_status(value, key)
                if status != 'good':
                    status_text = self.loc.t(f'qc_status_{status}')
                    status_color = {"warning": "orange", "problem": "red"}[status]
                    status_label = tk.Label(section_frame, text=f"[{status_text}]", 
                                          fg=status_color, font=("Arial", 8))
                    status_label.grid(row=row, column=2, sticky="w", padx=(10, 0))
            
            row += 1
            
        # Add recommendations if available
        if 'recommendations' in section_data and section_data['recommendations']:
            # Separator
            separator = ttk.Separator(section_frame, orient='horizontal')
            separator.grid(row=row, column=0, columnspan=3, sticky="ew", pady=(10, 5))
            row += 1
            
            # Recommendations title
            rec_title = ttk.Label(section_frame, text=self.loc.t('qc_recommendations'), 
                                font=("Arial", 10, "bold"))
            rec_title.grid(row=row, column=0, columnspan=3, sticky="w")
            row += 1
            
            # List recommendations
            for rec in section_data['recommendations']:
                rec_text = self.loc.t(rec, default=rec)
                rec_label = tk.Label(section_frame, text=f"• {rec_text}", 
                                   wraplength=600, justify="left", fg="darkblue")
                rec_label.grid(row=row, column=0, columnspan=3, sticky="w", pady=2)
                row += 1
        
    def create_buttons(self, parent):
        """Create bottom buttons"""
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=2, column=0, sticky="ew")
        button_frame.grid_columnconfigure(0, weight=1)
        
        # Export report button
        export_btn = ttk.Button(button_frame, text=self.loc.t('qc_export_report'),
                              command=self.export_report)
        export_btn.grid(row=0, column=0, sticky="w")
        
        # Close button
        close_btn = ttk.Button(button_frame, text=self.loc.t('close'),
                             command=self.close_dialog)
        close_btn.grid(row=0, column=1, sticky="e")
        
    def calculate_overall_score(self) -> float:
        """Calculate overall quality score (0-10)"""
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
        
    def calculate_section_score(self, section: str) -> float:
        """Calculate score for a specific section"""
        data = self.quality_results.get(section, {})
        
        if section == 'unrealistic_colors':
            # Lower is better for problems
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
            score += min(2.0, midtone_ratio * 5)  # Bonus for good midtone balance
            return score
            
        elif section == 'quality_improvements':
            contrast_imp = data.get('contrast_improvement', 0)
            entropy_imp = data.get('entropy_improvement', 0)
            color_enh = data.get('color_enhancement', 0)
            
            # Higher is better for improvements
            score = (contrast_imp + entropy_imp + color_enh) * 2
            return min(10.0, score)
            
        return 5.0  # Default neutral score
        
    def get_score_color(self, score: float) -> str:
        """Get color for score display"""
        if score >= 8.0:
            return "green"
        elif score >= 6.0:
            return "orange" 
        else:
            return "red"
            
    def get_status_text(self, score: float) -> str:
        """Get status text for score"""
        if score >= 8.0:
            return self.loc.t('qc_status_excellent')
        elif score >= 6.0:
            return self.loc.t('qc_status_good')
        else:
            return self.loc.t('qc_status_needs_improvement')
            
    def get_metric_color(self, value: float, key: str) -> str:
        """Get color for metric value based on key"""
        # Define thresholds for different metrics
        thresholds = {
            'extreme_red_pixels': (0.02, 0.05),  # warning, error
            'magenta_pixels': (0.01, 0.03),
            'red_dominance_ratio': (1.3, 1.5),
            'highly_saturated_pixels': (0.05, 0.1),
            'clipped_saturation': (0.02, 0.05),
            'red_noise_amplification': (0.1, 0.2),
            'halo_indicator': (0.3, 0.5),
            'contrast_improvement': (0.1, 0.05),  # inverted - higher is better
        }
        
        if key in thresholds:
            warning, error = thresholds[key]
            if key in ['contrast_improvement', 'entropy_improvement', 'color_enhancement']:
                # Higher is better
                if value >= warning:
                    return "green"
                elif value >= error:
                    return "orange"
                else:
                    return "red"
            else:
                # Lower is better  
                if value <= warning:
                    return "green"
                elif value <= error:
                    return "orange"
                else:
                    return "red"
        
        return "black"
        
    def get_metric_status(self, value: float, key: str) -> str:
        """Get status for metric value"""
        thresholds = {
            'extreme_red_pixels': (0.02, 0.05),
            'magenta_pixels': (0.01, 0.03),
            'red_dominance_ratio': (1.3, 1.5),
            'highly_saturated_pixels': (0.05, 0.1),
            'clipped_saturation': (0.02, 0.05),
            'red_noise_amplification': (0.1, 0.2),
            'halo_indicator': (0.3, 0.5),
        }
        
        if key in thresholds:
            warning, error = thresholds[key]
            if value <= warning:
                return "good"
            elif value <= error:
                return "warning"
            else:
                return "problem"
        
        return "good"
        
    def export_report(self):
        """Export quality report to text file"""
        try:
            filename = filedialog.asksaveasfilename(
                title=self.loc.t('qc_save_report'),
                defaultextension=".txt",
                filetypes=[
                    (self.loc.t('qc_text_files'), "*.txt"),
                    (self.loc.t('qc_all_files'), "*.*")
                ],
                initialfile=f"quality_report_{self.image_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            )
            
            if filename:
                self.save_report_to_file(filename)
                messagebox.showinfo(
                    self.loc.t('success'),
                    self.loc.t('qc_report_saved')
                )
        except Exception as e:
            messagebox.showerror(
                self.loc.t('error'),
                f"{self.loc.t('qc_report_save_error')}: {str(e)}"
            )
            
    def save_report_to_file(self, filename: str):
        """Save detailed report to file"""
        with open(filename, 'w', encoding='utf-8') as f:
            # Header
            f.write("=" * 60 + "\n")
            f.write(f"{self.loc.t('qc_quality_report')}\n")
            f.write("=" * 60 + "\n\n")
            
            f.write(f"Image: {self.image_name}\n")
            f.write(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Overall Score: {self.calculate_overall_score():.1f}/10\n\n")
            
            # Detailed sections
            for section_key, section_data in self.quality_results.items():
                section_title = self.loc.t(f'qc_{section_key}', default=section_key.title())
                f.write(f"\n{section_title}\n")
                f.write("-" * len(section_title) + "\n")
                
                for key, value in section_data.items():
                    if key == 'recommendations':
                        continue
                        
                    label = self.loc.t(f'qc_{key}', default=key.replace('_', ' ').title())
                    if isinstance(value, float):
                        f.write(f"{label}: {value:.3f}\n")
                    elif isinstance(value, (list, tuple)) and len(value) == 3:
                        f.write(f"{label}: R:{value[0]:.1f} G:{value[1]:.1f} B:{value[2]:.1f}\n")
                    else:
                        f.write(f"{label}: {value}\n")
                
                # Add recommendations
                if 'recommendations' in section_data and section_data['recommendations']:
                    f.write(f"\n{self.loc.t('qc_recommendations')}:\n")
                    for rec in section_data['recommendations']:
                        rec_text = self.loc.t(rec, default=rec)
                        f.write(f"  • {rec_text}\n")
                f.write("\n")
            
            # Summary recommendations
            all_recommendations = []
            for section_data in self.quality_results.values():
                if isinstance(section_data, dict) and 'recommendations' in section_data:
                    all_recommendations.extend(section_data['recommendations'])
            
            if not all_recommendations:
                f.write(f"{self.loc.t('qc_no_issues_found')}\n")
            else:
                f.write(f"{self.loc.t('qc_recommendations')} Summary:\n")
                f.write("-" * 30 + "\n")
                for i, rec in enumerate(set(all_recommendations), 1):
                    rec_text = self.loc.t(rec, default=rec)
                    f.write(f"{i}. {rec_text}\n")
                    
    def close_dialog(self):
        """Close the dialog"""
        if self.dialog:
            self.dialog.destroy()
            
    def show(self):
        """Show the dialog"""
        if self.dialog:
            self.dialog.focus()
            self.dialog.wait_window()

