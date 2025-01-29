import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# Dummy data placeholders
dummy_stock_prices = np.cumsum(np.random.randn(100)) + 100  # Random stock prices
dummy_dates = pd.date_range(start="2023-01-01", periods=100, freq="D")
dummy_error = np.random.uniform(2, 5)  # Dummy error percentage

# Dashboard Title
st.set_page_config(page_title="Financial Dashboard", layout="wide")
st.title("📊 Financial Dashboard - NIFTY Green Energy")

# Layout - Sidebar
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Overview", "Stock Analysis", "Index Analysis", "Predictions"])

# Layout - Main Sections
if page == "Overview":
    st.subheader("📌 Dashboard Overview")
    st.write("This dashboard provides real-time stock tracking, predictive analysis, and key financial insights.")

elif page == "Stock Analysis":
    st.subheader("📈 Stock Analysis")
    
    col1, col2 = st.columns([2, 1])  # Creating two columns

    with col1:
        st.write("### Stock Price Movement")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dummy_dates, y=dummy_stock_prices, mode="lines", name="Stock Price"))
        fig.update_layout(template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.metric(label="Latest Price", value=f"₹{dummy_stock_prices[-1]:.2f}")
        st.metric(label="Error Percentage", value=f"{dummy_error:.2f}%")

elif page == "Index Analysis":
    st.subheader("📊 NIFTY Green Energy Index")
    st.write("Index movement and contribution of key stocks (Dummy Data).")

    # Dummy heatmap (contribution of stocks)
    heatmap_data = pd.DataFrame(np.random.rand(5, 5), columns=list("ABCDE"))
    st.write("### Stock Contribution Heatmap")
    st.dataframe(heatmap_data)

elif page == "Predictions":
    st.subheader("📉 Stock Price Prediction")
    st.write("Predicted price movements and Buy/Sell decisions (Dummy Data).")

    # Buy/Sell Signal
    fig_pred = go.Figure()
    fig_pred.add_trace(go.Scatter(x=dummy_dates, y=dummy_stock_prices, mode="lines", name="Predicted Price"))
    fig_pred.update_layout(template="plotly_dark")
    st.plotly_chart(fig_pred, use_container_width=True)

st.success("✅ Layout Setup Complete! Ready to integrate real data.")
