# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['atualizador_shop9.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'gdown',
        'psutil',
        'requests',
        'gdown.download',
        'tkinter',
        'tkinter.ttk',
        'tkinter.scrolledtext',
        'tkinter.messagebox',
        'tkinter.filedialog',
        'threading',
        'ctypes',
        'ctypes.wintypes',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# Verificar se o ícone existe
import os
icon_path = os.path.join('images', 'icone.ico')
icon = icon_path if os.path.exists(icon_path) else None

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='AtualizadorShop9',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon,
)
