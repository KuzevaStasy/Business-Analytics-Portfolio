import os
import matplotlib.pyplot as plt
import pandas as pd

# Импорт от analysis.py
from src.analysis import (
    load_clean_data,
    monthly_revenue,
    top_products,
    country_revenue
)

# ===== AUTO PROJECT ROOT =====
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FIGURES_PATH = os.path.join(BASE_DIR, "reports", "figures")

# Създава папка за графики
os.makedirs(FIGURES_PATH, exist_ok=True)


# ===== PLOTTING FUNCTIONS =====

def plot_monthly_revenue(df):
    revenue = monthly_revenue(df)

    revenue.plot()
    plt.title("Monthly Revenue")
    plt.xlabel("Month")
    plt.ylabel("Revenue")

    plt.savefig(os.path.join(FIGURES_PATH, "monthly_revenue.png"))
    plt.show()


def plot_top_products(df):
    products = top_products(df)

    products.plot(kind="bar")
    plt.title("Top 10 Products")
    plt.xlabel("Product")
    plt.ylabel("Quantity Sold")

    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_PATH, "top_products.png"))
    plt.show()


def plot_country_revenue(df):
    countries = country_revenue(df)

    countries.plot(kind="bar")
    plt.title("Top Countries by Revenue")
    plt.xlabel("Country")
    plt.ylabel("Revenue")

    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_PATH, "country_revenue.png"))
    plt.show()


# ===== TEST RUN =====
if __name__ == "__main__":
    print("Loading cleaned data...")

    df = load_clean_data()

    print("Generating plots...")

    plot_monthly_revenue(df)
    plot_top_products(df)
    plot_country_revenue(df)

    print(f"✅ Plots saved in: {FIGURES_PATH}")
