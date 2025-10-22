"""
Script cài đặt dependencies an toàn cho Auto Maple trên VM
Tránh lỗi compiler bằng cách cài từng package với error handling
"""
import subprocess
import sys

# Danh sách packages theo thứ tự ưu tiên (dễ -> khó)
PACKAGES = [
    # Core packages (pure Python - dễ cài)
    ('GitPython', 'GitPython'),
    ('keyboard', 'keyboard'),
    ('Pillow', 'Pillow'),
    ('pygame', 'pygame'),
    
    # Windows-specific (có pre-built wheels)
    ('pywin32', 'pywin32'),
    
    # Scientific packages (có thể cần compiler)
    ('numpy', 'numpy'),
    ('mss', 'mss'),
    ('opencv-python-headless', 'opencv-python-headless'),
]

def run_pip(cmd):
    """Chạy pip command và trả về kết quả"""
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'pip'] + cmd,
            capture_output=True,
            text=True,
            timeout=300  # 5 phút timeout
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, '', str(e)

def upgrade_pip():
    """Upgrade pip trước khi cài"""
    print("=" * 60)
    print("BƯỚC 1: Upgrade pip, setuptools, wheel")
    print("=" * 60)
    success, stdout, stderr = run_pip(['install', '--upgrade', 'pip', 'setuptools', 'wheel'])
    if success:
        print("✅ Đã upgrade pip thành công\n")
    else:
        print("⚠️ Không upgrade được pip (không sao, tiếp tục...)\n")
    return success

def install_package(name, package):
    """Cài 1 package với nhiều cách thử"""
    print(f"\n{'=' * 60}")
    print(f"Đang cài: {name}")
    print('=' * 60)
    
    # Cách 1: Cài bình thường (dùng wheel nếu có)
    print(f"[1/3] Thử cài {package} (pre-built wheel)...")
    success, stdout, stderr = run_pip(['install', package, '--prefer-binary'])
    
    if success:
        print(f"✅ Đã cài {name} thành công!")
        return True
    
    # Cách 2: Cài version cụ thể (stable)
    print(f"[2/3] Thử cài version cũ hơn (stable)...")
    
    # Map package -> version ổn định
    stable_versions = {
        'numpy': 'numpy==1.23.5',
        'opencv-python-headless': 'opencv-python-headless==4.8.0.76',
        'Pillow': 'Pillow==10.0.0',
        'mss': 'mss==9.0.1',
        'pygame': 'pygame==2.5.0',
        'pywin32': 'pywin32==306',
    }
    
    if package in stable_versions:
        success, stdout, stderr = run_pip(['install', stable_versions[package], '--prefer-binary'])
        if success:
            print(f"✅ Đã cài {name} (stable version) thành công!")
            return True
    
    # Cách 3: Skip nếu không cài được
    print(f"❌ KHÔNG cài được {name}")
    print(f"Lỗi: {stderr[:200]}...")
    print(f"⚠️ Bỏ qua {name} và tiếp tục...\n")
    return False

def check_imports():
    """Kiểm tra xem import được không"""
    print("\n" + "=" * 60)
    print("KIỂM TRA: Import các packages")
    print("=" * 60)
    
    tests = [
        ('GitPython', 'import git'),
        ('keyboard', 'import keyboard'),
        ('Pillow', 'from PIL import Image'),
        ('pygame', 'import pygame'),
        ('pywin32', 'import win32api'),
        ('numpy', 'import numpy'),
        ('mss', 'import mss'),
        ('OpenCV', 'import cv2'),
    ]
    
    results = {}
    for name, code in tests:
        try:
            exec(code)
            print(f"✅ {name:20s} - OK")
            results[name] = True
        except ImportError:
            print(f"❌ {name:20s} - KHÔNG cài được")
            results[name] = False
        except Exception as e:
            print(f"⚠️  {name:20s} - Lỗi: {e}")
            results[name] = False
    
    return results

def main():
    print("\n" + "=" * 60)
    print("AUTO MAPLE - INSTALLER (VM-friendly)")
    print("=" * 60)
    print("Script sẽ cài từng package riêng lẻ để tránh lỗi compiler\n")
    
    # Bước 1: Upgrade pip
    upgrade_pip()
    
    # Bước 2: Cài từng package
    print("\n" + "=" * 60)
    print("BƯỚC 2: Cài đặt dependencies")
    print("=" * 60)
    
    success_count = 0
    for name, package in PACKAGES:
        if install_package(name, package):
            success_count += 1
    
    # Bước 3: Kiểm tra
    results = check_imports()
    
    # Tổng kết
    print("\n" + "=" * 60)
    print("TỔNG KẾT")
    print("=" * 60)
    print(f"Đã cài thành công: {success_count}/{len(PACKAGES)} packages")
    
    required = ['numpy', 'OpenCV', 'mss', 'Pillow', 'pywin32']
    missing = [name for name in required if not results.get(name, False)]
    
    if not missing:
        print("\n✅ ĐÃ CÀI ĐẦY ĐỦ! Bạn có thể chạy bot:")
        print("   python main.py")
    else:
        print(f"\n⚠️ CÒN THIẾU: {', '.join(missing)}")
        print("\nGiải pháp:")
        print("1. Cài Miniconda: https://docs.conda.io/en/latest/miniconda.html")
        print("2. Chạy:")
        print("   conda create -n automaple python=3.10")
        print("   conda activate automaple")
        print("   conda install numpy opencv pillow")
        print("   pip install mss keyboard pywin32 pygame GitPython")

if __name__ == '__main__':
    main()

