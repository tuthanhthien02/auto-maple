"""The central program that ties all the modules together."""

import time
from datetime import datetime
from src.modules.bot import Bot
from src.modules.capture import Capture
from src.modules.notifier import Notifier
from src.modules.listener import Listener
from src.modules.gui import GUI
from src.common.logger import get_logger


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

bot = Bot()
capture = Capture()
notifier = Notifier()
listener = Listener()

log.info("📦 Initializing modules...")
bot.start()
while not bot.ready:
    time.sleep(0.01)

capture.start()
while not capture.ready:
    time.sleep(0.01)

notifier.start()
while not notifier.ready:
    time.sleep(0.01)

listener.start()
while not listener.ready:
    time.sleep(0.01)

log.info("")
log.info("=" * 80)
log.info("✅ AUTO MAPLE - SUCCESSFULLY INITIALIZED")
log.info("=" * 80)
log.info("")

# Initialize VMware Receiver if enabled
from src.common import config
if config.enable_vmware_receiver:
    try:
        from src.modules.vmware_receiver_integrated import VMwareReceiverIntegrated
        log.info("📡 Initializing VMware Receiver (integrated)...")
        log.info(f"   Port: {config.vmware_receiver_port}")
        log.info(f"   Hotkey hook: {config.vmware_receiver_hotkey_hook}")
        config.vmware_receiver = VMwareReceiverIntegrated(
            server_port=config.vmware_receiver_port,
            enable_hotkey_hook=config.vmware_receiver_hotkey_hook,
            enable_logging=False  # Use log level instead of verbose logging
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
    log.info("🛑 Shutting down...")
    
    # Stop VMware Receiver
    if config.vmware_receiver:
        try:
            config.vmware_receiver.stop_tcp_server()
            log.info("✅ VMware Receiver stopped")
        except Exception as e:
            log.warning(f"⚠️  Error stopping VMware Receiver: {e}")
    
    # Disconnect shared Arduino connection
    try:
        from src.common.shared_arduino_connection import SharedArduinoConnection
        shared_conn = SharedArduinoConnection._instance
        if shared_conn:
            shared_conn.disconnect()
            log.info("✅ Shared Arduino connection closed")
    except Exception as e:
        log.debug(f"Error closing shared connection: {e}")

# Register cleanup
import atexit
atexit.register(cleanup)

gui.start()
