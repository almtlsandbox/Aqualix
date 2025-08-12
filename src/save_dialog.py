"""
Advanced Save Dialog for Aqualix Image Processor
Provides comprehensive file format and compression options
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from typing import Dict, Any, Optional
from localization import t


class SaveDialog:
    """Advanced save dialog with format and compression options"""
    
    def __init__(self, parent, initial_filename: str = "", current_format: str = "jpg"):
        self.parent = parent
        self.result = None
        self.initial_filename = initial_filename
        self.current_format = current_format.lower()
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(t('save_dialog_title'))
        self.dialog.geometry("500x600")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.center_dialog()
        
        # Create UI
        self.create_ui()
        
        # Load current settings
        self.load_default_settings()
        
    def center_dialog(self):
        """Center dialog on parent window"""
        self.dialog.update_idletasks()
        x = self.parent.winfo_x() + (self.parent.winfo_width() // 2) - (self.dialog.winfo_width() // 2)
        y = self.parent.winfo_y() + (self.parent.winfo_height() // 2) - (self.dialog.winfo_height() // 2)
        self.dialog.geometry(f"+{x}+{y}")
        
    def create_ui(self):
        """Create the user interface"""
        main_frame = ttk.Frame(self.dialog, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # File selection section
        self.create_file_section(main_frame)
        
        # Format selection section
        self.create_format_section(main_frame)
        
        # Quality/Compression section
        self.create_quality_section(main_frame)
        
        # Advanced options section
        self.create_advanced_section(main_frame)
        
        # Preview section
        self.create_preview_section(main_frame)
        
        # Buttons
        self.create_buttons(main_frame)
        
    def create_file_section(self, parent):
        """Create file selection section"""
        file_frame = ttk.LabelFrame(parent, text=t('save_file_location'), padding="10")
        file_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Filename entry
        filename_frame = ttk.Frame(file_frame)
        filename_frame.pack(fill=tk.X)
        
        ttk.Label(filename_frame, text=t('save_filename')).pack(side=tk.LEFT)
        
        self.filename_var = tk.StringVar(value=self.initial_filename)
        self.filename_entry = ttk.Entry(filename_frame, textvariable=self.filename_var)
        self.filename_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 5))
        
        self.browse_button = ttk.Button(filename_frame, text=t('browse'), command=self.browse_file)
        self.browse_button.pack(side=tk.RIGHT)
        
    def create_format_section(self, parent):
        """Create format selection section"""
        format_frame = ttk.LabelFrame(parent, text=t('save_file_format'), padding="10")
        format_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.format_var = tk.StringVar(value=self.current_format)
        
        formats = [
            ('JPEG', 'jpg', t('save_format_jpeg_desc')),
            ('PNG', 'png', t('save_format_png_desc')),
            ('TIFF', 'tiff', t('save_format_tiff_desc'))
        ]
        
        for i, (name, ext, desc) in enumerate(formats):
            frame = ttk.Frame(format_frame)
            frame.pack(fill=tk.X, pady=2)
            
            radio = ttk.Radiobutton(frame, text=name, variable=self.format_var, 
                                  value=ext, command=self.on_format_change)
            radio.pack(side=tk.LEFT)
            
            desc_label = ttk.Label(frame, text=desc, font=('Arial', 9), foreground='gray')
            desc_label.pack(side=tk.LEFT, padx=(10, 0))
            
    def create_quality_section(self, parent):
        """Create quality/compression section"""
        self.quality_frame = ttk.LabelFrame(parent, text=t('save_quality_compression'), padding="10")
        self.quality_frame.pack(fill=tk.X, pady=(0, 10))
        
        # JPEG Quality
        self.jpeg_frame = ttk.Frame(self.quality_frame)
        self.jpeg_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(self.jpeg_frame, text=t('save_jpeg_quality')).pack(side=tk.LEFT)
        
        self.jpeg_quality_var = tk.IntVar(value=95)
        self.jpeg_scale = ttk.Scale(self.jpeg_frame, from_=60, to=100, 
                                   variable=self.jpeg_quality_var, orient=tk.HORIZONTAL)
        self.jpeg_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 10))
        
        self.jpeg_quality_label = ttk.Label(self.jpeg_frame, text="95")
        self.jpeg_quality_label.pack(side=tk.RIGHT)
        
        self.jpeg_scale.configure(command=self.update_jpeg_quality_label)
        
        # PNG Compression
        self.png_frame = ttk.Frame(self.quality_frame)
        self.png_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(self.png_frame, text=t('save_png_compression')).pack(side=tk.LEFT)
        
        self.png_compression_var = tk.IntVar(value=6)
        self.png_scale = ttk.Scale(self.png_frame, from_=0, to=9, 
                                  variable=self.png_compression_var, orient=tk.HORIZONTAL)
        self.png_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 10))
        
        self.png_compression_label = ttk.Label(self.png_frame, text="6")
        self.png_compression_label.pack(side=tk.RIGHT)
        
        self.png_scale.configure(command=self.update_png_compression_label)
        
        # TIFF Compression
        self.tiff_frame = ttk.Frame(self.quality_frame)
        self.tiff_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(self.tiff_frame, text=t('save_tiff_compression')).pack(side=tk.LEFT)
        
        self.tiff_compression_var = tk.StringVar(value='lzw')
        tiff_combo = ttk.Combobox(self.tiff_frame, textvariable=self.tiff_compression_var,
                                 values=['none', 'lzw', 'zip'], state='readonly')
        tiff_combo.pack(side=tk.LEFT, padx=(10, 0))
        
    def create_advanced_section(self, parent):
        """Create advanced options section"""
        advanced_frame = ttk.LabelFrame(parent, text=t('save_advanced_options'), padding="10")
        advanced_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Preserve metadata
        self.preserve_metadata_var = tk.BooleanVar(value=True)
        metadata_check = ttk.Checkbutton(advanced_frame, text=t('save_preserve_metadata'),
                                       variable=self.preserve_metadata_var)
        metadata_check.pack(anchor=tk.W, pady=2)
        
        # Embed color profile
        self.embed_profile_var = tk.BooleanVar(value=True)
        profile_check = ttk.Checkbutton(advanced_frame, text=t('save_embed_color_profile'),
                                      variable=self.embed_profile_var)
        profile_check.pack(anchor=tk.W, pady=2)
        
        # Progressive JPEG
        self.progressive_var = tk.BooleanVar(value=False)
        self.progressive_check = ttk.Checkbutton(advanced_frame, text=t('save_progressive_jpeg'),
                                               variable=self.progressive_var)
        self.progressive_check.pack(anchor=tk.W, pady=2)
        
    def create_preview_section(self, parent):
        """Create preview section"""
        preview_frame = ttk.LabelFrame(parent, text=t('save_preview'), padding="10")
        preview_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.preview_text = tk.Text(preview_frame, height=4, wrap=tk.WORD, 
                                  font=('Consolas', 9), background='#f0f0f0')
        self.preview_text.pack(fill=tk.X)
        
        scrollbar = ttk.Scrollbar(preview_frame, orient=tk.VERTICAL, command=self.preview_text.yview)
        self.preview_text.configure(yscrollcommand=scrollbar.set)
        
    def create_buttons(self, parent):
        """Create dialog buttons"""
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Presets
        preset_frame = ttk.Frame(button_frame)
        preset_frame.pack(side=tk.LEFT)
        
        ttk.Button(preset_frame, text=t('save_preset_high_quality'), 
                  command=self.set_high_quality_preset).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(preset_frame, text=t('save_preset_web_optimized'), 
                  command=self.set_web_optimized_preset).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(preset_frame, text=t('save_preset_archive'), 
                  command=self.set_archive_preset).pack(side=tk.LEFT)
        
        # Main buttons
        main_buttons = ttk.Frame(button_frame)
        main_buttons.pack(side=tk.RIGHT)
        
        ttk.Button(main_buttons, text=t('cancel'), command=self.cancel).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(main_buttons, text=t('save'), command=self.save).pack(side=tk.RIGHT)
        
    def on_format_change(self):
        """Handle format change"""
        format_ext = self.format_var.get()
        
        # Show/hide relevant quality controls
        if format_ext == 'jpg':
            self.jpeg_frame.pack(fill=tk.X, pady=2)
            self.png_frame.pack_forget()
            self.tiff_frame.pack_forget()
            self.progressive_check.pack(anchor=tk.W, pady=2)
        elif format_ext == 'png':
            self.jpeg_frame.pack_forget()
            self.png_frame.pack(fill=tk.X, pady=2)
            self.tiff_frame.pack_forget()
            self.progressive_check.pack_forget()
        elif format_ext == 'tiff':
            self.jpeg_frame.pack_forget()
            self.png_frame.pack_forget()
            self.tiff_frame.pack(fill=tk.X, pady=2)
            self.progressive_check.pack_forget()
            
        # Update filename extension
        filename = self.filename_var.get()
        if filename and '.' in filename:
            base_name = os.path.splitext(filename)[0]
            self.filename_var.set(f"{base_name}.{format_ext}")
            
        self.update_preview()
        
    def update_jpeg_quality_label(self, value):
        """Update JPEG quality label"""
        quality = int(float(value))
        self.jpeg_quality_label.config(text=str(quality))
        self.update_preview()
        
    def update_png_compression_label(self, value):
        """Update PNG compression label"""
        compression = int(float(value))
        self.png_compression_label.config(text=str(compression))
        self.update_preview()
        
    def update_preview(self):
        """Update preview text"""
        format_ext = self.format_var.get()
        filename = self.filename_var.get()
        
        preview_lines = []
        preview_lines.append(f"{t('save_preview_file')}: {filename}")
        preview_lines.append(f"{t('save_preview_format')}: {format_ext.upper()}")
        
        if format_ext == 'jpg':
            quality = self.jpeg_quality_var.get()
            preview_lines.append(f"{t('save_preview_quality')}: {quality}%")
            if self.progressive_var.get():
                preview_lines.append(f"{t('save_preview_progressive')}: {t('yes')}")
        elif format_ext == 'png':
            compression = self.png_compression_var.get()
            preview_lines.append(f"{t('save_preview_compression')}: {compression}/9")
        elif format_ext == 'tiff':
            compression = self.tiff_compression_var.get()
            preview_lines.append(f"{t('save_preview_compression')}: {compression.upper()}")
            
        if self.preserve_metadata_var.get():
            preview_lines.append(f"{t('save_preview_metadata')}: {t('preserved')}")
            
        if self.embed_profile_var.get():
            preview_lines.append(f"{t('save_preview_color_profile')}: {t('embedded')}")
        
        self.preview_text.delete(1.0, tk.END)
        self.preview_text.insert(1.0, "\n".join(preview_lines))
        
    def browse_file(self):
        """Browse for save location"""
        format_ext = self.format_var.get()
        filetypes = []
        
        if format_ext == 'jpg':
            filetypes = [("JPEG files", "*.jpg *.jpeg"), ("All files", "*.*")]
        elif format_ext == 'png':
            filetypes = [("PNG files", "*.png"), ("All files", "*.*")]
        elif format_ext == 'tiff':
            filetypes = [("TIFF files", "*.tiff *.tif"), ("All files", "*.*")]
            
        filename = filedialog.asksaveasfilename(
            parent=self.dialog,
            title=t('save_select_location'),
            filetypes=filetypes,
            defaultextension=f'.{format_ext}',
            initialdir=os.path.dirname(self.filename_var.get()) if self.filename_var.get() else None
        )
        
        if filename:
            self.filename_var.set(filename)
            self.update_preview()
            
    def set_high_quality_preset(self):
        """Set high quality preset"""
        self.format_var.set('tiff')
        self.tiff_compression_var.set('lzw')
        self.preserve_metadata_var.set(True)
        self.embed_profile_var.set(True)
        self.on_format_change()
        # No need to update labels for TIFF as it uses a combobox
        
    def set_web_optimized_preset(self):
        """Set web optimized preset"""
        self.format_var.set('jpg')
        self.jpeg_quality_var.set(85)
        self.progressive_var.set(True)
        self.preserve_metadata_var.set(False)
        self.embed_profile_var.set(False)
        self.on_format_change()
        # Update the quality label manually
        self.update_jpeg_quality_label(85)
        
    def set_archive_preset(self):
        """Set archive preset"""
        self.format_var.set('png')
        self.png_compression_var.set(9)
        self.preserve_metadata_var.set(True)
        self.embed_profile_var.set(True)
        self.on_format_change()
        # Update the compression label manually
        self.update_png_compression_label(9)
        
    def load_default_settings(self):
        """Load default settings based on current format"""
        self.on_format_change()
        self.update_preview()
        
    def get_save_options(self) -> Dict[str, Any]:
        """Get save options dictionary"""
        format_ext = self.format_var.get()
        options = {
            'filename': self.filename_var.get(),
            'format': format_ext,
            'preserve_metadata': self.preserve_metadata_var.get(),
            'embed_color_profile': self.embed_profile_var.get()
        }
        
        if format_ext == 'jpg':
            options['quality'] = self.jpeg_quality_var.get()
            options['progressive'] = self.progressive_var.get()
        elif format_ext == 'png':
            options['compression'] = self.png_compression_var.get()
        elif format_ext == 'tiff':
            options['compression'] = self.tiff_compression_var.get()
            
        return options
        
    def save(self):
        """Save button clicked"""
        filename = self.filename_var.get().strip()
        
        if not filename:
            messagebox.showerror(t('error'), t('save_error_no_filename'), parent=self.dialog)
            return
            
        # Check if file exists
        if os.path.exists(filename):
            if not messagebox.askyesno(t('confirm'), t('save_confirm_overwrite'), parent=self.dialog):
                return
                
        self.result = self.get_save_options()
        self.dialog.destroy()
        
    def cancel(self):
        """Cancel button clicked"""
        self.result = None
        self.dialog.destroy()
        
    def show(self) -> Optional[Dict[str, Any]]:
        """Show dialog and return result"""
        self.dialog.wait_window()
        return self.result


def show_save_dialog(parent, initial_filename: str = "", current_format: str = "jpg") -> Optional[Dict[str, Any]]:
    """Show save dialog and return save options"""
    dialog = SaveDialog(parent, initial_filename, current_format)
    return dialog.show()
