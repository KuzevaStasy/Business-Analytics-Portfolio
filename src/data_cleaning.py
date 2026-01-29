import os
import pandas as pd


# ===== AUTO PROJECT ROOT =====
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RAW_PATH = os.path.join(BASE_DIR, "data", "raw", "data.csv")
PROCESSED_PATH = os.path.join(BASE_DIR, "data", "processed", "cleaned_data.csv")


def load_data():
    return pd.read_csv(RAW_PATH, encoding="latin-1")


def clean_data(df):
    df = df.dropna(subset=["CustomerID"])
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    df = df[df["Quantity"] > 0]
    df = df[df["UnitPrice"] > 0]
    df["TotalPrice"] = df["Quantity"] * df["UnitPrice"]
    return df


def save_cleaned_data(df):
    os.makedirs(os.path.dirname(PROCESSED_PATH), exist_ok=True)
    df.to_csv(PROCESSED_PATH, index=False)


if __name__ == "__main__":
    print("Loading from:", RAW_PATH)

    df = load_data()
    df = clean_data(df)
    save_cleaned_data(df)

    print("✅ Done! Saved to:", PROCESSED_PATH)
