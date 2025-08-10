"""
UI Components Module
Contains reusable UI components for the image processing application.
"""

import tkinter as tk
from tkinter import ttk
import numpy as np
from PIL import Image, ImageTk
from typing import Dict, Any, List, Callable, Union, Optional

class ParameterPanel(ttk.Frame):
    """Panel for adjusting processing parameters"""
    
    def __init__(self, parent, processor, update_callback: Callable):
        super().__init__(parent)
        self.processor = processor
        self.update_callback = update_callback
        self.param_widgets = {}
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the parameter panel UI"""
        # Title
        title_label = ttk.Label(self, text="Paramètres de traitement", font=('Arial', 12, 'bold'))
        title_label.pack(pady=(0, 10))
        
        # Scrollable frame for parameters
        canvas = tk.Canvas(self, height=500)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Create parameter widgets
        self.create_parameter_widgets(scrollable_frame)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel to canvas
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
    def create_parameter_widgets(self, parent):
        """Create widgets for all parameters"""
        param_info = self.processor.get_parameter_info()
        
        for param_name, info in param_info.items():
            frame = ttk.LabelFrame(parent, text=info['label'], padding="5")
            frame.pack(fill=tk.X, padx=5, pady=2)
            
            # Description
            desc_label = ttk.Label(frame, text=info['description'], 
                                 font=('Arial', 8), foreground='gray')
            desc_label.pack(anchor='w')
            
            # Create appropriate widget based on parameter type
            if info['type'] == 'boolean':
                self.create_boolean_widget(frame, param_name, info)
            elif info['type'] == 'float':
                self.create_float_widget(frame, param_name, info)
            elif info['type'] == 'int':
                self.create_int_widget(frame, param_name, info)
                
    def create_boolean_widget(self, parent, param_name: str, info: Dict[str, Any]):
        """Create a boolean parameter widget"""
        var = tk.BooleanVar(value=self.processor.get_parameter(param_name))
        
        checkbox = ttk.Checkbutton(
            parent, 
            text="Activé",
            variable=var,
            command=lambda: self.on_parameter_change(param_name, var.get())
        )
        checkbox.pack(anchor='w', pady=2)
        
        self.param_widgets[param_name] = var
        
    def create_float_widget(self, parent, param_name: str, info: Dict[str, Any]):
        """Create a float parameter widget"""
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, pady=2)
        
        var = tk.DoubleVar(value=self.processor.get_parameter(param_name))
        
        # Scale widget
        scale = ttk.Scale(
            frame,
            from_=info['min'],
            to=info['max'],
            variable=var,
            orient=tk.HORIZONTAL,
            command=lambda val: self.on_parameter_change(param_name, float(val))
        )
        scale.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Value label
        value_label = ttk.Label(frame, text=f"{var.get():.2f}")
        value_label.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Update label when value changes
        def update_label(*args):
            value_label.config(text=f"{var.get():.2f}")
        var.trace('w', update_label)
        
        self.param_widgets[param_name] = var
        
    def create_int_widget(self, parent, param_name: str, info: Dict[str, Any]):
        """Create an integer parameter widget"""
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, pady=2)
        
        var = tk.IntVar(value=self.processor.get_parameter(param_name))
        
        # Scale widget
        scale = ttk.Scale(
            frame,
            from_=info['min'],
            to=info['max'],
            variable=var,
            orient=tk.HORIZONTAL,
            command=lambda val: self.on_parameter_change(param_name, int(float(val)))
        )
        scale.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Value label
        value_label = ttk.Label(frame, text=str(var.get()))
        value_label.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Update label when value changes
        def update_label(*args):
            value_label.config(text=str(var.get()))
        var.trace('w', update_label)
        
        self.param_widgets[param_name] = var
        
    def on_parameter_change(self, param_name: str, value: Any):
        """Handle parameter change"""
        self.processor.set_parameter(param_name, value)
        self.update_callback()

class PipelinePanel(ttk.Frame):
    """Panel showing the processing pipeline description"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the pipeline panel UI"""
        # Title
        title_label = ttk.Label(self, text="Pipeline des opérations", font=('Arial', 12, 'bold'))
        title_label.pack(pady=(0, 5))
        
        # Scrollable text widget
        frame = ttk.Frame(self)
        frame.pack(fill=tk.BOTH, expand=True)
        
        self.text_widget = tk.Text(
            frame, 
            height=20, 
            width=50, 
            wrap=tk.WORD,
            font=('Arial', 9),
            state=tk.DISABLED
        )
        
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.text_widget.yview)
        self.text_widget.configure(yscrollcommand=scrollbar.set)
        
        self.text_widget.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def update_pipeline(self, pipeline_steps: List[Dict[str, str]]):
        """Update the pipeline description"""
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.delete(1.0, tk.END)
        
        for i, step in enumerate(pipeline_steps, 1):
            self.text_widget.insert(tk.END, f"{i}. {step['name']}\n", "title")
            self.text_widget.insert(tk.END, f"{step['description']}\n\n", "description")
            self.text_widget.insert(tk.END, f"Parameters: {step['parameters']}\n", "parameters")
            if i < len(pipeline_steps):
                self.text_widget.insert(tk.END, "↓\n", "arrow")
                
        # Configure tags for formatting
        self.text_widget.tag_config("title", font=('Arial', 10, 'bold'))
        self.text_widget.tag_config("description", font=('Arial', 9))
        self.text_widget.tag_config("parameters", font=('Arial', 8, 'italic'))
        self.text_widget.tag_config("arrow", font=('Arial', 12), justify='center')
        
        self.text_widget.config(state=tk.DISABLED)

