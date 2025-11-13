"""
Check for sensitive processes that might trigger NGS detection.

This script scans running processes and identifies those that could potentially
trigger NGS (Nexon Game Security) detection, such as:
- Virtual machines (VMware, VirtualBox, etc.)
- Keyboard hooks
- Automation tools
- Debugging tools
"""

import psutil
import sys
from typing import List, Dict, Tuple, Optional

try:
    import winreg

    WINREG_AVAILABLE = True
except ImportError:
    WINREG_AVAILABLE = False


# Sensitive processes that might trigger NGS detection
SENSITIVE_PROCESSES = {
    # Virtual Machines
    "vmware": [
        "vmware.exe",
        "vmwaretray.exe",
        "vmwareuser.exe",
        "vmware-vmx.exe",
        "vmware-vmx-debug.exe",
        "vmware-vmx-stats.exe",
        "vmwareauthd.exe",
        "vmwarehostopen.exe",
        "vmware-usbarbitrator.exe",
    ],
    "virtualbox": [
        "virtualbox.exe",
        "vboxsvc.exe",
        "vboxmanage.exe",
        "vboxheadless.exe",
        "vboxsds.exe",
        "vboxtray.exe",
        "vboxservice.exe",
        "vboxautostart.exe",
    ],
    "vbox": [
        "vboxsvc.exe",
        "vboxmanage.exe",
        "vboxheadless.exe",
        "vboxsds.exe",
        "vboxtray.exe",
        "vboxservice.exe",
    ],
    "ldplayer": [
        "ldplayer.exe",
        "ldbox.exe",
        "ldconsole.exe",
        "ldmultiplayer.exe",
        "ldstore.exe",
    ],
    "nox": ["nox.exe", "noxvm.exe", "noxplayer.exe"],
    "bluestacks": ["bluestacks.exe", "hd-player.exe", "bstkhelper.exe"],
    "memu": ["memu.exe", "memuheadless.exe", "memuconsole.exe"],
    # Keyboard Hooks / Input Tools
    "keyboard_hooks": [
        "keyboard_to_arduino.py",
        "keyboard_block_arduino.py",
        "host_sender.py",
        "vmware_receiver.py",
        "python.exe",
        "pythonw.exe",  # Python processes running keyboard hooks
    ],
    # Key Remapping / Input Simulation Tools
    "key_remapping": [
        "sharpkeys.exe",
        "keytweak.exe",
        "keymapper.exe",
        "keyremapper.exe",
        "remapkey.exe",
        "keyboardlayouts.exe",
        "keylayout.exe",
        "scancode.exe",
        "keyboardmaestro.exe",
        "karabiner.exe",
        "uikeyboard.exe",
    ],
    # Virtual Keyboard / Input Simulation
    "virtual_keyboard": [
        "vkbd.exe",
        "virtualkeyboard.exe",
        "onscreen.exe",
        "osk.exe",
        "screenkeyboard.exe",
        "virtualkb.exe",
        "keyboardemulator.exe",
    ],
    # Automation / Bot Tools
    "automation": [
        "autohotkey.exe",
        "autohotkeyu64.exe",
        "autohotkeyu32.exe",
        "ahk.exe",
        "ahk2exe.exe",
    ],
    # Debugging / Development Tools
    "debugging": [
        "cheatengine.exe",
        "cheatengine-x86_64.exe",
        "x64dbg.exe",
        "x32dbg.exe",
        "windbg.exe",
        "ollydbg.exe",
        "ida.exe",
        "ida64.exe",
        "wireshark.exe",
        "fiddler.exe",
        "charles.exe",
    ],
    # Screen Capture / Recording
    "screen_capture": [
        "obs.exe",
        "obs64.exe",
        "obs32.exe",
        "fraps.exe",
        "bandicam.exe",
        "dxtory.exe",
        "action.exe",
        "mirillis.exe",
    ],
    # Process Injection / DLL Injection
    "injection": [
        "injector.exe",
        "dllinjector.exe",
        "processhacker.exe",
        "processexplorer.exe",
        "procmon.exe",
    ],
    # Remote Desktop / Control
    "remote": [
        "teamviewer.exe",
        "anydesk.exe",
        "splashtop.exe",
        "vnc.exe",
        "ultravnc.exe",
        "tvnserver.exe",
    ],
    # Other Suspicious
    "other": [
        "sandboxie.exe",
        "sandboxiedcomlaunch.exe",
        "sandboxierpcss.exe",
        "sandboxiedllhost.exe",
    ],
}


