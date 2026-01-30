"""
CSV helper utilities.
"""

from typing import List

def validate_header(
    fieldnames: List[str] | None,
    expected: List[str],
) -> bool:
    """
    Check CSV header for an exact match.

    Args:
        fieldnames: Header list from csv.DictReader.fieldnames.
        expected: Expected header order list.

    Returns:
        True if exact match; otherwise False.
    """
    if fieldnames is None:
        return False
    return list(fieldnames) == expected
