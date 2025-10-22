"""
Download pre-built wheels từ PyPI để cài offline trên VM
Tránh lỗi compiler bằng cách download .whl files có sẵn
"""
import subprocess
import sys
import os

def main():
    print("=" * 60)
    print("DOWNLOAD WHEELS (để cài offline)")
    print("=" * 60)
    print("Script sẽ tải các .whl files vào thư mục 'wheels/'")
    print("Sau đó bạn có thể copy sang VM và cài offline\n")
    
    # Tạo thư mục wheels
    os.makedirs('wheels', exist_ok=True)
    
    packages = [
        'GitPython',
        'keyboard',
        'mss',
        'numpy',
        'opencv-python-headless',
        'Pillow',
        'pygame',
        'pywin32',
    ]
    
    print(f"Đang tải {len(packages)} packages...\n")
    
    # Download wheels
    cmd = [
        sys.executable, '-m', 'pip', 'download',
        '--dest', 'wheels',
        '--prefer-binary',
        '--platform', 'win_amd64',
        '--python-version', '310',  # Python 3.10
        '--only-binary', ':all:',
    ] + packages
    
    print(f"Lệnh: {' '.join(cmd)}\n")
    
    try:
        result = subprocess.run(cmd, check=True)
        print("\n" + "=" * 60)
        print("✅ ĐÃ TẢI XONG!")
        print("=" * 60)
        print(f"Các file .whl đã được lưu vào: {os.path.abspath('wheels')}")
        print("\nĐể cài trên VM:")
        print("1. Copy thư mục 'wheels/' sang VM")
        print("2. Chạy: python -m pip install --no-index --find-links=wheels -r requirements_no_ai.txt")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Lỗi khi download: {e}")
        print("\nThử download thủ công từ:")
        print("https://pypi.org/")

if __name__ == '__main__':
    main()

