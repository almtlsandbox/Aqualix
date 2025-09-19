# -*- coding: utf-8 -*-
"""
Version information file for Aqualix Windows executable
"""

VSVersionInfo(
    ffi=FixedFileInfo(
        filevers=(2, 0, 0, 0),
        prodvers=(2, 0, 0, 0),
        mask=0x3f,
        flags=0x0,
        OS=0x4,
        fileType=0x1,
        subtype=0x0,
        date=(0, 0)
    ),
    kids=[
        StringFileInfo([
            StringTable(
                '040904B0',  # English, Unicode
                [
                    StringStruct('CompanyName', 'Aqualix Development Team'),
                    StringStruct('FileDescription', 'Aqualix - Underwater Image Processing Application'),
                    StringStruct('FileVersion', '2.0.0.0'),
                    StringStruct('InternalName', 'Aqualix'),
                    StringStruct('LegalCopyright', 'Copyright © 2025 Arnaud Dominique Lina'),
                    StringStruct('OriginalFilename', 'Aqualix.exe'),
                    StringStruct('ProductName', 'Aqualix'),
                    StringStruct('ProductVersion', '2.0.0'),
                    StringStruct('LegalTrademarks', ''),
                ]
            )
        ]),
        VarFileInfo([
            VarStruct('Translation', [0x409, 1200])  # English, Unicode
        ])
    ]
)
