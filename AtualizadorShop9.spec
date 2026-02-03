# -*- mode: python ; coding: utf-8 -*-
import os

# Informações de versão para reduzir falsos positivos de antivírus
# PyInstaller aceita arquivos .txt com formato Python (VSVersionInfo)
version_info_file = None
if os.path.exists('version_info.txt'):
    version_info_file = 'version_info.txt'

a = Analysis(
    ['atualizador_shop9.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['gdown', 'psutil', 'requests', 'tkinter', 'tkinter.ttk', 'tkinter.scrolledtext', 'tkinter.messagebox', 'threading', 'ctypes', 'ctypes.wintypes'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Excluir módulos desnecessários que podem causar falsos positivos
        'matplotlib', 'numpy', 'pandas', 'scipy', 'PIL', 'pytest', 'unittest',
        'email', 'http', 'urllib3', 'distutils', 'setuptools', 'pkg_resources',
        'win32timezone', 'win32api', 'win32con', 'win32gui', 'win32ui',
        'pydoc', 'doctest', 'difflib', 'inspect', 'pdb', 'bdb', 'cmd',
        'pydoc_data', 'test', 'tests', 'testing', 'lib2to3',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='AtualizadorShop9',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,  # UPX desabilitado - causa muitos falsos positivos
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['images\\icone.ico'] if os.path.exists('images\\icone.ico') else None,
    version=version_info_file,  # Adiciona informações de versão ao executável
    uac_admin=False,  # Não solicitar admin automaticamente (reduz suspeitas)
    uac_uiaccess=False,
)
