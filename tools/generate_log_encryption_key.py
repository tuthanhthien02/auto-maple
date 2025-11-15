#!/usr/bin/env python3
"""
Generate encryption key for log encryption.

Usage:
    python tools/generate_log_encryption_key.py [--format hex|base64] [--output .env.prod]

Generates a 32-byte encryption key suitable for AUTO_MAPLE_LOG_ENCRYPTION_KEY.
"""

import argparse
import base64
import secrets
import sys
from pathlib import Path


def generate_key(format_type: str = "hex") -> str:
    """
    Generate a 32-byte encryption key.

    Args:
        format_type: 'hex' or 'base64'

    Returns:
        Encryption key as string
    """
    key_bytes = secrets.token_bytes(32)

    if format_type == "hex":
        return key_bytes.hex()
    elif format_type == "base64":
        return base64.b64encode(key_bytes).decode()
    else:
        raise ValueError(f"Invalid format: {format_type}. Use 'hex' or 'base64'")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Generate encryption key for Auto-Maple log encryption"
    )
    parser.add_argument(
        "--format",
        choices=["hex", "base64"],
        default="hex",
        help="Key format: hex (64 chars) or base64 (default: hex)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Output file path (e.g., .env.prod). If not provided, prints to stdout.",
    )
    parser.add_argument(
        "--append",
        action="store_true",
        help="Append to output file instead of overwriting (only if --output is provided)",
    )

    args = parser.parse_args()

    # Generate key
    key = generate_key(args.format)

    # Output
    if args.output:
        # Write to file
        output_lines = [
            "",
            "# Log Encryption Key (32 bytes)",
            f"AUTO_MAPLE_LOG_ENCRYPTION_KEY={key}",
            "AUTO_MAPLE_LOG_ENCRYPTION=1",
            "",
        ]

        if args.append and args.output.exists():
            # Append mode
            with open(args.output, "a", encoding="utf-8") as f:
                f.write("\n".join(output_lines))
            print(f"✅ Encryption key appended to: {args.output}", file=sys.stderr)
        else:
            # Overwrite mode
            with open(args.output, "w", encoding="utf-8") as f:
                f.write("\n".join(output_lines))
            print(f"✅ Encryption key written to: {args.output}", file=sys.stderr)

        print(f"\nGenerated {args.format.upper()} key:", file=sys.stderr)
        print(key)
    else:
        # Print to stdout
        print(key)
        print("\n# Add to .env.prod:", file=sys.stderr)
        print(f"AUTO_MAPLE_LOG_ENCRYPTION_KEY={key}", file=sys.stderr)
        print("AUTO_MAPLE_LOG_ENCRYPTION=1", file=sys.stderr)


if __name__ == "__main__":
    main()
