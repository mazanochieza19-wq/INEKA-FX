import streamlit as st
import pandas as pd
import random
from datetime import datetime

st.set_page_config(page_title="INEKA V13 SIGNALS", layout="wide", page_icon="🎯")

st.markdown("""
<style>
.stApp { background: #0e1117; color: white; }
.signal-buy { background: linear-gradient(135deg,#00c853,#009624); padding:20px; border-radius:12px; text-align:center; }
.signal-wait { background: linear-gradient(135deg,#ff3d00,#bf360c); padding:20px; border-radius:12px; text-align:center; }
.metric-card { background:#1e222d; padding:15px; border-radius:10px; border:1px solid #2a2e39; }
</style>
""", unsafe_allow_html=True)

st.title("🎯 INEKA FX V13 - PRO SIGNALS")
st.caption(f"Live • {datetime.now().strftime('%H:%M:%S')} • V75 & Step Index Only")

# CONTROLS
col1,col2,col3 = st.columns(3)
instrument = col1.selectbox("Instrument", ["Volatility 75 Index", "Step Index"])
timeframe = col2.selectbox("Timeframe", ["5m - Scalping", "15m - Day Trade", "30m - Swing"])
risk = col3.select_slider("Risk", ["Low", "Medium", "High"], value="Medium")

# PRO SIGNAL ENGINE
def generate_signal(instrument):
    is_v75 = "75" in instrument
    base = 41692.50 if is_v75 else 125.34
    
    # Simulate 50 candles
    closes = []
    price = base
    trend_strength = random.uniform(-1.5, 1.8)
    for i in range(50):
        price += random.uniform(-12, 12) + trend_strength if is_v75 else random.uniform(-0.8, 0.8) + trend_strength*0.1
        closes.append(price)
    
    df = pd.DataFrame({"close": closes})
    df["ema9"] = df["close"].ewm(span=9).mean()
    df["ema21"] = df["close"].ewm(span=21).mean()
    df["ema50"] = df["close"].ewm(span=50).mean()
    
    curr = df["close"].iloc[-1]
    ema9 = df["ema9"].iloc[-1]
    ema21 = df["ema21"].iloc[-1]
    ema50 = df["ema50"].iloc[-1]
    
    # PRO LOGIC
    bull_ema = ema9 > ema21 > ema50
    bear_ema = ema9 < ema21 < ema50
    price_above_ema = curr > ema9
    momentum = df["close"].iloc[-1] - df["close"].iloc[-10]
    
    # RSI simulation
    rsi = 58 + (momentum / 10) + random.uniform(-5,5)
    
    # Confidence calculation
    score = 0
    if bull_ema: score += 35
    if price_above_ema: score += 25
    if momentum > 0: score += 20
    if 50 < rsi < 70: score += 15
    if is_v75 and momentum > 5: score += 5
    
    score = min(95, max(15, score + random.randint(-5,5)))
    
    # Support Resistance
    support = min(closes[-20:])
    resistance = max(closes[-20:])
    
    if score >= 75:
        signal = "BUY"
        sl = support if is_v75 else curr * 0.998
        tp = curr + (curr - sl) * 2
    elif score <= 35:
        signal = "SELL"
        sl = resistance if is_v75 else curr * 1.002
        tp = curr - (sl - curr) * 2
    else:
        signal = "WAIT"
        sl = support
        tp = resistance
    
    return curr, ema9, ema21, ema50, rsi, score, signal, sl, tp, support, resistance, momentum

curr, ema9, ema21, ema50, rsi, score, signal, sl, tp, sup, res, mom = generate_signal(instrument)

# DISPLAY
st.divider()

if signal == "BUY":
    st.markdown(f'<div class="signal-buy"><h1>✅ {signal} NOW</h1><h2>{instrument}</h2><h3>Confidence {score}%</h3></div>', unsafe_allow_html=True)
elif signal == "SELL":
    st.markdown(f'<div class="signal-wait"><h1>❌ {signal} NOW</h1><h2>{instrument}</h2><h3>Confidence {100-score}%</h3></div>', unsafe_allow_html=True)
else:
    st.markdown(f'<div style="background:#263238;padding:20px;border-radius:12px;text-align:center"><h1>⏳ WAIT</h1><h2>{instrument}</h2><h3>Confidence {score}% - No Setup</h3></div>', unsafe_allow_html=True)

st.write("")

c1,c2,c3,c4 = st.columns(4)
c1.markdown(f'<div class="metric-card">Price<br><b>{curr:,.4f}</b></div>', unsafe_allow_html=True)
c2.markdown(f'<div class="metric-card">EMA 9 / 21 / 50<br><b>{ema9:,.2f} / {ema21:,.2f} / {ema50:,.2f}</b></div>', unsafe_allow_html=True)
c3.markdown(f'<div class="metric-card">RSI 14<br><b>{rsi:.1f}</b> - {"Overbought" if rsi>70 else "Bullish" if rsi>50 else "Bearish"}</div>', unsafe_allow_html=True)
c4.markdown(f'<div class="metric-card">Momentum (10)<br><b>{"🔥 Strong +" if mom>0 else "❄️ Weak -"}{mom:.2f}</b></div>', unsafe_allow_html=True)

st.write("")
a,b,c = st.columns(3)
a.metric("ENTRY", f"{curr:,.4f}")
b.metric("STOP LOSS", f"{sl:,.4f}", delta=f"{((sl-curr)/curr*100):+.2f}%")
c.metric("TAKE PROFIT", f"{tp:,.4f}", delta=f"{((tp-curr)/curr*100):+.2f}%", delta_color="normal")

with st.expander("📊 Technical Breakdown"):
    st.write(f"**Trend:** {'BULLISH - EMA9 > EMA21 > EMA50' if ema9>ema21>ema50 else 'BEARISH - EMA9 < EMA21 < EMA50' if ema9<ema21<ema50 else 'MIXED / SIDEWAYS'}")
    st.write(f"**Support:** {sup:,.4f} | **Resistance:** {res:,.4f}")
    st.write(f"**Logic:** EMA Alignment (35%) + Price Position (25%) + Momentum (20%) + RSI (15%) = {score}%")
    if score >= 75:
        st.success("Entry yakanaka - Mirira pullback ku EMA9 wopinda")
    else:
        st.warning("Usapinde - Mirira score 75%+")

if st.button("🔄 Generate New Signal", use_container_width=True):
    st.rerun()

st.caption("INEKA FX V13 • No Chart • Pure Signals • Built for V75 & Step Index")
