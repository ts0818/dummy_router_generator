"""
Tests for the CSV row validation model.
"""

import pytest
from src.models.row_model import CsvRouterRow

def test_valid_row() -> None:
    """
    CsvRouterRow should accept valid input values.
    """
    row = CsvRouterRow(
        prefix="OK",
        count=1,
        ip="192.168.0.1",
        model="TestModel",
        user="user",
        password="pwd",
        enable=""
    )
    assert row.prefix == "OK"
    assert row.count == 1

def test_invalid_ip_raises() -> None:
    """
    Invalid IPv4 format should raise ValueError.
    """
    with pytest.raises(ValueError):
        CsvRouterRow(
            prefix="X",
            count=1,
            ip="999.999.999.999",  # invalid ip
            model="M",
            user="U",
            password="P",
            enable=""
        )
