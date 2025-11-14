# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('assets', 'assets'), ('resources', 'resources'), ('src', 'src')],
    hiddenimports=[
        # Keep core numpy/cv2/PIL only
        'numpy.core.overrides',
        'numpy.core._multiarray_umath',
        'numpy.core._multiarray_tests',
        'cv2',
        'cv2.cv2',
        'PIL._imaging',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Exclude heavy ML stacks for light build (fixes VM build issues)
        'tensorflow',
        'tensorflow.lite',
        'tensorflow._api',
        'keras',
        'torch',
        'keras.src.backend.torch',
    ],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='ExplorerSettings',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['assets\\explorer-icon.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='ExplorerSettings',
)