class NGSRegistryChecker:
    """Check registry for keyboard simulation related keys."""

    # Registry paths to check for keyboard simulation
    REGISTRY_CHECKS = [
        # Scancode Map (key remapping)
        # (winreg.HKEY_LOCAL_MACHINE, r'SYSTEM\CurrentControlSet\Control\Keyboard Layout', 'Scancode Map'),
        # Keyboard Filter Drivers
        # (winreg.HKEY_LOCAL_MACHINE, r'SYSTEM\CurrentControlSet\Services', None),  # Check all services
        # Keyboard Hooks
        # (winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Run', None),
        # (winreg.HKEY_CURRENT_USER, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Run', None),
    ]

    # Suspicious service names/keywords
    SUSPICIOUS_SERVICES = [
        "keyboard",
        "keyhook",
        "keyremap",
        "keymap",
        "scancode",
        "vkbd",
        "virtualkb",
        "inputsim",
        "sendinput",
        "keylogger",
    ]

    def __init__(self):
        self.found_registry_items: List[Dict] = []

    def check_scancode_map(self) -> Optional[Dict]:
        """Check for Scancode Map registry key (key remapping)."""
        if not WINREG_AVAILABLE:
            return None

        try:
            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"SYSTEM\CurrentControlSet\Control\Keyboard Layout",
            )
            try:
                scancode_map, _ = winreg.QueryValueEx(key, "Scancode Map")
                if scancode_map:
                    return {
                        "type": "scancode_map",
                        "path": r"HKLM\SYSTEM\CurrentControlSet\Control\Keyboard Layout\Scancode Map",
                        "value": f"Binary data ({len(scancode_map)} bytes)",
                        "risk": "HIGH - Key remapping detected",
                    }
            except FileNotFoundError:
                pass
            finally:
                winreg.CloseKey(key)
        except Exception:
            pass

        return None

    def check_keyboard_services(self) -> List[Dict]:
        """Check for suspicious keyboard-related services."""
        if not WINREG_AVAILABLE:
            return []

        found = []
        try:
            services_key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services"
            )

            i = 0
            while True:
                try:
                    service_name = winreg.EnumKey(services_key, i)
                    service_lower = service_name.lower()

                    # Check if service name contains suspicious keywords
                    for keyword in self.SUSPICIOUS_SERVICES:
                        if keyword in service_lower:
                            try:
                                service_path = winreg.OpenKey(
                                    services_key, service_name
                                )
                                try:
                                    image_path, _ = winreg.QueryValueEx(
                                        service_path, "ImagePath"
                                    )
                                    found.append(
                                        {
                                            "type": "service",
                                            "path": f"HKLM\\SYSTEM\\CurrentControlSet\\Services\\{service_name}",
                                            "value": image_path,
                                            "risk": "MEDIUM - Keyboard-related service detected",
                                        }
                                    )
                                except FileNotFoundError:
                                    pass
                                finally:
                                    winreg.CloseKey(service_path)
                            except Exception:
                                pass
                            break

                    i += 1
                except OSError:
                    break

            winreg.CloseKey(services_key)
        except Exception:
            pass

        return found

    def check_startup_programs(self) -> List[Dict]:
        """Check startup programs for keyboard simulation tools."""
        if not WINREG_AVAILABLE:
            return []

        found = []
        startup_keywords = [
            "keyboard",
            "keyhook",
            "keyremap",
            "keymap",
            "scancode",
            "vkbd",
            "virtualkb",
            "inputsim",
            "autohotkey",
        ]

        # Check HKLM Run
        try:
            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run",
            )
            i = 0
            while True:
                try:
                    name, value, _ = winreg.EnumValue(key, i)
                    value_lower = value.lower()
                    name_lower = name.lower()

                    for keyword in startup_keywords:
                        if keyword in value_lower or keyword in name_lower:
                            found.append(
                                {
                                    "type": "startup_hklm",
                                    "path": f"HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run\\{name}",
                                    "value": value,
                                    "risk": "MEDIUM - Keyboard simulation tool in startup",
                                }
                            )
                            break
                    i += 1
                except OSError:
                    break
            winreg.CloseKey(key)
        except Exception:
            pass

        # Check HKCU Run
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run",
            )
            i = 0
            while True:
                try:
                    name, value, _ = winreg.EnumValue(key, i)
                    value_lower = value.lower()
                    name_lower = name.lower()

                    for keyword in startup_keywords:
                        if keyword in value_lower or keyword in name_lower:
                            found.append(
                                {
                                    "type": "startup_hkcu",
                                    "path": f"HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run\\{name}",
                                    "value": value,
                                    "risk": "MEDIUM - Keyboard simulation tool in startup",
                                }
                            )
                            break
                    i += 1
                except OSError:
                    break
            winreg.CloseKey(key)
        except Exception:
            pass

        return found

    def scan_registry(self) -> List[Dict]:
        """Scan registry for keyboard simulation related entries."""
        self.found_registry_items = []

        # Check Scancode Map
        scancode_map = self.check_scancode_map()
        if scancode_map:
            self.found_registry_items.append(scancode_map)

        # Check keyboard services
        services = self.check_keyboard_services()
        self.found_registry_items.extend(services)

        # Check startup programs
        startup = self.check_startup_programs()
        self.found_registry_items.extend(startup)

        return self.found_registry_items

    def print_registry_report(self):
        """Print registry findings."""
        items = self.scan_registry()

        if not items:
            print("✅ No keyboard simulation registry entries found.")
            return

        print("=" * 70)
        print("KEYBOARD SIMULATION REGISTRY CHECK")
        print("=" * 70)
        print()
        print(
            f"⚠️  Found {len(items)} registry entry(ies) related to keyboard simulation:"
        )
        print()

        for item in items:
            print(f"  • Type: {item['type']}")
            print(f"    Path: {item['path']}")
            print(f"    Value: {item['value']}")
            print(f"    Risk: {item['risk']}")
            print()


