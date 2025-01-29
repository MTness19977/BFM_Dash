import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt

# Dummy data for testing layout
dummy_stock_prices = np.cumsum(np.random.randn(100)) + 100  # Random stock prices
dummy_dates = pd.date_range(start="2023-01-01", periods=100, freq="D")
dummy_error = np.random.uniform(2, 5)  # Dummy error percentage

# Dummy heatmap data for Top 10 NIFTY Green Energy stocks
heatmap_data = pd.DataFrame(np.random.rand(10, 10), 
                            columns=[f"Stock {i+1}" for i in range(10)], 
                            index=[f"Stock {i+1}" for i in range(10)])

# Dashboard Title
st.set_page_config(page_title="Financial Dashboard", layout="wide")
st.title("📊 Financial Dashboard - NIFTY Green Energy")

# ================================
# TOP HALF - LIVE & PREDICTED STOCK DATA
# ================================
st.markdown("### 📈 Live & Predicted Stock Prices")

# Creating two columns for live stock and prediction graph
col1, col2 = st.columns(2)

with col1:
    st.write("#### Live Stock Price Movement")
    fig_live = go.Figure()
    fig_live.add_trace(go.Scatter(x=dummy_dates, y=dummy_stock_prices, mode="lines", name="Live Price"))
    fig_live.update_layout(template="plotly_dark", height=400)
    st.plotly_chart(fig_live, use_container_width=True)

with col2:
    st.write("#### Predicted Stock Price Trend")
    fig_pred = go.Figure()
    fig_pred.add_trace(go.Scatter(x=dummy_dates, y=dummy_stock_prices, mode="lines", name="Predicted Price", line=dict(color="red")))
    fig_pred.update_layout(template="plotly_dark", height=400)
    st.plotly_chart(fig_pred, use_container_width=True)

# ================================
# BOTTOM HALF - HEATMAP OF TOP 10 STOCKS
# ================================
st.markdown("### 🔥 Heatmap of Top 10 Stocks Affecting NIFTY Green Energy")

fig, ax = plt.subplots(figsize=(10, 5))
sns.heatmap(heatmap_data, annot=True, fmt=".2f", cmap="coolwarm", linewidths=0.5, ax=ax)
st.pyplot(fig)

st.success("✅ Dashboard Layout Complete! Ready for Real Data Integration.")
