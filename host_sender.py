"""
Host Sender - TCP Client để gửi input từ Host đến VMware
Gửi key commands qua TCP đến VMware receiver script
"""
import socket
import json
import os
import sys
import time
import threading
from typing import Optional

# Ensure console can print UTF-8
try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass


class HostSender:
    """TCP Client để gửi key commands đến VMware"""
    
    def __init__(self, vmware_ip: str = None, vmware_port: int = 12345, 
                 reconnect_interval: float = 1.0, enable_logging: bool = False):
        self.vmware_ip = vmware_ip
        self.vmware_port = vmware_port
        self.reconnect_interval = reconnect_interval
        self.enable_logging = enable_logging
        
        self.socket: Optional[socket.socket] = None
        self.connected = False
        self.running = False
        
        # Stats
        self.stats = {
            'total_sent': 0,
            'total_errors': 0,
            'total_reconnects': 0
        }
        
        # Config
        self.CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'host_sender.config.json')
        self._load_config()
        
        # Auto-reconnect thread
        self.reconnect_thread = None
    
    def _load_config(self):
        """Load config from JSON file"""
        try:
            if os.path.exists(self.CONFIG_PATH):
                with open(self.CONFIG_PATH, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.vmware_ip = config.get('vmware_ip', self.vmware_ip)
                    self.vmware_port = config.get('vmware_port', self.vmware_port)
                    self.reconnect_interval = config.get('reconnect_interval', self.reconnect_interval)
                    self.enable_logging = config.get('enable_logging', self.enable_logging)
                    if self.enable_logging:
                        print(f"[CONFIG] Loaded: vmware_ip={self.vmware_ip}, "
                              f"vmware_port={self.vmware_port}")
        except Exception as e:
            if self.enable_logging:
                print(f"[CONFIG] Load error: {e}")
    
    def _save_config(self):
        """Save config to JSON file"""
        try:
            config = {
                'vmware_ip': self.vmware_ip,
                'vmware_port': self.vmware_port,
                'reconnect_interval': self.reconnect_interval,
                'enable_logging': self.enable_logging
            }
            with open(self.CONFIG_PATH, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4)
        except Exception as e:
            if self.enable_logging:
                print(f"[CONFIG] Save error: {e}")
    
    def connect(self) -> bool:
        """Kết nối đến VMware receiver"""
        if not self.vmware_ip:
            print("[ERROR] VMware IP not set. Please configure vmware_ip in config file.")
            return False
        
        try:
            print(f"[CONNECT] Connecting to {self.vmware_ip}:{self.vmware_port}...")
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(5.0)  # 5s timeout for connect
            self.socket.connect((self.vmware_ip, self.vmware_port))
            self.socket.settimeout(None)  # No timeout after connect
            self.connected = True
            
            print(f"[CONNECT] ✓ Connected successfully to {self.vmware_ip}:{self.vmware_port}")
            return True
        except socket.timeout:
            print(f"[ERROR] Connection timeout to {self.vmware_ip}:{self.vmware_port}")
            print("[ERROR] Check if VMware receiver is running and firewall allows connection")
            self.connected = False
            if self.socket:
                try:
                    self.socket.close()
                except:
                    pass
                self.socket = None
            return False
        except Exception as e:
            print(f"[ERROR] Failed to connect to {self.vmware_ip}:{self.vmware_port}: {e}")
            print(f"[ERROR] Error type: {type(e).__name__}")
            self.connected = False
            if self.socket:
                try:
                    self.socket.close()
                except:
                    pass
                self.socket = None
            return False
    
    def disconnect(self):
        """Ngắt kết nối"""
        self.connected = False
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
            self.socket = None
        print("[DISCONNECT] Disconnected from VMware")
    
    def _auto_reconnect_loop(self):
        """Auto-reconnect thread"""
        while self.running:
            if not self.connected:
                print(f"[RECONNECT] Attempting to reconnect... (next try in {self.reconnect_interval}s)")
                if self.connect():
                    self.stats['total_reconnects'] += 1
                    print(f"[RECONNECT] ✓ Reconnected successfully (total reconnects: {self.stats['total_reconnects']})")
            time.sleep(self.reconnect_interval)
    
    def send_key(self, key: str, action: str) -> bool:
        """
        Gửi key command đến VMware
        Args:
            key: Tên phím (vd: 'a', 'space', 'ctrl')
            action: 'down' hoặc 'up'
        Returns:
            True if sent successfully, False otherwise
        """
        if not self.connected or not self.socket:
            if self.enable_logging:
                print(f"[ERROR] Not connected: {action}:{key}")
            return False
        
        try:
            command = f"{action}:{key}\n"
            bytes_sent = self.socket.send(command.encode('utf-8'))
            
            if bytes_sent == 0:
                if self.enable_logging:
                    print(f"[ERROR] Failed to send: {action}:{key}")
                self.connected = False
                return False
            
            self.stats['total_sent'] += 1
            if self.enable_logging:
                print(f"[SEND] {action}:{key} ({bytes_sent} bytes)")
            return True
            
        except Exception as e:
            print(f"[ERROR] Send error: {e}")
            self.connected = False
            self.stats['total_errors'] += 1
            return False
    
    def send_all_up(self) -> bool:
        """Gửi lệnh release tất cả keys"""
        if not self.connected or not self.socket:
            if self.enable_logging:
                print("[ERROR] Not connected: all_up")
            return False
        
        try:
            command = "all_up\n"
            bytes_sent = self.socket.send(command.encode('utf-8'))
            
            if bytes_sent == 0:
                if self.enable_logging:
                    print("[ERROR] Failed to send: all_up")
                self.connected = False
                return False
            
            self.stats['total_sent'] += 1
            if self.enable_logging:
                print(f"[SEND] all_up ({bytes_sent} bytes)")
            return True
            
        except Exception as e:
            print(f"[ERROR] Send error: {e}")
            self.connected = False
            self.stats['total_errors'] += 1
            return False
    
    def start(self):
        """Bắt đầu sender với auto-reconnect"""
        if not self.vmware_ip:
            print("[ERROR] VMware IP not configured. Please set vmware_ip in config file.")
            input("\nPress Enter to close...")
            return
        
        self.running = True
        
        print(f"\n[CONFIG] VMware IP: {self.vmware_ip}")
        print(f"[CONFIG] VMware Port: {self.vmware_port}")
        print(f"[CONFIG] Reconnect Interval: {self.reconnect_interval}s")
        print(f"[CONFIG] Logging: {self.enable_logging}")
        
        # Initial connect
        print(f"\n[CONNECT] Attempting to connect to {self.vmware_ip}:{self.vmware_port}...")
        if not self.connect():
            print(f"[WARN] Initial connection failed. Auto-reconnect will attempt every {self.reconnect_interval}s")
        
        # Start auto-reconnect thread
        self.reconnect_thread = threading.Thread(target=self._auto_reconnect_loop, daemon=True)
        self.reconnect_thread.start()
        
        print("[START] Host sender started with auto-reconnect")
        print(f"[STATUS] Connection: {'CONNECTED' if self.connected else 'DISCONNECTED'}")
        print(f"[STATUS] Press Ctrl+C to exit\n")
    
    def stop(self):
        """Dừng sender"""
        self.running = False
        
        if self.reconnect_thread and self.reconnect_thread.is_alive():
            self.reconnect_thread.join(timeout=2.0)
        
        self.disconnect()
        
        # Print stats
        print(f"\n{'='*50}")
        print("=== FINAL STATISTICS ===")
        print(f"{'='*50}")
        print(f"Connection: {'CONNECTED' if self.connected else 'DISCONNECTED'}")
        print(f"Total sent: {self.stats['total_sent']}")
        print(f"Total errors: {self.stats['total_errors']}")
        print(f"Total reconnects: {self.stats['total_reconnects']}")
        if self.stats['total_sent'] > 0:
            error_rate = (self.stats['total_errors'] / self.stats['total_sent'] * 100)
            print(f"Error rate: {error_rate:.1f}%")
        print(f"{'='*50}\n")
        
        # Save config
        self._save_config()
    
    def print_stats(self):
        """Print statistics"""
        print("\n=== STATISTICS ===")
        print(f"Connected: {self.connected}")
        print(f"Total sent: {self.stats['total_sent']}")
        print(f"Total errors: {self.stats['total_errors']}")
        print(f"Total reconnects: {self.stats['total_reconnects']}")


# Example usage
if __name__ == "__main__":
    import sys
    
    # Parse command line arguments
    vmware_ip = None
    if len(sys.argv) > 1:
        vmware_ip = sys.argv[1]
    
    vmware_port = 12345
    if len(sys.argv) > 2:
        vmware_port = int(sys.argv[2])
    
    enable_logging = False
    if len(sys.argv) > 3:
        enable_logging = sys.argv[3].lower() in ['true', '1', 'yes', 'on']
    
    try:
        sender = HostSender(vmware_ip=vmware_ip, vmware_port=vmware_port, enable_logging=enable_logging)
        sender.start()
        
        print("\n[INFO] Host sender running. Use sender.send_key(key, action) to send commands.")
        print("[INFO] Example: sender.send_key('a', 'down'), sender.send_key('a', 'up')")
        print("[INFO] Press Ctrl+C to exit\n")
        
        # Keep running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n[INTERRUPT] Keyboard interrupt received")
        
        sender.stop()
        
    except KeyboardInterrupt:
        print("\n[INTERRUPT] Keyboard interrupt received")
        if 'sender' in locals():
            sender.stop()
        print("[EXIT] Shutting down...")
    except Exception as e:
        import traceback
        print(f"\n{'='*50}")
        print(f"=== INITIALIZATION ERROR ===")
        print(f"{'='*50}")
        print(f"Error: {e}")
        print(f"Error type: {type(e).__name__}")
        print(f"\n=== Error Details ===")
        traceback.print_exc()
        print(f"=== End Error Details ===\n")
        print(f"{'='*50}\n")
        input("Press Enter to close...")

