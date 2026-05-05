"""Match parsed reports to their signal generator groups."""


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
