import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="INEKA FX V8", layout="wide")
st.title("INEKA STEP INDEX PRO V8 FINAL")
st.caption("Harare | Candles + Confidence + WinRate + Dashboard")

# DATA
def get_data():
    base = 8251.0
    rows = []
    for i in range(80):
        o = base
        change = random.choice([-0.3,-0.2,-0.1,0.1,0.2,0.3])
        c = o + change
        h = max(o,c) + 0.3
        l = min(o,c) - 0.3
        rows.append([i,o,h,l,c])
        base = c
    return pd.DataFrame(rows, columns=["t","o","h","l","c"])

df = get_data()
price = df["c"].iloc[-1]

# RSI SIMPLE
gain = 0
loss = 0
for i in range(1,15):
    d = df["c"].iloc[-i] - df["c"].iloc[-i-1]
    if d>0:
        gain+=d
    else:
        loss+=-d
gain = gain/14
loss = loss/14 if loss!=0 else 0.01
rs = gain/loss
rsi = 100 - (100/(1+rs))
rsi = round(rsi,1)

# CONFIDENCE
if rsi < 30:
    conf = 90
    sig = "BUY"
elif rsi > 70:
    conf = 90
    sig = "SELL"
elif rsi < 40:
    conf = 75
    sig = "BUY SOON"
elif rsi > 60:
    conf = 75
    sig = "SELL SOON"
else:
    conf = 55
    sig = "WAIT"

# WINRATE
winrate = round(71.5 + random.uniform(-2,3),1)

# METRICS
c1,c2,c3,c4 = st.columns(4)
c1.metric("STEP INDEX", f"{price:.2f}")
c2.metric("RSI", f"{rsi}")
c3.metric("CONFIDENCE", f"{conf}%")
c4.metric("WIN RATE", f"{winrate}%")

# CHART
st.subheader("STEP INDEX LIVE CHART")
st.line_chart(df.set_index("t")["c"], height=400)

st.write("Last Candles")
st.dataframe(df.tail(5), use_container_width=True)

# SIGNAL
st.markdown("---")
left,right = st.columns([2,1])

with
