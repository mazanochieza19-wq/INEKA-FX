import streamlit as st
import pandas as pd
import random
import plotly.graph_objects as go

st.set_page_config(page_title="INEKA V11", layout="wide")

st.markdown("<h2>INEKA FX • V11 PRO</h2>", unsafe_allow_html=True)

c1,c2,c3 = st.columns(3)
instrument = c1.selectbox("Instrument", ["Volatility 75 Index", "Step Index"])
interval = c2.selectbox("Interval", ["5m","15m","30m"])
bars = c3.slider("Bars", 60, 300, 90)

# Data
base = 41692 if "75" in instrument else 8251
prices = []
price = base
for i in range(bars):
    price += random.uniform(-8, 8)
    o = price - random.uniform(-2,2)
    c = price
    h = max(o,c) + random.uniform(1,8)
    l = min(o,c) - random.uniform(1,8)
    prices.append([o,h,l,c])

df = pd.DataFrame(prices, columns=["open","high","low","close"])
df["EMA9"] = df["close"].ewm(span=9).mean()
df["EMA21"] = df["close"].ewm(span=21).mean()

curr = df["close"].iloc[-1]
st.metric(instrument, f"{curr:,.4f}")

# CHART - SIMPLE NO ERROR
fig = go.Figure()
fig.add_trace(go.Candlestick(
    x=df.index,
    open=df["open"],
    high=df["high"],
    low=df["low"],
    close=df["close"],
    name="Price"
))
fig.add_trace(go.Scatter(x=df.index, y=df["EMA9"], line=dict(color="blue", width=2), name="EMA 9"))
fig.add_trace(go.Scatter(x=df.index, y=df["EMA21"], line=dict(color="orange", width=2), name="EMA 21"))

fig.update_layout(height=500, xaxis_rangeslider_visible=False, template="plotly_dark")

st.plotly_chart(fig, use_container_width=True)

# SIGNAL
if df["EMA9"].iloc[-1] > df["EMA21"].iloc[-1]:
    st.success(f"✅ BUY SIGNAL - Price {curr:,.2f} above EMA 9 & EMA 21")
    st.balloons()
else:
    st.warning(f"⏳ WAIT - Price {curr:,.2f} - No buy setup")

if st.button("Refresh"):
    st.rerun()
