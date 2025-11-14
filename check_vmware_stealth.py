"""
VMware Stealth Checker - Kiểm tra VM có stealth không để tránh NGS detection

Script này sẽ check:
- VMware processes
- VMware registry keys
- VMware services
- VMware device drivers
- Hardware traces (VID/PID, ACPI devices)
- VM detection signatures
"""

import psutil
import sys
import os
from typing import List, Dict

try:
    import winreg

    WINREG_AVAILABLE = True
except ImportError:
    WINREG_AVAILABLE = False


class VMwareStealthChecker:
    """Check VMware stealth configuration để tránh NGS detection."""

    # VMware processes that should NOT be running
    VMWARE_PROCESSES = [
        "vmware.exe",
        "vmwaretray.exe",
        "vmwareuser.exe",
        "vmware-vmx.exe",
        "vmware-vmx-debug.exe",
        "vmware-vmx-stats.exe",
        "vmwareauthd.exe",
        "vmwarehostopen.exe",
        "vmware-usbarbitrator.exe",
        "vmwaretools.exe",
        "vmtoolsd.exe",
        "vmusrvc.exe",
    ]

    # VMware registry keys that indicate VM
    VMWARE_REGISTRY_KEYS = [
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\VMware, Inc.\VMware Tools"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\VMware, Inc.\VMware Workstation"),
        (winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services\vmware"),
        (winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services\vmci"),
        (winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services\vmhgfs"),
    ]

    # VMware services that indicate VM
    VMWARE_SERVICES = [
        "vmware",
        "vmci",
        "vmhgfs",
        "vmmouse",
        "vmrawdsk",
        "vmwaretray",
        "vmwareuser",
        "vmwareauthd",
    ]

    # VMware device drivers
    VMWARE_DRIVERS = [
        "vmware",
        "vmci",
        "vmhgfs",
        "vmmouse",
        "vmrawdsk",
        "vmware_svga",
        "vmware_scsi",
        "vmware_ide",
    ]

    def __init__(self):
        self.issues: List[Dict] = []
        self.warnings: List[Dict] = []
        self.info: List[Dict] = []

    def check_vmware_processes(self) -> List[Dict]:
        """Check VMware processes đang chạy."""
        found = []

        try:
            all_processes = list(psutil.process_iter(["pid", "name", "exe"]))

            for proc in all_processes:
                try:
                    proc_name = proc.info["name"].lower() if proc.info["name"] else ""

                    for vmware_proc in self.VMWARE_PROCESSES:
                        if vmware_proc.lower() in proc_name:
                            # Skip VMware Workstation processes on Host (vmware.exe, vmware-vmx.exe)
                            # These are Host processes, not VM processes
                            if proc_name in [
                                "vmware.exe",
                                "vmware-vmx.exe",
                                "vmware-vmx-debug.exe",
                            ]:
                                # Check if running in VM or Host
                                exe_path = (
                                    proc.info["exe"].lower() if proc.info["exe"] else ""
                                )
                                # If exe path contains "Program Files" or typical Host paths, skip
                                if (
                                    "program files" in exe_path
                                    or "program files (x86)" in exe_path
                                ):
                                    # This is likely Host VMware Workstation - skip
                                    continue

                            found.append(
                                {
                                    "type": "process",
                                    "name": proc.info["name"],
                                    "pid": proc.info["pid"],
                                    "exe": proc.info["exe"],
                                    "risk": "HIGH",
                                    "message": f"VMware process đang chạy: {proc.info['name']}",
                                }
                            )
                            break
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        except Exception as e:
            self.warnings.append(
                {"type": "check_error", "message": f"Không thể check processes: {e}"}
            )

        return found

    def check_vmware_registry(self) -> List[Dict]:
        """Check VMware registry keys."""
        if not WINREG_AVAILABLE:
            return []

        found = []

        for hkey, subkey_path in self.VMWARE_REGISTRY_KEYS:
            try:
                key = winreg.OpenKey(hkey, subkey_path)

                # Check if service is running (only flag as HIGH RISK if service is running)
                service_name = subkey_path.split("\\")[-1]  # Get service name from path
                is_running = self._is_service_running(service_name)

                if is_running:
                    found.append(
                        {
                            "type": "registry",
                            "path": f"{self._hkey_name(hkey)}\\{subkey_path}",
                            "service_name": service_name,
                            "risk": "HIGH",
                            "message": f"VMware registry key tồn tại VÀ service đang chạy: {service_name}",
                        }
                    )
                else:
                    # Registry key exists but service is disabled -> Warning only
                    found.append(
                        {
                            "type": "registry",
                            "path": f"{self._hkey_name(hkey)}\\{subkey_path}",
                            "service_name": service_name,
                            "risk": "LOW",
                            "message": f"VMware registry key tồn tại (service đã disable): {service_name}",
                        }
                    )

                winreg.CloseKey(key)
            except FileNotFoundError:
                pass
            except Exception:
                pass

        return found

    def _is_service_running(self, service_name: str) -> bool:
        """Check if a Windows service is running."""
        try:
            services = list(psutil.win_service_iter())
            for service in services:
                if service.name().lower() == service_name.lower():
                    service_info = service.as_dict()
                    return service_info.get("status") == "running"
        except Exception:
            pass
        return False

    def check_vmware_services(self) -> List[Dict]:
        """Check VMware services."""
        found = []

        try:
            services = list(psutil.win_service_iter())

            for service in services:
                try:
                    service_name = service.name().lower()
                    service_info = service.as_dict()
                    display_name = service_info.get("display_name", "").lower()
                    status = service_info.get("status", "")

                    # Check by service name
                    for vmware_service in self.VMWARE_SERVICES:
                        if vmware_service.lower() in service_name:
                            if status == "running":
                                found.append(
                                    {
                                        "type": "service",
                                        "name": service.name(),
                                        "display_name": service_info.get(
                                            "display_name", ""
                                        ),
                                        "status": status,
                                        "risk": "HIGH",
                                        "message": f"VMware service đang chạy: {service.name()} ({service_info.get('display_name', '')})",
                                    }
                                )
                            break

                    # Also check by display name (catch VMware NAT Service, etc.)
                    if "vmware" in display_name and status == "running":
                        # Skip if already found
                        already_found = any(s["name"] == service.name() for s in found)
                        if not already_found:
                            found.append(
                                {
                                    "type": "service",
                                    "name": service.name(),
                                    "display_name": service_info.get(
                                        "display_name", ""
                                    ),
                                    "status": status,
                                    "risk": "HIGH",
                                    "message": f"VMware service đang chạy: {service.name()} ({service_info.get('display_name', '')})",
                                }
                            )
                except Exception:
                    continue
        except Exception as e:
            self.warnings.append(
                {"type": "check_error", "message": f"Không thể check services: {e}"}
            )

        return found

    def check_vmware_device_drivers(self) -> List[Dict]:
        """Check VMware device drivers."""
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

                    for driver in self.VMWARE_DRIVERS:
                        if driver.lower() in service_lower:
                            try:
                                service_path = winreg.OpenKey(
                                    services_key, service_name
                                )
                                try:
                                    image_path, _ = winreg.QueryValueEx(
                                        service_path, "ImagePath"
                                    )
                                    if "vmware" in image_path.lower():
                                        found.append(
                                            {
                                                "type": "driver",
                                                "name": service_name,
                                                "image_path": image_path,
                                                "risk": "HIGH",
                                                "message": f"VMware driver tồn tại: {service_name}",
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

    def check_hardware_traces(self) -> List[Dict]:
        """Check hardware traces (VID/PID, ACPI devices)."""
        warnings = []

        # Check for ACPI devices (common in VMs)
        try:
            # Try to enumerate USB devices
            # This is a simplified check - full implementation would require more Windows API calls
            warnings.append(
                {
                    "type": "hardware",
                    "risk": "MEDIUM",
                    "message": "Nên check RawInputViewer để xem hardware devices có VMware traces không",
                }
            )
        except Exception:
            pass

        return warnings

    def check_vm_detection_signatures(self) -> List[Dict]:
        """Check common VM detection signatures."""
        warnings = []

        # Check for VM-specific files/folders
        vm_paths = [
            r"C:\Program Files\VMware",
            r"C:\Program Files (x86)\VMware",
            r"C:\Windows\System32\drivers\vmware",
        ]

        for path in vm_paths:
            if os.path.exists(path):
                warnings.append(
                    {
                        "type": "file_path",
                        "path": path,
                        "risk": "MEDIUM",
                        "message": f"VMware installation path tồn tại: {path}",
                    }
                )

        return warnings

    def _hkey_name(self, hkey):
        """Convert HKEY constant to string."""
        if hkey == winreg.HKEY_LOCAL_MACHINE:
            return "HKLM"
        elif hkey == winreg.HKEY_CURRENT_USER:
            return "HKCU"
        elif hkey == winreg.HKEY_CLASSES_ROOT:
            return "HKCR"
        else:
            return "HKEY"

    def scan(self) -> Dict:
        """Scan tất cả các checks."""
        self.issues = []
        self.warnings = []
        self.info = []

        # Check processes
        processes = self.check_vmware_processes()
        self.issues.extend(processes)

        # Check registry
        registry = self.check_vmware_registry()
        self.issues.extend(registry)

        # Check services
        services = self.check_vmware_services()
        self.issues.extend(services)

        # Check drivers
        drivers = self.check_vmware_device_drivers()
        self.issues.extend(drivers)

        # Check hardware traces
        hardware = self.check_hardware_traces()
        self.warnings.extend(hardware)

        # Check VM detection signatures
        signatures = self.check_vm_detection_signatures()
        self.warnings.extend(signatures)

        # Separate HIGH RISK issues from LOW RISK warnings
        high_risk_issues = [
            issue for issue in self.issues if issue.get("risk") == "HIGH"
        ]
        low_risk_warnings_list = [
            issue for issue in self.issues if issue.get("risk") == "LOW"
        ]

        # Add LOW RISK registry warnings to warnings list
        self.warnings.extend(low_risk_warnings_list)

        # Summary
        total_issues = len(high_risk_issues)
        total_warnings = len(self.warnings)

        return {
            "issues": high_risk_issues,  # Only HIGH RISK issues
            "warnings": self.warnings,
            "total_issues": total_issues,
            "total_warnings": total_warnings,
            "is_stealth": total_issues == 0,
        }

    def print_report(self):
        """Print stealth check report."""
        result = self.scan()

        print("=" * 70)
        print("VMWARE STEALTH CHECK REPORT")
        print("=" * 70)
        print()

        # Summary
        if result["is_stealth"]:
            print("✅ VMware Stealth Status: PASS")
            print("   Không tìm thấy VMware traces quan trọng.")
        else:
            print("⚠️  VMware Stealth Status: FAIL")
            print(f"   Tìm thấy {result['total_issues']} vấn đề có thể bị NGS detect!")

        print()

        # High Risk Issues
        if result["issues"]:
            print("=" * 70)
            print(f"⚠️  HIGH RISK ISSUES ({len(result['issues'])}):")
            print("=" * 70)
            print()

            for issue in result["issues"]:
                print(f"  🔴 {issue['type'].upper()}: {issue['message']}")
                if "path" in issue:
                    print(f"     Path: {issue['path']}")
                if "name" in issue:
                    print(f"     Name: {issue['name']}")
                if "pid" in issue:
                    print(f"     PID: {issue['pid']}")
                if "service_name" in issue:
                    print(f"     Service: {issue['service_name']}")
                    print(
                        f"     Fix: Disable service '{issue['service_name']}' trong services.msc"
                    )
                print()

        # Warnings
        if result["warnings"]:
            print("=" * 70)
            print(f"⚠️  WARNINGS ({len(result['warnings'])}):")
            print("=" * 70)
            print()

            for warning in result["warnings"]:
                print(f"  🟡 {warning['type'].upper()}: {warning['message']}")
                if "path" in warning:
                    print(f"     Path: {warning['path']}")
                print()

        # Recommendations
        print("=" * 70)
        print("💡 RECOMMENDATIONS:")
        print("=" * 70)
        print()

        if result["is_stealth"]:
            print("✅ VM của bạn có vẻ stealth tốt!")
            print("   Tuy nhiên, vẫn nên:")
            print("   1. Check RawInputViewer để xem hardware devices")
            print("   2. Dùng Arduino HID Keyboard thay vì VM keyboard")
            print("   3. Tránh VMware mouse (dùng physical mouse hoặc pass-through)")
        else:
            print("⚠️  Cần fix các vấn đề sau:")
            print()

            if any("process" in issue["type"] for issue in result["issues"]):
                print("1. Kill VMware processes:")
                print("   - VM → Settings → VMware Tools → Disable")
                print("   - Hoặc kill processes thủ công")

            if any("service" in issue["type"] for issue in result["issues"]):
                print("2. Disable VMware services:")
                print("   - services.msc → Tìm VMware services → Disable")

            if any("registry" in issue["type"] for issue in result["issues"]):
                print("3. Registry keys với services đang chạy:")
                print("   - Disable service trong services.msc")
                print("   - Hoặc chạy: sc config <service_name> start= disabled")
                print(
                    "   - Registry key sẽ vẫn tồn tại nhưng service không chạy = SAFE"
                )

            # Check for LOW RISK registry warnings
            registry_warnings = [
                w for w in result["warnings"] if w.get("type") == "registry"
            ]
            if registry_warnings:
                print()
                print("ℹ️  Registry keys tồn tại nhưng services đã disable:")
                print("   - Đây là OK và không thể tránh được")
                print("   - Registry keys không quan trọng nếu services không chạy")
                print("   - NGS sẽ không chỉ dựa vào registry keys")

            print()
            print("4. General recommendations:")
            print("   - Dùng Arduino HID Keyboard (hardware riêng)")
            print("   - Pass-through physical mouse vào VM")
            print("   - Tránh VMware emulated devices")

        print()
        print("=" * 70)
        print()


def main():
    """Main function."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Check VMware stealth configuration để tránh NGS detection"
    )
    parser.add_argument("--brief", action="store_true", help="Show brief report")

    _args = parser.parse_args()

    checker = VMwareStealthChecker()
    checker.print_report()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
