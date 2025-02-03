import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt

# Dummy Data
dummy_stock_price = 500
dummy_stock_prices = np.cumsum(np.random.randn(100)) + 100
dummy_dates = pd.date_range(start="2023-01-01", periods=100, freq="D")
dummy_error = np.random.uniform(2, 5)
dummy_buy_sell = "BUY" if np.random.rand() > 0.5 else "SELL"

# Heatmap Data
heatmap_data = pd.DataFrame(np.random.rand(10, 10), 
                            columns=[f"Stock {i+1}" for i in range(10)], 
                            index=[f"Stock {i+1}" for i in range(10)])

# Set Full-Width Layout
st.set_page_config(page_title="Stock Dashboard", layout="wide")

# Page Title
st.title("📊 Stock Analysis Dashboard")

# ================================
# **TOP HALF**
# ================================
col1, col2 = st.columns([1, 3])  # Left = Name & Price, Right = Graph

# **Blue Section (Company Name & Price)**
with col1:
    st.markdown(
        f"""
        <div style="background-color:#3b82f6; padding:20px; border-radius:10px; text-align:center;">
            <h2 style="color:white;">Company Name</h2>
            <h1 style="color:white;">Rs. {dummy_stock_price}</h1>
        </div>
        """, unsafe_allow_html=True
    )

# **Red Section (Stock Price Graph)**
with col2:
    st.markdown('<div style="background-color:#dc2626; padding:10px; border-radius:10px;">', unsafe_allow_html=True)
    fig_live = go.Figure()
    fig_live.add_trace(go.Scatter(x=dummy_dates, y=dummy_stock_prices, mode="lines", name="Stock Price", line=dict(color="white")))
    fig_live.update_layout(template="plotly_dark", height=300, plot_bgcolor="red", paper_bgcolor="red", font_color="white")
    st.plotly_chart(fig_live, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ================================
# **MIDDLE SECTION**
# ================================
col3, col4 = st.columns([1, 2])  # Left = BUY/SELL, Right = Company Description

# **Pink Section (BUY/SELL & Stock Data)**
with col3:
    st.markdown(
        f"""
        <div style="background-color:#ec4899; padding:20px; border-radius:10px; text-align:center;">
            <h2 style="color:white;">{dummy_buy_sell}</h2>
            <p style="color:white;">Open: 490 | P. Close: 510</p>
            <h3 style="color:white;">Error = {dummy_error:.2f}%</h3>
        </div>
        """, unsafe_allow_html=True
    )

# **Yellow Section (Company Info)**
with col4:
    st.markdown(
        """
        <div style="background-color:#facc15; padding:20px; border-radius:10px; text-align:center;">
            <p style="color:black;">This section contains a brief description about the company and its operations in the renewable energy sector.</p>
        </div>
        """, unsafe_allow_html=True
    )

# ================================
# **BOTTOM HALF - HEATMAP**
# ================================
st.markdown('<div style="background-color:#2563eb; padding:10px; border-radius:10px; text-align:center;">', unsafe_allow_html=True)
st.markdown("<h3 style='color:white;'>🔥 Heatmap of Top 10 Stocks</h3>", unsafe_allow_html=True)

fig, ax = plt.subplots(figsize=(10, 5))
sns.heatmap(heatmap_data, annot=True, fmt=".2f", cmap="coolwarm", linewidths=0.5, ax=ax)
st.pyplot(fig)

st.markdown("</div>", unsafe_allow_html=True)

st.success("✅ Layout Successfully Implemented! Ready for Data Integration.")
