# Auto-Maple Logging Overview

Auto-Maple now uses a shared logging utility (`src/common/logger.py`) instead of ad-hoc `print()` statements. This keeps console output consistent and writes a persistent log file for troubleshooting.

## Log Locations

-   **File**: `logs/auto_maple.log`
-   **Rotation**: Up to five files (5 MB each) are kept automatically.
-   **Executable builds**: When running a PyInstaller build, the log directory is created next to the executable (`ExplorerSettings.exe`).

## Log Contents

-   Status messages when subsystems start (bot, capture, notifier, listener, etc.)
-   Warnings or errors, such as invalid key presses, failed minimap calibration, or command-book loading issues.
-   Debug details from the capture module when `DEBUG = True` in `src/modules/capture.py`.

## Viewing Logs

-   **Console**: Messages still appear in the CLI window via the logger's console handler.
-   **File**: Open `logs/auto_maple.log` in any text editor for historical records.
-   **Action traces**: When detailed logging is enabled (see below), per-key and per-wait entries are appended to the same log.

## Adjusting Verbosity

-   Change the default log level in `src/common/logger.py` (`logger.setLevel(logging.INFO)`).
-   For module-specific debugging, obtain a child logger and adjust its level:

    ```python
    from src.common.logger import get_logger

    log = get_logger(__name__)
    log.setLevel(logging.DEBUG)
    ```

## Enabling Detailed Action Logging (press/key_down/wait)

-   Python API:

    ```python
    from src.common.logger import set_action_logging

    set_action_logging(True)   # enable
    set_action_logging(False)  # disable
    ```

-   Environment variable: `AUTO_MAPLE_ACTION_LOG=1` (also accepts `true`, `yes`, `on`).
-   When enabled, `key_down`, `key_up`, `press`, `click`, `wait`, and `wait_random` emit DEBUG entries via the `auto_maple.action` logger.
-   Disable again after debugging to keep log files small.
-   Bạn cũng có thể tạo file `.env` trong thư mục dự án với dòng `AUTO_MAPLE_ACTION_LOG=1`; logger sẽ tự đọc file này khi khởi động.

## Notes

-   The logger automatically creates the `logs/` directory if it does not exist. If the application is running from a read-only location, it falls back to the current working directory.
-   When running inside PyInstaller (`--noconsole` builds), the file log remains available even if no terminal is attached.
