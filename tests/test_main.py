"""Tests for main module."""

import runpy
from io import StringIO
from unittest.mock import patch

from containment_chamber.main import main


def test_main() -> None:
    """Test the main function output."""
    with (
        patch("sys.stdout", new_callable=StringIO) as mock_stdout,
        patch("sys.argv", ["containment-chamber"]),
    ):
        main()
        output: str = mock_stdout.getvalue()
        assert output == "Containment Chamber is in alpha!\n"


def test_main_help() -> None:
    """Test the help flag output."""
    with (
        patch("sys.stdout", new_callable=StringIO) as mock_stdout,
        patch("sys.argv", ["containment-chamber", "help"]),
    ):
        main()
        output: str = mock_stdout.getvalue()
        expected = (
            "containment-chamber [help|init]\n"
            "  help  Show this help message\n"
            "  init  Initialize a new containment chamber\n"
        )
        assert output == expected


def test_main_help_long() -> None:
    """Test the --help flag output."""
    with (
        patch("sys.stdout", new_callable=StringIO) as mock_stdout,
        patch("sys.argv", ["containment-chamber", "--help"]),
    ):
        main()
        output: str = mock_stdout.getvalue()
        expected = (
            "containment-chamber [help|init]\n"
            "  help  Show this help message\n"
            "  init  Initialize a new containment chamber\n"
        )
        assert output == expected


def test_main_help_short() -> None:
    """Test the -h flag output."""
    with (
        patch("sys.stdout", new_callable=StringIO) as mock_stdout,
        patch("sys.argv", ["containment-chamber", "-h"]),
    ):
        main()
        output: str = mock_stdout.getvalue()
        expected = (
            "containment-chamber [help|init]\n"
            "  help  Show this help message\n"
            "  init  Initialize a new containment chamber\n"
        )
        assert output == expected


def test_main_init() -> None:
    """Test the init command output."""
    with (
        patch("sys.stdout", new_callable=StringIO) as mock_stdout,
        patch("sys.argv", ["containment-chamber", "init"]),
    ):
        main()
        output: str = mock_stdout.getvalue()
        assert output == "Initializing containment chamber...\n"


def test_main_unknown_command() -> None:
    """Test unknown command falls back to alpha message."""
    with (
        patch("sys.stdout", new_callable=StringIO) as mock_stdout,
        patch("sys.argv", ["containment-chamber", "unknown"]),
    ):
        main()
        output: str = mock_stdout.getvalue()
        assert output == "Containment Chamber is in alpha!\n"


def test_main_entry_point() -> None:
    """Test the __main__ entry point."""
    with (
        patch("sys.stdout", new_callable=StringIO) as mock_stdout,
        patch("sys.argv", ["containment-chamber"]),
    ):
        runpy.run_module("containment_chamber.main", run_name="__main__")
        output: str = mock_stdout.getvalue()
        assert output == "Containment Chamber is in alpha!\n"


def test_main_module_entry_point() -> None:
    """Test the __main__.py module entry point."""
    with (
        patch("sys.stdout", new_callable=StringIO) as mock_stdout,
        patch("sys.argv", ["containment-chamber"]),
    ):
        runpy.run_module("containment_chamber", run_name="__main__")
        output: str = mock_stdout.getvalue()
        assert output == "Containment Chamber is in alpha!\n"


def test_main_module_import() -> None:
    """Test importing __main__.py as a regular module doesn't execute main."""
    with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
        __import__("containment_chamber.__main__")
        output: str = mock_stdout.getvalue()
        assert output == "", "Importing __main__.py should not execute main()"
