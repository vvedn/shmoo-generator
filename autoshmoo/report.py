"""Generate summary reports in CSV and Markdown formats."""

from pathlib import Path

import pandas as pd


def build_summary_dataframe(records: list[dict]) -> pd.DataFrame:
    """Convert list of parsed records into a pandas DataFrame."""
    columns = [
        "source_file",
        "siggen",
        "voltage",
        "frequency",
        "result",
        "total_power",
    ]
    df = pd.DataFrame(records)
    # Keep only columns that exist in the data
    available = [c for c in columns if c in df.columns]
    return df[available]


def write_csv(df: pd.DataFrame, output_path: Path) -> None:
    """Write the summary DataFrame to a CSV file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)


def write_markdown(df: pd.DataFrame, output_path: Path) -> None:
    """Write the summary DataFrame to a Markdown table file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    md_table = df.to_markdown(index=False)
    output_path.write_text(md_table + "\n")
