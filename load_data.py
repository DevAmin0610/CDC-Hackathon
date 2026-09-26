from pathlib import Path
import pandas as pd

# Folder containing the CSVs, found relative to this file
DATA_DIR = Path(__file__).resolve().parent / "CDC_Hackathon_Data"

YEARS = ["2021", "2022", "2023", "2024"]


def load_year(year):
    """Load one year's debt collection complaints."""
    return pd.read_csv(DATA_DIR / f"debt-complaints-{year}.csv", dtype=str)


def load_all():
    """Load all years into one dataframe, with a year column and the target."""
    df = pd.concat(
        [load_year(y).assign(year=y) for y in YEARS],
        ignore_index=True,
    )
    # Target: 1 = company did not respond on time
    df["late"] = df["Timely response?"].eq("No").astype(int)
    return df