class InteractivePreviewPanel(ttk.Frame):
    """Interactive split view panel with zoom, pan, rotate, and moveable divider"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.original_image = None
        self.processed_image = None
        
        # View state
        self.zoom_factor = 1.0
        self.pan_x = 0
        self.pan_y = 0
        self.rotation = 0.0
        self.split_position = 0.5  # 0.0 = all original, 1.0 = all processed
        
        # Mouse interaction state
        self.last_mouse_x = 0
        self.last_mouse_y = 0
        self.panning = False
        self.dragging_divider = False
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the interactive preview panel UI"""
        # Title
        title_label = ttk.Label(self, text="Vue comparative interactive", font=('Arial', 12, 'bold'))
        title_label.pack(pady=(0, 5))
        
        # Control panel
        controls_frame = ttk.Frame(self)
        controls_frame.pack(fill=tk.X, pady=(0, 5))
        
        # Split position slider
        ttk.Label(controls_frame, text="Division:").pack(side=tk.LEFT)
        self.split_var = tk.DoubleVar(value=0.5)
        self.split_slider = ttk.Scale(
            controls_frame,
            from_=0.0,
            to=1.0,
            variable=self.split_var,
            orient=tk.HORIZONTAL,
            command=self.on_split_change
        )
        self.split_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 10))
        
        # Zoom controls
        ttk.Label(controls_frame, text="Zoom:").pack(side=tk.LEFT)
        ttk.Button(controls_frame, text="-", width=3, command=self.zoom_out).pack(side=tk.LEFT, padx=(5, 2))
        ttk.Button(controls_frame, text="+", width=3, command=self.zoom_in).pack(side=tk.LEFT, padx=(2, 10))
        
        # Reset button
        ttk.Button(controls_frame, text="Réinitialiser", command=self.reset_view).pack(side=tk.LEFT, padx=(10, 5))
        
        # Rotation controls
        ttk.Label(controls_frame, text="Rotation:").pack(side=tk.LEFT, padx=(10, 5))
        ttk.Button(controls_frame, text="↺", width=3, command=self.rotate_left).pack(side=tk.LEFT, padx=(2, 2))
        ttk.Button(controls_frame, text="↻", width=3, command=self.rotate_right).pack(side=tk.LEFT, padx=(2, 5))
        
        # Canvas for interactive image display
        self.canvas_frame = ttk.Frame(self, relief=tk.SUNKEN, borderwidth=1)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(self.canvas_frame, bg='gray20')
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Bind mouse events
        self.canvas.bind("<Button-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)
        self.canvas.bind("<MouseWheel>", self.on_mouse_wheel)
        self.canvas.bind("<Configure>", self.on_canvas_resize)
        
        # Instructions
        instructions = "Contrôles: Clic gauche + glisser pour déplacer • Molette pour zoomer • Glisser la ligne de division"
        ttk.Label(self, text=instructions, font=('Arial', 8), foreground='gray').pack(pady=(2, 0))
        
    def on_split_change(self, value):
        """Handle split slider change"""
        self.split_position = float(value)
        self.update_display()
        
    def zoom_in(self):
        """Zoom in by 25%"""
        self.zoom_factor *= 1.25
        self.update_display()
        
    def zoom_out(self):
        """Zoom out by 25%"""
        self.zoom_factor /= 1.25
        if self.zoom_factor < 0.1:
            self.zoom_factor = 0.1
        self.update_display()
        
    def rotate_left(self):
        """Rotate image 90 degrees counter-clockwise"""
        self.rotation -= 90
        self.rotation = self.rotation % 360
        self.update_display()
        
    def rotate_right(self):
        """Rotate image 90 degrees clockwise"""
        self.rotation += 90
        self.rotation = self.rotation % 360
        self.update_display()
        
    def reset_view(self):
        """Reset all view parameters"""
        self.zoom_factor = 1.0
        self.pan_x = 0
        self.pan_y = 0
        self.rotation = 0.0
        self.split_var.set(0.5)
        self.split_position = 0.5
        self.update_display()
        
    def on_mouse_down(self, event):
        """Handle mouse button press"""
        self.last_mouse_x = event.x
        self.last_mouse_y = event.y
        
        # Check if clicking near the split line
        canvas_width = self.canvas.winfo_width()
        split_x = canvas_width * self.split_position
        
        if abs(event.x - split_x) < 10:  # Within 10 pixels of split line
            self.dragging_divider = True
            self.canvas.configure(cursor="sb_h_double_arrow")
        else:
            self.panning = True
            self.canvas.configure(cursor="fleur")
            
    def on_mouse_drag(self, event):
        """Handle mouse drag"""
        dx = event.x - self.last_mouse_x
        dy = event.y - self.last_mouse_y
        
        if self.dragging_divider:
            # Update split position
            canvas_width = self.canvas.winfo_width()
            new_split = event.x / canvas_width
            new_split = max(0.0, min(1.0, new_split))  # Clamp between 0 and 1
            self.split_var.set(new_split)
            self.split_position = new_split
            self.update_display()
        elif self.panning:
            # Update pan position
            self.pan_x += dx
            self.pan_y += dy
            self.update_display()
            
        self.last_mouse_x = event.x
        self.last_mouse_y = event.y
        
    def on_mouse_up(self, event):
        """Handle mouse button release"""
        self.panning = False
        self.dragging_divider = False
        self.canvas.configure(cursor="")
        
    def on_mouse_wheel(self, event):
        """Handle mouse wheel for zooming"""
        # Get mouse position relative to canvas
        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)
        
        # Zoom factor
        zoom_delta = 1.1 if event.delta > 0 else 1/1.1
        old_zoom = self.zoom_factor
        self.zoom_factor *= zoom_delta
        
        # Limit zoom
        if self.zoom_factor < 0.1:
            self.zoom_factor = 0.1
        elif self.zoom_factor > 10.0:
            self.zoom_factor = 10.0
            
        # Adjust pan to zoom towards mouse position
        zoom_ratio = self.zoom_factor / old_zoom
        self.pan_x = canvas_x - (canvas_x - self.pan_x) * zoom_ratio
        self.pan_y = canvas_y - (canvas_y - self.pan_y) * zoom_ratio
        
        self.update_display()
        
    def on_canvas_resize(self, event):
        """Handle canvas resize"""
        self.update_display()
        
    def apply_transform(self, image_array):
        """Apply zoom, pan, and rotation to image"""
        if image_array is None:
            return None
            
        # Convert to PIL Image
        pil_image = Image.fromarray(image_array)
        
        # Apply rotation if needed
        if self.rotation != 0:
            pil_image = pil_image.rotate(self.rotation, expand=True, fillcolor=(128, 128, 128))
            
        # Apply zoom
        if self.zoom_factor != 1.0:
            new_width = int(pil_image.width * self.zoom_factor)
            new_height = int(pil_image.height * self.zoom_factor)
            pil_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
        return pil_image
        
    def update_images(self, original: np.ndarray, processed: np.ndarray):
        """Update the displayed images"""
        self.original_image = original
        self.processed_image = processed
        self.update_display()
        
    def update_display(self):
        """Update the interactive split view display"""
        if self.original_image is None or self.processed_image is None:
            self.canvas.delete("all")
            self.canvas.create_text(
                self.canvas.winfo_width() // 2,
                self.canvas.winfo_height() // 2,
                text="Aucune image chargée",
                fill="white",
                font=('Arial', 14)
            )
            return
            
        try:
            # Get canvas dimensions
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            
            if canvas_width <= 1 or canvas_height <= 1:
                return  # Canvas not ready yet
                
            # Apply transforms to both images
            original_transformed = self.apply_transform(self.original_image)
            processed_transformed = self.apply_transform(self.processed_image)
            
            if original_transformed is None or processed_transformed is None:
                return
                
            # Calculate display position with pan offset
            img_x = canvas_width // 2 + self.pan_x - original_transformed.width // 2
            img_y = canvas_height // 2 + self.pan_y - original_transformed.height // 2
            
            # Clear canvas
            self.canvas.delete("all")
            
            # Calculate split position
            split_x = canvas_width * self.split_position
            
            # Create composite image for split view
            composite = Image.new('RGB', (canvas_width, canvas_height), (64, 64, 64))
            
            # Paste original image (left side)
            if img_x < split_x:
                # Calculate crop area for original image
                crop_width = min(original_transformed.width, int(split_x - img_x))
                if crop_width > 0:
                    cropped_original = original_transformed.crop((0, 0, crop_width, original_transformed.height))
                    paste_x = max(0, int(img_x))
                    paste_y = max(0, int(img_y))
                    
                    # Adjust crop if image starts before canvas
                    if img_x < 0:
                        crop_left = int(-img_x)
                        if crop_left < cropped_original.width:
                            cropped_original = cropped_original.crop((crop_left, 0, cropped_original.width, cropped_original.height))
                            paste_x = 0
                            
                    # Adjust crop if image extends beyond canvas
                    if paste_y < 0:
                        crop_top = int(-img_y)
                        if crop_top < cropped_original.height:
                            cropped_original = cropped_original.crop((0, crop_top, cropped_original.width, cropped_original.height))
                            paste_y = 0
                            
                    if paste_x < canvas_width and paste_y < canvas_height:
                        composite.paste(cropped_original, (paste_x, paste_y))
            
            # Paste processed image (right side)
            if img_x + processed_transformed.width > split_x:
                # Calculate crop area for processed image
                crop_left = max(0, int(split_x - img_x))
                crop_width = processed_transformed.width - crop_left
                
                if crop_width > 0 and crop_left < processed_transformed.width:
                    cropped_processed = processed_transformed.crop((crop_left, 0, processed_transformed.width, processed_transformed.height))
                    paste_x = max(0, int(split_x))
                    paste_y = max(0, int(img_y))
                    
                    # Adjust crop if image extends beyond canvas
                    if paste_y < 0:
                        crop_top = int(-img_y)
                        if crop_top < cropped_processed.height:
                            cropped_processed = cropped_processed.crop((0, crop_top, cropped_processed.width, cropped_processed.height))
                            paste_y = 0
                            
                    if paste_x < canvas_width and paste_y < canvas_height:
                        composite.paste(cropped_processed, (paste_x, paste_y))
            
            # Convert to PhotoImage and display
            self.photo = ImageTk.PhotoImage(composite)
            self.canvas.create_image(0, 0, anchor="nw", image=self.photo)
            
            # Draw split line
            self.canvas.create_line(split_x, 0, split_x, canvas_height, fill="white", width=2, tags="split_line")
            self.canvas.create_line(split_x-1, 0, split_x-1, canvas_height, fill="black", width=1, tags="split_line")
            self.canvas.create_line(split_x+1, 0, split_x+1, canvas_height, fill="black", width=1, tags="split_line")
            
            # Add labels
            label_y = 20
            self.canvas.create_text(split_x // 2, label_y, text="ORIGINAL", fill="white", font=('Arial', 12, 'bold'), tags="labels")
            self.canvas.create_text(split_x + (canvas_width - split_x) // 2, label_y, text="TRAITÉ", fill="white", font=('Arial', 12, 'bold'), tags="labels")
            
            # Add zoom info
            zoom_text = f"Zoom: {self.zoom_factor:.1f}x"
            if self.rotation != 0:
                zoom_text += f" | Rotation: {self.rotation}°"
            self.canvas.create_text(10, canvas_height - 10, anchor="sw", text=zoom_text, fill="white", font=('Arial', 10), tags="info")
            
        except Exception as e:
            print(f"Error updating display: {e}")
            # Get canvas dimensions for error display
            canvas_width = self.canvas.winfo_width() or 400
            canvas_height = self.canvas.winfo_height() or 300
            
            self.canvas.delete("all")
            self.canvas.create_text(
                canvas_width // 2,
                canvas_height // 2,
                text=f"Display error: {str(e)}",
                fill="red",
                font=('Arial', 10)
            )
