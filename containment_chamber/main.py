"""Simple arithmetic operations."""

import sys


def add(x: int, y: int) -> int:
    """Add two integers."""
    return x + y


def subtract(x: int, y: int) -> int:
    """Subtract y from x."""
    return x - y


def main() -> None:
    """Run the main entry point for containment-chamber."""
    sys.stdout.write("Hello from containment-chamber!\n")


if __name__ == "__main__":
    main()
