#!/usr/bin/env python3
"""
Decrypt encrypted log files.

Usage:
    python tools/decrypt_log.py <encrypted_log_file> [--key KEY] [--output OUTPUT_FILE]

If --key is not provided, will read from AUTO_MAPLE_LOG_ENCRYPTION_KEY environment variable.
If --output is not provided, will write to stdout.
"""

import argparse
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

try:
    from src.common.log_encryption import LogEncryptor
except ImportError as e:
    print(f"Error importing LogEncryptor: {e}", file=sys.stderr)
    print("Make sure you're running from the project root directory.", file=sys.stderr)
    sys.exit(1)


def decrypt_log_file(
    input_file: Path, output_file: Path = None, encryption_key: str = None
) -> None:
    """
    Decrypt an encrypted log file.

    Args:
        input_file: Path to encrypted log file
        output_file: Path to output file (None = stdout)
        encryption_key: Encryption key (hex or base64, 32 bytes)
    """
    if not input_file.exists():
        print(f"Error: Input file not found: {input_file}", file=sys.stderr)
        sys.exit(1)

    # Get encryption key
    if not encryption_key:
        encryption_key = os.getenv("AUTO_MAPLE_LOG_ENCRYPTION_KEY", "").strip()
        if not encryption_key:
            print(
                "Error: Encryption key not provided. Use --key or set AUTO_MAPLE_LOG_ENCRYPTION_KEY environment variable.",
                file=sys.stderr,
            )
            sys.exit(1)

    # Set environment variable for LogEncryptor
    os.environ["AUTO_MAPLE_LOG_ENCRYPTION_KEY"] = encryption_key
    os.environ["AUTO_MAPLE_LOG_ENCRYPTION"] = "1"

    # Create encryptor
    encryptor = LogEncryptor(enabled=True)

    if not encryptor.enabled:
        print("Error: Failed to initialize encryption (invalid key?)", file=sys.stderr)
        sys.exit(1)

    # Open output file or use stdout
    output_fp = open(output_file, "w", encoding="utf-8") if output_file else sys.stdout

    try:
        # Read and decrypt each line
        with open(input_file, "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                line = line.rstrip("\n\r")

                # Check if line is encrypted
                if "[ENCRYPTED]" in line:
                    # Extract encrypted part
                    # Format: "timestamp | level | logger | [ENCRYPTED]base64_data"
                    parts = line.rsplit(" | ", 1)
                    if len(parts) == 2:
                        metadata, encrypted_part = parts
                        # Decrypt message
                        decrypted_message = encryptor.decrypt(encrypted_part)
                        # Reconstruct line
                        decrypted_line = f"{metadata} | {decrypted_message}"
                        print(decrypted_line, file=output_fp)
                    else:
                        # Entire line might be encrypted
                        decrypted_line = encryptor.decrypt(line)
                        print(decrypted_line, file=output_fp)
                else:
                    # Plain text line, output as-is
                    print(line, file=output_fp)

    except Exception as e:
        print(f"Error decrypting log file: {e}", file=sys.stderr)
        import traceback

        traceback.print_exc()
        sys.exit(1)
    finally:
        if output_file and output_fp != sys.stdout:
            output_fp.close()

    if output_file:
        print(f"Decrypted log written to: {output_file}", file=sys.stderr)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Decrypt encrypted log files from Auto-Maple bot"
    )
    parser.add_argument(
        "input_file",
        type=Path,
        help="Path to encrypted log file",
    )
    parser.add_argument(
        "--key",
        type=str,
        help="Encryption key (32 bytes hex or base64). If not provided, reads from AUTO_MAPLE_LOG_ENCRYPTION_KEY environment variable.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Output file path (default: stdout)",
    )

    args = parser.parse_args()

    decrypt_log_file(
        input_file=args.input_file,
        output_file=args.output,
        encryption_key=args.key,
    )


if __name__ == "__main__":
    main()
