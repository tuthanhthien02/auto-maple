"""
Log encryption utilities using AES-256-GCM.

Encrypts log message content to protect sensitive information in production builds.
Only message content is encrypted, metadata (timestamp, level, logger name) remains readable.

Key source: AUTO_MAPLE_LOG_ENCRYPTION_KEY environment variable (32 bytes hex or base64)
"""

import base64
import os
from typing import Optional

try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM

    CRYPTOGRAPHY_AVAILABLE = True
except ImportError:
    CRYPTOGRAPHY_AVAILABLE = False

from src.common.logger import get_logger

log = get_logger(__name__)


class LogEncryptor:
    """
    Encrypts and decrypts log messages using AES-256-GCM.

    Features:
    - AES-256-GCM authenticated encryption
    - Random IV (12 bytes) per message
    - Base64 encoding for encrypted data
    - Key from environment variable
    """

    # GCM requires 12-byte IV (nonce) for optimal security
    IV_SIZE = 12
    KEY_SIZE = 32  # AES-256 requires 32 bytes

    def __init__(self, enabled: bool = True):
        """
        Initialize LogEncryptor.

        Args:
            enabled: Enable/disable encryption
        """
        self.enabled = enabled
        self._key: Optional[bytes] = None
        self._aesgcm: Optional[AESGCM] = None

        if not CRYPTOGRAPHY_AVAILABLE:
            log.warning(
                "[LogEncryptor] cryptography library not available, encryption disabled"
            )
            self.enabled = False
            return

        if self.enabled:
            self._load_key()

    def _load_key(self) -> bool:
        """
        Load encryption key from environment variable.

        Returns:
            True if key loaded successfully, False otherwise
        """
        key_str = os.getenv("AUTO_MAPLE_LOG_ENCRYPTION_KEY", "").strip()

        if not key_str:
            log.warning(
                "[LogEncryptor] AUTO_MAPLE_LOG_ENCRYPTION_KEY not set, encryption disabled"
            )
            self.enabled = False
            return False

        try:
            # Try hex first (64 hex chars = 32 bytes)
            if len(key_str) == 64:
                self._key = bytes.fromhex(key_str)
            else:
                # Try base64
                self._key = base64.b64decode(key_str)
                if len(self._key) != self.KEY_SIZE:
                    raise ValueError(
                        f"Key must be {self.KEY_SIZE} bytes, got {len(self._key)}"
                    )

            # Initialize AESGCM with loaded key
            self._aesgcm = AESGCM(self._key)
            log.debug("[LogEncryptor] Encryption key loaded successfully")
            return True

        except (ValueError, base64.binascii.Error) as e:
            log.error(
                "[LogEncryptor] Invalid encryption key format: %s, encryption disabled",
                e,
            )
            self.enabled = False
            self._key = None
            self._aesgcm = None
            return False

    def encrypt(self, message: str) -> str:
        """
        Encrypt a log message.

        Args:
            message: Plain text message to encrypt

        Returns:
            Base64-encoded encrypted data with IV prefix, or original message if encryption disabled/failed
        """
        if not self.enabled or not self._aesgcm:
            return message

        try:
            # Generate random IV for this message
            import secrets

            iv = secrets.token_bytes(self.IV_SIZE)

            # Encrypt message (GCM automatically handles authentication)
            encrypted_data = self._aesgcm.encrypt(iv, message.encode("utf-8"), None)

            # Combine IV + encrypted_data and encode as base64
            # Format: IV (12 bytes) + encrypted_data (variable length)
            combined = iv + encrypted_data
            encrypted_b64 = base64.b64encode(combined).decode("utf-8")

            return f"[ENCRYPTED]{encrypted_b64}"

        except Exception as e:
            log.error("[LogEncryptor] Encryption failed: %s, returning plain text", e)
            return message

    def decrypt(self, encrypted_message: str) -> str:
        """
        Decrypt an encrypted log message.

        Args:
            encrypted_message: Encrypted message (with [ENCRYPTED] prefix and base64 data)

        Returns:
            Decrypted plain text message, or original if decryption fails
        """
        if not self.enabled or not self._aesgcm:
            return encrypted_message

        # Check if message is encrypted
        if not encrypted_message.startswith("[ENCRYPTED]"):
            return encrypted_message  # Plain text, return as-is

        try:
            # Extract base64 data
            encrypted_b64 = encrypted_message[11:]  # Remove "[ENCRYPTED]" prefix

            # Decode base64
            combined = base64.b64decode(encrypted_b64)

            # Extract IV and encrypted data
            iv = combined[: self.IV_SIZE]
            encrypted_data = combined[self.IV_SIZE :]

            # Decrypt
            decrypted_bytes = self._aesgcm.decrypt(iv, encrypted_data, None)
            return decrypted_bytes.decode("utf-8")

        except Exception as e:
            log.error("[LogEncryptor] Decryption failed: %s, returning original", e)
            return encrypted_message


def get_log_encryptor() -> LogEncryptor:
    """
    Get or create LogEncryptor instance.

    Returns:
        LogEncryptor instance
    """
    # Check if encryption should be enabled
    encryption_env = os.getenv("AUTO_MAPLE_LOG_ENCRYPTION", "").strip().lower()
    enabled = encryption_env in {"1", "true", "yes", "on"}

    # Auto-enable in production (frozen executable)
    import sys

    if not enabled and getattr(sys, "frozen", False):
        enabled = True
        log.debug("[LogEncryptor] Auto-enabled encryption in production mode")

    return LogEncryptor(enabled=enabled)
