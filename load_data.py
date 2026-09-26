from pathlib import Path
import pandas as pd

# Folder containing the CSVs, found relative to this file
DATA_DIR = Path(__file__).resolve().parent / "CDC_Hackathon_Data"

YEARS = ["2021", "2022", "2023", "2024", "2025"]

def load_year(year):
    """Load one year's complaints, combining the parts if a year is split into several files."""
    files = sorted(DATA_DIR.glob(f"debt-complaints-{year}*.csv"))
    if not files:
        raise FileNotFoundError(f"No files found for {year} in {DATA_DIR}")
    df = pd.concat([pd.read_csv(f, dtype=str) for f in files], ignore_index=True)
    return df.drop_duplicates(subset="Complaint ID")


def load_all():
    """Load all years into one dataframe, with a year column and the target."""
    df = pd.concat(
        [load_year(y).assign(year=y) for y in YEARS],
        ignore_index=True,
    )
    # Target: 1 = company did not respond on time
    df["late"] = df["Timely response?"].eq("No").astype(int)
    return df