"""
Build script for vmware_receiver.py
Compiles to standalone executable using PyInstaller
"""

import os
import shutil
import subprocess
import sys

# Build configuration
BUILD_DIR = "build"
DIST_DIR = "dist"
EXE_NAME = "system_service"  # Generic name to reduce detection
SCRIPT_NAME = "vmware_receiver.py"
ICON_FILE = None  # Optional: path to .ico file

# PyInstaller options
PYINSTALLER_OPTIONS = [
    "--onefile",  # Single executable file
    "--noconsole",  # No console window (GUI mode)
    "--clean",  # Clean cache before building
    "--noupx",  # Disable UPX compression (faster, more compatible)
    f"--name={EXE_NAME}",
    "--add-data=src;src",  # Include src directory
    "--hidden-import=serial",
    "--hidden-import=serial.tools.list_ports",
    "--hidden-import=ctypes",
    "--hidden-import=ctypes.wintypes",
    "--hidden-import=winsound",
    "--hidden-import=src.common.serial_obfuscation",
    "--hidden-import=src.common.logger",
    "--collect-all=serial",  # Collect all serial submodules
]

# Optional: Add icon if available
if ICON_FILE and os.path.exists(ICON_FILE):
    PYINSTALLER_OPTIONS.append(f"--icon={ICON_FILE}")


def check_pyinstaller():
    """Check if PyInstaller is installed"""
    try:
        import PyInstaller

        print(f"✓ PyInstaller found: {PyInstaller.__version__}")
        return True
    except ImportError:
        print("✗ PyInstaller not found")
        print("  Installing PyInstaller...")
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "pyinstaller"]
            )
            print("✓ PyInstaller installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("✗ Failed to install PyInstaller")
            return False


def check_dependencies():
    """Check if required dependencies are installed"""
    required = ["pyserial", "ctypes"]
    missing = []

    for dep in required:
        try:
            __import__(dep.replace("-", "_"))
            print(f"✓ {dep} found")
        except ImportError:
            missing.append(dep)
            print(f"✗ {dep} not found")

    if missing:
        print(f"\nInstalling missing dependencies: {', '.join(missing)}")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing)
            print("✓ Dependencies installed")
            return True
        except subprocess.CalledProcessError:
            print("✗ Failed to install dependencies")
            return False

    return True


def build():
    """Build the executable"""
    print("=" * 60)
    print("Building vmware_receiver.py")
    print("=" * 60)

    # Check if script exists
    if not os.path.exists(SCRIPT_NAME):
        print(f"✗ Error: {SCRIPT_NAME} not found")
        return False

    # Check dependencies
    if not check_pyinstaller():
        return False

    if not check_dependencies():
        return False

    # Clean previous builds
    print("\nCleaning previous builds...")
    for dir_name in [BUILD_DIR, DIST_DIR]:
        if os.path.exists(dir_name):
            try:
                shutil.rmtree(dir_name)
                print(f"✓ Removed {dir_name}/")
            except Exception as e:
                print(f"⚠ Warning: Could not remove {dir_name}/: {e}")

    # Build command
    cmd = [sys.executable, "-m", "PyInstaller"] + PYINSTALLER_OPTIONS + [SCRIPT_NAME]

    print(f"\nBuilding executable: {EXE_NAME}.exe")
    print(f"Command: {' '.join(cmd)}")
    print("-" * 60)

    try:
        subprocess.run(cmd, check=True, capture_output=False)
        print("-" * 60)

        # Check if exe was created
        exe_path = os.path.join(DIST_DIR, f"{EXE_NAME}.exe")
        if os.path.exists(exe_path):
            exe_size = os.path.getsize(exe_path) / (1024 * 1024)  # MB
            print("✓ Build successful!")
            print(f"✓ Executable: {exe_path}")
            print(f"✓ Size: {exe_size:.2f} MB")
            print(f"\nYou can find the executable in: {os.path.abspath(DIST_DIR)}")
            return True
        else:
            print("✗ Build completed but executable not found")
            return False

    except subprocess.CalledProcessError as e:
        print(f"✗ Build failed with error code: {e.returncode}")
        return False
    except Exception as e:
        print(f"✗ Build error: {e}")
        return False


def main():
    """Main build function"""
    print("\n" + "=" * 60)
    print("VMware Receiver Build Script")
    print("=" * 60)

    # Change to script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    print(f"Working directory: {os.getcwd()}\n")

    success = build()

    if success:
        print("\n" + "=" * 60)
        print("Build completed successfully!")
        print("=" * 60)
        print("\nNext steps:")
        print(f"1. Test the executable: {os.path.join(DIST_DIR, f'{EXE_NAME}.exe')}")
        print("2. Copy to VMware machine")
        print(
            f"3. Run with: {EXE_NAME}.exe [COM_PORT] [BAUDRATE] [SERVER_PORT] [ENABLE_LOGGING]"
        )
        sys.exit(0)
    else:
        print("\n" + "=" * 60)
        print("Build failed!")
        print("=" * 60)
        sys.exit(1)


if __name__ == "__main__":
    main()
