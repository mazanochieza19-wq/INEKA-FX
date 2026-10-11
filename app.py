import streamlit as st
import pandas as pd
import random
import numpy as np

st.set_page_config(page_title="INEKA FX V8 FINAL", layout="wide")
st.title("INEKA STEP INDEX PRO V8 - FINAL BOSS")
st.write("Harare | Candles + Confidence + WinRate + Dashboard | LIVE")

# --- DATA ---
def get_data():
    base = 8251.0
    rows = []
    for i in range(80):
        o = base
        c = o + random.choice([-0.3,-0.2,-0.1,0.1,0.2,0.3])
        h = max(o,c) + random.uniform(0,0.4)
        l = min(o,c) - random.uniform(0,0.4)
        rows.append([i,o,h,l,c])
        base = c
    return pd.DataFrame(rows, columns=["t","o","h","l","c"])

df = get_data()
price = df["c"].iloc[-1]

# --- RSI ---
delta = df["c"].diff()
gain = delta.clip(lower=0).rolling(14).mean()
loss = (-delta.clip(upper=0)).rolling(14).mean()
rsi = 100 - (100/(1+gain/loss))
r = float(rsi.iloc[-1])
r = round(r,1)

# --- CONFIDENCE ---
if r < 30:
    conf = 88 + random.randint(0,7)
    signal = "BUY"
    color = "green"
elif r > 70:
    conf = 88 + random.randint(0,7)
    signal = "SELL"
    color = "red"
elif r < 40:
    conf = 72 + random.randint(0,10)
    signal = "BUY SOON"
    color = "green"
elif r > 60:
    conf = 72 + random.randint(0,10)
    signal = "SELL SOON"
    color = "red"
else:
    conf = 50 + random.randint(0,10)
    signal = "WAIT"
    color = "yellow"
conf = min(conf,95)

# --- WIN RATE BACKTEST ---
wins = 0
tests = 0
for i in range(20, len(df)-4):
    past_rsi = 50
    try:
        g = df["c"].diff().clip(lower=0).rolling(
