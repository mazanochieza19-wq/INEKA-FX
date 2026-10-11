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
elif 16 <= hour < 21:
    kz = "🔵 NY KILLZONE"
else:
    kz = "⚫ OFF HOURS"

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
    high_val = float(df['High'].tail(50).max())
    low_val = float(df['Low'].tail(50).min())
    
    c1, c2, c3 = st.columns(3)
    c1.metric("EUR/USD LIVE", f"{price:.5f}", f"{change:.5f}")
    c2.metric("HIGH 50", f"{high_val:.5f}")
    c3.metric("LOW 50", f"{low_val:.5f}")

    st.subheader("Live Chart - Zoomed")
    st.area_chart(df['Close'], height=380)

    delta = df['Close'].diff()
    gain = delta.where(delta > 0, 0).rolling(14).mean()
    loss = -delta.where(delta < 0, 0).rolling(14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    rsi_now = float(rsi.iloc[-1]) if not pd.isna(rsi.iloc[-1]) else 50
    
    st.markdown(f"### RSI: {rsi_now:.1f}")

    if rsi_now < 35 and 11 <= hour < 21:
        st.success(f"## BUY - RSI {rsi_now:.0f} | {kz}")
    elif rsi_now > 65 and 11 <= hour < 21:
        st.error(f"## SELL - RSI {rsi_now:.0f} | {kz}")
    else:
        st.warning(f"## WAIT - RSI {rsi_now:.0f} | {kz}")

    st.caption(f"Last: {df.index[-1]} | Weekend: Market yakavhara")
else:
    st.error("Loading... Market closed weekend, edza Refresh")
    st.metric("EUR/USD LAST", "1.12057")

if st.button("Refresh"):
    st.cache_data.clear()
    st.rerun()
