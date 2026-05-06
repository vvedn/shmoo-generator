"""Tests for the report generation module."""

import pandas as pd

from autoshmoo.report import build_summary_dataframe, write_csv, write_markdown


def test_build_summary_dataframe():
    """Test that the summary DataFrame contains expected columns."""
    records = [
        {
            "source_file": "test.rpt",
            "siggen": "siggen_random",
            "voltage": 0.90,
            "frequency": 200,
            "result": "PASS",
            "total_power": 21.5,
        }
    ]
    df = build_summary_dataframe(records)

    assert list(df.columns) == ["source_file", "siggen", "voltage", "frequency", "result", "total_power"]
    assert len(df) == 1
    assert df.iloc[0]["siggen"] == "siggen_random"


def test_write_csv(tmp_path):
    """Test CSV output creates a valid file."""
    df = pd.DataFrame([{"siggen": "sg1", "voltage": 0.9, "frequency": 200, "result": "PASS"}])
    out = tmp_path / "summary.csv"
    write_csv(df, out)

    assert out.exists()
    content = out.read_text()
    assert "siggen" in content
    assert "sg1" in content


def test_write_markdown(tmp_path):
    """Test Markdown output creates a valid file with table formatting."""
    df = pd.DataFrame([{"siggen": "sg1", "voltage": 0.9, "frequency": 200, "result": "PASS"}])
    out = tmp_path / "summary.md"
    write_markdown(df, out)

    assert out.exists()
    content = out.read_text()
    # Markdown tables use pipe characters
    assert "|" in content
    assert "sg1" in content
