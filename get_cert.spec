# -*- mode: python ; coding: utf-8 -*-

import sys

a = Analysis(
    ['get_cert.py'],
    pathex=[],
    binaries=[],
    datas=[("README.md", '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[".venv"],
    noarchive=False,
    optimize=2,
)
pyz = PYZ(a.pure, optimize=2)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name=sys.argv[2] if len(sys.argv) > 2 else "get_cert",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
