"""
Test script để gửi key commands từ Host
"""

from host_sender import HostSender
import time


def main():
    print("=== Host Sender Test ===\n")

    # Create sender
    sender = HostSender(enable_logging=True)
    sender.start()

    # Wait for connection
    print("\n[TEST] Waiting for connection...")
    for i in range(5):
        if sender.connected:
            print("[TEST] ✓ Connected!")
            break
        time.sleep(1)
        print(f"[TEST] Waiting... ({i + 1}/5)")
    else:
        print("[TEST] ✗ Connection timeout!")
        sender.stop()
        return

    # Test: Press 'a'
    print("\n[TEST] Sending: down:a")
    success = sender.send_key("a", "down")
    print(f"[TEST] Send result: {success}")

    time.sleep(0.5)

    # Test: Release 'a'
    print("[TEST] Sending: up:a")
    success = sender.send_key("a", "up")
    print(f"[TEST] Send result: {success}")

    time.sleep(0.5)

    # Test: Press space
    print("\n[TEST] Sending: down:space")
    success = sender.send_key("space", "down")
    print(f"[TEST] Send result: {success}")

    time.sleep(0.1)

    print("[TEST] Sending: up:space")
    success = sender.send_key("space", "up")
    print(f"[TEST] Send result: {success}")

    time.sleep(0.5)

    # Test: All up
    print("\n[TEST] Sending: all_up")
    success = sender.send_all_up()
    print(f"[TEST] Send result: {success}")

    # Print stats
    print("\n[TEST] Final stats:")
    sender.print_stats()

    # Stop
    print("\n[TEST] Stopping sender...")
    sender.stop()
    print("[TEST] Done!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[TEST] Interrupted")
    except Exception as e:
        import traceback

        print(f"\n[TEST] Error: {e}")
        traceback.print_exc()
        input("\nPress Enter to close...")
