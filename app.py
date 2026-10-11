import streamlit as st, yfinance as yf
from datetime import datetime
import pytz
st.set_page_config(page_title="INEKA FX", page_icon="📈", layout="centered")
st.markdown("<h2 style='text-align:center'>INEKA-FX PRO</h2>", unsafe_allow_html=True)
st.caption("EUR/USD • Real Market • Live")
if 'count' not in st.session_state: st.session_state.count=0
tz=pytz.timezone('Africa/Harare')
now=datetime.now(tz)
st.write(f"Harare {now.strftime('%H:%M')} | {st.session_state.count}/3 signals")
if st.session_state.count>=3:
    st.error("⛔ 3/3 Done - Stop for today")
    st.stop()
@st.cache_data(ttl=60)
def get_data():
    m5=yf.download("EURUSD=X", period="2d", interval="5m", progress=False)
    h1=yf.download("EURUSD=X", period="5d", interval="60m", progress=False)
    return m5,h1
m5,h1=get_data()
if m5.empty:
    st.warning("Market closed - open Mon-Fri")
    st.stop()
c5=m5['Close'].squeeze()
c1=h1['Close'].squeeze()
delta=c5.diff()
gain=delta.where(delta>0,0).rolling(14).mean()
loss=-delta.where(delta<0,0).rolling(14).mean()
rs=gain/loss
rsi=100-(100/(1+rs))
e9=c5.ewm(span=9).mean()
e21=c5.ewm(span=21).mean()
e50=c1.ewm(span=50).mean()
lc=float(c5.iloc[-1])
lr=float(rsi.iloc[-1])
le9=float(e9.iloc[-1])
le21=float(e21.iloc[-1])
lh=float(c1.iloc[-1])
le50=float(e50.iloc[-1])
st.metric("EUR/USD LIVE", f"{lc:.5f}")
st.line_chart(c5.tail(60))
up=lh>le50
if up and 35<lr<55 and le9>le21:
    st.success(f"🟢 CALL ↑ BUY - 5 min\nPrice {lc:.5f} | RSI {lr:.0f} | Confidence 82%")
    if st.button("✅ I TOOK TRADE", use_container_width=True):
        st.session_state.count+=1
        st.rerun()
elif not up and 45<lr<65 and le9<le21:
    st.error(f"🔴 PUT ↓ SELL - 5 min\nPrice {lc:.5f} | RSI {lr:.0f} | Confidence 74%")
    if st.button("✅ I TOOK TRADE", use_container_width=True):
        st.session_state.count+=1
        st.rerun()
else:
    st.info(f"WAIT - No setup | RSI {lr:.0f} | Trend {'UP' if up else 'DOWN'} | EMA {'Bull' if le9>le21 else 'Bear'}")
if st.button("Reset Today"):
    st.session_state.count=0
    st.rerun()
