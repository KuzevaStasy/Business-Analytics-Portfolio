import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import streamlit as st

# ── Page config ────────────────────────────────────────
st.set_page_config(
    page_title="E-Commerce Sales Dashboard",
    page_icon="🛒",
    layout="wide"
)

# ── Paths ──────────────────────────────────────────────
ROOT      = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_PATH = os.path.join(ROOT, "data", "processed", "cleaned_data.csv")

# ── Load data ──────────────────────────────────────────
@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH, parse_dates=["InvoiceDate"])

df = load_data()

# ── Sidebar filters ────────────────────────────────────
st.sidebar.header("🔎 Filters")

# Date filter
min_date = df["InvoiceDate"].min().date()
max_date = df["InvoiceDate"].max().date()
date_range = st.sidebar.date_input(
    "Date Range",
    value=[min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

# Country filter
countries = ["All"] + sorted(df["Country"].unique().tolist())
selected_country = st.sidebar.selectbox("Country", countries)

# Apply filters
filtered = df.copy()
if len(date_range) == 2:
    filtered = filtered[
        (filtered["InvoiceDate"].dt.date >= date_range[0]) &
        (filtered["InvoiceDate"].dt.date <= date_range[1])
    ]
if selected_country != "All":
    filtered = filtered[filtered["Country"] == selected_country]

# ── Header ─────────────────────────────────────────────
st.title("🛒 E-Commerce Sales Dashboard")
st.caption("UK-based online retailer · 2010–2011 · Source: Kaggle")
st.divider()

# ── KPI cards ──────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)

total_revenue   = filtered["TotalPrice"].sum()
total_orders    = filtered["InvoiceNo"].nunique()
total_customers = filtered["CustomerID"].nunique()
avg_order_value = total_revenue / total_orders if total_orders > 0 else 0

col1.metric("💰 Total Revenue",    f"£{total_revenue:,.0f}")
col2.metric("📦 Total Orders",     f"{total_orders:,}")
col3.metric("👥 Unique Customers", f"{total_customers:,}")
col4.metric("🧾 Avg Order Value",  f"£{avg_order_value:,.2f}")

st.divider()

# ── Helper style ───────────────────────────────────────
def base_style():
    plt.rcParams.update({
        "figure.figsize"   : (10, 4),
        "axes.spines.top"  : False,
        "axes.spines.right": False,
        "axes.grid"        : True,
        "grid.alpha"       : 0.3,
        "font.size"        : 10,
    })

# ── Row 1: Monthly revenue + Top products ──────────────
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("📈 Monthly Revenue")
    monthly = (
        filtered.groupby(filtered["InvoiceDate"].dt.to_period("M"))["TotalPrice"]
        .sum()
        .reset_index()
    )
    monthly["InvoiceDate"] = monthly["InvoiceDate"].astype(str)

    base_style()
    fig, ax = plt.subplots()
    ax.plot(monthly["InvoiceDate"], monthly["TotalPrice"],
            marker="o", linewidth=2, color="#2563eb")
    ax.fill_between(range(len(monthly)), monthly["TotalPrice"],
                    alpha=0.1, color="#2563eb")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"£{x:,.0f}"))
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col_right:
    st.subheader("🛍 Top 10 Products")
    top_products = (
        filtered.groupby("Description")["TotalPrice"]
        .sum()
        .sort_values(ascending=True)
        .tail(10)
    )

    base_style()
    fig, ax = plt.subplots()
    bars = ax.barh(top_products.index, top_products.values, color="#2563eb")
    ax.bar_label(bars, fmt="£{:,.0f}", padding=4, fontsize=8)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"£{x:,.0f}"))
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

# ── Row 2: Country + Day of week ───────────────────────
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🌍 Revenue by Country (Top 10)")
    top_countries = (
        filtered.groupby("Country")["TotalPrice"]
        .sum()
        .sort_values(ascending=True)
        .tail(10)
    )

    base_style()
    fig, ax = plt.subplots()
    colors = ["#2563eb" if c == "United Kingdom" else "#93c5fd"
              for c in top_countries.index]
    bars = ax.barh(top_countries.index, top_countries.values, color=colors)
    ax.bar_label(bars, fmt="£{:,.0f}", padding=4, fontsize=8)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"£{x:,.0f}"))
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col_right:
    st.subheader("📅 Revenue by Day of Week")
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    by_day = filtered.groupby("Day")["TotalPrice"].sum().reindex(day_order)

    base_style()
    fig, ax = plt.subplots()
    ax.bar(by_day.index, by_day.values, color="#2563eb")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"£{x:,.0f}"))
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

# ── Row 3: RFM segments ────────────────────────────────
st.divider()
st.subheader("💎 Customer Segments (RFM)")

ref_date = filtered["InvoiceDate"].max() + pd.Timedelta(days=1)
rfm = filtered.groupby("CustomerID").agg(
    Recency   = ("InvoiceDate", lambda x: (ref_date - x.max()).days),
    Frequency = ("InvoiceNo",   "nunique"),
    Monetary  = ("TotalPrice",  "sum")
).reset_index()

import numpy as np
rfm["R_score"] = pd.qcut(rfm["Recency"],   q=4, labels=[4, 3, 2, 1]).astype(int)
rfm["F_score"] = pd.qcut(rfm["Frequency"].rank(method="first"), q=4, labels=[1, 2, 3, 4]).astype(int)
rfm["M_score"] = pd.qcut(rfm["Monetary"],  q=4, labels=[1, 2, 3, 4]).astype(int)
rfm["RFM_Score"] = rfm["R_score"] + rfm["F_score"] + rfm["M_score"]

def segment(score):
    if score >= 10: return "💎 Champions"
    elif score >= 8: return "🌟 Loyal"
    elif score >= 6: return "🔄 Potential"
    elif score >= 4: return "⚠️ At Risk"
    else:            return "❌ Lost"

rfm["Segment"] = rfm["RFM_Score"].apply(segment)

col_left, col_right = st.columns(2)

with col_left:
    segment_counts = rfm["Segment"].value_counts()
    base_style()
    fig, ax = plt.subplots()
    colors = ["#1d4ed8", "#2563eb", "#3b82f6", "#60a5fa", "#93c5fd"]
    ax.barh(segment_counts.index, segment_counts.values,
            color=colors[:len(segment_counts)])
    ax.bar_label(ax.containers[0], fmt="%d", padding=4, fontsize=9)
    ax.set_xlabel("Number of Customers")
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col_right:
    segment_revenue = rfm.groupby("Segment")["Monetary"].sum().sort_values(ascending=True)
    base_style()
    fig, ax = plt.subplots()
    ax.barh(segment_revenue.index, segment_revenue.values, color="#2563eb")
    ax.bar_label(ax.containers[0], fmt="£{:,.0f}", padding=4, fontsize=9)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"£{x:,.0f}"))
    ax.set_xlabel("Total Revenue (£)")
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

# ── Footer ─────────────────────────────────────────────
st.divider()
st.caption("Built with Python · pandas · matplotlib · Streamlit | © Stasy Kuzeva")
