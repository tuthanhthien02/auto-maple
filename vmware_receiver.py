"""
VMware Receiver - TCP Server để nhận input từ Host và forward đến Arduino
Nhận key commands từ Host sender và forward qua Serial đến Arduino
"""
import socket
import serial
import serial.tools.list_ports
import threading
import json
import os
import sys
import time

# Ensure console can print UTF-8
try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass


class VMwareReceiver:
    """TCP Server nhận commands từ Host và forward đến Arduino"""
    
    def __init__(self, com_port=None, baudrate=115200, server_port=12345, 
                 block_local_input=False, enable_logging=False):
        self.serial = None
        self.com_port = com_port
        self.baudrate = baudrate
        self.server_port = server_port
        self.block_local_input = block_local_input
        self.enable_logging = enable_logging
        
        self.server_socket = None
        self.running = False
        self.client_socket = None
        self.client_address = None
        
        # Stats
        self.stats = {
            'total_received': 0,
            'total_forwarded': 0,
            'total_errors': 0,
            'total_clients': 0
        }
        
        # Config
        self.CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'vmware_receiver.config.json')
        self._load_config()
    
    def _load_config(self):
        """Load config from JSON file"""
        try:
            if os.path.exists(self.CONFIG_PATH):
                with open(self.CONFIG_PATH, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.com_port = config.get('com_port', self.com_port)
                    self.baudrate = config.get('baudrate', self.baudrate)
                    self.server_port = config.get('server_port', self.server_port)
                    self.block_local_input = config.get('block_local_input', self.block_local_input)
                    self.enable_logging = config.get('enable_logging', self.enable_logging)
                    if self.enable_logging:
                        print(f"[CONFIG] Loaded: com_port={self.com_port}, "
                              f"server_port={self.server_port}")
        except Exception as e:
            if self.enable_logging:
                print(f"[CONFIG] Load error: {e}")
    
    def _save_config(self):
        """Save config to JSON file"""
        try:
            config = {
                'com_port': self.com_port,
                'baudrate': self.baudrate,
                'server_port': self.server_port,
                'block_local_input': self.block_local_input,
                'enable_logging': self.enable_logging
            }
            with open(self.CONFIG_PATH, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4)
        except Exception as e:
            if self.enable_logging:
                print(f"[CONFIG] Save error: {e}")
    
    def find_arduino_port(self):
        """Tự động tìm COM port của Arduino"""
        ports = serial.tools.list_ports.comports()
        arduino_keywords = ['arduino', 'micro', 'leonardo', 'ch340', 'cp210']
        
        for port in ports:
            port_desc = port.description.lower()
            port_name = port.device.lower()
            
            for keyword in arduino_keywords:
                if keyword in port_desc or keyword in port_name:
                    return port.device
        
        return None
    
    def connect_arduino(self) -> bool:
        """Kết nối với Arduino"""
        if not self.com_port:
            print("[ARDUINO] Auto-detecting Arduino port...")
            self.com_port = self.find_arduino_port()
        
        if not self.com_port:
            print("[ERROR] Arduino not found. Please specify COM port in config file.")
            print("[ERROR] Available ports:")
            ports = serial.tools.list_ports.comports()
            for port in ports:
                print(f"[ERROR]   - {port.device}: {port.description}")
            return False
        
        try:
            print(f"[ARDUINO] Connecting to {self.com_port} at {self.baudrate} baud...")
            self.serial = serial.Serial(
                self.com_port,
                self.baudrate,
                timeout=0.1,
                write_timeout=0.1,
                inter_byte_timeout=0.01
            )
            time.sleep(0.5)
            print(f"[ARDUINO] ✓ Connected successfully to {self.com_port} (baudrate: {self.baudrate})")
            # Sync state: release all keys
            self.send_all_up()
            print(f"[ARDUINO] Initialized - all keys released")
            return True
        except serial.SerialException as e:
            print(f"[ERROR] Serial connection error: {e}")
            print(f"[ERROR] Check if Arduino is connected and {self.com_port} is correct")
            return False
        except Exception as e:
            print(f"[ERROR] Failed to connect Arduino: {e}")
            print(f"[ERROR] Error type: {type(e).__name__}")
            return False
    
    def send_key_to_arduino(self, key_name: str, action: str) -> bool:
        """
        Gửi command đến Arduino
        Format: <action>:<key>\n
        Returns: True if sent successfully, False otherwise
        """
        if not self.serial or not self.serial.is_open:
            if self.enable_logging:
                print(f"[ERROR] Serial not connected: {action}:{key_name}")
            return False
        
        try:
            command = f"{action}:{key_name}\n"
            bytes_written = self.serial.write(command.encode('utf-8'))
            self.serial.flush()
            
            if bytes_written == 0:
                if self.enable_logging:
                    print(f"[ERROR] Failed to write: {action}:{key_name}")
                return False
            
            self.stats['total_forwarded'] += 1
            if self.enable_logging:
                print(f"[FORWARD] {action}:{key_name} ({bytes_written} bytes)")
            return True
            
        except Exception as e:
            print(f"[ERROR] Send error: {e}")
            self.stats['total_errors'] += 1
            return False
    
    def send_all_up(self):
        """Gửi lệnh release tất cả keys đến Arduino"""
        try:
            if self.serial and self.serial.is_open:
                self.serial.write(b"all_up\n")
                self.serial.flush()
                if self.enable_logging:
                    print("[FORWARD] all_up")
        except Exception as e:
            print(f"[ERROR] Send all_up error: {e}")
    
    def handle_client(self, client_socket, client_address):
        """Xử lý client connection"""
        self.client_socket = client_socket
        self.client_address = client_address
        self.stats['total_clients'] += 1
        
        print(f"[CLIENT] ✓ Connected from {client_address[0]}:{client_address[1]}")
        print(f"[STATUS] Client: CONNECTED ({client_address[0]}:{client_address[1]})")
        
        try:
            buffer = ""
            while self.running:
                data = client_socket.recv(1024)
                if not data:
                    break
                
                buffer += data.decode('utf-8', errors='ignore')
                
                # Process complete commands (ending with \n)
                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    line = line.strip()
                    
                    if line:
                        self.stats['total_received'] += 1
                        self.process_command(line)
                
        except Exception as e:
            print(f"[ERROR] Client handler error: {e}")
            print(f"[ERROR] Error type: {type(e).__name__}")
        finally:
            print(f"[CLIENT] ✗ Disconnected from {client_address[0]}:{client_address[1]}")
            print(f"[STATUS] Client: DISCONNECTED")
            try:
                client_socket.close()
            except:
                pass
            self.client_socket = None
            self.client_address = None
    
    def process_command(self, command: str):
        """
        Xử lý command từ Host
        Commands: "down:<key>", "up:<key>", "all_up"
        """
        command = command.strip()
        
        if not command:
            return
        
        if command == "all_up":
            self.send_all_up()
            return
        
        # Parse: "action:key"
        if ':' not in command:
            if self.enable_logging:
                print(f"[WARN] Invalid command format: {command}")
            return
        
        action, key_name = command.split(':', 1)
        action = action.strip().lower()
        key_name = key_name.strip().lower()
        
        if action in ('down', 'up'):
            self.send_key_to_arduino(key_name, action)
        else:
            if self.enable_logging:
                print(f"[WARN] Unknown action: {action}")
    
    def start_server(self):
        """Bắt đầu TCP server"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind(('0.0.0.0', self.server_port))
            self.server_socket.listen(5)
            self.server_socket.settimeout(1.0)  # Timeout for accept to check running flag
            
            print(f"[SERVER] ✓ TCP server started on port {self.server_port}")
            print(f"[SERVER] Listening for Host sender connection...")
            print(f"[STATUS] Arduino: {'CONNECTED' if (self.serial and self.serial.is_open) else 'DISCONNECTED'}")
            print(f"[STATUS] Client: Waiting...")
            print(f"[STATUS] Press Ctrl+C to exit\n")
            
            self.running = True
            
            while self.running:
                try:
                    client_socket, client_address = self.server_socket.accept()
                    # Handle client in separate thread (for now, single client)
                    # If new client connects, close old one
                    if self.client_socket:
                        try:
                            self.client_socket.close()
                        except:
                            pass
                    
                    client_thread = threading.Thread(
                        target=self.handle_client,
                        args=(client_socket, client_address),
                        daemon=True
                    )
                    client_thread.start()
                    
                except socket.timeout:
                    continue
                except Exception as e:
                    if self.running:
                        print(f"[ERROR] Accept error: {e}")
                    break
            
        except Exception as e:
            print(f"[ERROR] Server error: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.stop()
    
    def start(self):
        """Bắt đầu receiver - connect Arduino và start server"""
        print(f"\n[CONFIG] COM Port: {self.com_port or 'AUTO-DETECT'}")
        print(f"[CONFIG] Baudrate: {self.baudrate}")
        print(f"[CONFIG] Server Port: {self.server_port}")
        print(f"[CONFIG] Logging: {self.enable_logging}")
        
        # Connect Arduino (retry until success)
        print(f"\n[ARDUINO] Connecting to Arduino...")
        retry_count = 0
        while True:
            if self.connect_arduino():
                break
            retry_count += 1
            print(f"[RETRY] Arduino connection failed (attempt {retry_count}). Retrying in 2s...")
            time.sleep(2.0)
        
        # Start TCP server
        print(f"\n[SERVER] Starting TCP server on port {self.server_port}...")
        self.start_server()
    
    def stop(self):
        """Dừng receiver"""
        self.running = False
        
        # Close client connection
        if self.client_socket:
            try:
                self.client_socket.close()
            except:
                pass
            self.client_socket = None
        
        # Close server socket
        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass
            self.server_socket = None
        
        # Close Arduino
        if self.serial and self.serial.is_open:
            self.send_all_up()  # Release all keys before closing
            self.serial.close()
            print("[ARDUINO] Disconnected")
        
        # Print stats
        print(f"\n{'='*50}")
        print("=== FINAL STATISTICS ===")
        print(f"{'='*50}")
        print(f"Total received: {self.stats['total_received']}")
        print(f"Total forwarded: {self.stats['total_forwarded']}")
        print(f"Total errors: {self.stats['total_errors']}")
        print(f"Total clients: {self.stats['total_clients']}")
        if self.stats['total_received'] > 0:
            success_rate = (self.stats['total_forwarded'] / self.stats['total_received'] * 100)
            print(f"Success rate: {success_rate:.1f}%")
        print(f"{'='*50}\n")
        
        # Save config
        self._save_config()
    
    def print_stats(self):
        """Print statistics"""
        print("\n=== STATISTICS ===")
        print(f"Arduino connected: {self.serial and self.serial.is_open}")
        print(f"Client connected: {self.client_socket is not None}")
        print(f"Total received: {self.stats['total_received']}")
        print(f"Total forwarded: {self.stats['total_forwarded']}")
        print(f"Total errors: {self.stats['total_errors']}")
        print(f"Total clients: {self.stats['total_clients']}")


# Example usage
if __name__ == "__main__":
    import sys
    
    # Parse command line arguments
    com_port = None
    if len(sys.argv) > 1:
        com_port = sys.argv[1]
    
    baudrate = 115200
    if len(sys.argv) > 2:
        baudrate = int(sys.argv[2])
    
    server_port = 12345
    if len(sys.argv) > 3:
        server_port = int(sys.argv[3])
    
    enable_logging = False
    if len(sys.argv) > 4:
        enable_logging = sys.argv[4].lower() in ['true', '1', 'yes', 'on']
    
    try:
        receiver = VMwareReceiver(
            com_port=com_port,
            baudrate=baudrate,
            server_port=server_port,
            enable_logging=enable_logging
        )
        receiver.start()
        
    except KeyboardInterrupt:
        print("\n[INTERRUPT] Keyboard interrupt received")
        if 'receiver' in locals():
            receiver.stop()
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

