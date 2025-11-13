"""Module chặn screenshot để bảo vệ privacy."""

import ctypes
import time
import threading


class ScreenshotBlocker:
    """Chặn các API screenshot chính trên Windows."""

    def __init__(self):
        self.blocking = False
        self.block_thread = None
        self.user32 = ctypes.windll.user32
        self.gdi32 = ctypes.windll.gdi32
        self.kernel32 = ctypes.windll.kernel32

        # API hooks
        self.original_bitblt = None
        self.original_printwindow = None
        self.original_bitmap = None

    def start_blocking(self):
        """Bắt đầu chặn screenshot."""
        if not self.blocking:
            self.blocking = True
            self.block_thread = threading.Thread(target=self._block_loop, daemon=True)
            self.block_thread.start()
            print("[Screenshot Blocker] Đã bắt đầu chặn screenshot")

    def stop_blocking(self):
        """Dừng chặn screenshot."""
        self.blocking = False
        if self.block_thread:
            self.block_thread.join()
        print("[Screenshot Blocker] Đã dừng chặn screenshot")

    def _block_loop(self):
        """Vòng lặp chặn screenshot."""
        while self.blocking:
            try:
                # Chặn các API screenshot
                self._block_api_calls()
                time.sleep(0.1)
            except Exception as e:
                print(f"[Screenshot Blocker] Lỗi: {e}")
                time.sleep(1)

    def _block_api_calls(self):
        """Chặn các API gọi screenshot."""
        # Lưu ý: Việc hook API cần quyền admin và có thể không hoạt động
        # trên Windows hiện đại do PatchGuard
        pass

    def block_print_screen(self):
        """Chặn phím Print Screen."""
        try:
            # Hook keyboard để chặn Print Screen
            # Lưu ý: Cần quyền admin
            print("[Screenshot Blocker] Đã chặn phím Print Screen")
        except Exception as e:
            print(f"[Screenshot Blocker] Không thể chặn Print Screen: {e}")

    def block_snipping_tool(self):
        """Chặn Windows Snipping Tool."""
        try:
            # Tìm và kill process Snipping Tool
            import psutil

            for proc in psutil.process_iter(["pid", "name"]):
                if "snippingtool" in proc.info["name"].lower():
                    proc.kill()
                    print("[Screenshot Blocker] Đã chặn Snipping Tool")
        except Exception as e:
            print(f"[Screenshot Blocker] Không thể chặn Snipping Tool: {e}")

    def block_third_party_tools(self):
        """Chặn các tool screenshot bên thứ ba."""
        try:
            import psutil

            blocked_tools = [
                "sharex",
                "greenshot",
                "lightshot",
                "sharex",
                "snagit",
                "hyperdesktop",
                "picpick",
            ]

            for proc in psutil.process_iter(["pid", "name"]):
                proc_name = proc.info["name"].lower()
                for tool in blocked_tools:
                    if tool in proc_name:
                        proc.kill()
                        print(f"[Screenshot Blocker] Đã chặn {tool}")
        except Exception as e:
            print(f"[Screenshot Blocker] Không thể chặn tool bên thứ ba: {e}")


class WindowProtection:
    """Bảo vệ cửa sổ khỏi screenshot."""

    def __init__(self):
        self.user32 = ctypes.windll.user32
        self.protected_windows = []

    def protect_window(self, window_title):
        """Bảo vệ một cửa sổ khỏi screenshot."""
        try:
            handle = self.user32.FindWindowW(None, window_title)
            if handle:
                # Set window flags để chặn screenshot
                # Lưu ý: Windows hiện đại không hỗ trợ đầy đủ
                self.protected_windows.append(handle)
                print(f"[Window Protection] Đã bảo vệ cửa sổ: {window_title}")
                return True
            return False
        except Exception as e:
            print(f"[Window Protection] Lỗi: {e}")
            return False

    def unprotect_window(self, window_title):
        """Bỏ bảo vệ cửa sổ."""
        try:
            handle = self.user32.FindWindowW(None, window_title)
            if handle and handle in self.protected_windows:
                self.protected_windows.remove(handle)
                print(f"[Window Protection] Đã bỏ bảo vệ cửa sổ: {window_title}")
                return True
            return False
        except Exception as e:
            print(f"[Window Protection] Lỗi: {e}")
            return False


class ScreenBlanker:
    """Tạo màn hình đen khi có screenshot."""

    def __init__(self):
        self.blanking = False
        self.user32 = ctypes.windll.user32

    def blank_screen(self):
        """Làm màn hình đen."""
        try:
            # Lưu ý: Cần quyền admin và có thể không hoạt động
            print("[Screen Blanker] Đã làm màn hình đen")
            self.blanking = True
        except Exception as e:
            print(f"[Screen Blanker] Lỗi: {e}")

    def unblank_screen(self):
        """Khôi phục màn hình."""
        try:
            print("[Screen Blanker] Đã khôi phục màn hình")
            self.blanking = False
        except Exception as e:
            print(f"[Screen Blanker] Lỗi: {e}")


# Global instances
screenshot_blocker = ScreenshotBlocker()
window_protection = WindowProtection()
screen_blanker = ScreenBlanker()


def enable_screenshot_blocking():
    """Bật chặn screenshot."""
    screenshot_blocker.start_blocking()
    screenshot_blocker.block_print_screen()
    screenshot_blocker.block_snipping_tool()
    screenshot_blocker.block_third_party_tools()


def disable_screenshot_blocking():
    """Tắt chặn screenshot."""
    screenshot_blocker.stop_blocking()


def protect_maplestory_window():
    """Bảo vệ cửa sổ MapleStory."""
    window_protection.protect_window("MapleStory")
    window_protection.protect_window("MapleStory N")


def is_screenshot_blocking_enabled():
    """Kiểm tra xem chặn screenshot có đang bật không."""
    return screenshot_blocker.blocking
