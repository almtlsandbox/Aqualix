# -*- mode: python ; coding: utf-8 -*-

"""
PyInstaller spec file for Aqualix - Single File Standalone Executable
Creates a Windows executable with ALL dependencies bundled in ONE file.
"""

import os
from pathlib import Path

# Get the current directory
current_dir = Path(SPECPATH)

# Define essential data files to include (keep minimal for single file)
data_files = [
    # Include essential config files only
    ('config/aqualix_config.json', 'config'),
    ('LICENSE', '.'),
]

# Check for optional essential files
if (current_dir / 'test_images').exists():
    # Include only a few sample images to keep size reasonable
    sample_images = list((current_dir / 'test_images').glob('*.jpg'))[:3]
    for img in sample_images:
        data_files.append((str(img), 'test_images'))

# Hidden imports - modules that PyInstaller might miss
hidden_imports = [
    'tkinter',
    'tkinter.ttk',
    'tkinter.filedialog',
    'tkinter.messagebox',
    'PIL._tkinter_finder',
    'PIL.Image',
    'PIL.ImageTk',
    'cv2',
    'numpy',
    'scipy',
    'scipy.stats',
    'scipy.ndimage',
    'threading',
    'queue',
    'pathlib',
    'json',
    'logging',
    'datetime',
    'hashlib',
    'tempfile',
    'configparser',
    'importlib.util',
]

# Analysis configuration
a = Analysis(
    ['main.py'],  # Entry point script
    pathex=[str(current_dir)],
    binaries=[],
    datas=data_files,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',  # Exclude matplotlib if not needed
        'pandas',      # Exclude pandas if not needed
        'jupyter',     # Exclude jupyter
        'IPython',     # Exclude IPython
        'sphinx',      # Exclude documentation tools
        'pytest',      # Exclude testing frameworks
        'setuptools',  # Exclude build tools
        'distutils',   # Exclude build tools
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

# Remove duplicate files
pyz = PYZ(a.pure, a.zipped_data, cipher=None)

# Create the SINGLE FILE executable
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,    # INCLUDE binaries in the EXE
    a.zipfiles,    # INCLUDE zipfiles in the EXE  
    a.datas,       # INCLUDE data files in the EXE
    [],
    name='Aqualix-Standalone',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,      # Enable UPX compression to reduce size
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window for GUI app
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add icon file path if available
    version_file='version_info.py',  # Windows version information
)

# Note: No COLLECT section needed for single file executable