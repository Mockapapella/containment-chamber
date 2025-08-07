"""Tests for main module arithmetic functions."""

import runpy
from io import StringIO
from unittest.mock import patch

from hypothesis import given
from hypothesis import strategies as st

from containment_chamber.main import add, main, subtract


@given(st.integers(min_value=0, max_value=50), st.integers(min_value=0, max_value=50))
def test_add_commutative(x: int, y: int) -> None:
    """Test that addition is commutative."""
    assert add(x, y) == add(y, x)  # noqa: S101


@given(st.integers(), st.integers())
def test_subtract_add_inverse(x: int, y: int) -> None:
    """Test that subtraction is the inverse of addition."""
    assert subtract(add(x, y), y) == x  # noqa: S101


def test_main() -> None:
    """Test the main function output."""
    with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
        main()
        output: str = mock_stdout.getvalue()
        assert output == "Hello from containment-chamber!\n"  # noqa: S101


def test_main_entry_point() -> None:
    """Test the __main__ entry point."""
    with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
        runpy.run_module("containment_chamber.main", run_name="__main__")
        output: str = mock_stdout.getvalue()
        assert output == "Hello from containment-chamber!\n"  # noqa: S101
