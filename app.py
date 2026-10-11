import streamlit as st
import pandas as pd
import random

st.title("INEKA STEP INDEX PRO")

def get_data():
    p = 8250.0
    d = []
    for i in range(120):
        p += random.choice([-0.2,-0.1,0.1,0.2])
        d.append(p)
    return pd.DataFrame(d, columns=["price"])

df = get_data()
price = df["price"].iloc[-1]

st.metric("STEP INDEX", round(price,2))
st.area_chart(df, height=350)

# RSI simple
delta = df["price"].diff()
gain = delta.clip(lower=0).rolling(14).mean()
loss = (-delta.clip(upper=0)).rolling(14).mean()
rs = gain / loss
rsi = 100 - (100/(1+rs))
r = float(rsi.iloc[-1])

st.write("RSI:", round(r,1))

if r < 35:
    st.success("BUY - RSI LOW")
elif r > 65:
    st.error("SELL - RSI HIGH")
else:
    st.warning("WAIT")

if st.button("Refresh"):
    st.rerun()
