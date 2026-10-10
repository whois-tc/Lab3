"""Settings for the psychiatristsummary package."""

from pathlib import Path

API_URL = "https://ghoapi.azureedge.net/api/MH_6"
TIMEOUT = 10
OUTPUT_PATH = Path("data/processed/summary.json")