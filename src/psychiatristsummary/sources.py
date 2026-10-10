"""Downloads the WHO records. This is the only module that imports requests."""

import requests

from .config import API_URL, TIMEOUT
from .models import PsychiatristRecord


class WHOSource:
    """Downloads the WHO psychiatrist data and turns it into records."""

    def __init__(self, url=API_URL, timeout=TIMEOUT):
        self.url = url
        self.timeout = timeout
        self.downloaded_count = 0
        self.skipped_count = 0

    def fetch(self):
        """Download the data and return a list of records, or None if the download fails."""
        try:
            response = requests.get(self.url, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
        except requests.RequestException:
            return None

        raw_records = data["value"]
        self.downloaded_count = len(raw_records)

        records = []
        for raw_record in raw_records:
            try:
                records.append(PsychiatristRecord(raw_record))
            except ValueError:
                self.skipped_count += 1

        return records