import streamlit as st
import pandas as pd
import os

# ===== PAGE CONFIG =====
st.set_page_config(layout="wide")

# ===== PATH =====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "cleaned_data.csv"
)

# ===== LOAD DATA =====
@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH, parse_dates=["InvoiceDate"])

df = load_data()

# ===== SIDEBAR FILTERS =====
st.sidebar.header("🔍 Filters")

# Date filter
min_date = df["InvoiceDate"].min()
max_date = df["InvoiceDate"].max()

date_range = st.sidebar.date_input(
    "Select Date Range",
    [min_date, max_date]
)

# Country filter
countries = df["Country"].unique()
selected_countries = st.sidebar.multiselect(
    "Select Country",
    countries,
    default=countries
)

# Apply filters
filtered_df = df[
    (df["InvoiceDate"] >= pd.to_datetime(date_range[0])) &
    (df["InvoiceDate"] <= pd.to_datetime(date_range[1])) &
    (df["Country"].isin(selected_countries))
]

# ===== TITLE =====
st.title("🛒 E-Commerce Analytics Dashboard")

# ===== KPIs =====
st.header("📊 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Revenue", f"£{filtered_df['TotalPrice'].sum():,.0f}")
col2.metric("Orders", filtered_df["InvoiceNo"].nunique())
col3.metric("Customers", filtered_df["CustomerID"].nunique())

# ===== MONTHLY REVENUE =====
st.header("📈 Monthly Revenue")

monthly = (
    filtered_df
    .set_index("InvoiceDate")
    .resample("MS")["TotalPrice"]
    .sum()
)

st.line_chart(monthly)

# ===== TOP PRODUCTS =====
st.header("🛍 Top Products")

top_products = (
    filtered_df
    .groupby("Description")["Quantity"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.bar_chart(top_products)

# ===== COUNTRY REVENUE =====
st.header("🌍 Revenue by Country")

country_rev = (
    filtered_df
    .groupby("Country")["TotalPrice"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(country_rev)

# ===== DATA PREVIEW =====
if st.checkbox("Show Data Sample"):
    st.dataframe(filtered_df.head(50))
