"""
PyInstaller hook for numpy - Simplified version.
Only includes essential imports to avoid slow builds.
"""
# Minimal hidden imports - PyInstaller will auto-detect most dependencies
hiddenimports = [
    'numpy.core.overrides',  # Critical for numpy to work
    'numpy.core._multiarray_umath',
]


