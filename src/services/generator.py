"""
Generate colon-separated lines and append to router.db
with:
  - model-local sequence (per CSV count)
  - global unique sequence at the end
  - format: {prefix}-{model_seq}-{global_seq}
"""

from pathlib import Path
from typing import List

from src.models.row_model import CsvRouterRow


class RouterGenerator:
    """
    Generate and save router configuration lines.

    Uses:
        - model_local: sequence within the CSV count
        - global index: unique across entire router.db
    """

    OUTPUT_FILE: str = "router.db"

    def __init__(self, data: CsvRouterRow) -> None:
        """
        Args:
            data: A validated CsvRouterRow object.
        """
        self.data: CsvRouterRow = data

    def _get_last_global(self) -> int:
        """
        Read OUTPUT_FILE to find the highest existing global index.
        Returns 0 if the file doesn't exist.
        """
        path = Path(self.OUTPUT_FILE)
        if not path.exists():
            return 0

        max_global = 0
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                # Hostname部分を取り出し
                hostname = line.split(":")[0]
                parts = hostname.split("-")

                # global は parts[-1] にある想定
                try:
                    global_str = parts[-1]
                    idx = int(global_str)
                    if idx > max_global:
                        max_global = idx
                except ValueError:
                    continue
        return max_global

    def generate_lines(self) -> List[str]:
        """
        Build colon-separated lines with:
            - model-local sequential index
            - global unique numbering appended at end
        """
        lines: List[str] = []
        last_global = self._get_last_global()
        next_global = last_global + 1

        # model_local は1〜count
        for model_local in range(1, self.data.count + 1):
            model_str = str(model_local).zfill(5)
            global_str = str(next_global).zfill(5)

            # prefix-model_local-global
            hostname = f"{self.data.prefix}-{model_str}-{global_str}"

            line = (
                f"{hostname}:"
                f"{self.data.ip}:"
                f"{self.data.model}:"
                f"{self.data.user}:"
                f"{self.data.password}:"
                f"{self.data.enable}"
            )
            lines.append(line)
            next_global += 1

        return lines

    def save(self) -> None:
        """
        Append lines to OUTPUT_FILE.
        """
        with open(self.OUTPUT_FILE, "a", encoding="utf-8") as f:
            for line in self.generate_lines():
                f.write(line + "\n")
