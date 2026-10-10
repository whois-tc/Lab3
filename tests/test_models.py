"""Tests for PsychiatristRecord using handmade records and no network."""

import unittest

from psychiatristsummary import PsychiatristRecord


class TestPsychiatristRecord(unittest.TestCase):
    """Checks that PsychiatristRecord cleans its own values."""

    def test_rate_text_becomes_number(self):
        record = PsychiatristRecord({"ParentLocation": "Europe", "NumericValue": "12.5", "TimeDim": 2016, "SpatialDim": "FRA"})
        self.assertEqual(record.rate, 12.5)

    def test_missing_region_is_rejected(self):
        with self.assertRaises(ValueError):
            PsychiatristRecord({"ParentLocation": "", "NumericValue": 3})

    def test_malformed_rate_is_rejected(self):
        with self.assertRaises(ValueError):
            PsychiatristRecord({"ParentLocation": "Africa", "NumericValue": "not a number"})