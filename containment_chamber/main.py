"""Simple CLI for Containment Chamber."""

import sys


def main() -> None:
    """Run the main entry point for containment-chamber."""
    if len(sys.argv) > 1:
        if sys.argv[1] == "help" or sys.argv[1] == "--help" or sys.argv[1] == "-h":
            sys.stdout.write("containment-chamber [help|init]\n")
            sys.stdout.write("  help  Show this help message\n")
            sys.stdout.write("  init  Initialize a new containment chamber\n")
        elif sys.argv[1] == "init":
            sys.stdout.write("Initializing containment chamber...\n")
        else:
            sys.stdout.write("Containment Chamber is in alpha!\n")
    else:
        sys.stdout.write("Containment Chamber is in alpha!\n")


if __name__ == "__main__":
    main()
