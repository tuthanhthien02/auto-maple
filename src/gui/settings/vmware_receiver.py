"""
GUI Settings Panel for VMware Receiver Integration
"""
import tkinter as tk
from src.gui.interfaces import LabelFrame, Frame
from src.common.interfaces import Configurable
from src.common import config
from src.common.logger import get_logger

log = get_logger(__name__)

# Constants for settings keys
VMWARE_RECEIVER_ENABLED_KEY = 'VMware Receiver Enabled'
VMWARE_RECEIVER_PORT_KEY = 'VMware Receiver Port'
VMWARE_RECEIVER_HOTKEY_HOOK_KEY = 'VMware Receiver Hotkey Hook'


class VMwareReceiverSettings(Configurable):
    """Settings manager for VMware Receiver"""
    DEFAULT_CONFIG = {
        VMWARE_RECEIVER_ENABLED_KEY: False,
        VMWARE_RECEIVER_PORT_KEY: 12345,
        VMWARE_RECEIVER_HOTKEY_HOOK_KEY: False
    }

    def get(self, key):
        return self.config.get(key, self.DEFAULT_CONFIG.get(key))

    def set(self, key, value):
        self.config[key] = value


class VMwareReceiver(LabelFrame):
    """GUI Panel for VMware Receiver settings"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, 'VMware Receiver', **kwargs)
        
        self.settings = VMwareReceiverSettings('vmware_receiver')
        
        # Load settings
        enabled = self.settings.get(VMWARE_RECEIVER_ENABLED_KEY)
        if not isinstance(enabled, bool):
            enabled = False
        
        port = self.settings.get(VMWARE_RECEIVER_PORT_KEY)
        try:
            port = int(port) if port else 12345
            if port < 1 or port > 65535:
                port = 12345
        except (ValueError, TypeError):
            port = 12345
        
        hotkey_hook = self.settings.get(VMWARE_RECEIVER_HOTKEY_HOOK_KEY)
        if not isinstance(hotkey_hook, bool):
            hotkey_hook = False
        
        # Enable/Disable checkbox
        self.enabled_var = tk.BooleanVar(value=enabled)
        enabled_check = tk.Checkbutton(
            self,
            variable=self.enabled_var,
            text='Enable VMware Receiver (TCP Server)',
            command=self._on_enabled_change
        )
        enabled_check.pack(side=tk.TOP, anchor='w', padx=5, pady=5)
        
        # Status label
        self.status_label = tk.Label(
            self,
            text='Status: Not Running',
            fg='gray'
        )
        self.status_label.pack(side=tk.TOP, anchor='w', padx=5, pady=2)
        
        # Settings frame (only enabled when checkbox is checked)
        self.settings_frame = Frame(self)
        self.settings_frame.pack(side=tk.TOP, fill='x', expand=True, padx=5, pady=5)
        
        # Port setting
        port_row = Frame(self.settings_frame)
        port_row.pack(side=tk.TOP, fill='x', expand=True, pady=2)
        
        port_label = tk.Label(port_row, text='TCP Server Port:')
        port_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.port_var = tk.StringVar(value=str(port))
        port_entry = tk.Entry(port_row, textvariable=self.port_var, width=10)
        port_entry.pack(side=tk.LEFT)
        port_entry.bind('<FocusOut>', self._on_port_change)
        
        # Hotkey hook checkbox
        self.hotkey_hook_var = tk.BooleanVar(value=hotkey_hook)
        hotkey_check = tk.Checkbutton(
            self.settings_frame,
            variable=self.hotkey_hook_var,
            text='Enable End Key Hotkey (Toggle Remapping)',
            command=self._on_hotkey_hook_change
        )
        hotkey_check.pack(side=tk.TOP, anchor='w', padx=5, pady=5)
        
        hotkey_note = tk.Label(
            self.settings_frame,
            text='Note: Hotkey hook causes delay. Disable for zero delay.',
            fg='gray',
            font=('TkDefaultFont', 8)
        )
        hotkey_note.pack(side=tk.TOP, anchor='w', padx=20, pady=(0, 5))
        
        # Update UI state
        self._update_ui_state()
        
        # Sync with config
        self._sync_to_config()
    
    def _update_ui_state(self):
        """Update UI state based on enabled checkbox"""
        enabled = self.enabled_var.get()
        if enabled:
            self.settings_frame.pack(side=tk.TOP, fill='x', expand=True, padx=5, pady=5)
        else:
            self.settings_frame.pack_forget()
    
    def _sync_to_config(self):
        """Sync settings to config module"""
        try:
            enabled = self.settings.get(VMWARE_RECEIVER_ENABLED_KEY)
            port = self.settings.get(VMWARE_RECEIVER_PORT_KEY)
            hotkey_hook = self.settings.get(VMWARE_RECEIVER_HOTKEY_HOOK_KEY)
            
            config.enable_vmware_receiver = enabled
            config.vmware_receiver_port = port
            config.vmware_receiver_hotkey_hook = hotkey_hook
            
            log.debug(f"[VMWARE_RECEIVER_GUI] Synced to config: enabled={enabled}, port={port}, hotkey_hook={hotkey_hook}")
        except Exception as e:
            log.warning(f"[VMWARE_RECEIVER_GUI] Failed to sync to config: {e}")
    
    def _on_enabled_change(self):
        """Callback when enabled checkbox changes"""
        enabled = self.enabled_var.get()
        self.settings.set(VMWARE_RECEIVER_ENABLED_KEY, enabled)
        self.settings.save_config()
        
        self._update_ui_state()
        self._sync_to_config()
        
        # Start/Stop VMware Receiver
        self._toggle_vmware_receiver(enabled)
        
        log.info(f"[VMWARE_RECEIVER_GUI] Enabled changed to: {enabled}")
    
    def _on_port_change(self, event=None):
        """Callback when port changes"""
        try:
            port_str = self.port_var.get().strip()
            if not port_str:
                port = 12345
            else:
                port = int(port_str)
                if port < 1 or port > 65535:
                    log.warning(f"[VMWARE_RECEIVER_GUI] Invalid port: {port}, using default 12345")
                    port = 12345
                    self.port_var.set(str(port))
        except ValueError:
            log.warning(f"[VMWARE_RECEIVER_GUI] Invalid port format, using default 12345")
            port = 12345
            self.port_var.set(str(port))
        
        self.settings.set(VMWARE_RECEIVER_PORT_KEY, port)
        self.settings.save_config()
        
        self._sync_to_config()
        
        # Restart VMware Receiver if running
        if config.vmware_receiver and config.vmware_receiver.is_running():
            log.info(f"[VMWARE_RECEIVER_GUI] Port changed to {port}, restarting server...")
            config.vmware_receiver.stop_tcp_server()
            config.vmware_receiver.server_port = port
            config.vmware_receiver.start_tcp_server()
            self._update_status()
        
        log.info(f"[VMWARE_RECEIVER_GUI] Port changed to: {port}")
    
    def _on_hotkey_hook_change(self):
        """Callback when hotkey hook checkbox changes"""
        hotkey_hook = self.hotkey_hook_var.get()
        self.settings.set(VMWARE_RECEIVER_HOTKEY_HOOK_KEY, hotkey_hook)
        self.settings.save_config()
        
        self._sync_to_config()
        
        # Restart VMware Receiver if running to apply hotkey hook setting
        if config.vmware_receiver and config.vmware_receiver.is_running():
            log.info(f"[VMWARE_RECEIVER_GUI] Hotkey hook changed to {hotkey_hook}, restarting server...")
            config.vmware_receiver.stop_tcp_server()
            config.vmware_receiver.enable_hotkey_hook = hotkey_hook
            config.vmware_receiver.start_tcp_server()
            self._update_status()
        
        log.info(f"[VMWARE_RECEIVER_GUI] Hotkey hook changed to: {hotkey_hook}")
    
    def _toggle_vmware_receiver(self, enabled: bool):
        """Start or stop VMware Receiver"""
        try:
            if enabled:
                # Start VMware Receiver
                if config.vmware_receiver and config.vmware_receiver.is_running():
                    log.info("[VMWARE_RECEIVER_GUI] VMware Receiver is already running")
                    self._update_status()
                    return
                
                log.info("[VMWARE_RECEIVER_GUI] Starting VMware Receiver...")
                from src.modules.vmware_receiver_integrated import VMwareReceiverIntegrated
                
                config.vmware_receiver = VMwareReceiverIntegrated(
                    server_port=config.vmware_receiver_port,
                    enable_hotkey_hook=config.vmware_receiver_hotkey_hook,
                    enable_logging=False
                )
                config.vmware_receiver.start_tcp_server()
                
                log.info("[VMWARE_RECEIVER_GUI] ✅ VMware Receiver started successfully")
            else:
                # Stop VMware Receiver
                if config.vmware_receiver:
                    log.info("[VMWARE_RECEIVER_GUI] Stopping VMware Receiver...")
                    config.vmware_receiver.stop_tcp_server()
                    log.info("[VMWARE_RECEIVER_GUI] ✅ VMware Receiver stopped")
                else:
                    log.debug("[VMWARE_RECEIVER_GUI] VMware Receiver is not running")
            
            self._update_status()
        except Exception as e:
            log.error(f"[VMWARE_RECEIVER_GUI] Error toggling VMware Receiver: {e}")
            import traceback
            traceback.print_exc()
            self._update_status()
    
    def _update_status(self):
        """Update status label"""
        try:
            # Check if widget still exists (might be destroyed)
            if not hasattr(self, 'status_label') or not self.status_label.winfo_exists():
                return
            
            if config.vmware_receiver and config.vmware_receiver.is_running():
                port = config.vmware_receiver.server_port
                try:
                    arduino_connected = config.vmware_receiver.shared_connection.is_connected()
                    arduino_status = "Connected" if arduino_connected else "Disconnected"
                except Exception:
                    arduino_status = "Unknown"
                self.status_label.config(
                    text=f'Status: Running on port {port} | Arduino: {arduino_status}',
                    fg='green'
                )
            else:
                self.status_label.config(
                    text='Status: Not Running',
                    fg='gray'
                )
        except tk.TclError:
            # Widget destroyed, ignore
            pass
        except Exception as e:
            log.debug(f"[VMWARE_RECEIVER_GUI] Error updating status: {e}")
            try:
                if hasattr(self, 'status_label') and self.status_label.winfo_exists():
                    self.status_label.config(
                        text='Status: Error',
                        fg='red'
                    )
            except:
                pass
    
    def refresh_status(self):
        """Refresh status (called periodically)"""
        self._update_status()

