"""Builds the summary dictionary and writes it to a JSON file."""

import json


def build_summary(source, records, aggregations):
    """Combine the record counts and every aggregation result into one dictionary."""
    summary = {
        "source_url": source.url,
        "downloaded_record_count": source.downloaded_count,
        "valid_record_count": len(records),
        "skipped_record_count": source.skipped_count
    }

    for aggregation in aggregations:
        summary[aggregation.name] = aggregation.compute(records)

    return summary


def write_summary(summary, path):
    """Write the summary dictionary to a JSON file."""
    path.write_text(
        json.dumps(summary, indent=2),
        encoding="utf-8"
    )