#!/usr/bin/env python3
"""
Aqualix CLI - Command Line Interface for batch image/video processing
"""

import argparse
import sys
import os
import time
from pathlib import Path
import cv2
import numpy as np

from image_processing import ImageProcessor
from logger import AqualixLogger

class AqualixCLI:
    def __init__(self):
        self.processor = ImageProcessor()
        self.logger = AqualixLogger()
        
    def process_image(self, input_path, output_path=None, **kwargs):
        """Process a single image"""
        try:
            input_path = Path(input_path)
            if not input_path.exists():
                self.logger.error(f"Input file not found: {input_path}")
                return False
                
            # Set parameters from kwargs
            for param, value in kwargs.items():
                if param in self.processor.parameters:
                    self.processor.set_parameter(param, value)
                    
            # Load image
            start_time = time.time()
            image = cv2.imread(str(input_path))
            if image is None:
                self.logger.error(f"Could not load image: {input_path}")
                return False
                
            # Convert BGR to RGB for processing
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Process image
            processed_image = self.processor.process_image(image_rgb)
            
            # Convert back to BGR for saving
            processed_bgr = cv2.cvtColor(processed_image, cv2.COLOR_RGB2BGR)
            
            # Determine output path
            if output_path is None:
                stem = input_path.stem
                suffix = input_path.suffix
                output_path = input_path.parent / f"{stem}_processed{suffix}"
            else:
                output_path = Path(output_path)
                
            # Save processed image
            success = cv2.imwrite(str(output_path), processed_bgr)
            processing_time = time.time() - start_time
            
            if success:
                active_operations = []
                if self.processor.parameters['gray_world_enabled']:
                    active_operations.append('gray_world_white_balance')
                if self.processor.parameters['hist_eq_enabled']:
                    active_operations.append('histogram_equalization')
                    
                self.logger.log_image_processing(str(input_path), active_operations, processing_time)
                self.logger.log_file_operation("SAVE", str(output_path), True)
                print(f"✓ Processed: {input_path} -> {output_path}")
                return True
            else:
                self.logger.error(f"Failed to save processed image: {output_path}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error processing image {input_path}: {str(e)}")
            return False
            
    def process_video(self, input_path, output_path=None, **kwargs):
        """Process a video file"""
        try:
            input_path = Path(input_path)
            if not input_path.exists():
                self.logger.error(f"Input file not found: {input_path}")
                return False
                
            # Set parameters from kwargs
            for param, value in kwargs.items():
                if param in self.processor.parameters:
                    self.processor.set_parameter(param, value)
                    
            start_time = time.time()
            
            # Open video
            cap = cv2.VideoCapture(str(input_path))
            if not cap.isOpened():
                self.logger.error(f"Could not open video: {input_path}")
                return False
                
            # Get video properties
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            # Determine output path
            if output_path is None:
                stem = input_path.stem
                output_path = input_path.parent / f"{stem}_processed.mp4"
            else:
                output_path = Path(output_path)
                
            # Setup video writer
            fourcc = cv2.VideoWriter.fourcc(*'mp4v')
            out = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))
            
            frame_count = 0
            print(f"Processing {total_frames} frames...")
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                    
                # Convert BGR to RGB for processing
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Process frame
                processed_frame = self.processor.process_image(frame_rgb)
                
                # Convert back to BGR and write
                processed_bgr = cv2.cvtColor(processed_frame, cv2.COLOR_RGB2BGR)
                out.write(processed_bgr)
                
                frame_count += 1
                if frame_count % 30 == 0:  # Progress every 30 frames
                    progress = (frame_count / total_frames) * 100
                    print(f"Progress: {progress:.1f}% ({frame_count}/{total_frames})")
                    
            cap.release()
            out.release()
            
            processing_time = time.time() - start_time
            self.logger.log_video_processing(str(input_path), total_frames, processing_time)
            self.logger.log_file_operation("SAVE", str(output_path), True)
            print(f"✓ Video processed: {input_path} -> {output_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error processing video {input_path}: {str(e)}")
            return False
            
    def batch_process(self, input_dir, output_dir=None, **kwargs):
        """Process all images/videos in a directory"""
        input_dir = Path(input_dir)
        if not input_dir.exists():
            self.logger.error(f"Input directory not found: {input_dir}")
            return False
            
        if output_dir is None:
            output_dir = input_dir / "processed"
        else:
            output_dir = Path(output_dir)
            
        output_dir.mkdir(exist_ok=True)
        
        # Supported extensions
        image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff'}
        video_extensions = {'.mp4', '.avi', '.mov', '.mkv'}
        
        files_processed = 0
        files_failed = 0
        
        for file_path in input_dir.iterdir():
            if file_path.is_file():
                ext = file_path.suffix.lower()
                output_path = output_dir / file_path.name
                
                if ext in image_extensions:
                    if self.process_image(file_path, output_path, **kwargs):
                        files_processed += 1
                    else:
                        files_failed += 1
                elif ext in video_extensions:
                    if self.process_video(file_path, output_path, **kwargs):
                        files_processed += 1
                    else:
                        files_failed += 1
                        
        print(f"Batch processing complete: {files_processed} processed, {files_failed} failed")
        self.logger.info(f"Batch processing complete: {files_processed} processed, {files_failed} failed")
        return files_failed == 0