class NGSProcessChecker:
    """Check for sensitive processes that might trigger NGS detection."""

    def __init__(self):
        self.found_processes: List[Dict] = []
        self.process_by_category: Dict[str, List[Dict]] = {}

    def scan_processes(self) -> Tuple[int, Dict[str, int]]:
        """
        Scan all running processes for sensitive ones.

        Returns:
            Tuple of (total_found, counts_by_category)
        """
        self.found_processes = []
        self.process_by_category = {
            category: [] for category in SENSITIVE_PROCESSES.keys()
        }

        try:
            all_processes = list(psutil.process_iter(["pid", "name", "exe", "cmdline"]))
        except Exception as e:
            print(f"[ERROR] Failed to scan processes: {e}")
            return 0, {}

        for proc in all_processes:
            try:
                proc_name = proc.info["name"].lower() if proc.info["name"] else ""
                proc_exe = proc.info["exe"].lower() if proc.info["exe"] else ""
                proc_cmdline = (
                    " ".join(proc.info["cmdline"]).lower()
                    if proc.info["cmdline"]
                    else ""
                )

                # Check each category
                for category, patterns in SENSITIVE_PROCESSES.items():
                    for pattern in patterns:
                        pattern_lower = pattern.lower()

                        # Check process name
                        if pattern_lower in proc_name or pattern_lower in proc_exe:
                            # Special check for Python processes - only flag if running keyboard hooks
                            if "python" in pattern_lower:
                                if any(
                                    keyword in proc_cmdline
                                    for keyword in [
                                        "keyboard_to_arduino",
                                        "keyboard_block_arduino",
                                        "host_sender",
                                        "vmware_receiver",
                                    ]
                                ):
                                    self._add_process(proc, category, pattern)
                            else:
                                self._add_process(proc, category, pattern)
                                break

                        # Check command line for Python scripts
                        if "python" in pattern_lower and pattern_lower in proc_cmdline:
                            self._add_process(proc, category, pattern)
                            break

            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
            except Exception:
                continue

        # Count by category
        counts = {
            category: len(processes)
            for category, processes in self.process_by_category.items()
        }
        total = len(self.found_processes)

        return total, counts

    def _add_process(self, proc, category: str, matched_pattern: str):
        """Add a found process to the list."""
        try:
            proc_info = {
                "pid": proc.info["pid"],
                "name": proc.info["name"] or "Unknown",
                "exe": proc.info["exe"] or "Unknown",
                "cmdline": (
                    " ".join(proc.info["cmdline"]) if proc.info["cmdline"] else ""
                ),
                "category": category,
                "matched_pattern": matched_pattern,
            }
            self.found_processes.append(proc_info)
            self.process_by_category[category].append(proc_info)
        except Exception:
            pass

    def print_report(self, show_details: bool = True):
        """Print a report of found sensitive processes."""
        total, _ = self.scan_processes()

        print("=" * 70)
        print("NGS SENSITIVE PROCESSES SCAN REPORT")
        print("=" * 70)
        print()

        if total == 0:
            print("✅ No sensitive processes found. Safe to start game.")
            print()
            return

        print(
            f"⚠️  Found {total} sensitive process(es) that might trigger NGS detection:"
        )
        print()

        # Print by category
        for category, processes in self.process_by_category.items():
            if not processes:
                continue

            category_name = category.replace("_", " ").title()
            print(f"📁 {category_name} ({len(processes)} process(es)):")
            print("-" * 70)

            for proc in processes:
                print(f"  • PID: {proc['pid']:6d} | {proc['name']}")
                if show_details:
                    if proc["exe"] != "Unknown":
                        print(f"    Path: {proc['exe']}")
                    if proc["cmdline"]:
                        cmdline_preview = (
                            proc["cmdline"][:100] + "..."
                            if len(proc["cmdline"]) > 100
                            else proc["cmdline"]
                        )
                        print(f"    Cmdline: {cmdline_preview}")
                    print(f"    Matched: {proc['matched_pattern']}")
                print()

        print("=" * 70)
        print("⚠️  WARNING: These processes might trigger NGS detection!")
        print("   Recommendation: Close these processes before starting game.")
        print("=" * 70)
        print()

    def get_process_list(self) -> List[Dict]:
        """Get list of found sensitive processes."""
        self.scan_processes()
        return self.found_processes

    def kill_processes(self, category: str = None, confirm: bool = True) -> int:
        """
        Kill sensitive processes.

        Args:
            category: Category to kill (None = all)
            confirm: Ask for confirmation before killing

        Returns:
            Number of processes killed
        """
        processes_to_kill = []

        if category:
            processes_to_kill = self.process_by_category.get(category, [])
        else:
            processes_to_kill = self.found_processes

        if not processes_to_kill:
            print("No processes to kill.")
            return 0

        if confirm:
            print(f"\n⚠️  WARNING: About to kill {len(processes_to_kill)} process(es):")
            for proc in processes_to_kill:
                print(f"  • PID {proc['pid']}: {proc['name']}")

            response = input("\nContinue? (yes/no): ").strip().lower()
            if response not in ["yes", "y"]:
                print("Cancelled.")
                return 0

        killed = 0
        for proc_info in processes_to_kill:
            try:
                proc = psutil.Process(proc_info["pid"])
                proc.terminate()
                killed += 1
                print(f"✅ Killed PID {proc_info['pid']}: {proc_info['name']}")
            except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                print(
                    f"❌ Failed to kill PID {proc_info['pid']}: {proc_info['name']} - {e}"
                )
            except Exception as e:
                print(f"❌ Error killing PID {proc_info['pid']}: {e}")

        return killed


