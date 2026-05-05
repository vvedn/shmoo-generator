"""Tests for the report parser module."""

import pytest

from autoshmoo.parser import parse_report, parse_all_reports, group_by_siggen


@pytest.fixture
def sample_report(tmp_path):
    """Create a sample report file for testing."""
    content = """\
Design: int_mac
Signal Generator: siggen_random
Voltage: 0.90 V
Frequency: 200 MHz
Result: PASS
Internal Power: 12.4 mW
Switching Power: 8.2 mW
Leakage Power: 0.9 mW
Total Power: 21.5 mW
"""
    rpt = tmp_path / "test_report.rpt"
    rpt.write_text(content)
    return rpt


@pytest.fixture
def multi_record_report(tmp_path):
    """Create a report with multiple records."""
    content = """\
Design: int_mac
Signal Generator: siggen_random
Voltage: 0.80 V
Frequency: 100 MHz
Result: PASS
Total Power: 17.3 mW

Design: int_mac
Signal Generator: siggen_random
Voltage: 0.70 V
Frequency: 300 MHz
Result: FAIL
Total Power: 26.0 mW
"""
    rpt = tmp_path / "multi.rpt"
    rpt.write_text(content)
    return rpt


@pytest.fixture
def missing_power_report(tmp_path):
    """Create a report missing total power."""
    content = """\
Design: int_mac
Signal Generator: siggen_zero
Voltage: 0.80 V
Frequency: 100 MHz
Result: PASS
"""
    rpt = tmp_path / "no_power.rpt"
    rpt.write_text(content)
    return rpt


def test_parse_report_basic(sample_report):
    """Test parsing a well-formed report with all fields."""
    records = parse_report(sample_report)
    assert len(records) == 1

    r = records[0]
    assert r["design"] == "int_mac"
    assert r["siggen"] == "siggen_random"
    assert r["voltage"] == 0.90
    assert r["frequency"] == 200
    assert r["result"] == "PASS"
    assert r["total_power"] == 21.5
    assert r["internal_power"] == 12.4
    assert r["switching_power"] == 8.2
    assert r["leakage_power"] == 0.9
    assert r["source_file"] == "test_report.rpt"


def test_parse_multi_record(multi_record_report):
    """Test parsing a file with multiple records separated by blank lines."""
    records = parse_report(multi_record_report)
    assert len(records) == 2
    assert records[0]["frequency"] == 100
    assert records[1]["frequency"] == 300
    assert records[0]["result"] == "PASS"
    assert records[1]["result"] == "FAIL"


def test_parse_missing_total_power(missing_power_report):
    """Test that missing optional fields do not crash the parser."""
    records = parse_report(missing_power_report)
    assert len(records) == 1
    assert "total_power" not in records[0]
    assert records[0]["voltage"] == 0.80
    assert records[0]["result"] == "PASS"


def test_parse_all_reports(tmp_path):
    """Test parsing a directory with multiple .rpt files."""
    (tmp_path / "a.rpt").write_text("Design: x\nSignal Generator: sg1\nVoltage: 1.00 V\nFrequency: 100 MHz\nResult: PASS\n")
    (tmp_path / "b.rpt").write_text("Design: x\nSignal Generator: sg2\nVoltage: 0.80 V\nFrequency: 200 MHz\nResult: FAIL\n")
    (tmp_path / "not_a_report.txt").write_text("ignore me")

    records = parse_all_reports(tmp_path)
    assert len(records) == 2
    # Only .rpt files are parsed
    siggens = {r["siggen"] for r in records}
    assert siggens == {"sg1", "sg2"}


def test_group_by_siggen_basic():
    """Test grouping records by signal generator name."""
    records = [
        {"siggen": "siggen_random", "voltage": 0.9, "frequency": 200},
        {"siggen": "siggen_zero", "voltage": 0.8, "frequency": 100},
        {"siggen": "siggen_random", "voltage": 0.7, "frequency": 300},
    ]
    groups = group_by_siggen(records)

    assert len(groups) == 2
    assert len(groups["siggen_random"]) == 2
    assert len(groups["siggen_zero"]) == 1


def test_group_by_siggen_missing_key():
    """Test that records without a siggen field are grouped under 'unknown'."""
    records = [
        {"voltage": 1.0, "frequency": 100},
        {"siggen": "siggen_random", "voltage": 0.9, "frequency": 200},
    ]
    groups = group_by_siggen(records)

    assert "unknown" in groups
    assert len(groups["unknown"]) == 1
    assert len(groups["siggen_random"]) == 1