def main():
    parser = argparse.ArgumentParser(description='Aqualix CLI - Process images and videos from command line')
    
    # Input/Output arguments
    parser.add_argument('input', help='Input file or directory path')
    parser.add_argument('-o', '--output', help='Output file or directory path')
    parser.add_argument('--batch', action='store_true', help='Process all files in input directory')
    
    # Processing parameters
    parser.add_argument('--gray-world', action='store_true', default=True, 
                       help='Enable gray-world white balance (default: True)')
    parser.add_argument('--no-gray-world', action='store_true', 
                       help='Disable gray-world white balance')
    parser.add_argument('--gray-world-percentile', type=float, default=50, 
                       help='Gray-world percentile (default: 50)')
    parser.add_argument('--gray-world-max-adj', type=float, default=2.0, 
                       help='Gray-world max adjustment factor (default: 2.0)')
    
    parser.add_argument('--hist-eq', action='store_true', default=True,
                       help='Enable histogram equalization (default: True)')
    parser.add_argument('--no-hist-eq', action='store_true',
                       help='Disable histogram equalization')
    parser.add_argument('--hist-eq-clip', type=float, default=2.0,
                       help='CLAHE clip limit (default: 2.0)')
    parser.add_argument('--hist-eq-tile-size', type=int, default=8,
                       help='CLAHE tile grid size (default: 8)')
    
    # Logging
    parser.add_argument('--log-level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'], 
                       default='INFO', help='Logging level (default: INFO)')
    parser.add_argument('--log-dir', default='logs', help='Log directory (default: logs)')
    
    args = parser.parse_args()
    
    # Create CLI instance
    cli = AqualixCLI()
    
    # Set log level
    log_level = getattr(__import__('logging'), args.log_level)
    cli.logger = AqualixLogger(args.log_dir, log_level)
    
    # Prepare parameters
    params = {}
    
    # Gray-world parameters
    params['gray_world_enabled'] = args.gray_world and not args.no_gray_world
    params['gray_world_percentile'] = args.gray_world_percentile
    params['gray_world_max_adjustment'] = args.gray_world_max_adj
    
    # Histogram equalization parameters
    params['hist_eq_enabled'] = args.hist_eq and not args.no_hist_eq
    params['hist_eq_clip_limit'] = args.hist_eq_clip
    params['hist_eq_tile_grid_size'] = args.hist_eq_tile_size
    
    # Log parameters
    cli.logger.info("=== Aqualix CLI Processing Started ===")
    cli.logger.info(f"Input: {args.input}")
    cli.logger.info(f"Output: {args.output}")
    cli.logger.info(f"Parameters: {params}")
    
    # Process based on mode
    success = False
    if args.batch:
        success = cli.batch_process(args.input, args.output, **params)
    else:
        input_path = Path(args.input)
        if input_path.is_file():
            ext = input_path.suffix.lower()
            if ext in {'.jpg', '.jpeg', '.png', '.bmp', '.tiff'}:
                success = cli.process_image(args.input, args.output, **params)
            elif ext in {'.mp4', '.avi', '.mov', '.mkv'}:
                success = cli.process_video(args.input, args.output, **params)
            else:
                print(f"Error: Unsupported file format: {ext}")
                cli.logger.error(f"Unsupported file format: {ext}")
        else:
            print(f"Error: Input is not a file: {args.input}")
            cli.logger.error(f"Input is not a file: {args.input}")
            
    # Log completion
    cli.logger.info(f"=== Processing {'SUCCESS' if success else 'FAILED'} ===")
    cli.logger.info(f"Log file: {cli.logger.get_log_file_path()}")
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
