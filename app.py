import streamlit as st
import pandas as pd
import pytz
from datetime import datetime
import random
import numpy as np
import time

st.set_page_config(page_title="INEKA STEP INDEX PRO", layout="wide")
st.markdown("<h1 style='text-align:center'>INEKA STEP INDEX PRO</h1>", unsafe_allow_html=True)

tz = pytz.timezone('Africa/Harare')
now = datetime.now(tz)
st.info(f"Harare: {now.strftime('%H:%M:%S')} | STEP INDEX 24/7 LIVE")

@st.cache_data(ttl=10)
def get_step_data():
    np.random.seed(int(time.time()/10))
    base = 8250.0
    steps = []
    price = base
    for i in range(200):
        move = random.choice([-0.1, -0.1, 0.1, 0.1, 0.1, -0.1, 0.2, -0.2, 0, 0, 0.1])
        price += move
        steps.append(price)
    df = pd.DataFrame(steps, columns=['Close'])
    df['High'] = df['Close'] + 0.3
    df['Low'] = df['Close'] - 0.3
    return df

df = get_step_data()
price = float(df['Close'].iloc[-1])
prev = float(df['Close'].iloc[-2])
change = price - prev
high_val = float(df['High'].max())
low_val = float(df['Low'].min())

c1, c2, c3 = st.columns(3)
c1.metric("STEP INDEX", f"{price:.2f}", f"{change:.2f}")
c2.metric("HIGH", f"{high_val:.2f}")
c3.metric("LOW", f"{low_val:.2f}")

st.subheader("Live Chart - 200 Ticks")
st.area_chart(df['Close'], height=380)

delta = df['Close'].diff()
gain = delta.where(delta > 0, 0).rolling(14).mean()
loss = -delta.where(delta < 0, 0).rolling(14).mean()
rs = gain / loss
rsi = 100 - (100 / (1 + rs))
rsi_now = float(rsi.iloc[-1]) if not pd.isna(rsi.iloc[-1]) else 50

resistance = float(df['Close'].tail(50).max())
support = float(df['Close'].tail(50).min())

st.write(f"RSI: {rsi_now:.1f} | Support: {support:.2f} | Resistance: {resistance:.2f}")

if rsi_now < 30:
    st.success(f"STRONG BUY - RSI {rsi_now:.0f}
