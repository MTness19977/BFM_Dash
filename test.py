import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import datetime

# Set Streamlit Page Configuration
st.set_page_config(page_title="Stock Dashboard", layout="wide")

# Define the available companies
companies = {
    "Nifty Energy": "^CNXENERGY",
    "Adani Green": "ADANIGREEN.NS",
    "Tata Power": "TATAPOWER.NS",
    "JSW Energy": "JSWENERGY.NS",
    "NTPC": "NTPC.NS",
    "Power Grid Corp": "POWERGRID.NS",
    "NHPC": "NHPC.NS",
}

# Store Prediction Data
@st.cache_data
def get_historical_data(ticker):
    stock = yf.Ticker(ticker)
    data = stock.history(period="5y")  # Fetching last 5 years data
    data = data.loc[data.index <= "2025-01-25"]  # Use data only until Jan 25, 2025
    return data

# Function to predict stock price using linear regression
@st.cache_data
def predict_stock_price(data):
    data["Days"] = (data.index - data.index[0]).days
    X = np.array(data["Days"]).reshape(-1, 1)
    y = np.array(data["Close"]).reshape(-1, 1)

    model = LinearRegression()
    model.fit(X, y)
    future_days = np.array([X[-1][0] + i for i in range(1, 31)]).reshape(-1, 1)  # Predict next 30 days
    future_predictions = model.predict(future_days)

    return future_days.flatten(), future_predictions.flatten()

# Function to get real-time stock data
def get_live_stock_price(ticker):
    stock = yf.Ticker(ticker)
    return stock.history(period="1d")["Close"].iloc[-1]

# Layout using Streamlit Columns
st.title("📈 Green Energy Stock Dashboard")

# Dropdown for selecting company
selected_company = st.selectbox("Select a company:", list(companies.keys()), index=0)

# Fetch stock data
ticker = companies[selected_company]
data = get_historical_data(ticker)

# Fetch real-time price
real_time_price = get_live_stock_price(ticker)

# Predict stock prices
future_days, future_predictions = predict_stock_price(data)

# Layout Grid
col1, col2 = st.columns([1, 3])  # Sidebar section for Name & Price | Graph Section
col3, col4, col5 = st.columns([1, 2, 1])  # BUY/SELL, Description, Heatmap

# BLUE SECTION - Company Name & Price
with col1:
    st.markdown(
        f"""
        <div style="background-color:#5DADE2; padding:20px; text-align:center; border-radius:10px;">
            <h2 style="color:white;">{selected_company}</h2>
            <h3 style="color:white;">Rs. {real_time_price:.2f}</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )

# RED SECTION - Stock Price Graph
with col2:
    fig = px.line(data, x=data.index, y="Close", title=f"{selected_company} Stock Price", template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

# PINK SECTION - BUY/SELL Indicator
with col3:
    buy_sell_signal = "BUY" if future_predictions[-1] > data["Close"].iloc[-1] else "SELL"
    st.markdown(
        f"""
        <div style="background-color:#EC407A; padding:20px; text-align:center; border-radius:10px;">
            <h2 style="color:white;">{buy_sell_signal}</h2>
            <h4 style="color:white;">Open: {data['Open'].iloc[-1]:.2f} | Close: {data['Close'].iloc[-1]:.2f}</h4>
            <h3 style="color:white;">Error: ±2%</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )

# YELLOW SECTION - Company Description
with col4:
    st.markdown(
        """
        <div style="background-color:#FBC02D; padding:20px; border-radius:10px;">
            <p style="color:black; font-size:16px;">Lorem ipsum is simply dummy text of the printing and typesetting industry.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# BLUE SECTION - Market Cap Heatmap (Treemap)
with col5:
    market_caps = {
        "Adani Green": 150000,
        "Tata Power": 120000,
        "JSW Energy": 100000,
        "NTPC": 90000,
        "Power Grid": 85000,
        "NHPC": 70000,
        "Company 7": 65000,
        "Company 8": 60000,
        "Company 9": 50000,
        "Company 10": 40000,
    }
    df_market_caps = pd.DataFrame(list(market_caps.items()), columns=["Company", "Market Cap"])
    fig_heatmap = px.treemap(df_market_caps, path=["Company"], values="Market Cap", title="Top 10 Market Cap Distribution")
    st.plotly_chart(fig_heatmap, use_container_width=True)
