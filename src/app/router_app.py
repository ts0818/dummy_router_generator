"""
Controller for CSV ingestion and processing.
"""

import csv
from typing import Dict

from pydantic import ValidationError

from src.models.row_model import CsvRouterRow
from src.services.generator import RouterGenerator
from src.utils.csv_utils import validate_header

class RouterApp:
    """
    Orchestrates reading, validating, and generating router entries.

    Args:
        csv_file: Path to the CSV input file.
    """

    EXPECTED_HEADER: list[str] = [
        "prefix",
        "count",
        "ip",
        "model",
        "user",
        "password",
        "enable",
    ]

    def __init__(self, csv_file: str) -> None:
        """
        Initialize with CSV path.
        """
        self.csv_file: str = csv_file

    def run(self) -> None:
        """
        Execute the workflow:

        1) Read CSV file
        2) Validate header
        3) For each row:
           a) Validate using CsvRouterRow
           b) Generate output via RouterGenerator
        """
        with open(self.csv_file, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            if not validate_header(reader.fieldnames, self.EXPECTED_HEADER):
                raise ValueError(
                    f"CSV header mismatch: {reader.fieldnames}; "
                    f"expected: {self.EXPECTED_HEADER}"
                )

            for idx, row in enumerate(reader, start=2):
                try:
                    validated = CsvRouterRow(**row)
                except ValidationError as e:
                    print(f"❌ Validation error on CSV line {idx}:\n{e}\n")
                    continue

                gen = RouterGenerator(validated)
                gen.save()
