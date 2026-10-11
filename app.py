import streamlit as st
import yfinance as yf
import pandas as pd
import pytz
from datetime import datetime

st.set_page_config(page_title="INEKA-FX PRO V2", layout="wide")
st.markdown("<h1 style='text-align:center'>INEKA-FX PRO V2 🔥</h1>", unsafe_allow_html=True)

tz = pytz.timezone('Africa/Harare')
now = datetime.now(tz)
hour = now.hour
kz = "🟢 LONDON KILLZONE" if 11 <= hour < 16 else "🔵 NY KILLZONE" if 16 <= hour < 21 else "⏳ WAIT"
st.info(f"Harare: {now.strftime('%H:%M:%S')} | {kz}")

@st.cache_data(ttl=60)
def get_data():
    try:
        d = yf.download("EURUSD=X", period="2d", interval="15m", progress=False)
        if d.empty:
            d = yf.download("EURUSD=X", period="5d", interval="1h", progress=False)
        return d
    except:
        return pd.DataFrame()

df = get_data()
if not df.empty:
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    price = float(df['Close'].iloc[-1])
    st.metric("EUR/USD LIVE", f"{price:.5f}")
    st.line_chart(df['Close'].tail(150), height=400)
    delta = df['Close'].diff()
    gain = delta.where(delta > 0, 0).rolling(14).mean()
    loss = -delta.where(delta < 0, 0).rolling(14).mean()
    rsi = 100 - (100 / (1 + gain/loss))
    rsi_now = float(rsi.iloc[-1]) if not pd.isna(rsi.iloc[-1]) else 50
    if rsi_now < 35:
        st.success(f"🟢 BUY - RSI {rsi_now:.0f}")
    elif rsi_now > 65:
        st.error(f"🔴 SELL - RSI {rsi_now:.0f}")
    else:
        st.warning(f"⏳ WAIT - RSI {rsi_now:.0f} | {kz}")
else:
    st.error("Loading...")

if st.button("🔄 Refresh"):
    st.cache_data.clear()
    st.rerun()