def main():
    """Main function."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Check for sensitive processes that might trigger NGS detection"
    )
    parser.add_argument(
        "--kill",
        action="store_true",
        help="Kill found sensitive processes (with confirmation)",
    )
    parser.add_argument(
        "--kill-all",
        action="store_true",
        help="Kill all found sensitive processes without confirmation",
    )
    parser.add_argument(
        "--category",
        type=str,
        help="Only check/kill processes in specific category (vmware, virtualbox, keyboard_hooks, etc.)",
    )
    parser.add_argument(
        "--brief", action="store_true", help="Show brief report without details"
    )
    parser.add_argument(
        "--list-categories", action="store_true", help="List all available categories"
    )
    parser.add_argument(
        "--check-registry",
        action="store_true",
        help="Check registry for keyboard simulation related keys",
    )

    args = parser.parse_args()

    if args.list_categories:
        print("Available categories:")
        for category in SENSITIVE_PROCESSES.keys():
            print(f"  • {category}")
        return

    # Check registry if requested
    if args.check_registry:
        registry_checker = NGSRegistryChecker()
        registry_checker.print_registry_report()
        print()

    checker = NGSProcessChecker()

    if args.kill or args.kill_all:
        checker.scan_processes()
        killed = checker.kill_processes(
            category=args.category, confirm=not args.kill_all
        )
        if killed > 0:
            print(f"\n✅ Killed {killed} process(es).")
    else:
        checker.print_report(show_details=not args.brief)

        # Always show registry check if not explicitly disabled
        if not args.brief:
            print()
            registry_checker = NGSRegistryChecker()
            registry_checker.print_registry_report()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] {e}")
        sys.exit(1)
