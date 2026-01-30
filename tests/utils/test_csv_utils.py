"""
Tests for csv_utils.validate_header function.
"""

from src.utils.csv_utils import validate_header

def test_validate_header_exact_match() -> None:
    """
    validate_header should return True when list matches expected.
    """
    expected = ["a", "b", "c"]
    assert validate_header(["a", "b", "c"], expected)

def test_validate_header_none() -> None:
    """
    validate_header should return False when fieldnames is None.
    """
    assert not validate_header(None, ["x", "y"])
