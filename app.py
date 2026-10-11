import streamlit as st
import yfinance as yf
import pandas as pd
import pytz
from datetime import datetime

st.set_page_config(page_title="INEKA-FX PRO V3", layout="wide")
st.markdown("<h1 style='text-align:center'>INEKA-FX PRO V3 🔥</h1>", unsafe_allow_html=True)

tz = pytz.timezone('Africa/Harare')
now = datetime.now(tz)
hour = now.hour

if 11 <= hour < 16:
    kz = "🟢 LONDON KILLZONE - BEST"
    col = "green"
elif 16 <= hour < 21:
    kz = "🔵 NY KILLZONE"
    col = "blue"
else:
    kz = "⚫ OFF - WAIT"
    col = "gray"

st.info(f"Harare: {now.strftime('%H:%M:%S')} | {kz}")

@st.cache_data(ttl=60)
def get_data():
    try:
        df = yf.download("EURUSD=X", period="5d", interval="15m", progress=False, auto_adjust=True)
        if df.empty:
            df = yf.download("EURUSD=X", period="5d", interval="1h", progress=False, auto_adjust=True)
        return df
    except:
        return pd.DataFrame()

df = get_data()

if not df.empty:
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    
    df = df.tail(150).copy()
    price = float(df['Close'].iloc[-1])
    prev = float(df['Close'].iloc[-2])
    change = price - prev
    
    c1, c2, c3 = st.columns(3)
    c1.metric("EUR/USD LIVE", f"{price:.5f}", f"{change:.5f}")
    c2.metric("HIGH", f"{float
