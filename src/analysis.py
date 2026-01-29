import os
import pandas as pd


# ===== AUTO PROJECT ROOT =====
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CLEAN_DATA_PATH = os.path.join(
    BASE_DIR, "data", "processed", "cleaned_data.csv"
)


def load_clean_data():
    """Load cleaned dataset"""
    return pd.read_csv(CLEAN_DATA_PATH, parse_dates=["InvoiceDate"])


# ===== ANALYSIS FUNCTIONS =====

def monthly_revenue(df):
    # Гарантираме datetime
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

    # Групиране по месец чрез resample (най-сигурният начин)
    revenue = (
        df.set_index("InvoiceDate")
          .resample("ME")["TotalPrice"]
          .sum()
    )

    return revenue


def top_products(df, n=10):
    return (
        df.groupby("Description")["Quantity"]
        .sum()
        .sort_values(ascending=False)
        .head(n)
    )


def top_customers(df, n=10):
    return (
        df.groupby("CustomerID")["TotalPrice"]
        .sum()
        .sort_values(ascending=False)
        .head(n)
    )


def country_revenue(df, n=10):
    return (
        df.groupby("Country")["TotalPrice"]
        .sum()
        .sort_values(ascending=False)
        .head(n)
    )


def rfm_analysis(df):
    snapshot_date = df["InvoiceDate"].max()

    rfm = df.groupby("CustomerID").agg({
        "InvoiceDate": lambda x: (snapshot_date - x.max()).days,
        "InvoiceNo": "count",
        "TotalPrice": "sum"
    })

    rfm.columns = ["Recency", "Frequency", "Monetary"]

    return rfm


# =====
