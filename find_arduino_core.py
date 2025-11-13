"""
Script để tìm Arduino core files (USBCore.cpp, HID.cpp, boards.txt)
Chạy script này để tìm đường dẫn chính xác đến các files cần sửa
"""

import os
import glob


def find_arduino_core_files():
    """Tìm Arduino core files trên Windows"""

    print("=" * 70)
    print("Tìm Arduino Core Files...")
    print("=" * 70)

    # Các locations có thể có
    possible_paths = [
        # Option 1: Arduino IDE Installation
        r"C:\Program Files\Arduino\hardware\arduino\avr",
        r"C:\Program Files (x86)\Arduino\hardware\arduino\avr",
        # Option 2: User AppData (Arduino 1.8.13+)
        os.path.expanduser(r"~\AppData\Local\Arduino15\packages\arduino\hardware\avr"),
        # Option 3: Portable installation
        r"~\Documents\Arduino\portable\packages\arduino\hardware\avr",
    ]

    found_files = {}

    print("\n[SEARCHING] Đang tìm Arduino installation...")

    # Tìm boards.txt
    boards_txt_paths = []
    for base_path in possible_paths:
        expanded = os.path.expanduser(base_path)
        if os.path.exists(expanded):
            # Tìm tất cả boards.txt trong các version folders
            boards_txt_pattern = os.path.join(expanded, "*", "boards.txt")
            boards_txt_pattern_parent = os.path.join(expanded, "boards.txt")

            # Check parent dir
            if os.path.exists(boards_txt_pattern_parent):
                boards_txt_paths.append(boards_txt_pattern_parent)

            # Check version folders
            for path in glob.glob(boards_txt_pattern):
                boards_txt_paths.append(path)

    # Tìm USBCore.cpp và HID.cpp
    usbcore_paths = []
    hid_paths = []

    for base_path in possible_paths:
        expanded = os.path.expanduser(base_path)
        if os.path.exists(expanded):
            # Pattern: cores/arduino/USBCore.cpp
            usbcore_pattern = os.path.join(
                expanded, "*", "cores", "arduino", "USBCore.cpp"
            )
            hid_pattern = os.path.join(expanded, "*", "cores", "arduino", "HID.cpp")

            # Check version folders
            for path in glob.glob(usbcore_pattern):
                usbcore_paths.append(path)
            for path in glob.glob(hid_pattern):
                hid_paths.append(path)

            # Also check direct path (older Arduino versions)
            direct_usbcore = os.path.join(expanded, "cores", "arduino", "USBCore.cpp")
            direct_hid = os.path.join(expanded, "cores", "arduino", "HID.cpp")

            if os.path.exists(direct_usbcore):
                usbcore_paths.append(direct_usbcore)
            if os.path.exists(direct_hid):
                hid_paths.append(direct_hid)

    # Display results
    print("\n" + "=" * 70)
    print("KẾT QUẢ TÌM KIẾM")
    print("=" * 70)

    if boards_txt_paths:
        print("\n[✓] FOUND boards.txt:")
        for i, path in enumerate(boards_txt_paths, 1):
            print(f"  {i}. {path}")
        found_files["boards.txt"] = boards_txt_paths
    else:
        print("\n[✗] NOT FOUND: boards.txt")

    if usbcore_paths:
        print("\n[✓] FOUND USBCore.cpp:")
        for i, path in enumerate(usbcore_paths, 1):
            print(f"  {i}. {path}")
        found_files["USBCore.cpp"] = usbcore_paths
    else:
        print("\n[✗] NOT FOUND: USBCore.cpp")

    if hid_paths:
        print("\n[✓] FOUND HID.cpp:")
        for i, path in enumerate(hid_paths, 1):
            print(f"  {i}. {path}")
        found_files["HID.cpp"] = hid_paths
    else:
        print("\n[✗] NOT FOUND: HID.cpp")

    # Recommendations
    print("\n" + "=" * 70)
    print("HƯỚNG DẪN")
    print("=" * 70)

    if usbcore_paths:
        print("\n[PRIORITY 1] Để đổi USB Strings:")
        print(f"  → Mở file: {usbcore_paths[0]}")
        print(
            "  → Tìm dòng: STRING_PRODUCT, STRING_MANUFACTURER, STRING_SERIAL_PLACEHOLDER"
        )
        print("  → Đổi thành strings mong muốn")

    if boards_txt_paths:
        print("\n[PRIORITY 2] Để đổi VID/PID:")
        print(f"  → Mở file: {boards_txt_paths[0]}")
        print("  → Tìm dòng: pro.vid.0=, pro.pid.0=")
        print("  → Đổi thành VID/PID mong muốn")

    if hid_paths:
        print("\n[PRIORITY 3] Để đổi TotalKeys:")
        print(f"  → Mở file: {hid_paths[0]}")
        print("  → Tìm dòng: 0x29, 0x65 (101 keys)")
        print("  → Đổi thành: 0x29, 0x68 (104 keys)")

    # Manual search instructions
    print("\n" + "=" * 70)
    print("NẾU KHÔNG TÌM THẤY - TÌM THỦ CÔNG")
    print("=" * 70)
    print("\n1. Tìm Arduino IDE installation:")
    print("   - Mở File Explorer")
    print("   - Vào: C:\\Program Files\\Arduino\\hardware\\arduino\\avr\\")
    print(
        "   - Hoặc: C:\\Users\\<YOUR_USER>\\AppData\\Local\\Arduino15\\packages\\arduino\\hardware\\avr\\"
    )
    print("\n2. Trong folder đó, tìm:")
    print("   - boards.txt (root folder)")
    print("   - cores/arduino/USBCore.cpp")
    print("   - cores/arduino/HID.cpp")

    return found_files


if __name__ == "__main__":
    try:
        results = find_arduino_core_files()
        print("\n" + "=" * 70)
        print("Nhấn Enter để đóng...")
        input()
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback

        traceback.print_exc()
        input("\nNhấn Enter để đóng...")
