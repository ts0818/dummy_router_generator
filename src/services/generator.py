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
    OUTPUT_FILE: str = "router.db"

    def __init__(self, data: CsvRouterRow) -> None:
        self.data: CsvRouterRow = data

    def _get_last_global(self) -> int:
        path = Path(self.OUTPUT_FILE)
        if not path.exists():
            return 0

        max_global = 0
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                hostname = line.split(":")[0]
                parts = hostname.split("-")
                try:
                    idx = int(parts[-1])
                    if idx > max_global:
                        max_global = idx
                except ValueError:
                    continue
        return max_global

    def generate_lines(self) -> List[str]:
        lines: List[str] = []
        last_global = self._get_last_global()
        next_global = last_global + 1

        for model_local in range(1, self.data.count + 1):
            model_str = str(model_local).zfill(5)
            global_str = str(next_global).zfill(5)
            hostname = f"{self.data.prefix}-{model_str}-{global_str}"

            # 全フィールドをリストにする
            fields = [
                hostname,
                self.data.ip,
                self.data.model,
                self.data.user,
                self.data.password,
            ]

            # enable が空でなければ追加（空なら skip）
            if self.data.enable:
                fields.append(self.data.enable)

            # 空フィールドを含めずに join → 行末に : が付かない
            line = ":".join(fields)
            lines.append(line)

            next_global += 1

        return lines

    def save(self) -> None:
        with open(self.OUTPUT_FILE, "a", encoding="utf-8") as f:
            for line in self.generate_lines():
                f.write(line + "\n")

