"""Tests for main module arithmetic functions."""

from hypothesis import given
from hypothesis import strategies as st

from containment_chamber.main import add, subtract


@given(st.integers(min_value=0, max_value=50), st.integers(min_value=0, max_value=50))
def test_add_commutative(x: int, y: int) -> None:
    """Test that addition is commutative."""
    assert add(x, y) == add(y, x)  # noqa: S101


@given(st.integers(), st.integers())
def test_subtract_add_inverse(x: int, y: int) -> None:
    """Test that subtraction is the inverse of addition."""
    assert subtract(add(x, y), y) == x  # noqa: S101