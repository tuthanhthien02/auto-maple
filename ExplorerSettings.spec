# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('assets', 'assets'), ('resources', 'resources'), ('src', 'src')],
    hiddenimports=[
        # Critical numpy modules only
        'numpy.core.overrides',  # Critical for numpy to work
        'numpy.core._multiarray_umath',
        'numpy.core._multiarray_tests',
        # Minimal cv2 and PIL
        'cv2',
        'cv2.cv2',
        'PIL._imaging',
        # TensorFlow modules (needed for detection module)
        'tensorflow',
        'tensorflow.lite',
        'tensorflow.lite.python',
        'tensorflow.lite.python.lite_constants',
        'tensorflow._api',
        'tensorflow._api.v2',
        'tensorflow._api.v2.compat',
        'tensorflow._api.v2.compat.v1',
        'tensorflow._api.v2.compat.v1.compat',
        'tensorflow._api.v2.compat.v1.compat.v1',
        'tensorflow._api.v2.compat.v1.lite',
    ],
    hookspath=[],  # Disable hooks for faster build (use hiddenimports instead)
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'torch',  # Not used
        'matplotlib',  # Not used
        'scipy',  # Not used
        'pandas',  # Not used
        'jupyter',  # Not used
        'IPython',  # Not used
        # Note: tensorflow is needed (detection module imports it)
    ],
    noarchive=False,
    optimize=0,  # Disable optimization (optimize=2 removes docstrings which breaks numpy)
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
    strip=False,  # Strip not available on Windows by default
    upx=False,    # Disable UPX for faster builds (can cause issues with large packages)
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
    strip=False,  # Strip not available on Windows by default
    upx=False,    # Disable UPX for faster builds (can cause issues with large packages)
    upx_exclude=[],  # Not needed when upx=False
    name='ExplorerSettings',
)
