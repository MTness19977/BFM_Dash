import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Dummy Data
companies = ["Adani Green", "Suzlon Energy", "Tata Power", "ReNew Energy", "JSW Energy", "NHPC"]
selected_company = st.selectbox("Select a Company", companies)

dummy_stock_price = 500
dummy_stock_prices = np.cumsum(np.random.randn(100)) + 100
dummy_dates = pd.date_range(start="2023-01-01", periods=100, freq="D")
dummy_error = np.random.uniform(2, 5)
dummy_buy_sell = "BUY" if np.random.rand() > 0.5 else "SELL"

dummy_market_caps = [120, 95, 80, 70, 60, 50]  # Market Cap values for treemap

df_market = pd.DataFrame({"Company": companies, "Market Cap": dummy_market_caps})

# Set Full-Width Layout
st.set_page_config(page_title="Stock Dashboard", layout="wide")

# ================================
# **TOP HALF**
# ================================
col1, col2 = st.columns([1, 3])  # Left = Dropdown & Price, Right = Graph

# **Dropdown for Company Selection & Price Display**
with col1:
    st.markdown("<div style='background-color:#3b82f6; padding:20px; border-radius:10px; text-align:center;'>", unsafe_allow_html=True)
    st.write(f"### {selected_company}")
    st.write(f"## Rs. {dummy_stock_price}")
    st.markdown("</div>", unsafe_allow_html=True)

# **Stock Price Graph**
with col2:
    fig_live = go.Figure()
    fig_live.add_trace(go.Scatter(x=dummy_dates, y=dummy_stock_prices, mode="lines", name="Stock Price", line=dict(color="white")))
    fig_live.update_layout(template="plotly_dark", height=300, plot_bgcolor="red", paper_bgcolor="red", font_color="white")
    st.plotly_chart(fig_live, use_container_width=True)

# ================================
# **MIDDLE SECTION**
# ================================
col3, col4 = st.columns([1, 2])  # Left = BUY/SELL, Right = Company Description

# **BUY/SELL Section**
with col3:
    st.markdown(f"""
        <div style="background-color:#ec4899; padding:20px; border-radius:10px; text-align:center;">
            <h2 style="color:white;">{dummy_buy_sell}</h2>
            <p style="color:white;">Open: 490 | P. Close: 510</p>
            <h3 style="color:white;">Error = {dummy_error:.2f}%</h3>
        </div>
    """, unsafe_allow_html=True)

# **Company Description**
with col4:
    st.markdown("""
        <div style="background-color:#facc15; padding:20px; border-radius:10px; text-align:center;">
            <p style="color:black;">This section contains a brief description about the company and its operations in the renewable energy sector.</p>
        </div>
    """, unsafe_allow_html=True)

# ================================
# **BOTTOM HALF - TREEMAP**
# ================================
st.markdown('<div style="background-color:#2563eb; padding:10px; border-radius:10px; text-align:center;">', unsafe_allow_html=True)
st.markdown("<h3 style='color:white;'>📊 Market Cap Distribution</h3>", unsafe_allow_html=True)

fig_tree = px.treemap(df_market, path=["Company"], values="Market Cap", color="Market Cap", color_continuous_scale="Blues")
st.plotly_chart(fig_tree, use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

st.success("✅ Layout Successfully Updated!")
