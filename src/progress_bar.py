"""
Progress Bar Component for Aqualix
Non-invasive progress indication for long-running operations
"""

import tkinter as tk
from tkinter import ttk
import threading
import time
from typing import Optional, Callable, Any
from contextlib import contextmanager

class ProgressDialog:
    """
    Modal progress dialog with indeterminate progress bar
    Thread-safe and non-blocking for the main operation
    """
    
    def __init__(self, parent: tk.Tk, title: str = "Processing", message: str = "Please wait..."):
        self.parent = parent
        self.title = title
        self.message = message
        self.dialog = None
        self.progress_bar = None
        self.message_label = None
        self.cancelled = False
        self.lock = threading.Lock()
        
    def show(self):
        """Show the progress dialog"""
        if self.dialog is not None:
            return  # Already showing
            
        # Create modal dialog
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title(self.title)
        self.dialog.geometry("350x120")
        self.dialog.resizable(False, False)
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (self.dialog.winfo_width() // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (self.dialog.winfo_height() // 2)
        self.dialog.geometry(f"+{x}+{y}")
        
        # Create content
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Message label
        self.message_label = ttk.Label(main_frame, text=self.message, font=("Arial", 10))
        self.message_label.pack(pady=(0, 15))
        
        # Progress bar - using determinate mode for real progress
        self.progress_bar = ttk.Progressbar(
            main_frame, 
            mode='determinate', 
            length=280,
            style="Custom.Horizontal.TProgressbar",
            maximum=100
        )
        self.progress_bar.pack(pady=(0, 10))
        
        # Initialize at 0%
        self.progress_bar['value'] = 0
        
        # Cancel button (optional)
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        # Update the dialog to make it visible
        self.dialog.update()
        
    def update_message(self, new_message: str):
        """Update the progress message"""
        with self.lock:
            if self.message_label and self.dialog:
                self.message_label.config(text=new_message)
                self.dialog.update()
                
    def update_progress(self, percentage: float):
        """Update the progress bar percentage (0-100)"""
        with self.lock:
            if self.progress_bar and self.dialog:
                # Clamp percentage between 0 and 100
                percentage = max(0, min(100, percentage))
                self.progress_bar['value'] = percentage
                self.dialog.update()
                
    def update_message_and_progress(self, message: str, percentage: float):
        """Update both message and progress at once"""
        with self.lock:
            if self.dialog:
                if self.message_label:
                    self.message_label.config(text=message)
                if self.progress_bar:
                    percentage = max(0, min(100, percentage))
                    self.progress_bar['value'] = percentage
                self.dialog.update()
                
    def hide(self):
        """Hide the progress dialog immediately"""
        with self.lock:
            if self.dialog:
                try:
                    if self.progress_bar:
                        # No need to stop() for determinate mode
                        pass
                    self.dialog.grab_release()
                    # Force immediate destruction and update
                    self.dialog.destroy()
                    self.parent.update_idletasks()  # Force UI update
                    self.parent.update()  # Process all pending events
                except:
                    pass  # Dialog might have been destroyed already
                finally:
                    self.dialog = None
                    self.progress_bar = None
                    self.message_label = None

class ProgressManager:
    """
    Context manager for easy progress dialog usage
    Ensures proper cleanup even if exceptions occur
    """
    
    def __init__(self, parent: tk.Tk, title: str, message: str = "Processing..."):
        self.parent = parent
        self.title = title
        self.message = message
        self.dialog = None
        
    def __enter__(self):
        self.dialog = ProgressDialog(self.parent, self.title, self.message)
        self.dialog.show()
        return self.dialog
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.dialog:
            self.dialog.hide()
            
@contextmanager
def show_progress(parent: tk.Tk, title: str, message: str = "Processing..."):
    """
    Convenient context manager for showing progress
    
    Usage:
        with show_progress(self.root, "Loading Image", "Please wait...") as progress:
            # Long running operation
            time.sleep(2)
            progress.update_message("Almost done...")
            time.sleep(1)
    """
    progress_manager = ProgressManager(parent, title, message)
    with progress_manager as dialog:
        yield dialog

class InlineProgressBar:
    """
    Inline progress bar that can be embedded in existing UI
    For less intrusive progress indication
    """
    
    def __init__(self, parent_frame: ttk.Frame):
        self.parent_frame = parent_frame
        self.progress_frame = None
        self.progress_bar = None
        self.label = None
        self.visible = False
        
    def show(self, message: str = "Processing..."):
        """Show inline progress bar"""
        if self.visible:
            self.update_message(message)
            return
            
        self.progress_frame = ttk.Frame(self.parent_frame)
        self.progress_frame.pack(fill=tk.X, pady=5)
        
        self.label = ttk.Label(self.progress_frame, text=message, font=("Arial", 9))
        self.label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            mode='indeterminate',
            length=200
        )
        self.progress_bar.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.progress_bar.start(15)
        
        self.visible = True
        self.parent_frame.update()
        
    def update_message(self, message: str):
        """Update progress message"""
        if self.label:
            self.label.config(text=message)
            self.parent_frame.update()
            
    def hide(self):
        """Hide inline progress bar"""
        if self.progress_frame:
            if self.progress_bar:
                self.progress_bar.stop()
            self.progress_frame.destroy()
            self.progress_frame = None
            self.progress_bar = None
            self.label = None
            self.visible = False

def delayed_operation(operation: Callable[[], Any], delay_threshold: float = 0.5) -> Callable[[], Any]:
    """
    Decorator to add automatic progress indication for operations that might take time
    Only shows progress if operation takes longer than delay_threshold seconds
    """
    def wrapper(*args, **kwargs):
        start_time = time.time()
        
        # Start operation in thread to measure time
        result = None
        exception = None
        
        def run_operation():
            nonlocal result, exception
            try:
                result = operation(*args, **kwargs)
            except Exception as e:
                exception = e
                
        # Quick check - if operation completes fast, don't show progress
        thread = threading.Thread(target=run_operation)
        thread.start()
        thread.join(timeout=delay_threshold)
        
        if thread.is_alive():
            # Operation is taking time, it probably already has its own progress
            thread.join()
            
        if exception:
            raise exception
        return result
    
    return wrapper

# Convenience functions for common patterns
def with_progress_dialog(parent, title, message="Processing..."):
    """Decorator for methods that should show progress dialog"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            with show_progress(parent, title, message) as progress:
                return func(*args, **kwargs)
        return wrapper
    return decorator

class ProgressStyle:
    """Configure custom progress bar styles"""
    
    @staticmethod
    def setup_styles():
        """Setup custom ttk styles for progress bars"""
        style = ttk.Style()
        
        # Custom style for main progress bars
        style.configure(
            "Custom.Horizontal.TProgressbar",
            troughcolor="#E0E0E0",
            borderwidth=1,
            lightcolor="#4CAF50",
            darkcolor="#2E7D32"
        )
        
        # Style for inline progress bars
        style.configure(
            "Inline.Horizontal.TProgressbar", 
            troughcolor="#F5F5F5",
            borderwidth=0,
            lightcolor="#2196F3",
            darkcolor="#1976D2"
        )

# Initialize styles when module is imported
try:
    ProgressStyle.setup_styles()
except:
    pass  # Might fail if no Tk root exists yet
