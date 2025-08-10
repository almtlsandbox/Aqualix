# Aqualix - Traitement d'Images et Vidéos

[![GitHub](https://img.shields.io/github/license/almtlsandbox/Aqualix)](https://github.com/almtlsandbox/Aqualix/blob/main/LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![OpenCV](https://img.shields.io/badge/opencv-4.8+-green.svg)](https://opencv.org/)

Une application Python Tkinter pour le traitement interactif d'images et de vidéos avec une interface utilisateur intuitive et des fonctionnalités avancées de visualisation.

![Aqualix Interface](https://img.shields.io/badge/Interface-Fran%C3%A7ais-blue)

## Features

### File Management
- **File Selection**: Choose individual image or video files
- **Folder Selection**: Select folders containing multiple images/videos
- **Navigation**: Browse through files with Previous/Next buttons
- **Supported Formats**: 
  - Images: JPEG, PNG, BMP, TIFF
  - Videos: MP4, AVI, MOV, MKV

### Video Support
- **Frame Navigation**: Slider to navigate through video frames
- **Batch Processing**: Apply processing to entire video when saving
- **Real-time Preview**: See processing effects on current frame

### Image Processing Pipeline

1. **Gray-World White Balance**
   - Corrects color temperature assuming scene average should be neutral gray
   - Configurable percentile calculation (more robust than mean)
   - Adjustable maximum correction factor to prevent overcorrection

2. **Adaptive Histogram Equalization (CLAHE)**
   - Enhances local contrast using Contrast Limited Adaptive Histogram Equalization
   - Applied to luminance channel in LAB color space
   - Configurable clip limit and tile grid size

### User Interface

- **Parameter Panel**: Adjust processing parameters in real-time
- **Pipeline Panel**: View description of current processing operations
- **Interactive Split View**: 
  - **Adjustable Split**: Drag the split line or use the slider to adjust the divider position
  - **Zoom Controls**: Mouse wheel zoom or +/- buttons for zooming in/out
  - **Pan Support**: Left-click and drag to pan around the image
  - **Rotation**: 90-degree rotation buttons (↺ ↻)
  - **Reset View**: Button to reset zoom, pan, and rotation to defaults
- **Video Controls**: Frame slider for video navigation

## Installation

1. **Clonez le repository** :
   ```bash
   git clone https://github.com/almtlsandbox/Aqualix.git
   cd Aqualix
   ```

2. **Installez Python** (3.8 ou plus récent recommandé)

3. **Créez un environnement virtuel** (recommandé) :
   ```bash
   python -m venv .venv
   # Sur Windows:
   .venv\Scripts\activate
   # Sur macOS/Linux:
   source .venv/bin/activate
   ```

4. **Installez les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the application**:
   ```bash
   python main.py
   ```

2. **Load files**:
   - Click "Select File" for individual images/videos
   - Click "Select Folder" for batch processing multiple files

3. **Adjust parameters**:
   - Use the Parameter Panel on the left to tune processing settings
   - Changes are applied in real-time to the preview

4. **Navigate**:
   - Use Previous/Next buttons for multiple files
   - Use the frame slider for video files

5. **Interactive Preview**:
   - **Split View**: The main view shows before (left) and after (right) side by side
   - **Adjust Split**: Drag the white split line or use the slider to change the division
   - **Zoom**: Use mouse wheel or +/- buttons to zoom in/out
   - **Pan**: Left-click and drag to move around zoomed images
   - **Rotate**: Use ↺ ↻ buttons to rotate the view in 90-degree increments
   - **Reset**: Click "Reset" to return to default zoom/pan/rotation

6. **Save results**:
   - Click "Save Result" to export processed images/videos
   - For videos, processing is applied to all frames

## Processing Parameters

### Gray-World White Balance
- **Enable**: Toggle the white balance correction on/off
- **Percentile**: Which percentile to use for channel average calculation (10-90%)
- **Max Adjustment**: Maximum allowed scaling factor for color channels (1.0-5.0x)

### Histogram Equalization
- **Enable**: Toggle adaptive histogram equalization on/off
- **Clip Limit**: Threshold for contrast limiting in CLAHE (1.0-10.0)
- **Tile Size**: Size of tiles for adaptive processing (4x4 to 16x16)

## Technical Details

### Architecture
- **main.py**: Main application class and UI coordination
- **image_processing.py**: Image processing algorithms and pipeline management
- **ui_components.py**: Reusable UI components (parameter panel, interactive split view, etc.)

### Dependencies
- **OpenCV**: Image and video processing
- **Pillow (PIL)**: Image handling and display
- **NumPy**: Numerical operations
- **Tkinter**: GUI framework (included with Python)

### Performance Considerations
- Real-time parameter adjustment with interactive preview
- Efficient image transformations (zoom, pan, rotate) using PIL
- Background processing for video files with progress indication
- Memory-efficient rendering for large images
- Threaded video processing to prevent UI freezing
- Optimized split-view rendering for smooth interaction

## Extending the Application

### Adding New Processing Operations

1. **Add parameters** to `ImageProcessor.parameters` dictionary
2. **Implement processing function** in `ImageProcessor` class
3. **Add operation** to `pipeline_order` list
4. **Update parameter info** in `get_parameter_info()` method
5. **Parameter widgets** will be automatically generated

### Example: Adding Gaussian Blur

```python
# In ImageProcessor.__init__():
self.parameters['blur_enabled'] = False
self.parameters['blur_kernel_size'] = 5
self.parameters['blur_sigma'] = 1.0

# Add to pipeline_order:
self.pipeline_order.append('gaussian_blur')

# Implement processing function:
def gaussian_blur(self, image):
    if self.parameters['blur_enabled']:
        kernel_size = self.parameters['blur_kernel_size']
        sigma = self.parameters['blur_sigma']
        return cv2.GaussianBlur(image, (kernel_size, kernel_size), sigma)
    return image

# Update parameter info and process_image method accordingly
```

## Troubleshooting

### Common Issues
- **Import errors**: Ensure all dependencies are installed
- **Video codec issues**: Install additional codecs if needed
- **Memory issues**: Close other applications when processing large videos
- **Performance**: Reduce image/video resolution for faster processing

### System Requirements
- Python 3.8+
- 4GB+ RAM recommended for video processing
- OpenCV-compatible video codecs for video support

## Contribuer

Les contributions sont les bienvenues ! N'hésitez pas à :

1. Fork le projet
2. Créer une branche pour votre fonctionnalité (`git checkout -b feature/AmazingFeature`)
3. Commiter vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## Remerciements

- [OpenCV](https://opencv.org/) pour les algorithmes de traitement d'image
- [Pillow](https://python-pillow.org/) pour la manipulation d'images
- [Tkinter](https://docs.python.org/3/library/tkinter.html) pour l'interface utilisateur

## Support

Pour toute question ou problème, n'hésitez pas à ouvrir une [issue](https://github.com/almtlsandbox/Aqualix/issues) sur GitHub.
