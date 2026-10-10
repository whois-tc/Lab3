"""Aggregations: one base class and one subclass for each summary value."""


class Aggregation:
    """Base class for one calculation over a list of records."""

    def __init__(self, name):
        self.name = name

    def compute(self, records):
        """Each subclass replaces this with its own calculation."""
        raise NotImplementedError("Subclasses must define compute().")


class RegionAverages(Aggregation):
    """Average psychiatrist rate for each WHO region."""

    def __init__(self):
        super().__init__("region_averages")

    def compute(self, records):
        region_rates = {}

        for record in records:
            current_rates = region_rates.get(record.region)

            if current_rates is None:
                region_rates[record.region] = [record.rate]
            else:
                current_rates.append(record.rate)

        region_averages = {}

        for region in region_rates:
            rates = region_rates[region]
            average = sum(rates) / len(rates)
            region_averages[region] = round(average, 2)

        return region_averages


class AccessLevelCounts(Aggregation):
    """Number of records in each psychiatrist access level."""

    def __init__(self):
        super().__init__("access_counts")

    def compute(self, records):
        access_counts = {
            "Under 1": 0,
            "1 to 5": 0,
            "Over 5": 0
        }

        for record in records:
            if record.rate < 1:
                access_counts["Under 1"] += 1
            elif record.rate <= 5:
                access_counts["1 to 5"] += 1
            else:
                access_counts["Over 5"] += 1

        return access_counts


class YearsCovered(Aggregation):
    """The unique years in the records, in order."""

    def __init__(self):
        super().__init__("years")

    def compute(self, records):
        years = {record.year for record in records}
        return sorted(years)