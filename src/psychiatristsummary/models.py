"""The record class for one WHO psychiatrist record."""


class PsychiatristRecord:
    """One country's psychiatrists per 100,000 people for one year."""

    def __init__(self, raw_record):
        region = raw_record.get("ParentLocation")
        rate = raw_record.get("NumericValue")

        if region is None or region == "":
            raise ValueError("Record has no region.")

        if rate is None:
            raise ValueError("Record has no psychiatrist rate.")

        try:
            rate = float(rate)
        except (TypeError, ValueError):
            raise ValueError("Psychiatrist rate is not a number.")

        self.region = region
        self.rate = rate
        self.year = raw_record.get("TimeDim")
        self.country_code = raw_record.get("SpatialDim")

    def __str__(self):
        return f"{self.country_code} ({self.region}, {self.year}): {self.rate} psychiatrists per 100,000"