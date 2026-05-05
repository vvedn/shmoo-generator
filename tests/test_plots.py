"""Tests for the plot generation module."""

from autoshmoo.plots import generate_shmoo_plot, generate_power_plot


def test_generate_shmoo_plot_creates_file(tmp_path):
    """Test that a shmoo plot PNG is created."""
    records = [
        {"voltage": 0.9, "frequency": 200, "result": "PASS"},
        {"voltage": 0.7, "frequency": 300, "result": "FAIL"},
    ]
    output = generate_shmoo_plot("siggen_test", records, tmp_path)

    assert output.exists()
    assert output.suffix == ".png"
    assert output.stat().st_size > 0


def test_generate_power_plot_creates_file(tmp_path):
    """Test that a power plot PNG is created when total_power is present."""
    records = [
        {"voltage": 0.9, "frequency": 200, "result": "PASS", "total_power": 21.5},
        {"voltage": 0.7, "frequency": 300, "result": "FAIL", "total_power": 26.0},
    ]
    output = generate_power_plot("siggen_test", records, tmp_path)

    assert output is not None
    assert output.exists()
    assert output.suffix == ".png"


def test_generate_power_plot_no_power_data(tmp_path):
    """Test that power plot returns None when no records have total_power."""
    records = [
        {"voltage": 0.9, "frequency": 200, "result": "PASS"},
    ]
    output = generate_power_plot("siggen_test", records, tmp_path)

    assert output is None
