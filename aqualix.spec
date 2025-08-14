# -*- mode: python ; coding: utf-8 -*-

"""
PyInstaller spec file for Aqualix - Underwater Image Processing Application
Creates a Windows executable with all dependencies bundled.
"""

import os
from pathlib import Path

# Get the current directory
current_dir = Path(SPECPATH)

# Define data files to include
data_files = [
    # Include the entire src directory
    ('src', 'src'),
    # Include config files
    ('config', 'config'),
    # Include documentation
    ('docs/README.md', 'docs'),
    ('LICENSE', '.'),
    ('CHANGELOG.md', '.'),
    # Include requirements for reference
    ('requirements.txt', '.'),
]

# Additional data files to include if they exist
optional_files = [
    ('test_images', 'test_images'),  # Sample images if available
    ('logs', 'logs'),  # Log directory structure
]

# Check for optional files and add them if they exist
for src, dst in optional_files:
    if (current_dir / src).exists():
        data_files.append((src, dst))

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
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

# Remove duplicate files
pyz = PYZ(a.pure, a.zipped_data, cipher=None)

# Create the executable
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Aqualix',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # No console window for GUI app
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add icon file path if available
    version_file='version_info.py',  # Windows version information
)

# Create distribution folder
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Aqualix',
    distpath='dist'
)
