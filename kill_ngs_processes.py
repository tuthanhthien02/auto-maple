"""
Kill ALL processes that might trigger NGS detection BEFORE starting bot.

This script kills:
- VM processes (VMware, VirtualBox, etc.)
- Keyboard hooks (Python scripts with hooks)
- Automation tools (AutoHotkey, etc.)
- Debugging tools
- Other suspicious processes

Run this BEFORE starting bot to avoid NGS detection.
"""

import psutil
import sys
import time
from typing import List, Dict

# Import from check_ngs_processes
try:
    from check_ngs_processes import SENSITIVE_PROCESSES, NGSProcessChecker
except ImportError:
    print("[ERROR] Cannot import check_ngs_processes.py")
    print("Make sure check_ngs_processes.py is in the same directory")
    sys.exit(1)


class NGSProcessKiller:
    """Kill all processes that might trigger NGS detection."""

    def __init__(self):
        self.killed_processes: List[Dict] = []
        self.failed_kills: List[Dict] = []
        self.checker = NGSProcessChecker()

    def kill_all_sensitive_processes(self, force: bool = True) -> Dict:
        """
        Kill all sensitive processes.

        Args:
            force: Use force kill (terminate immediately)

        Returns:
            Dict with kill statistics
        """
        print("=" * 70)
        print("NGS PROCESS KILLER - Killing ALL sensitive processes")
        print("=" * 70)
        print()

        # Scan for processes
        print("[1/3] Scanning for sensitive processes...")
        total, counts = self.checker.scan_processes()

        if total == 0:
            print("✅ No sensitive processes found. Safe to start bot.")
            print()
            return {"killed": 0, "failed": 0, "total_found": 0}

        print(f"⚠️  Found {total} sensitive process(es):")
        for category, count in counts.items():
            if count > 0:
                print(f"   • {category}: {count} process(es)")
        print()

        # Get all processes to kill
        processes_to_kill = self.checker.get_process_list()

        print(f"[2/3] Killing {len(processes_to_kill)} process(es)...")
        print()

        killed_count = 0
        failed_count = 0

        for proc_info in processes_to_kill:
            try:
                proc = psutil.Process(proc_info["pid"])
                proc_name = proc_info["name"]
                proc_pid = proc_info["pid"]
                proc_category = proc_info["category"]

                print(f"   Killing PID {proc_pid:6d}: {proc_name} ({proc_category})")

                if force:
                    proc.kill()  # Force kill
                else:
                    proc.terminate()  # Graceful termination

                # Wait a bit for process to terminate
                try:
                    proc.wait(timeout=2)
                except psutil.TimeoutExpired:
                    # Force kill if still running
                    proc.kill()

                killed_count += 1
                self.killed_processes.append(proc_info)
                print(f"   ✅ Killed PID {proc_pid}: {proc_name}")

            except psutil.NoSuchProcess:
                print(f"   ⚠️  PID {proc_info['pid']}: Process already terminated")
                killed_count += 1
            except psutil.AccessDenied:
                print(f"   ❌ PID {proc_info['pid']}: Access denied (need admin)")
                failed_count += 1
                self.failed_kills.append(proc_info)
            except psutil.ZombieProcess:
                print(f"   ⚠️  PID {proc_info['pid']}: Zombie process")
                killed_count += 1
            except Exception as e:
                print(f"   ❌ PID {proc_info['pid']}: Unexpected error - {e}")
                failed_count += 1
                self.failed_kills.append(proc_info)

        print()
        print("[3/3] Kill summary:")
        print(f"   ✅ Killed: {killed_count}")
        if failed_count > 0:
            print(f"   ❌ Failed: {failed_count}")
        print()

        # Wait a bit for cleanup
        time.sleep(1)

        # Verify no processes remain
        print("Verifying no sensitive processes remain...")
        remaining_total, _ = self.checker.scan_processes()

        if remaining_total == 0:
            print("✅ All sensitive processes killed successfully!")
            print()
            print("=" * 70)
            print("✅ READY TO START BOT")
            print("=" * 70)
            print()
            print("Safe to start bot now.")
            print()
        else:
            print(f"⚠️  Warning: {remaining_total} process(es) still running!")
            print("   You may need to run this script as Administrator.")
            print()
            print("Remaining processes:")
            for proc_info in self.checker.get_process_list():
                print(
                    f"   • PID {proc_info['pid']}: {proc_info['name']} ({proc_info['category']})"
                )
            print()

        return {
            "killed": killed_count,
            "failed": failed_count,
            "total_found": total,
            "remaining": remaining_total,
        }

    def kill_by_category(self, category: str, force: bool = True) -> int:
        """
        Kill processes by category.

        Args:
            category: Category name (vmware, keyboard_hooks, etc.)
            force: Use force kill

        Returns:
            Number of processes killed
        """
        self.checker.scan_processes()
        processes = self.checker.process_by_category.get(category, [])

        if not processes:
            print(f"No processes found in category: {category}")
            return 0

        print(f"Killing {len(processes)} process(es) in category: {category}")

        killed = 0
        for proc_info in processes:
            try:
                proc = psutil.Process(proc_info["pid"])
                if force:
                    proc.kill()
                else:
                    proc.terminate()
                killed += 1
                print(f"✅ Killed PID {proc_info['pid']}: {proc_info['name']}")
            except Exception as e:
                print(f"❌ Failed to kill PID {proc_info['pid']}: {e}")

        return killed


def main():
    """Main function."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Kill all processes that might trigger NGS detection"
    )
    parser.add_argument(
        "--category",
        type=str,
        help="Only kill processes in specific category (vmware, keyboard_hooks, etc.)",
    )
    parser.add_argument(
        "--list-categories", action="store_true", help="List all available categories"
    )
    parser.add_argument(
        "--check-only", action="store_true", help="Only check, do not kill"
    )

    args = parser.parse_args()

    if args.list_categories:
        print("Available categories:")
        for category in SENSITIVE_PROCESSES.keys():
            print(f"  • {category}")
        return

    killer = NGSProcessKiller()

    if args.check_only:
        checker = NGSProcessChecker()
        checker.print_report(show_details=True)
        return

    if args.category:
        killed = killer.kill_by_category(args.category, force=True)
        print(f"\n✅ Killed {killed} process(es) in category: {args.category}")
    else:
        result = killer.kill_all_sensitive_processes(force=True)
        if result["killed"] > 0:
            print(f"\n✅ Successfully killed {result['killed']} process(es)")
        if result["failed"] > 0:
            print(f"\n⚠️  Failed to kill {result['failed']} process(es)")
            print("   Try running as Administrator")


if __name__ == "__main__":
    try:
        # Check admin privileges
        try:
            import ctypes

            if not ctypes.windll.shell32.IsUserAnAdmin():
                print("⚠️  WARNING: Not running as Administrator")
                print("   Some processes may fail to kill.")
                print("   For best results, run as Administrator.")
                print()
        except Exception:
            pass

        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
