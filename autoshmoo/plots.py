"""Generate shmoo plots from grouped report data."""

from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


def generate_shmoo_plot(siggen_name: str, records: list[dict], output_dir: Path) -> Path:
    """Create a shmoo plot for one signal generator.

    X-axis: frequency (MHz)
    Y-axis: voltage (V)
    Color: green for PASS, red for FAIL
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(8, 6))

    for record in records:
        freq = record.get("frequency")
        volt = record.get("voltage")
        result = record.get("result", "FAIL")

        color = "green" if result == "PASS" else "red"
        marker = "s"  # square marker for shmoo-style grid look
        ax.scatter(freq, volt, c=color, marker=marker, s=200, edgecolors="black")

    ax.set_xlabel("Frequency (MHz)")
    ax.set_ylabel("Voltage (V)")
    ax.set_title(f"Shmoo Plot: {siggen_name}")

    # Legend
    pass_patch = mpatches.Patch(color="green", label="PASS")
    fail_patch = mpatches.Patch(color="red", label="FAIL")
    ax.legend(handles=[pass_patch, fail_patch], loc="upper right")

    ax.grid(True, alpha=0.3)

    filename = f"shmoo_{siggen_name}.png"
    output_path = output_dir / filename
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return output_path


def generate_power_plot(siggen_name: str, records: list[dict], output_dir: Path) -> Path:
    """Create a bar chart of total power per frequency for one signal generator."""
    output_dir.mkdir(parents=True, exist_ok=True)

    # Only include records that have total_power
    powered = [r for r in records if r.get("total_power") is not None]
    if not powered:
        return None

    fig, ax = plt.subplots(figsize=(8, 5))

    powers = [r["total_power"] for r in powered]
    labels = [f'{r["voltage"]}V\n{r["frequency"]}MHz' for r in powered]

    ax.bar(range(len(powers)), powers, color="steelblue", edgecolor="black")
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels)
    ax.set_xlabel("Operating Point")
    ax.set_ylabel("Total Power (mW)")
    ax.set_title(f"Power Summary: {siggen_name}")
    ax.grid(True, axis="y", alpha=0.3)

    filename = f"power_{siggen_name}.png"
    output_path = output_dir / filename
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return output_path
