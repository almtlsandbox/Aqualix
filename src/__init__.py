"""
Aqualix - Underwater Image Processing Application

A comprehensive tool for processing underwater images with advanced algorithms
including white balance correction, underwater dark channel prior (UDCP),
histogram equalization, and multi-scale fusion.
"""

__version__ = "1.0.0"
__author__ = "Aqualix Development Team"
__email__ = "contact@aqualix.com"

from .main import ImageVideoProcessorApp
from .image_processing import ImageProcessor

__all__ = [
    "ImageVideoProcessorApp",
    "ImageProcessor",
]
