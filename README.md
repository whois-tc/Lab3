# Psychiatrist Summary

This package downloads WHO mental-health workforce records and summarizes psychiatrist access across WHO regions. It reports the average number of psychiatrists per 100,000 people in each region and counts records in three access levels.

## Data source

The data comes from the WHO Global Health Observatory API:

https://ghoapi.azureedge.net/api/MH_6

One record is one country's reported number of psychiatrists per 100,000 people for one year. The API returned 146 records when this project was run. The records sit inside a field named `value`, and countries are identified by three-letter codes rather than names.

## Setup

```bash
conda env create -f environment.yml
conda activate psychiatristsummary
pip install -r requirements.txt
pip install -e .
```

## Run

```bash
python main.py
```

A successful run prints the counts and results and saves them to `data/processed/summary.json`. If the download fails, the program prints an error message and stops without a traceback.

## Test

```bash
python -m unittest discover -s tests
```

The tests use handmade records and do not need a network connection.

## Layout

- `main.py`: the entry point. It creates the objects, connects them and prints the results. It contains no calculations.
- `src/psychiatristsummary/__init__.py`: re-exports the public classes and functions so they can be imported directly from the package.
- `src/psychiatristsummary/config.py`: the source URL, the timeout and the output path, kept in one place so they can change without editing the code.
- `src/psychiatristsummary/models.py`: the `PsychiatristRecord` class. It is separate because every other module depends on what a clean record looks like.
- `src/psychiatristsummary/sources.py`: the `WHOSource` class, which downloads the data. It is the only module that imports `requests`, so a change to the data source only affects this file.
- `src/psychiatristsummary/aggregations.py`: the `Aggregation` base class and its subclasses. Each calculation lives here, apart from the code that fetches or writes data.
- `src/psychiatristsummary/report.py`: builds the summary dictionary and writes it to JSON. It is separate because writing the output is a different job from calculating it.
- `tests/test_models.py`: tests for `PsychiatristRecord`.

## What moved where

| Lab 02 function | Where the code lives now |
|---|---|
| `download_data` | `WHOSource.fetch()` in `sources.py` |
| `clean_data` | The checks moved into `PsychiatristRecord.__init__()` in `models.py`. Skipping and counting bad records moved into the loop in `WHOSource.fetch()`. |
| `group_by_region` | `RegionAverages.compute()` in `aggregations.py` |
| `calculate_region_averages` | `RegionAverages.compute()` in `aggregations.py` |
| `count_access_levels` | `AccessLevelCounts.compute()` in `aggregations.py` |
| Set comprehension for years in `main` | `YearsCovered.compute()` in `aggregations.py` |
| `build_summary` | `build_summary()` in `report.py`, which now loops over a list of aggregation objects |
| `write_summary` | `write_summary()` in `report.py` |
| `main` | `main()` in `main.py` |
| `API_URL`, `OUTPUT` and the timeout of 10 | `config.py` |

## Design choices

`PsychiatristRecord` exists so that missing and malformed values are dealt with in one place. Its `__init__` raises a `ValueError` when the region is missing or blank, when the rate is missing, or when the rate cannot be converted to a number. A record that exists is always clean, so no other code needs to check the values again.

`WHOSource` exists to keep the download separate from everything else. Its `fetch()` method catches download errors and returns `None`, so `main.py` can print the error message without importing `requests`. It also catches the `ValueError` from each bad record, skips that record and counts it, which keeps the downloaded, valid and skipped counts the same as in Lab 02.

Inheritance is used for the aggregations. The `Aggregation` base class stores each aggregation's `name`, which becomes its key in the summary, and defines a `compute()` method that every subclass must replace. `RegionAverages`, `AccessLevelCounts` and `YearsCovered` each override `compute()`. `build_summary()` calls `compute()` on every object in the list without checking which subclass it is.

Adding one more aggregation means writing one new subclass with an `__init__` that passes its key name to `super().__init__()` and its own `compute()` method, then adding it to the list in `main.py`. Nothing in `report.py` needs to change.

## Known limitations

- The available records are from 2013 to 2017, so the results do not describe current psychiatrist access.
- The regional averages are simple averages of the country records. They are not weighted by population.
- Countries report in different years, so the regional averages do not represent one common year.
- The program depends on the WHO API being available. During this lab the API returned a 502 error for a period, and the program printed its error message as intended.
- The year and country code are stored without being checked, as in Lab 02.
- The output path is relative, so the program must be run from the repository root.
- The tests only cover `PsychiatristRecord`. Lab 04 will add tests for the other classes.