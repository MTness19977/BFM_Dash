import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

# Define stock ticker
ticker = "ADANIGREEN.NS"

st.title("📈 Adani Green Energy Stock Dashboard")

# Fetch 5 years of stock data
st.sidebar.header("Fetching Stock Data...")
data = yf.download(ticker, period="5y", interval="1d")
st.sidebar.success("Data Fetched Successfully!")

# Normalize Data
scaler = MinMaxScaler(feature_range=(0, 1))
data_scaled = scaler.fit_transform(data[['Close']])

# Split Data
train_size = int(len(data_scaled) * 0.8)
train_data, test_data = data_scaled[:train_size], data_scaled[train_size:]

# Create Sequences for LSTM
def create_sequences(data, seq_length=60):
    X, y = [], []
    for i in range(len(data) - seq_length):
        X.append(data[i:i + seq_length])
        y.append(data[i + seq_length])
    return np.array(X), np.array(y)

X_train, y_train = create_sequences(train_data)
X_test, y_test = create_sequences(test_data)

# Build LSTM Model
st.sidebar.header("Training LSTM Model...")
model = Sequential([
    LSTM(50, return_sequences=True, input_shape=(X_train.shape[1], 1)),
    Dropout(0.2),
    LSTM(50, return_sequences=False),
    Dropout(0.2),
    Dense(25),
    Dense(1)
])

model.compile(optimizer="adam", loss="mean_squared_error")
model.fit(X_train, y_train, epochs=20, batch_size=32, validation_data=(X_test, y_test))

# Make Predictions
predictions = model.predict(X_test)
predictions = scaler.inverse_transform(predictions)
actual_prices = scaler.inverse_transform(y_test.reshape(-1, 1))

# Calculate Error Percentage
mae = mean_absolute_error(actual_prices, predictions)
rmse = np.sqrt(mean_squared_error(actual_prices, predictions))
error_percentage = (mae / np.mean(actual_prices)) * 100

# Generate Buy/Sell Signals
buy_signals, sell_signals = [], []
for i in range(1, len(predictions)):
    if predictions[i] > predictions[i - 1]:  # Price increasing → BUY
        buy_signals.append(predictions[i])
        sell_signals.append(np.nan)
    else:  # Price decreasing → SELL
        sell_signals.append(predictions[i])
        buy_signals.append(np.nan)

# Live Stock Price
st.header("📊 Live Stock Price")
live_data = yf.Ticker(ticker).history(period="1d", interval="1m")
latest_price = live_data["Close"].iloc[-1]
st.metric(label="Current Price (₹)", value=f"{latest_price:.2f}")

# Stock Price Prediction Graph
st.header("📈 Stock Price Prediction (LSTM Model)")
fig_pred = go.Figure()
fig_pred.add_trace(go.Scatter(y=actual_prices.flatten(), mode="lines", name="Actual Price"))
fig_pred.add_trace(go.Scatter(y=predictions.flatten(), mode="lines", name="Predicted Price", line=dict(color="red")))
fig_pred.update_layout(title="Stock Price Prediction", xaxis_title="Days", yaxis_title="Price (₹)", template="plotly_dark")
st.plotly_chart(fig_pred)

# Buy/Sell Decision Graph
st.header("📉 Buy/Sell Decision")
fig_signals = go.Figure()
fig_signals.add_trace(go.Scatter(y=actual_prices.flatten(), mode="lines", name="Actual Price", opacity=0.6))
fig_signals.add_trace(go.Scatter(y=buy_signals, mode="markers", name="Buy Signal", marker=dict(color="green", symbol="triangle-up")))
fig_signals.add_trace(go.Scatter(y=sell_signals, mode="markers", name="Sell Signal", marker=dict(color="red", symbol="triangle-down")))
fig_signals.update_layout(title="Buy/Sell Decisions", xaxis_title="Days", yaxis_title="Price (₹)", template="plotly_dark")
st.plotly_chart(fig_signals)

# Error Metrics
st.header("📊 Prediction Error Metrics")
st.write(f"**Mean Absolute Error (MAE):** {mae:.2f}")
st.write(f"**Root Mean Squared Error (RMSE):** {rmse:.2f}")
st.write(f"**Error Percentage:** {error_percentage:.2f}%")

st.success("Dashboard Updated Successfully! ✅")

