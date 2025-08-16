"""Simple CLI for Containment Chamber."""

import shutil
import sys
from pathlib import Path


def init_containment_chamber() -> None:
    """Initialize containment chamber in current directory."""
    sys.stdout.write("Initializing containment chamber...\n")

    # Get template paths
    template_dir = Path(__file__).parent / "templates"
    precommit_template = template_dir / ".pre-commit-config.yaml"
    pyproject_template = template_dir / "pyproject.toml"

    # Get current directory
    current_dir = Path.cwd()

    # Copy .pre-commit-config.yaml
    precommit_target = current_dir / ".pre-commit-config.yaml"
    if precommit_target.exists():
        sys.stdout.write("Warning: .pre-commit-config.yaml already exists, skipping.\n")
    else:
        shutil.copy2(precommit_template, precommit_target)
        sys.stdout.write("Created .pre-commit-config.yaml\n")

    # Copy pyproject.toml
    pyproject_target = current_dir / "pyproject.toml"
    if pyproject_target.exists():
        sys.stdout.write("Warning: pyproject.toml already exists, skipping.\n")
    else:
        shutil.copy2(pyproject_template, pyproject_target)
        sys.stdout.write("Created pyproject.toml\n")

    sys.stdout.write("Containment chamber initialized!\n")


def main() -> None:
    """Run the main entry point for containment-chamber."""
    if len(sys.argv) > 1:
        if sys.argv[1] == "help" or sys.argv[1] == "--help" or sys.argv[1] == "-h":
            sys.stdout.write("containment-chamber [help|init]\n")
            sys.stdout.write("  help  Show this help message\n")
            sys.stdout.write("  init  Initialize a new containment chamber\n")
        elif sys.argv[1] == "init":
            init_containment_chamber()
        else:
            sys.stdout.write("Containment Chamber is in alpha!\n")
    else:
        sys.stdout.write("Containment Chamber is in alpha!\n")


if __name__ == "__main__":
    main()
