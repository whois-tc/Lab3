"""Entry point: downloads, summarizes and saves the WHO psychiatrist data."""

from psychiatristsummary import (
    WHOSource, RegionAverages, AccessLevelCounts, YearsCovered,
    build_summary, write_summary
)
from psychiatristsummary.config import OUTPUT_PATH


def main():
    """Download, analyze, display, and save the mental-health data."""
    source = WHOSource()
    records = source.fetch()

    if records is None:
        print("Error: Could not download data from the WHO API.")
        return

    aggregations = [YearsCovered(), RegionAverages(), AccessLevelCounts()]
    summary = build_summary(source, records, aggregations)
    write_summary(summary, OUTPUT_PATH)

    print(f"Downloaded records: {summary['downloaded_record_count']}")
    print(f"Valid records: {summary['valid_record_count']}")
    print(f"Skipped records: {summary['skipped_record_count']}")
    print("Average psychiatrists per 100,000 by region:")
    print(summary["region_averages"])
    print("Records by psychiatrist access level:")
    print(summary["access_counts"])
    print("Years included in the data:")
    print(summary["years"])
    print(f"Results saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()