"""
Integration test for RouterApp end-to-end workflow.

This test uses a temporary CSV file and verifies
that the output file gets the correct content.
"""

import os
from pathlib import Path
import pytest

from src.app.router_app import RouterApp

CSV_CONTENT = """prefix,count,ip,model,user,password,enable
A,1,192.168.1.10,Mod,Auser,pass,en
"""

def test_router_app_writes_output(tmp_path, monkeypatch) -> None:
    """
    RouterApp should read the CSV and write to router.db.
    Using tmp_path to isolate file system side effects.
    """
    csv_file = tmp_path / "input.csv"
    csv_file.write_text(CSV_CONTENT)

    # run inside tmp_path so output file is local
    monkeypatch.chdir(tmp_path)

    app = RouterApp(str(csv_file))
    app.run()

    output_lines = (tmp_path / "router.db").read_text().strip().splitlines()
    assert output_lines[0] == "A_00001_00001:192.168.1.10:Mod:Auser:pass:en"
