"""
Pydantic model for validating CSV row data.
"""

from pydantic import BaseModel, Field, field_validator
import re

class CsvRouterRow(BaseModel):
    """
    Represents a single row of CSV input with expected fields.

    Attributes:
        prefix: Hostname prefix.
        count: Number of entries to generate.
        ip: IPv4 address.
        model: Device model name.
        user: Username.
        password: Password.
        enable: Enable password (optional).
    """

    prefix: str = Field(..., min_length=1, description="Hostname prefix")
    count: int = Field(..., ge=1, description="Number of entries to generate")
    ip: str = Field(..., description="IPv4 address")
    model: str = Field(..., min_length=1, description="Device model")
    user: str = Field(..., min_length=1, description="Username")
    password: str = Field(..., min_length=1, description="Password")
    enable: str = Field("", description="Enable password (optional)")

    @field_validator("ip")
    @classmethod
    def check_ipv4(cls, v: str) -> str:
        """
        Validate that the IP address is in IPv4 format.

        Args:
            v: Raw IP string from CSV.

        Returns:
            The validated IP string.

        Raises:
            ValueError: If the IP format is invalid.
        """
        pattern = r"^(\d{1,3}\.){3}\d{1,3}$"
        if not re.match(pattern, v):
            raise ValueError(f"Invalid IPv4 format: {v}")
        parts = v.split(".")
        if not all(0 <= int(p) <= 255 for p in parts):
            raise ValueError(f"IPv4 octet out of range: {v}")
        return v
