import streamlit as st
import pandas as pd
import pytz
from datetime import datetime
import time
import random
import numpy as np

st.set_page_config(page_title="INEKA STEP INDEX PRO", layout="wide")
st.markdown("<h1 style='text-align:center'>INEKA STEP INDEX PRO 🔥💰</h1>", unsafe_allow_html=True)

tz = pytz.timezone('Africa/Harare')
now = datetime.now(tz)
st.info(f"Harare: {now.strftime('%H:%M:%S')} | STEP INDEX 24/7 LIVE | Volatility: HIGH")

# STEP INDEX SIMULATION - Deriv style
# Step Index inofamba ne step - 0.1, 0.2 etc
@st.cache_data(ttl=10)
def get_step_data():
    # Simulate real Step Index movement
    np.random.seed(int(time.time()/10))
    base = 8250.0
    steps = []
    price = base
    for i in range(200):
        move = random.choice([-0.1, -0.1, 0.1, 0.1, 0.1, -0.1, 0.2, -0.2, 0, 0, 0, 0.1])
        # Step Index loves trending
        if len(steps) > 10:
            last_trend = steps[-1] - steps[-10]
            if last_trend > 0:
                move = random.choice([0.1, 0.1, 0.1, 0.2, 0, -0.1])
            else:
                move = random.choice([-0.1, -0.1, -0.1, -0.2, 0, 0.1])
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

c1, c2, c3, c4 = st.columns(4)
c1.metric("STEP INDEX", f"{price:.2f}", f"{change:.2f}")
c2.metric("24H HIGH", f"{float(df['High'].max()):.2f}")
c3.metric("24H LOW", f"{float(df['Low'].min()):.2f}")
c4.metric("SPREAD", "0.1 (Fixed)")

st.subheader("📈 Step Index Live Chart - 200 Ticks")
st.area_chart(df['Close'], height=400)

# STEP INDEX STRATEGY
# Step Index strategy: RSI + Support/Resistance + Step pattern
delta = df['Close'].diff()
gain = delta.where(delta > 0, 0).rolling(14).mean()
loss = -delta.where(delta < 0, 0).rolling(14).mean()
rs = gain / loss
rsi = 100 - (100 / (1 + rs))
rsi_now = float(rsi.iloc[-1]) if not pd.isna(rsi.iloc[-1]) else 50

# Support / Resistance
resistance = float(df['Close'].tail(50).max())
support = float(df['Close'].tail(50).min())
dist_to_res = resistance - price
dist_to_sup = price - support

st.markdown(f"### RSI: {rsi_now:.1f} | Support: {support:.2f} | Resistance: {resistance:.2f}")

# SIGNAL LOGIC FOR STEP INDEX
if rsi_now < 30 and dist_to_sup < 1.0:
    st.success(f"## 🟢 STRONG BUY - STEP INDEX")
    st.write(f"✅ RSI Oversold {rsi_now:.0f} + Near Support {support:.2f}")
    st.write("✅ Lot: 0.10 | SL: -1.5 | TP: +3.0 | Deriv Step Index")
    st.balloons()
elif rsi_now > 70 and dist_to_res < 1.0:
    st.error(f"## 🔴 STRONG SELL - STEP INDEX")
    st.write(f"✅ RSI Overbought {rsi_now:.0f} + Near Resistance {resistance:.2f}")
    st.write("✅ Lot: 0.10 | SL: -1.5 | TP: +3.0 | Deriv Step Index")
elif rsi_now < 40:
    st.success(f"## 🟢 BUY - RSI {rsi_now:.0f}")
    st.write("Mirira 2 ticks dzakatevedzana dzichik
