"""The central program that ties all the modules together."""

import atexit
import time
from datetime import datetime

from src.common import config
from src.common.crash_detection import log_shutdown, mark_graceful_shutdown
from src.common.health_check import stop_health_monitoring
from src.common.logger import get_logger
from src.common.manual_capture_config import (
    initialize_manual_region,
    save_manual_region,
)
from src.modules.bot import Bot
from src.modules.capture import Capture
from src.modules.gui import GUI
from src.modules.listener import Listener
from src.modules.mirror_input import MirrorInput
from src.modules.notifier import Notifier

log = get_logger(__name__)

# Log session separator and header
log.info("")
log.info("=" * 80)
log.info("=" * 80)
log.info("🚀 AUTO MAPLE - STARTING NEW SESSION")
log.info("=" * 80)
log.info(f"   Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
log.info("=" * 80)
log.info("")
initialize_manual_region()

bot = Bot()
capture = Capture()
notifier = Notifier()
listener = Listener()
mirror_input = MirrorInput()
config.mirror_input = mirror_input

log.info("📦 Initializing modules...")
bot.start()
timeout = 30  # 30 seconds timeout
elapsed = 0
while not bot.ready:
    time.sleep(0.1)
    elapsed += 0.1
    if elapsed >= timeout:
        log.error("❌ Bot module failed to initialize within %d seconds", timeout)
        raise TimeoutError("Bot module initialization timeout")
log.info("✅ Bot module ready")

log.info("🖥️ Capture will start after you choose a region in the GUI.")

notifier.start()
elapsed = 0
while not notifier.ready:
    time.sleep(0.1)
    elapsed += 0.1
    if elapsed >= timeout:
        log.error("❌ Notifier module failed to initialize within %d seconds", timeout)
        raise TimeoutError("Notifier module initialization timeout")
log.info("✅ Notifier module ready")

listener.start()
if config.enable_keyboard_listener:
    elapsed = 0
    while not listener.ready:
        time.sleep(0.1)
        elapsed += 0.1
        if elapsed >= timeout:
            log.error(
                "❌ Listener module failed to initialize within %d seconds", timeout
            )
            raise TimeoutError("Listener module initialization timeout")
    log.info("✅ Listener module ready")
else:
    log.info("🔕 Keyboard listener disabled by configuration")

mirror_input.configure(
    config.mirror_input_host,
    config.mirror_input_port,
    config.mirror_input_block_original,
)
if config.mirror_input_auto_connect:
    if mirror_input.connect():
        log.info(
            "🔌 Mirror input TCP auto-connect enabled (%s:%s)",
            config.mirror_input_host,
            config.mirror_input_port,
        )
if config.mirror_input_enabled:
    mirror_input.start()
    log.info("✅ Mirror input auto-started")

log.info("")
log.info("=" * 80)
log.info("✅ AUTO MAPLE - SUCCESSFULLY INITIALIZED")
log.info("=" * 80)
log.info("")

if config.enable_vmware_receiver:
    try:
        from src.modules.vmware_receiver_integrated import VMwareReceiverIntegrated

        log.info("📡 Initializing VMware Receiver (integrated)...")
        log.info(f"   Port: {config.vmware_receiver_port}")
        log.info(f"   Hotkey hook: {config.vmware_receiver_hotkey_hook}")
        config.vmware_receiver = VMwareReceiverIntegrated(
            server_port=config.vmware_receiver_port,
            enable_hotkey_hook=config.vmware_receiver_hotkey_hook,
            enable_logging=False,  # Use log level instead of verbose logging
        )
        config.vmware_receiver.start_tcp_server()
        log.info("✅ VMware Receiver started successfully")
    except Exception as e:
        log.warning(f"⚠️  Failed to initialize VMware Receiver: {e}")
        log.warning("   Continuing without VMware Receiver...")
        import traceback

        log.debug(f"Traceback: {traceback.format_exc()}")
        config.vmware_receiver = None
else:
    log.debug("VMware Receiver is disabled in config")

gui = GUI()


# Cleanup function
def cleanup():
    """Cleanup on exit"""
    # Mark graceful shutdown
    mark_graceful_shutdown("cleanup_called")

    log.info("🛑 Shutting down...")

    # Stop health monitoring
    try:
        stop_health_monitoring()
    except Exception as e:
        log.debug(f"Error stopping health monitoring: {e}")

    # Stop VMware Receiver
    if config.vmware_receiver:
        try:
            config.vmware_receiver.stop_tcp_server()
            log.info("✅ VMware Receiver stopped")
        except Exception as e:
            log.warning(f"⚠️  Error stopping VMware Receiver: {e}")

    # Stop mirror input
    mirror = getattr(config, "mirror_input", None)
    if mirror:
        mirror.shutdown()

    # Disconnect shared Arduino connection
    try:
        from src.common.shared_arduino_connection import SharedArduinoConnection

        shared_conn = SharedArduinoConnection._instance
        if shared_conn:
            shared_conn.disconnect()
            log.info("✅ Shared Arduino connection closed")
    except Exception as e:
        log.debug(f"Error closing shared connection: {e}")

    # Save manual capture region if it exists
    if hasattr(config, "manual_capture_rect") and config.manual_capture_rect:
        try:
            save_manual_region(config.manual_capture_rect)
            log.debug("✅ Manual capture region saved on shutdown")
        except Exception as e:
            log.debug(f"Error saving manual region on shutdown: {e}")

    # Log shutdown event
    log_shutdown()


atexit.register(cleanup)

# Main execution with crash handling
try:
    gui.start()
except KeyboardInterrupt:
    log.info("🛑 Interrupted by user")
    mark_graceful_shutdown("keyboard_interrupt")
    cleanup()
except Exception as e:
    import traceback

    log.error("=" * 80)
    log.error("❌ CRITICAL ERROR - APPLICATION CRASHED")
    log.error("=" * 80)
    log.error(f"Error: {e}")
    log.error("")
    log.error("Full traceback:")
    log.error(traceback.format_exc())
    log.error("=" * 80)

    # Cleanup on crash
    try:
        cleanup()
    except Exception as cleanup_error:
        log.error(f"Error during cleanup: {cleanup_error}")

    # Pause console for debugging
    print("\n" + "=" * 80)
    print("❌ APPLICATION CRASHED - CONSOLE PAUSED FOR DEBUGGING")
    print("=" * 80)
    print(f"Error: {e}")
    print("\nPress Enter to exit...")
    try:
        input()
    except (EOFError, KeyboardInterrupt):
        pass
