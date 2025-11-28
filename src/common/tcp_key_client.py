"""TCP client used to forward key commands to vmware_receiver.py running in the VM."""

from __future__ import annotations

import socket
import threading
import time
from typing import Optional

from src.common.logger import get_logger

log = get_logger(__name__)


class TcpKeyClient:
    """Maintains a TCP connection to vmware_receiver and sends key commands."""

    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 12345,
        reconnect_interval: float = 2.0,
        auto_reconnect: bool = True,
    ):
        self.host = host
        self.port = port
        self.reconnect_interval = max(0.5, reconnect_interval)
        self.auto_reconnect = auto_reconnect
        self.socket: Optional[socket.socket] = None
        self.lock = threading.Lock()
        self.connected = False
        self._stop = False
        self._bg_thread: Optional[threading.Thread] = None

    def start(self):
        """Start background thread to maintain TCP connection."""
        if self._bg_thread and self._bg_thread.is_alive():
            return

        self._stop = False
        if self.auto_reconnect:
            self._bg_thread = threading.Thread(
                target=self._maintain_connection, daemon=True
            )
            self._bg_thread.start()
        else:
            self._connect()

    def stop(self):
        """Stop background thread and close connection."""
        self._stop = True
        if self._bg_thread:
            self._bg_thread.join(timeout=1.0)

        with self.lock:
            if self.socket:
                try:
                    self.socket.close()
                except Exception:
                    pass
                self.socket = None
            self.connected = False

    def _maintain_connection(self):
        """Background thread: connect and keep connection open."""
        while not self._stop:
            if not self.connected:
                self._connect()
            time.sleep(self.reconnect_interval)

    def _connect(self):
        """Attempt to connect once."""
        with self.lock:
            if self.socket:
                return
            try:
                sock = socket.create_connection((self.host, self.port), timeout=3.0)
                self.socket = sock
                self.connected = True
                log.info("TCP key client connected to %s:%s", self.host, self.port)
            except Exception as exc:
                self.socket = None
                self.connected = False
                log.warning(
                    "TCP key client failed to connect to %s:%s (%s)",
                    self.host,
                    self.port,
                    exc,
                )

    def send(self, payload: str):
        """Send raw command line."""
        with self.lock:
            if not self.socket:
                raise RuntimeError("TCP key client not connected")
            try:
                self.socket.sendall(payload.encode("utf-8") + b"\n")
            except Exception as exc:
                log.warning("TCP key client send failed (%s)", exc)
                try:
                    self.socket.close()
                except Exception:
                    pass
                self.socket = None
                self.connected = False
                raise

    def close(self):
        self.stop()

    def send_key(self, action: str, key: Optional[str]):
        action = action.lower()
        if action not in ("down", "up"):
            raise ValueError(f"Unsupported action: {action}")
        if not key:
            raise ValueError("Key is required for down/up actions")
        self.send(f"{action}:{key}")

    def send_down(self, key: str):
        self.send_key("down", key)

    def send_up(self, key: str):
        self.send_key("up", key)

    def send_all_up(self):
        self.send("all_up")
