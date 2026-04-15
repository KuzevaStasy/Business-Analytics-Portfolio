import os
import pandas as pd


def load_data(path: str) -> pd.DataFrame:
    """Load raw CSV data."""
    return pd.read_csv(path, encoding="latin-1")


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Full cleaning pipeline:
    1. Fix date type
    2. Remove missing CustomerID
    3. Remove returns (negative quantity)
    4. Remove invalid prices
    5. Remove duplicates
    6. Create TotalPrice
    7. Extract date parts
    8. Fix CustomerID type
    """
    df = df.copy()

    # 1. Fix date type
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

    # 2. Remove missing CustomerID
    df = df.dropna(subset=["CustomerID"])

    # 3. Remove returns
    df = df[df["Quantity"] > 0]

    # 4. Remove invalid prices
    df = df[df["UnitPrice"] > 0]

    # 5. Remove duplicates
    df = df.drop_duplicates()

    # 6. Create TotalPrice
    df["TotalPrice"] = df["Quantity"] * df["UnitPrice"]

    # 7. Extract date parts
    df["Year"]  = df["InvoiceDate"].dt.year
    df["Month"] = df["InvoiceDate"].dt.month
    df["Day"]   = df["InvoiceDate"].dt.day_name()
    df["Hour"]  = df["InvoiceDate"].dt.hour

    # 8. Fix CustomerID type
    df["CustomerID"] = df["CustomerID"].astype(int).astype(str)

    return df


def save_sample(df: pd.DataFrame, path: str, n: int = 10000) -> None:
    """Save a random sample of the cleaned data to CSV."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    sample = df.sample(n=min(n, len(df)), random_state=42)
    sample.to_csv(path, index=False)
    print(f"Saved {len(sample):,} rows to: {path}")
