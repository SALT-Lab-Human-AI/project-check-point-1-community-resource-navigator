import pandas as pd
from prototype.app import load_services_csv, parse_latlon

def test_load_services_csv_structure():
    df = load_services_csv("data/services.csv")
    # Basic structure validation
    required_cols = {"name", "category", "address", "description", "retrieval_text"}
    assert required_cols.issubset(df.columns)
    assert len(df) > 0

def test_parse_latlon_formats():
    samples = ["39.95,-75.16", "-75.16,39.95", "39.95 -75.16"]
    results = [parse_latlon(s) for s in samples]
    for lat, lon in results:
        assert -90 <= lat <= 90
        assert -180 <= lon <= 180
