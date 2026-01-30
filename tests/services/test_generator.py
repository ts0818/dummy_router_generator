"""
Tests for the router configuration generator.
"""

from src.services.generator import RouterGenerator
from src.models.row_model import CsvRouterRow

def test_generate_multiple_lines() -> None:
    """
    RouterGenerator.generate_lines should return expected colon-separated lines.
    """
    data = CsvRouterRow(
        prefix="NODE",
        count=2,
        ip="10.0.0.5",
        model="X100",
        user="usr",
        password="pw",
        enable="en"
    )
    gen = RouterGenerator(data)
    lines = gen.generate_lines()

    assert lines == [
        "NODE_00001_00001:10.0.0.5:X100:usr:pw:en",
        "NODE_00002_00002:10.0.0.5:X100:usr:pw:en"
    ]
