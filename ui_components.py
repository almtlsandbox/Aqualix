"""
UI Components Module
Contains reusable UI components for the image processing application.
"""

import tkinter as tk
from tkinter import ttk
import numpy as np
from PIL import Image, ImageTk
from typing import Dict, Any, List, Callable, Union, Optional
from image_info import ImageInfoExtractor
from localization import t

class ParameterPanel(ttk.Frame):
    """Panel for adjusting processing parameters"""
    
    def __init__(self, parent, processor, update_callback: Callable):
        super().__init__(parent)
        self.processor = processor
        self.update_callback = update_callback
        self.param_widgets = {}
        self.frame_order = []  # Keep track of frame order for proper re-packing
        self.step_frames = {}  # Store collapsible step frames
        self.step_expanded = {}  # Track expanded/collapsed state
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the parameter panel UI"""
        # Title
        title_label = ttk.Label(self, text=t('parameters_title'), font=('Arial', 12, 'bold'))
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
        self.create_step_based_widgets(scrollable_frame)
        
        # Initialize parameter visibility
        self.update_parameter_visibility()
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel to canvas
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    def get_processing_steps(self):
        """Get processing steps with their parameters organized by pipeline order"""
        pipeline_order = self.processor.pipeline_order
        param_info = self.processor.get_parameter_info()
        
        steps = {}
        
        # Define step configurations
        step_configs = {
            'white_balance': {
                'title': 'Balance des blancs',
                'description': 'Correction de la température de couleur',
                'enable_param': 'white_balance_enabled',
                'method_param': 'white_balance_method',
                'parameters': [
                    'white_balance_method',
                    'gray_world_percentile', 'gray_world_max_adjustment',
                    'white_patch_percentile', 'white_patch_max_adjustment',
                    'shades_of_gray_norm', 'shades_of_gray_percentile', 'shades_of_gray_max_adjustment',
                    'grey_edge_norm', 'grey_edge_sigma', 'grey_edge_max_adjustment'
                ]
            },
            'udcp': {
                'title': 'UDCP (Underwater Dark Channel Prior)',
                'description': 'Amélioration spécialisée pour images sous-marines',
                'enable_param': 'udcp_enabled',
                'parameters': [
                    'udcp_omega', 'udcp_t0', 'udcp_window_size',
                    'udcp_guided_radius', 'udcp_guided_eps', 'udcp_enhance_contrast'
                ]
            },
            'histogram_equalization': {
                'title': 'Égalisation d\'histogramme (CLAHE)',
                'description': 'Amélioration du contraste local',
                'enable_param': 'hist_eq_enabled',
                'parameters': [
                    'hist_eq_clip_limit', 'hist_eq_tile_grid_size'
                ]
            }
        }
        
        # Build steps in pipeline order
        for step_key in pipeline_order:
            if step_key in step_configs:
                config = step_configs[step_key]
                step_params = []
                
                # Add parameters that exist in param_info
                for param_name in config['parameters']:
                    if param_name in param_info:
                        step_params.append({
                            'name': param_name,
                            'info': param_info[param_name]
                        })
                
                steps[step_key] = {
                    'title': config['title'],
                    'description': config['description'],
                    'enable_param': config['enable_param'],
                    'method_param': config.get('method_param'),
                    'parameters': step_params,
                    'order': pipeline_order.index(step_key)
                }
        
        return steps
        
    def create_step_based_widgets(self, parent):
        """Create widgets organized by processing steps"""
        steps = self.get_processing_steps()
        
        # Create widgets for each step in order
        sorted_steps = sorted(steps.items(), key=lambda x: x[1]['order'])
        
        for step_key, step_info in sorted_steps:
            self.create_step_frame(parent, step_key, step_info)
        
    def create_step_frame(self, parent, step_key, step_info):
        """Create a collapsible frame for a processing step"""
        # Main step frame
        step_frame = ttk.LabelFrame(parent, text="", padding="5")
        step_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Header frame with enable/disable and collapse/expand
        header_frame = ttk.Frame(step_frame)
        header_frame.pack(fill=tk.X, pady=(0, 5))
        
        # Step enable/disable checkbox
        enable_var = tk.BooleanVar(value=self.processor.get_parameter(step_info['enable_param']))
        enable_checkbox = ttk.Checkbutton(
            header_frame,
            text=step_info['title'],
            variable=enable_var,
            command=lambda: self.on_parameter_change(step_info['enable_param'], enable_var.get())
        )
        enable_checkbox.pack(side=tk.LEFT)
        
        # Store enable widget
        self.param_widgets[step_info['enable_param']] = enable_var
        
        # Collapse/Expand button
        self.step_expanded[step_key] = tk.BooleanVar(value=False)  # Collapsed by default
        expand_button = ttk.Button(
            header_frame,
            text="▶",
            width=3,
            command=lambda: self.toggle_step_expansion(step_key)
        )
        expand_button.pack(side=tk.RIGHT)
        
        # Description label
        desc_label = ttk.Label(step_frame, text=step_info['description'], 
                             font=('Arial', 9), foreground='gray')
        desc_label.pack(anchor='w', pady=(0, 5))
        
        # Parameters frame (collapsible)
        params_frame = ttk.Frame(step_frame)
        # Don't pack initially - will be shown/hidden by toggle_step_expansion
        
        # Create parameter widgets within this step
        for param_info in step_info['parameters']:
            self.create_single_parameter_widget(params_frame, param_info['name'], param_info['info'])
        
        # Store references
        self.step_frames[step_key] = {
            'main_frame': step_frame,
            'params_frame': params_frame,
            'expand_button': expand_button,
            'enable_checkbox': enable_checkbox
        }
        
    def create_single_parameter_widget(self, parent, param_name, info):
        """Create a single parameter widget"""
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, padx=10, pady=2)
        
        # Parameter label
        label = ttk.Label(frame, text=info['label'], font=('Arial', 9))
        label.pack(anchor='w')
        
        # Description
        if info.get('description'):
            desc_label = ttk.Label(frame, text=info['description'], 
                                 font=('Arial', 8), foreground='gray')
            desc_label.pack(anchor='w', padx=(10, 0))
        
        # Create appropriate widget based on parameter type
        widget_frame = ttk.Frame(frame)
        widget_frame.pack(fill=tk.X, padx=(10, 0), pady=2)
        
        if info['type'] == 'boolean':
            self.create_boolean_widget(widget_frame, param_name, info)
        elif info['type'] == 'float':
            self.create_float_widget(widget_frame, param_name, info)
        elif info['type'] == 'int':
            self.create_int_widget(widget_frame, param_name, info)
        elif info['type'] == 'choice':
            self.create_choice_widget(widget_frame, param_name, info)
        
        # Store frame reference for visibility control
        self.param_widgets[f"{param_name}_frame"] = frame
        self.frame_order.append((param_name, frame))
        
    def toggle_step_expansion(self, step_key):
        """Toggle the expansion state of a step"""
        is_expanded = self.step_expanded[step_key].get()
        new_state = not is_expanded
        self.step_expanded[step_key].set(new_state)
        
        # Update button text and frame visibility
        step_frame_info = self.step_frames[step_key]
        button = step_frame_info['expand_button']
        params_frame = step_frame_info['params_frame']
        
        if new_state:  # Expanding
            button.config(text="▼")
            params_frame.pack(fill=tk.X)
        else:  # Collapsing
            button.config(text="▶")
            params_frame.pack_forget()
        
    def create_parameter_widgets(self, parent):
        """Legacy method - kept for compatibility but replaced by create_step_based_widgets"""
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
            elif info['type'] == 'choice':
                self.create_choice_widget(frame, param_name, info)
            
            # Store frame reference for visibility control
            self.param_widgets[f"{param_name}_frame"] = frame
            self.frame_order.append((param_name, frame))  # Track order
                
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
    
    def create_choice_widget(self, parent, param_name: str, info: Dict[str, Any]):
        """Create a choice parameter widget (combobox)"""
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, pady=2)
        
        current_value = self.processor.get_parameter(param_name)
        choices = info.get('choices', [])
        choice_values = [choice[0] for choice in choices]
        choice_labels = [choice[1] for choice in choices]
        
        var = tk.StringVar(value=current_value)
        
        combobox = ttk.Combobox(
            frame,
            textvariable=var,
            values=choice_labels,
            state='readonly',
            width=25
        )
        combobox.pack(fill=tk.X, pady=2)
        
        # Set initial selection
        if current_value in choice_values:
            index = choice_values.index(current_value)
            combobox.set(choice_labels[index])
        
        def on_choice_change(*args):
            selected_label = var.get()
            if selected_label in choice_labels:
                index = choice_labels.index(selected_label)
                selected_value = choice_values[index]
                self.on_parameter_change(param_name, selected_value)
        
        var.trace('w', on_choice_change)
        self.param_widgets[param_name] = var
        
    def on_parameter_change(self, param_name: str, value: Any):
        """Handle parameter change"""
        self.processor.set_parameter(param_name, value)
        
        # Update parameter visibility if this is a method selection
        if param_name == 'white_balance_method':
            self.update_parameter_visibility()
        
        self.update_callback()
    
    def update_parameter_visibility(self):
        """Update visibility of parameters based on current settings"""
        param_info = self.processor.get_parameter_info()
        current_method = self.processor.get_parameter('white_balance_method')
        
        # First, forget all conditional frames to reset their packing order
        for param_name, info in param_info.items():
            if 'visible_when' in info:
                frame_key = f"{param_name}_frame"
                frame = self.param_widgets.get(frame_key)
                if frame:
                    frame.pack_forget()
        
        # Then, re-pack frames in the correct order based on visibility
        for param_name, frame in self.frame_order:
            info = param_info.get(param_name, {})
            
            if 'visible_when' in info:
                condition = info['visible_when']
                show = True
                for condition_param, condition_value in condition.items():
                    current_value = self.processor.get_parameter(condition_param)
                    if current_value != condition_value:
                        show = False
                        break
                
                if show:
                    frame.pack(fill=tk.X, padx=5, pady=2)
            else:
                # Non-conditional parameters should always be visible
                if frame.winfo_manager() == '':  # Not packed
                    frame.pack(fill=tk.X, padx=5, pady=2)
        
    def refresh_ui(self):
        """Refresh UI texts after language change"""
        # Find and update title label
        for child in self.winfo_children():
            if isinstance(child, ttk.Label):
                child.config(text=t('parameters_title'))
                break

class PipelinePanel(ttk.Frame):
    """Panel showing the processing pipeline description"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the pipeline panel UI"""
        # Title
        title_label = ttk.Label(self, text=t('pipeline_title'), font=('Arial', 12, 'bold'))
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
        
    def refresh_ui(self):
        """Refresh UI texts after language change"""
        # Find and update title label
        for child in self.winfo_children():
            if isinstance(child, ttk.Label):
                child.config(text=t('pipeline_title'))
                break

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
        title_label = ttk.Label(self, text=t('preview_title'), font=('Arial', 12, 'bold'))
        title_label.pack(pady=(0, 5))
        
        # Control panel
        controls_frame = ttk.Frame(self)
        controls_frame.pack(fill=tk.X, pady=(0, 5))
        
        # Split position slider
        ttk.Label(controls_frame, text=t('split_position') + ':').pack(side=tk.LEFT)
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
        ttk.Label(controls_frame, text=t('zoom') + ':').pack(side=tk.LEFT)
        ttk.Button(controls_frame, text="-", width=3, command=self.zoom_out).pack(side=tk.LEFT, padx=(5, 2))
        ttk.Button(controls_frame, text="+", width=3, command=self.zoom_in).pack(side=tk.LEFT, padx=(2, 10))
        
        # View control buttons
        ttk.Button(controls_frame, text=t('fit_image'), command=self.fit_to_canvas).pack(side=tk.LEFT, padx=(10, 5))
        ttk.Button(controls_frame, text=t('reset_view'), command=self.reset_view).pack(side=tk.LEFT, padx=(5, 5))
        
        # Rotation controls
        ttk.Label(controls_frame, text=t('rotation') + ':').pack(side=tk.LEFT, padx=(10, 5))
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
        self.instructions_label = ttk.Label(self, text=t('preview_instructions'), font=('Arial', 8), foreground='gray')
        self.instructions_label.pack(pady=(2, 0))
        
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
        """Reset all view parameters to 1:1 scale"""
        self.zoom_factor = 1.0
        self.pan_x = 0
        self.pan_y = 0
        self.rotation = 0.0
        self.split_var.set(0.5)
        self.split_position = 0.5
        self.update_display()
        
    def fit_to_canvas(self):
        """Fit image to canvas size"""
        if not hasattr(self, 'original_image') or self.original_image is None:
            return
            
        # Get canvas dimensions - wait for canvas to be rendered
        self.canvas.update_idletasks()
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        # If canvas is not yet rendered properly, try again later
        if canvas_width <= 1 or canvas_height <= 1:
            self.canvas.after(100, self.fit_to_canvas)
            return
            
        # Get image dimensions
        img_height, img_width = self.original_image.shape[:2]
        
        # Calculate scale factors
        scale_x = canvas_width / img_width
        scale_y = canvas_height / img_height
        
        # Use the smaller scale to fit entirely within canvas
        fit_scale = min(scale_x, scale_y) * 0.9  # 90% to leave some margin
        
        # Apply the calculated scale
        self.zoom_factor = fit_scale
        self.pan_x = 0
        self.pan_y = 0
        self.rotation = 0.0
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
        
        # Auto-fit image to canvas when loading a new image
        self.canvas.after(50, self.fit_to_canvas)  # Small delay to ensure canvas is rendered
        
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
            
    def refresh_ui(self):
        """Refresh UI texts after language change"""
        # Find and update title label
        for child in self.winfo_children():
            if isinstance(child, ttk.Label):
                child.config(text=t('preview_title'))
                break
                
        # Update controls frame texts
        for child in self.winfo_children():
            if isinstance(child, ttk.Frame) and len(child.winfo_children()) > 5:  # Controls frame
                for control_child in child.winfo_children():
                    if isinstance(control_child, ttk.Label):
                        text = control_child.cget('text')
                        if 'Position' in text or 'position' in text:
                            control_child.config(text=t('split_position') + ':')
                        elif 'Zoom' in text or 'zoom' in text:
                            control_child.config(text=t('zoom') + ':')
                        elif 'Rotation' in text or 'rotation' in text:
                            control_child.config(text=t('rotation') + ':')
                    elif isinstance(control_child, ttk.Button):
                        text = control_child.cget('text')
                        if 'Fit' in text or 'Ajuster' in text:
                            control_child.config(text=t('fit_image'))
                        elif 'Reset' in text or 'Réinitialiser' in text or '1:1' in text:
                            control_child.config(text=t('reset_view'))
                break
                
        # Update instructions
        if hasattr(self, 'instructions_label'):
            self.instructions_label.config(text=t('preview_instructions'))

