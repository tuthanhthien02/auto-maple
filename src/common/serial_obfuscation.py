"""
Serial obfuscation utilities for Arduino communication.

The goal is giảm khả năng nhận diện bằng cách:
    - Sử dụng frame nhị phân thay vì ASCII plain-text.
    - Thêm handshake tạo session key ngẫu nhiên cho mỗi kết nối.
    - XOR payload với keystream sinh từ HMAC-SHA256.

Firmware phía Arduino cần implement cùng giao thức để giải mã.
"""

import hashlib
import hmac
import os
from typing import List

from src.common.logger import get_logger

log = get_logger(__name__)


class SerialObfuscator:
    """
    Obfuscates command payloads trước khi gửi xuống Arduino.

    Frame format:
        [0]    : 0x7E (START byte)
        [1]    : counter (8-bit, rollover)
        [2]    : payload length (8-bit)
        [3..n] : payload XOR keystream
        [n+1]  : checksum = (counter + sum(obfuscated payload)) % 256

    Handshake frame (gửi một lần đầu kết nối):
        START(0x7E) + 0xFF + 0x10 + session_key(16B) + checksum
    """

    START_BYTE = 0x7E
    HANDSHAKE_COUNTER = 0xFF
    HANDSHAKE_LENGTH = 16

    def __init__(self, enabled: bool = True):
        self.enabled = enabled
        self._session_key = os.urandom(self.HANDSHAKE_LENGTH)
        self._counter = 0
        self._handshake_sent = False

    def reset(self):
        """Reset state khi reconnect."""
        self._counter = 0
        self._session_key = os.urandom(self.HANDSHAKE_LENGTH)
        self._handshake_sent = False

    def encode_command(self, action: str, key: str = None) -> List[bytes]:
        """
        Encode command thành frame nhị phân. Trả về list frame (có thể gồm handshake).

        Args:
            action: 'down' | 'up' | 'all_up'
            key: tên phím (None nếu all_up)
        """
        if not self.enabled:
            payload = self._build_ascii_payload(action, key)
            return [payload]

        frames: List[bytes] = []

        if not self._handshake_sent:
            frames.append(self._build_handshake_frame())
            self._handshake_sent = True

        payload = self._build_payload(action, key)
        frames.append(self._build_obfuscated_frame(payload))

        return frames

    def _build_ascii_payload(self, action: str, key: str = None) -> bytes:
        if action == "all_up":
            return b"all_up\n"
        if not key:
            raise ValueError("Key is required for action %s" % action)
        return f"{action}:{key}\n".encode("utf-8")

    def _build_handshake_frame(self) -> bytes:
        checksum = (self.HANDSHAKE_COUNTER + sum(self._session_key)) & 0xFF
        frame = (
            bytes([self.START_BYTE, self.HANDSHAKE_COUNTER, self.HANDSHAKE_LENGTH])
            + self._session_key
            + bytes([checksum])
        )
        log.debug("[SerialObfuscator] Handshake frame generated")
        return frame

    def _build_payload(self, action: str, key: str = None) -> bytes:
        if action == "all_up":
            return b"all_up"
        if not key:
            raise ValueError("Key is required for action %s" % action)
        return f"{action}:{key}".encode("utf-8")

    def _build_obfuscated_frame(self, payload: bytes) -> bytes:
        self._counter = (self._counter + 1) % 256
        counter_byte = self._counter.to_bytes(1, "big")
        keystream = self._derive_keystream(counter_byte, len(payload))
        obfuscated = bytes(p ^ k for p, k in zip(payload, keystream))
        checksum = (self._counter + sum(obfuscated)) & 0xFF
        frame = (
            bytes([self.START_BYTE])
            + counter_byte
            + len(obfuscated).to_bytes(1, "big")
            + obfuscated
            + bytes([checksum])
        )
        return frame

    def _derive_keystream(self, counter: bytes, length: int) -> bytes:
        """
        Sinh keystream dùng HMAC-SHA256(session_key, counter || block_index)
        """
        stream = bytearray()
        block_index = 0
        while len(stream) < length:
            block_index_bytes = block_index.to_bytes(2, "big")
            digest = hmac.new(
                self._session_key, counter + block_index_bytes, hashlib.sha256
            ).digest()
            stream.extend(digest)
            block_index += 1
        return bytes(stream[:length])
