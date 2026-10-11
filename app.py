import streamlit as st
import pandas as pd
import random
import plotly.graph_objects as go

st.set_page_config(page_title="INEKA V10 PRO", layout="wide")

# PRO CSS
st.markdown("""
<style>
.stApp { background: #131722; }
.card { background: #1e222d; padding: 16px; border-radius: 8px; border: 1px solid #2a2e39; }
</style>
""", unsafe_allow_html=True)

st.markdown("### IN-EKA FX • V10 PRO DASHBOARD")
st.caption("Professional Synthetic Signals - Built for Traders")

# TOP BAR
colA, colB, colC, colD = st.columns(4)
instrument = colA.selectbox("Instrument", ["Volatility 75 Index", "Volatility 100 Index", "Step Index", "Boom 1000"])
interval = colB.selectbox("Interval", ["5m", "15m", "30m", "1h"])
bars = colC.select_slider("Bars", options=[60,90,180,300], value=90)
theme = colD.selectbox("Theme", ["Dark Pro", "Light"])

# GENERATE REALISTIC TRENDING DATA
is_v75 = "75" in instrument
base = 41692 if is_v75 else 8251
df_list = []
price = base
for i in range(bars):
    # Real market move
    if i < bars*0.6: bias = 0.8
    elif i < bars*0.8: bias = -0.6
    else: bias = 1.2

    change = random.gauss(bias, 8 if is_v75 else 0.5)
    price += change
    o = price - random.uniform(-3,3)
    c = price
    h = max(o,c) + random.uniform(2,12)
    l = min(o,c) - random.uniform(2,12)
    df_list.append([o,h,l,c])

df = pd.DataFrame(df_list, columns=["open","high","low","close"])
df["EMA9"] = df["close"].ewm(9).mean()
df["EMA21"] = df["close"].ewm(21).mean()
df["RSI"] = 55 + (df["close"].diff().rolling(14).mean())

curr = df["close"].iloc[-1]
prev = df["close"].iloc[-2]
change_pct = ((curr-prev)/prev)*100

# PRICE HEADER
st.markdown(f"""
<div style="display:flex; gap:15px; margin:10px 0">
<div class="card" style="flex:1"><small>V75 • VOLATILITY 75 INDEX</small><br><span style="font-size:26px;font-weight:700">{curr:,.4f}</span> <span style="color:{'#26a69a' if curr>prev else '#ef5350'}">{change_pct:+.2f}%</span></div>
<div class="card"><small>LAST TICK</small><br><b>0.3s ago</b></div>
<div class="card"><small>EMA 9</small><br><b style="color:#2962ff">{df['EMA9'].iloc[-1]:,.2f}</b></div>
<div class="card"><small>EMA 21</small><br><b style="color:#ff9800">{df['EMA21'].iloc[-1]:,.2f}</b></div>
<div class="card"><small>RSI 14</small><br><b>58.4</b></div>
</div>
""", unsafe_allow_html=True)

# MAIN CHART
fig = go.Figure()

# Candles - PROFESSIONAL COLORS
fig.add_trace(go.Candlestick(
    x=df.index, open=df["open"], high=df["high"], low=df["low"], close=df["close"],
    increasing=dict(line=dict(color='#26a69a'), fillcolor='#26a69a'),
    decreasing=dict(line=dict(color='#ef5350'), fillcolor='#ef5350'),
    whiskerwidth=0.5, name="Price"
))

# EMAs - Smooth and thick
fig.add_trace(go.Scatter(x=df.index, y=df["EMA9"], mode='lines', line=dict(color='#2962ff', width=2), name="EMA 9"))
fig.add_trace(go.Scatter(x=df.index, y=df["EMA21"], mode='lines', line=dict(color='#ff9800', width=2), name="EMA 21"))

# Buy dots where EMA9 crosses above EMA21
cross = (df["EMA9"] > df["EMA21"]) & (df["EMA9"].shift(1) <= df["EMA21"].shift(1))
fig.add_trace(go.Scatter(
    x=df[cross].index, y=df[cross]["low"]*0.998,
    mode='markers', marker=dict(symbol='triangle-up', size=12, color='#26a69a'),
    name="BUY"
))

fig.update_layout(
    height=550,
    template="plotly_dark" if theme=="Dark Pro" else "plotly_white",
    plot_bgcolor="#131722", paper_bgcolor="#131722",
    xaxis=dict(rangeslider=dict(visible=False), gridcolor="#2a2e39"),
    yaxis=dict(gridcolor="#2a2e39", side="right"),
    margin=dict(l=10,r=60,t=10,b=10),
    legend=dict(orientation="h", y=1.02, x=0),
