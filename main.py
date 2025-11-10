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

gui = GUI()
gui.start()
