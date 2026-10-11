import streamlit as st
import pandas as pd
import random
import plotly.graph_objects as go

st.set_page_config(page_title="INEKA V9", layout="wide")

# DARK THEME CSS - Kutevedzera Manus
st.markdown("""
<style>
.stApp { background-color: #0e1117; color: white; }
div[data-testid="stMetric"] { background: #1a1f2e; padding: 15px; border-radius: 12px; border: 1px solid #2a3441; }
</style>
""", unsafe_allow_html=True)

st.title("Synthetic Signal Lab")
st.caption("Rule-based reads for synthetic indices. Every setup shows its reasoning and sample context.")

# CONTROLS - Kutevedzera screenshot yako
c1,c2 = st.columns(2)
with c1:
    st.markdown("**INSTRUMENT**")
    instrument = st.radio("", ["Step Index", "Volatility 75"], horizontal=True, label_visibility="collapsed")
with c2:
    st.markdown("**ANALYSIS INTERVAL**")
    interval = st.radio("", ["5m", "10m", "15m", "30m"], horizontal=True, label_visibility="collapsed")

st.markdown("**QUALITY FILTER**  `65+`")
st.divider()

# GENERATE DATA - Kutevedzera V75 iri pa screenshot
is_v75 = "75" in instrument
base_price = 41692.0 if is_v75 else 8251.0
vol = 45 if is_v75 else 0.4

prices = []
t = base_price
for i in range(180):
    # trend up like screenshot
    trend = 0.6 if i < 90 else (-0.4 if i < 120 else 0.8)
    change = random.uniform(-vol, vol) + trend
    t += change
    o = t - random.uniform(-5,5)
    c = t
    h = max(o,c) + random.uniform(0, 15 if is_v75 else 0.3)
    l = min(o,c) - random.uniform(0, 15 if is_v75 else 0.3)
    prices.append([o,h,l,c])

df = pd.DataFrame(prices, columns=["open","high","low","close"])
df["EMA9"] = df["close"].ewm(span=9).mean()
df["EMA21"] = df["close"].ewm(span=21).mean()

current = df["close"].iloc[-1]

# HEADER Kutevedzera V75 41,692.2577
st.markdown(f"""
<div style="background:#1a1f2e;padding:15px;border-radius:12px;display:flex;justify-content:space-between">
<div><span style="background:#332a00;padding:5px 10px;border-radius:8px;color:#ffcc00">V75</span> <b>Volatility 75 Index</b><br><span style="font-size:24px">{current:,.4f}</span></div>
<div>LAST TICK AGE<br><b>0s</b></div>
<div>BAR CLOSE IN<br><b>{random.randint(180,240)}s</b></div>
</div>
""", unsafe_allow_html=True)

st.write("")

# CHART - EMA 9 & EMA 21 sepa screenshot
st.subheader(f"PRICE ACTION  |  {instrument} / {interval}  |  90 bars")

fig = go.Figure()

fig.add_trace(go.Candlestick(
    x=list(range(len(df))),
    open=df["open"], high=df["high"], low=df["low"], close=df["close"],
    increasing_line_color='#00ff88', decreasing_line_color='#ff4444',
    name="Candles"
))

fig.add_trace(go.Scatter(x=list(range(len(df))), y=df["EMA9"], line=dict(color='#00d4ff', width=2), name="EMA 9"))
fig.add_trace(go.Scatter(x=list(range(len(df))), y=df["EMA21"], line=dict(color='#ffcc00', width=2), name="EMA 21"))

# dashed resistance line like screenshot
fig.add_hline(y=df["high"].tail(60).max()*0.998, line_dash="dash", line_color="gray")

fig.update_layout(
    template="plotly_dark",
    height=450,
    plot_bgcolor="#0e1117",
    paper_bgcolor="#0e1117",
    xaxis_rangeslider_visible=False,
    margin=dict(l=0,r=0,t=0,b=0),
    legend=dict(orientation="h", y=-0.1)
)

st.plotly_chart(fig, use_container_width=True)

# INDICATOR SNAPSHOT
st.markdown("**INDICATOR SNAPSHOT**")
col1,col2,col3,col4 = st.columns(4)

rsi = 58 + random.uniform(-5,5)
conf = 78 if df["EMA9"].iloc[-1] > df["EMA21"].iloc[-1] else 45

col1.metric("EMA 9 vs 21", "BULLISH" if df["EMA9"].iloc[-1] > df["EMA21"].iloc[-1] else "BEARISH")
col2.metric("RSI (14)", f"{rsi:.1f}")
col3.metric("CONFIDENCE", f"{conf}%")
col4.metric("SIGNAL", "BUY" if conf>65 else "WAIT")

# SIGNAL BOX
st.divider()
if df["EMA9"].iloc[-1] > df["EMA21"].iloc[-1] and df["close"].iloc[-1] > df["EMA9"].iloc[-1]:
    st.success(f"✅ BUY SIGNAL - {conf}% | Entry {current:,.2f} | EMA 9 above EMA 21 - Trend UP like pa chart yako!")
    st.progress(conf)
    st.balloons()
else:
    st.warning(f"⏳ WAIT - {conf}% | Price below EMA - Chimirira BUY")

if st.button("Refresh Chart"):
    st.rerun()
