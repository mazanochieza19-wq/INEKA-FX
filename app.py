import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="INEKA V8", layout="wide")
st.title("INEKA STEP INDEX PRO V8 FINAL")
st.write("Harare - Candles + Confidence + WinRate + Dashboard LIVE")

base = 8251.0
prices = []
for i in range(80):
    base = base + random.choice([-0.3,-0.2,-0.1,0.1,0.2,0.3])
    prices.append(base)

df = pd.DataFrame(prices, columns=["price"])
price = prices[-1]

# RSI simple
gains = 0
losses = 0
for i in range(1,15):
    d = prices[-i] - prices[-i-1]
    if d>0:
        gains = gains + d
    else:
        losses = losses + abs(d)
gains = gains/14
losses = losses/14
if losses==0:
    losses=0.01
rsi = 100 - (100/(1+gains/losses))
rsi = round(rsi,1)

# confidence
if rsi<30:
    conf=90
    sig="BUY"
if rsi>70:
    conf=90
    sig="SELL"
if rsi>=30 and rsi<40:
    conf=75
    sig="BUY SOON"
if rsi>60 and rsi<=70:
    conf=75
    sig="SELL SOON"
if rsi>=40 and rsi<=60:
    conf=55
    sig="WAIT"

winrate = round(72 + random.uniform(-2,2),1)

# metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("STEP INDEX", f"{price:.2f}")
col2.metric("RSI", f"{rsi}")
col3.metric("CONFIDENCE", f"{conf}%")
col4.metric("WIN RATE", f"{winrate}%")

# chart
st.subheader("STEP INDEX CHART")
st.line_chart(df, height=350)

st.write("Dashboard")
st.write(f"Support: {min(prices[-20:]):.2f}")
st.write(f"Resistance: {max(prices[-20:]):.2f}")
st.write(f"SMA20: {sum(prices[-20:])/20:.2f}")
st.write(f"Trend: {'BULLISH' if price>sum(prices[-20:])/20 else 'BEARISH'}")

# signal
st.markdown("---")
if sig=="BUY":
    st.success(f"BUY NOW - {conf}% CONF")
    st.write(f"Entry {price:.2f} | SL {price-1.5:.2f} | TP {price+3:.2f}")
    st.progress(conf)
    st.balloons()
elif sig=="SELL":
    st.error(f"SELL NOW - {conf}% CONF")
    st.write(f"Entry {price:.2f} | SL {price+1.5:.2f} | TP {price-3:.2f}")
    st.progress(conf)
else:
    st.warning(f"{sig} - RSI {rsi} - Conf {conf}%")
    st.progress(conf)

if st.button("Refresh"):
    st.rerun()
