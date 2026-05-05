"""Parse hardware sweep report files into structured data."""

from pathlib import Path


# Maps report file labels to internal dictionary keys
FIELD_MAP = {
    "Design": "design",
    "Signal Generator": "siggen",
    "Voltage": "voltage",
    "Frequency": "frequency",
    "Result": "result",
    "Internal Power": "internal_power",
    "Switching Power": "switching_power",
    "Leakage Power": "leakage_power",
    "Total Power": "total_power",
}


def parse_report(filepath: Path) -> list[dict]:
    """Parse a .rpt file that may contain multiple records separated by blank lines.

    Returns a list of dictionaries, one per record.
    """
    text = filepath.read_text()
    blocks = _split_into_blocks(text)

    records = []
    for block in blocks:
        record = _parse_block(block)
        record["source_file"] = filepath.name
        records.append(record)

    return records


def _split_into_blocks(text: str) -> list[str]:
    """Split file content into blocks separated by blank lines."""
    blocks = []
    current = []
    for line in text.strip().splitlines():
        if line.strip() == "":
            if current:
                blocks.append("\n".join(current))
                current = []
        else:
            current.append(line)
    if current:
        blocks.append("\n".join(current))
    return blocks


def _parse_block(block: str) -> dict:
    """Parse one block of key-value lines into a record dictionary."""
    data = {}
    for line in block.splitlines():
        for label, key in FIELD_MAP.items():
            if line.startswith(label + ":"):
                raw_value = line.split(":", 1)[1].strip()
                data[key] = _convert_value(key, raw_value)
                break
    return data


def _convert_value(key: str, raw: str):
    """Convert raw string values to appropriate Python types."""
    if key == "voltage":
        return float(raw.replace("V", "").strip())
    elif key == "frequency":
        return int(raw.replace("MHz", "").strip())
    elif key in ("internal_power", "switching_power", "leakage_power", "total_power"):
        return float(raw.replace("mW", "").strip())
    elif key == "result":
        return raw.upper()
    else:
        return raw


def parse_all_reports(directory: Path) -> list[dict]:
    """Parse all .rpt files in a directory and return a flat list of records."""
    records = []
    for rpt_file in sorted(directory.glob("*.rpt")):
        file_records = parse_report(rpt_file)
        records.extend(file_records)
    return records


def group_by_siggen(records: list[dict]) -> dict[str, list[dict]]:
    """Group a list of parsed report records by signal generator name.

    Returns a dictionary mapping siggen name to list of records.
    """
    groups = {}
    for record in records:
        siggen = record.get("siggen", "unknown")
        if siggen not in groups:
            groups[siggen] = []
        groups[siggen].append(record)
    return groups
