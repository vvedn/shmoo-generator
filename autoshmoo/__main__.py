"""Run the full pipeline: parse reports -> summarize -> generate plots.

Usage: python -m autoshmoo examples/sample_project/reports outputs
"""

import sys
from pathlib import Path

from autoshmoo.parser import parse_all_reports, group_by_siggen
from autoshmoo.report import build_summary_dataframe, write_csv, write_markdown
from autoshmoo.plots import generate_shmoo_plot, generate_power_plot


def main():
    if len(sys.argv) != 3:
        print("Usage: python -m autoshmoo <report_dir> <output_dir>")
        sys.exit(1)

    report_dir = Path(sys.argv[1])
    output_dir = Path(sys.argv[2])

    records = parse_all_reports(report_dir)
    if not records:
        print(f"No .rpt files found in {report_dir}")
        sys.exit(1)

    print(f"Parsed {len(records)} report(s)")

    df = build_summary_dataframe(records)
    write_csv(df, output_dir / "shmoo_summary.csv")
    write_markdown(df, output_dir / "shmoo_summary.md")
    print(f"Summary written to {output_dir}/shmoo_summary.csv and .md")

    groups = group_by_siggen(records)
    for siggen_name, group_records in groups.items():
        shmoo_path = generate_shmoo_plot(siggen_name, group_records, output_dir)
        print(f"Shmoo plot: {shmoo_path}")

        power_path = generate_power_plot(siggen_name, group_records, output_dir)
        if power_path:
            print(f"Power plot: {power_path}")

    print("Done.")


main()