class ImageInfoPanel(ttk.Frame):
    """Panel showing detailed image information"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.info_extractor = ImageInfoExtractor()
        self.current_info = {}
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the image info panel UI"""
        # Title
        title_label = ttk.Label(self, text=t('info_title'), font=('Arial', 12, 'bold'))
        title_label.pack(pady=(0, 5))
        
        # Notebook for different info categories
        self.info_notebook = ttk.Notebook(self)
        self.info_notebook.pack(fill=tk.BOTH, expand=True)
        
        # File info tab
        self.file_frame = ttk.Frame(self.info_notebook)
        self.info_notebook.add(self.file_frame, text=t('info_tab_file'))
        self.setup_file_info_tab()
        
        # Properties tab
        self.props_frame = ttk.Frame(self.info_notebook)
        self.info_notebook.add(self.props_frame, text=t('info_tab_properties'))
        self.setup_properties_tab()
        
        # Analysis tab
        self.analysis_frame = ttk.Frame(self.info_notebook)
        self.info_notebook.add(self.analysis_frame, text=t('info_tab_analysis'))
        self.setup_analysis_tab()
        
        # EXIF tab (for images)
        self.exif_frame = ttk.Frame(self.info_notebook)
        self.info_notebook.add(self.exif_frame, text=t('info_tab_exif'))
        self.setup_exif_tab()
        
    def setup_file_info_tab(self):
        """Setup file information display"""
        # Scrollable frame
        canvas = tk.Canvas(self.file_frame)
        scrollbar = ttk.Scrollbar(self.file_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        self.file_info_frame = scrollable_frame
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def setup_properties_tab(self):
        """Setup properties display"""
        # Scrollable frame
        canvas = tk.Canvas(self.props_frame)
        scrollbar = ttk.Scrollbar(self.props_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        self.properties_info_frame = scrollable_frame
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def setup_analysis_tab(self):
        """Setup color analysis display"""
        # Scrollable frame
        canvas = tk.Canvas(self.analysis_frame)
        scrollbar = ttk.Scrollbar(self.analysis_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        self.analysis_info_frame = scrollable_frame
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def setup_exif_tab(self):
        """Setup EXIF data display"""
        # Scrollable text widget
        frame = ttk.Frame(self.exif_frame)
        frame.pack(fill=tk.BOTH, expand=True)
        
        self.exif_text = tk.Text(
            frame,
            wrap=tk.WORD,
            font=('Consolas', 9),
            state=tk.DISABLED
        )
        
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.exif_text.yview)
        self.exif_text.configure(yscrollcommand=scrollbar.set)
        
        self.exif_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def update_info(self, file_path, image_array=None, is_video=False):
        """Update the information display"""
        try:
            if is_video:
                self.current_info = self.info_extractor.get_video_info(file_path)
                # Hide EXIF tab for videos
                self.info_notebook.tab(3, state='hidden')
            else:
                self.current_info = self.info_extractor.get_image_info(file_path, image_array)
                # Show EXIF tab for images
                self.info_notebook.tab(3, state='normal')
                
            self.display_file_info()
            self.display_properties_info()
            self.display_analysis_info()
            if not is_video:
                self.display_exif_info()
                
        except Exception as e:
            self.display_error(str(e))
            
    def display_file_info(self):
        """Display file information"""
        # Clear previous content
        for widget in self.file_info_frame.winfo_children():
            widget.destroy()
            
        if 'file' not in self.current_info:
            return
            
        file_info = self.current_info['file']
        
        info_items = [
            ("Nom", file_info.get('name', 'N/A')),
            ("Chemin", file_info.get('path', 'N/A')),
            ("Taille", file_info.get('size', 'N/A')),
            ("Modifié", file_info.get('modified', 'N/A')),
            ("Créé", file_info.get('created', 'N/A')),
            ("Extension", file_info.get('extension', 'N/A')),
            ("Hash MD5", file_info.get('hash_md5', 'N/A'))
        ]
        
        for i, (label, value) in enumerate(info_items):
            frame = ttk.Frame(self.file_info_frame)
            frame.pack(fill=tk.X, padx=5, pady=2)
            
            ttk.Label(frame, text=f"{label}:", font=('Arial', 9, 'bold')).pack(side=tk.LEFT)
            ttk.Label(frame, text=str(value), font=('Arial', 9)).pack(side=tk.LEFT, padx=(10, 0))
            
    def display_properties_info(self):
        """Display properties information"""
        # Clear previous content
        for widget in self.properties_info_frame.winfo_children():
            widget.destroy()
            
        if 'properties' not in self.current_info:
            return
            
        props = self.current_info['properties']
        
        # Different properties for images vs videos
        if 'fps' in props:  # Video properties
            info_items = [
                ("Largeur", f"{props.get('width', 'N/A')} px"),
                ("Hauteur", f"{props.get('height', 'N/A')} px"),
                ("Ratio d'aspect", str(props.get('aspect_ratio', 'N/A'))),
                ("FPS", str(props.get('fps', 'N/A'))),
                ("Frames totales", str(props.get('total_frames', 'N/A'))),
                ("Durée", str(props.get('duration', 'N/A'))),
                ("Codec", str(props.get('fourcc', 'N/A')))
            ]
        else:  # Image properties
            info_items = [
                ("Largeur", f"{props.get('width', 'N/A')} px"),
                ("Hauteur", f"{props.get('height', 'N/A')} px"),
                ("Canaux", str(props.get('channels', 'N/A'))),
                ("Pixels totaux", f"{props.get('total_pixels', 0):,}" if isinstance(props.get('total_pixels'), int) and props.get('total_pixels') else 'N/A'),
                ("Ratio d'aspect", str(props.get('aspect_ratio', 'N/A'))),
                ("Format", str(props.get('format', 'N/A'))),
                ("Mode", str(props.get('mode', 'N/A'))),
                ("Transparence", "Oui" if props.get('has_transparency') else "Non"),
                ("Type de données", str(props.get('dtype', 'N/A'))),
                ("Valeur min", str(props.get('min_value', 'N/A'))),
                ("Valeur max", str(props.get('max_value', 'N/A'))),
                ("Valeur moyenne", str(props.get('mean_value', 'N/A')))
            ]
            
        for i, (label, value) in enumerate(info_items):
            frame = ttk.Frame(self.properties_info_frame)
            frame.pack(fill=tk.X, padx=5, pady=2)
            
            ttk.Label(frame, text=f"{label}:", font=('Arial', 9, 'bold')).pack(side=tk.LEFT)
            ttk.Label(frame, text=str(value), font=('Arial', 9)).pack(side=tk.LEFT, padx=(10, 0))
            
    def display_analysis_info(self):
        """Display color analysis information"""
        # Clear previous content
        for widget in self.analysis_info_frame.winfo_children():
            widget.destroy()
            
        if 'color_analysis' not in self.current_info:
            ttk.Label(self.analysis_info_frame, text="Aucune analyse de couleur disponible").pack(pady=20)
            return
            
        analysis = self.current_info['color_analysis']
        
        info_items = []
        if 'red_mean' in analysis:  # RGB analysis
            info_items = [
                ("Moyenne Rouge", str(analysis.get('red_mean', 'N/A'))),
                ("Moyenne Vert", str(analysis.get('green_mean', 'N/A'))),
                ("Moyenne Bleu", str(analysis.get('blue_mean', 'N/A'))),
                ("Écart-type Rouge", str(analysis.get('red_std', 'N/A'))),
                ("Écart-type Vert", str(analysis.get('green_std', 'N/A'))),
                ("Écart-type Bleu", str(analysis.get('blue_std', 'N/A'))),
                ("Luminosité", str(analysis.get('brightness', 'N/A'))),
                ("Contraste", str(analysis.get('contrast', 'N/A'))),
                ("Temp. couleur estimée", f"{analysis.get('estimated_color_temp', 'N/A')} K"),
                ("Couleurs uniques", f"{analysis.get('unique_colors', 0):,}" if isinstance(analysis.get('unique_colors'), int) and analysis.get('unique_colors') else 'N/A')
            ]
        else:  # Grayscale analysis
            info_items = [
                ("Luminosité", str(analysis.get('brightness', 'N/A'))),
                ("Contraste", str(analysis.get('contrast', 'N/A'))),
                ("Intensité min", str(analysis.get('min_intensity', 'N/A'))),
                ("Intensité max", str(analysis.get('max_intensity', 'N/A')))
            ]
            
        for i, (label, value) in enumerate(info_items):
            frame = ttk.Frame(self.analysis_info_frame)
            frame.pack(fill=tk.X, padx=5, pady=2)
            
            ttk.Label(frame, text=f"{label}:", font=('Arial', 9, 'bold')).pack(side=tk.LEFT)
            ttk.Label(frame, text=str(value), font=('Arial', 9)).pack(side=tk.LEFT, padx=(10, 0))
            
    def display_exif_info(self):
        """Display EXIF information"""
        self.exif_text.config(state=tk.NORMAL)
        self.exif_text.delete(1.0, tk.END)
        
        if 'exif' not in self.current_info or not self.current_info['exif']:
            self.exif_text.insert(tk.END, "Aucune donnée EXIF trouvée")
        else:
            exif_data = self.current_info['exif']
            for key, value in sorted(exif_data.items()):
                self.exif_text.insert(tk.END, f"{key}: {value}\n")
                
        self.exif_text.config(state=tk.DISABLED)
        
    def display_error(self, error_message):
        """Display error message"""
        for frame in [self.file_info_frame, self.properties_info_frame, self.analysis_info_frame]:
            for widget in frame.winfo_children():
                widget.destroy()
            ttk.Label(frame, text=f"Erreur: {error_message}", foreground='red').pack(pady=20)
            
        self.exif_text.config(state=tk.NORMAL)
        self.exif_text.delete(1.0, tk.END)
        self.exif_text.insert(tk.END, f"Erreur: {error_message}")
        self.exif_text.config(state=tk.DISABLED)
        
    def refresh_ui(self):
        """Refresh UI texts after language change"""
        # Find and update title label
        for child in self.winfo_children():
            if isinstance(child, ttk.Label):
                child.config(text=t('info_title'))
                break
        
        # Update tab names
        if hasattr(self, 'info_notebook'):
            self.info_notebook.tab(0, text=t('info_tab_file'))
            self.info_notebook.tab(1, text=t('info_tab_properties'))
            self.info_notebook.tab(2, text=t('info_tab_analysis'))
            self.info_notebook.tab(3, text=t('info_tab_exif'))
