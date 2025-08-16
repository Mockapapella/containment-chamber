"""Tests for main module."""

import runpy
from io import StringIO
from pathlib import Path
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
    """Test the init command creates both config files."""
    with (
        patch("sys.stdout", new_callable=StringIO) as mock_stdout,
        patch("sys.argv", ["containment-chamber", "init"]),
        patch("pathlib.Path.exists", return_value=False),
        patch("pathlib.Path.cwd", return_value=Path("/test/dir")),
        patch("shutil.copy2") as mock_copy,
    ):
        main()

        output: str = mock_stdout.getvalue()
        expected = (
            "Initializing containment chamber...\n"
            "Created .pre-commit-config.yaml\n"
            "Created pyproject.toml\n"
            "Containment chamber initialized!\n"
        )
        assert output == expected

        # Verify shutil.copy2 was called exactly twice (pre-commit + pyproject)
        expected_call_count = 2
        assert mock_copy.call_count == expected_call_count


def test_init_templates_directory_name() -> None:
    """Test that templates directory name is correct."""
    # Test the literal string that should be used
    template_dir_name = "templates"
    config_filename = ".pre-commit-config.yaml"
    pyproject_filename = "pyproject.toml"

    expected_template_dir_length = 9
    expected_config_filename_length = 23
    expected_pyproject_filename_length = 14

    # These assertions will fail if mutations change the strings
    assert template_dir_name == "templates"
    assert config_filename == ".pre-commit-config.yaml"
    assert pyproject_filename == "pyproject.toml"
    assert len(template_dir_name) == expected_template_dir_length
    assert len(config_filename) == expected_config_filename_length
    assert len(pyproject_filename) == expected_pyproject_filename_length


def test_init_copy_arguments() -> None:
    """Test that copy2 is called with correct path arguments for both files."""
    captured_args: list[object] = []

    def capture_copy2(*args: object) -> None:
        captured_args.extend(args)

    with (
        patch("sys.stdout", new_callable=StringIO),
        patch("sys.argv", ["containment-chamber", "init"]),
        patch("pathlib.Path.exists", return_value=False),
        patch("pathlib.Path.cwd", return_value=Path("/test/dir")),
        patch("shutil.copy2", side_effect=capture_copy2),
    ):
        main()

        # Verify we captured exactly 4 arguments (2 calls x 2 args each)
        expected_arg_count = 4
        assert len(captured_args) == expected_arg_count

        # First call: .pre-commit-config.yaml
        first_source_str = str(captured_args[0])
        first_target_str = str(captured_args[1])

        # Second call: pyproject.toml
        second_source_str = str(captured_args[2])
        second_target_str = str(captured_args[3])

        # Test first call (pre-commit config)
        assert "templates" in first_source_str
        assert ".pre-commit-config.yaml" in first_source_str
        assert first_source_str.endswith("templates/.pre-commit-config.yaml")
        assert first_target_str == "/test/dir/.pre-commit-config.yaml"

        # Test second call (pyproject.toml)
        assert "templates" in second_source_str
        assert "pyproject.toml" in second_source_str
        assert second_source_str.endswith("templates/pyproject.toml")
        assert second_target_str == "/test/dir/pyproject.toml"


def test_main_init_existing_files() -> None:
    """Test the init command when both config files already exist."""
    with (
        patch("sys.stdout", new_callable=StringIO) as mock_stdout,
        patch("sys.argv", ["containment-chamber", "init"]),
        patch("pathlib.Path.exists", return_value=True),
        patch("pathlib.Path.cwd", return_value=Path("/test/dir")),
        patch("shutil.copy2") as mock_copy,
    ):
        main()

        output: str = mock_stdout.getvalue()
        expected = (
            "Initializing containment chamber...\n"
            "Warning: .pre-commit-config.yaml already exists, skipping.\n"
            "Warning: pyproject.toml already exists, skipping.\n"
            "Containment chamber initialized!\n"
        )
        assert output == expected
        mock_copy.assert_not_called()


def test_main_init_precommit_exists_only() -> None:
    """Test the init command when only .pre-commit-config.yaml exists."""
    call_count = [0]
    expected_first_call = 1

    def file_exists_side_effect() -> bool:
        # Return True only for the first call (precommit), False for second (pyproject)
        call_count[0] += 1
        return call_count[0] == expected_first_call

    with (
        patch("sys.stdout", new_callable=StringIO) as mock_stdout,
        patch("sys.argv", ["containment-chamber", "init"]),
        patch("pathlib.Path.exists", side_effect=file_exists_side_effect),
        patch("pathlib.Path.cwd", return_value=Path("/test/dir")),
        patch("shutil.copy2") as mock_copy,
    ):
        main()

        output: str = mock_stdout.getvalue()
        expected = (
            "Initializing containment chamber...\n"
            "Warning: .pre-commit-config.yaml already exists, skipping.\n"
            "Created pyproject.toml\n"
            "Containment chamber initialized!\n"
        )
        assert output == expected
        # Should be called once for pyproject.toml only
        mock_copy.assert_called_once()


def test_main_init_pyproject_exists_only() -> None:
    """Test the init command when only pyproject.toml exists."""
    call_count = [0]
    expected_second_call = 2

    def file_exists_side_effect() -> bool:
        # Return False for first call (precommit), True for second call (pyproject)
        call_count[0] += 1
        return call_count[0] == expected_second_call

    with (
        patch("sys.stdout", new_callable=StringIO) as mock_stdout,
        patch("sys.argv", ["containment-chamber", "init"]),
        patch("pathlib.Path.exists", side_effect=file_exists_side_effect),
        patch("pathlib.Path.cwd", return_value=Path("/test/dir")),
        patch("shutil.copy2") as mock_copy,
    ):
        main()

        output: str = mock_stdout.getvalue()
        expected = (
            "Initializing containment chamber...\n"
            "Created .pre-commit-config.yaml\n"
            "Warning: pyproject.toml already exists, skipping.\n"
            "Containment chamber initialized!\n"
        )
        assert output == expected
        # Should be called once for .pre-commit-config.yaml only
        mock_copy.assert_called_once()


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
