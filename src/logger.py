"""
Logging Module for Aqualix
Handles application logging and file output.
"""

import logging
import os
from datetime import datetime
from pathlib import Path

class AqualixLogger:
    def __init__(self, log_dir="logs", log_level=logging.INFO):
        """Initialize the logger with specified directory and level"""
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Create log filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = self.log_dir / f"aqualix_{timestamp}.log"
        
        # Configure logging
        self.setup_logger(log_level)
        
    def setup_logger(self, log_level):
        """Setup the logger with file and console handlers"""
        # Create logger
        self.logger = logging.getLogger('aqualix')
        self.logger.setLevel(log_level)
        
        # Remove existing handlers to avoid duplicates
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)
            
        # Create formatters
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
        )
        console_formatter = logging.Formatter(
            '%(levelname)s - %(message)s'
        )
        
        # File handler
        file_handler = logging.FileHandler(self.log_file, encoding='utf-8')
        file_handler.setLevel(log_level)
        file_handler.setFormatter(file_formatter)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)  # Only warnings and errors to console
        console_handler.setFormatter(console_formatter)
        
        # Add handlers to logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
    def info(self, message):
        """Log info message"""
        self.logger.info(message)
        
    def warning(self, message):
        """Log warning message"""
        self.logger.warning(message)
        
    def error(self, message):
        """Log error message"""
        self.logger.error(message)
        
    def debug(self, message):
        """Log debug message"""
        self.logger.debug(message)
        
    def log_image_processing(self, image_path, operations, processing_time):
        """Log image processing details"""
        self.info(f"Image processed: {image_path}")
        self.info(f"Operations applied: {', '.join(operations)}")
        self.info(f"Processing time: {processing_time:.3f}s")
        
    def log_video_processing(self, video_path, total_frames, processing_time):
        """Log video processing details"""
        self.info(f"Video processed: {video_path}")
        self.info(f"Total frames: {total_frames}")
        self.info(f"Processing time: {processing_time:.3f}s")
        
    def log_parameter_change(self, parameter, old_value, new_value):
        """Log parameter changes"""
        self.info(f"Parameter changed: {parameter} from {old_value} to {new_value}")
        
    def log_file_operation(self, operation, file_path, success=True):
        """Log file operations"""
        status = "SUCCESS" if success else "FAILED"
        self.info(f"File {operation}: {file_path} - {status}")
        
    def get_log_file_path(self):
        """Get current log file path"""
        return str(self.log_file)
