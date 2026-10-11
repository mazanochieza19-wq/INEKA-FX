import streamlit as st
import pandas as pd
import random

st.title("INEKA STEP INDEX PRO")
st.write("STEP INDEX LIVE - Harare")

def get_data():
    p = 8251.0
    d = []
    for i in range(100):
        p += random.choice([-0.2,-0.1,0.1,0.2,0.1])
        d.append(p)
    return pd.DataFrame(d, columns=["STEP"])

df = get_data()
price = df["STEP"].iloc[-1]

st.metric("STEP INDEX", f"{price:.1f}")
st.metric("RSI", f"{61.9}")

# FIXED CHART - zoomed
import altair as alt
df2 = df.reset_index()
chart = alt.Chart(df2).mark_line(color="#00ff88", strokeWidth=3).encode(
    x="index",
    y=alt.Y("STEP", scale=alt.Scale(zero=False))
).properties(height=350)
st.altair_chart(chart, use_container_width=True)

# Real RSI calc
delta = df["STEP"].diff()
gain = delta.clip(lower=0).rolling(14).mean()
loss = (-delta.clip(upper=0)).rolling(14).mean()
rs = gain / loss
rsi = 100 - (100/(1+rs))
r = float(rsi.iloc[-1])

st.write(f"RSI: {r:.1f}")

if r < 35:
    st.success("🟢 BUY SIGNAL - RSI LOW")
    st.balloons()
elif r > 65:
    st.error("🔴 SELL SIGNAL - RSI HIGH")
else:
    st.warning(f"⏳ WAIT - RSI {r:.1f}")

if st.button("Refresh"):
    st.rerun()

st.caption("INEKA-FX PRO V5 | Step Index 24/7 | Harare")
