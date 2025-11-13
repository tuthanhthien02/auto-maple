"""
GUI Settings Panel for VM Input Blocker + Force Arduino Output
"""
import tkinter as tk
from src.gui.interfaces import LabelFrame, Frame
from src.common.interfaces import Configurable
from src.common import config
from src.common.logger import get_logger

log = get_logger(__name__)

# Constants for settings keys
VM_INPUT_BLOCKER_ENABLED_KEY = 'VM Input Blocker Enabled'


class VMInputBlockerSettings(Configurable):
    """Settings manager for VM Input Blocker"""
    DEFAULT_CONFIG = {
        VM_INPUT_BLOCKER_ENABLED_KEY: False
    }

    def get(self, key):
        return self.config.get(key, self.DEFAULT_CONFIG.get(key))

    def set(self, key, value):
        self.config[key] = value


class VMInputBlocker(LabelFrame):
    """GUI Panel for VM Input Blocker settings"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, 'VM Input Blocker + Force Arduino', **kwargs)
        
        self.settings = VMInputBlockerSettings('vm_input_blocker')
        
        # Load settings - ensure default is False (disabled)
        enabled = self.settings.get(VM_INPUT_BLOCKER_ENABLED_KEY)
        if not isinstance(enabled, bool):
            enabled = False
        
        # Force disable on first load if config says disabled
        if not hasattr(config, '_vm_input_blocker_gui_loaded'):
            if config.block_vm_input is False and config.force_arduino_output is False:
                enabled = False
                self.settings.set(VM_INPUT_BLOCKER_ENABLED_KEY, False)
            self.settings.save_config()
            config._vm_input_blocker_gui_loaded = True
        
        # Single checkbox: Block VM Input + Force Arduino Output
        self.enabled_var = tk.BooleanVar(value=enabled)
        enabled_check = tk.Checkbutton(
            self,
            variable=self.enabled_var,
            text='Block VM Input + Force Arduino Output',
            command=self._on_enabled_change
        )
        enabled_check.pack(side=tk.TOP, anchor='w', padx=5, pady=5)
        
        # Description label
        desc_label = tk.Label(
            self,
            text='Block input từ VM hardware và force dùng Arduino (dùng chung COM với bot)',
            fg='gray',
            font=('TkDefaultFont', 8)
        )
        desc_label.pack(side=tk.TOP, anchor='w', padx=20, pady=(0, 5))
        
        # Warning label
        self.warning_label = tk.Label(
            self,
            text='⚠️ Cần Arduino connected để sử dụng tính năng này',
            fg='orange',
            font=('TkDefaultFont', 8)
        )
        self.warning_label.pack(side=tk.TOP, anchor='w', padx=5, pady=2)
        
        # Status label
        self.status_label = tk.Label(
            self,
            text='Status: Disabled',
            fg='gray'
        )
        self.status_label.pack(side=tk.TOP, anchor='w', padx=5, pady=2)
        
        # Arduino connection status
        self.arduino_status_label = tk.Label(
            self,
            text='Arduino: Not Connected',
            fg='red'
        )
        self.arduino_status_label.pack(side=tk.TOP, anchor='w', padx=5, pady=2)
        
        # Sync with config
        self._sync_to_config()
        
        # Update status
        self._update_status()
        
        # Ensure default is disabled on first load
        if not hasattr(config, '_vm_input_blocker_initialized'):
            if (config.block_vm_input or config.force_arduino_output) and not enabled:
                config.block_vm_input = False
                config.force_arduino_output = False
            config._vm_input_blocker_initialized = True
    
    def _sync_to_config(self):
        """Sync settings to config module"""
        try:
            enabled = self.settings.get(VM_INPUT_BLOCKER_ENABLED_KEY)
            
            # When enabled, set both block_vm_input and force_arduino_output to True
            config.block_vm_input = enabled
            config.force_arduino_output = enabled
            
            log.debug(f"[VM_INPUT_BLOCKER_GUI] Synced to config: enabled={enabled} (block_vm_input={enabled}, force_arduino={enabled})")
        except Exception as e:
            log.warning(f"[VM_INPUT_BLOCKER_GUI] Failed to sync to config: {e}")
    
    def _on_enabled_change(self):
        """Handle enabled checkbox change"""
        enabled = self.enabled_var.get()
        self.settings.set(VM_INPUT_BLOCKER_ENABLED_KEY, enabled)
        self.settings.save_config()
        self._sync_to_config()
        self._toggle_vm_input_blocker(enabled)
        log.info(f"[VM_INPUT_BLOCKER_GUI] VM Input Blocker changed to: {enabled}")
    
    def _toggle_vm_input_blocker(self, enabled):
        """Toggle VM Input Blocker based on settings"""
        try:
            # Check Arduino connection if enabled (force_arduino_output requires Arduino)
            if enabled:
                from src.common.shared_arduino_connection import SharedArduinoConnection
                arduino_conn = SharedArduinoConnection.get_instance()
                if not arduino_conn.is_connected():
                    log.warning("[VM_INPUT_BLOCKER_GUI] Enabled but Arduino not connected! Disabling...")
                    self.enabled_var.set(False)
                    self.settings.set(VM_INPUT_BLOCKER_ENABLED_KEY, False)
                    self.settings.save_config()
                    enabled = False
                    config.block_vm_input = False
                    config.force_arduino_output = False
                    self._update_status()
                    return
            
            # Enable/disable VM Input Blocker
            if enabled:
                if not config.vm_input_blocker:
                    log.info("[VM_INPUT_BLOCKER_GUI] Starting VM Input Blocker...")
                    from src.modules.vm_input_blocker import VMInputBlocker
                    config.vm_input_blocker = VMInputBlocker(enable_logging=False)
                    
                    # Install hook
                    if config.vm_input_blocker.install_hook():
                        log.info("[VM_INPUT_BLOCKER_GUI] ✅ VM Input Blocker started successfully")
                    else:
                        log.error("[VM_INPUT_BLOCKER_GUI] Failed to start VM Input Blocker")
                        config.vm_input_blocker = None
                        self.enabled_var.set(False)
                        self.settings.set(VM_INPUT_BLOCKER_ENABLED_KEY, False)
                        self.settings.save_config()
                        config.block_vm_input = False
                        config.force_arduino_output = False
                        return
                
                # Start blocking
                config.vm_input_blocker.start_blocking()
                log.info("[VM_INPUT_BLOCKER_GUI] ✅ Blocking VM input and forcing Arduino output")
            else:
                # Disable
                if config.vm_input_blocker:
                    log.info("[VM_INPUT_BLOCKER_GUI] Stopping VM Input Blocker...")
                    try:
                        config.vm_input_blocker.stop_blocking()
                        config.vm_input_blocker.uninstall_hook()
                    except Exception as cleanup_error:
                        log.warning(f"[VM_INPUT_BLOCKER_GUI] Error during cleanup: {cleanup_error}")
                    finally:
                        # Always set to None to ensure cleanup
                        config.vm_input_blocker = None
                        config.block_vm_input = False
                        config.force_arduino_output = False
                    log.info("[VM_INPUT_BLOCKER_GUI] ✅ VM Input Blocker stopped")
                else:
                    # Ensure config is synced even if blocker doesn't exist
                    config.block_vm_input = False
                    config.force_arduino_output = False
            
            self._update_status()
            
        except Exception as e:
            log.error(f"[VM_INPUT_BLOCKER_GUI] Error toggling VM Input Blocker: {e}")
    
    def _update_status(self):
        """Update status labels"""
        try:
            enabled = self.enabled_var.get()
            
            # Update main status
            if enabled:
                if config.vm_input_blocker and config.vm_input_blocker.is_blocking():
                    self.status_label.config(text='Status: Blocking VM Input + Force Arduino', fg='green')
                else:
                    self.status_label.config(text='Status: Enabled', fg='green')
            else:
                self.status_label.config(text='Status: Disabled', fg='gray')
            
            # Update Arduino status
            try:
                from src.common.shared_arduino_connection import SharedArduinoConnection
                arduino_conn = SharedArduinoConnection.get_instance()
                if arduino_conn.is_connected():
                    self.arduino_status_label.config(text='Arduino: Connected', fg='green')
                else:
                    self.arduino_status_label.config(text='Arduino: Not Connected', fg='red')
            except Exception:
                self.arduino_status_label.config(text='Arduino: Unknown', fg='gray')
                
        except Exception as e:
            log.debug(f"[VM_INPUT_BLOCKER_GUI] Error updating status: {e}")
    
    def refresh_status(self):
        """Refresh status (called periodically)"""
        self._update_status()

