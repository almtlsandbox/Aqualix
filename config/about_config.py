"""
Configuration file for application information and author details
"""

APP_INFO = {
    'name': 'Aqualix',
    'version': '2.2.0',
    'description': 'Advanced Underwater Image Enhancement Tool',
    'long_description': '''Aqualix is a comprehensive underwater image processing application 
that applies advanced algorithms for color correction, depth compensation, and quality enhancement.

Features:
- Advanced white balance algorithms (Gray World, White Patch, Shades of Gray, Grey Edge)
- Beer-Lambert law depth correction
- Underwater Dark Channel Prior (UDCP) dehazing
- Multiscale fusion enhancement
- Color rebalancing with matrix transforms
- Post-processing quality checks
- Interactive preview with zoom, pan, and split view
- Batch processing support
- Professional quality assessment tools

Based on academic research from leading computer vision conferences (CVPR, IEEE TIP).''',
    'license': 'MIT',
    'copyright': '© 2024-2025 Aqualix Project',
    'website': 'https://github.com/almtlsandbox/Aqualix',
    'documentation': 'https://github.com/almtlsandbox/Aqualix/wiki'
}

AUTHOR_INFO = {
    'name': 'Aqualix Development Team',
    'email': 'contact@aqualix.dev',
    'organization': 'Open Source Project',
    'contributors': [
        'Primary Developer',
        'Computer Vision Researcher',
        'UI/UX Designer',
        'Quality Assurance Team'
    ],
    'acknowledgments': [
        'OpenCV Community',
        'Academic Research Community',
        'Underwater Photography Community',
        'Open Source Contributors'
    ]
}

# Technical information
TECHNICAL_INFO = {
    'python_version_required': '3.7+',
    'key_dependencies': [
        'OpenCV (cv2)',
        'NumPy', 
        'PIL/Pillow',
        'Tkinter',
        'SciPy'
    ],
    'algorithms_implemented': [
        'Gray World White Balance',
        'White Patch Algorithm', 
        'Shades of Gray',
        'Grey Edge Algorithm',
        'Beer-Lambert Depth Correction',
        'Underwater Dark Channel Prior',
        'Multiscale Fusion Enhancement',
        'CLAHE & Global Histogram Equalization',
        'Color Matrix Rebalancing',
        'Post-Processing Quality Analysis'
    ],
    'research_references': [
        'Berman et al. - Underwater Single Image Color Restoration (CVPR 2017)',
        'Ancuti et al. - Color Balance and Fusion for Underwater Enhancement (IEEE TIP 2018)',
        'Chiang & Chen - Underwater Image Enhancement by Wavelength Compensation (IEEE TIP 2012)',
        'van de Weijer et al. - Edge-Based Color Constancy (IEEE TIP 2007)',
        'Finlayson & Trezzi - Shades of Gray and Colour Constancy (CIC 2004)'
    ]
}
