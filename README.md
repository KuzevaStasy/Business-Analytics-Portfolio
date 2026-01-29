# 🛒 E-Commerce Sales Analysis

## 📌 Project Overview

This project analyzes real-world e-commerce transaction data to uncover sales trends, customer behavior, and revenue drivers.

The goal is to transform raw transactional data into actionable business insights that can support decision-making in marketing, sales, and operations.

---

## 🎯 Business Objectives

This analysis aims to answer:

- When does the business generate the most revenue?
- Which products drive the majority of sales?
- Who are the most valuable customers?
- How does performance vary by country?
- Are there signs of seasonality?

---

## 📊 Dataset

Source: Kaggle E-Commerce dataset  
Contains ~500k transactions from a UK-based online retailer (2010–2011).

Main fields:

- InvoiceNo
- Product Description
- Quantity
- InvoiceDate
- UnitPrice
- CustomerID
- Country

---

## 🧹 Data Cleaning

Steps performed:

- Removed missing CustomerID records  
- Filtered out returns (negative quantities)  
- Removed invalid prices  
- Converted dates to datetime format  
- Created TotalPrice metric  

---

## 📈 Exploratory Analysis

Key analyses include:

- Monthly revenue trends  
- Top-selling products  
- Revenue by country  
- Customer revenue ranking  
- RFM customer analysis  

---

## 🔍 Key Findings

- 📈 Revenue peaks in Q4, showing strong seasonality  
- 🛍 ~20% of products generate ~80% of sales  
- 🇬🇧 The UK dominates revenue contribution  
- 💎 A small group of customers drives a large share of revenue  

---

## 💡 Business Recommendations

- Focus marketing campaigns on high-value customers  
- Increase stock for top-performing products  
- Prepare for demand spikes in Q4  
- Explore expansion in high-performing countries  

---

## 📊 Interactive Dashboard

This project includes an interactive Streamlit dashboard.

Run locally:

streamlit run dashboard.py

---

## 🛠 Tech Stack

- Python  
- pandas  
- matplotlib  
- Jupyter Notebook  

---

## 📂 Project Structure

data/

notebooks/

src/

reports/

README.md


---

## 🚀 How to Run

1. Clone the repo  
2. Install requirements:

pip install -r requirements.txt


3. Run notebooks in order

---

