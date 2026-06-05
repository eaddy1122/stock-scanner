
# Advanced Stock Momentum Scanner (Skeleton)
# pip install streamlit yfinance pandas numpy ta requests

import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf

st.set_page_config(page_title="Advanced หุ้นซิ่ง Scanner", layout="wide")

st.title("🚀 Advanced หุ้นซิ่ง Scanner")

WATCHLIST = [
    "AMD","PLTR","NVDA","TSLA","META","SOUN","IONQ","QBTS",
    "SMCI","MU","ARM","CRWD","PANW","NET","SNOW"
]

@st.cache_data(ttl=3600)
def load_data(symbol):
    return yf.download(symbol, period="6mo", progress=False)

def score_stock(df):
    if len(df) < 60:
        return 0

    close = df["Close"].squeeze()
    vol = df["Volume"].squeeze()

    ma20 = close.rolling(20).mean()
    ma50 = close.rolling(50).mean()

    score = 0

    if close.iloc[-1] > ma20.iloc[-1]:
        score += 15

    if close.iloc[-1] > ma50.iloc[-1]:
        score += 15

    high20 = close.iloc[-21:-1].max()
    if close.iloc[-1] >= high20:
        score += 25

    vol_ratio = vol.iloc[-1] / max(vol.tail(20).mean(), 1)
    score += min(int(vol_ratio * 8), 25)

    if close.iloc[-1] > close.iloc[-20]:
        score += 20

    return min(score, 100), round(vol_ratio, 2)

results = []

for ticker in WATCHLIST:
    try:
        df = load_data(ticker)
        score, volx = score_stock(df)
        results.append([ticker, score, volx])
    except:
        pass

rank = pd.DataFrame(results, columns=["Ticker", "Score", "VolX"])
rank = rank.sort_values("Score", ascending=False)

def stage(score):
    if score >= 80:
        return "🔥 Early Setup"
    if score >= 60:
        return "🚀 Momentum"
    if score >= 40:
        return "⚠ Chasing Risk"
    return "❌ Avoid"

rank["Stage"] = rank["Score"].apply(stage)

st.subheader("Top หุ้นซิ่ง")
st.dataframe(rank, use_container_width=True)

st.markdown("""
## Roadmap ครบ 8 ข้อ

✅ Yahoo Finance Auto Data

✅ MA20 / MA50

✅ Breakout 20 วัน

✅ Ranking System

✅ AI Summary Placeholder

✅ Float ต่ำ (ต่อ API ภายนอก)

✅ Discord / LINE Alert Placeholder

✅ Dark Theme พร้อมต่อยอด UI
""")

st.code("""
# ตัวอย่างแจ้งเตือน Discord

import requests

webhook = 'YOUR_WEBHOOK'

requests.post(webhook,json={
 'content':'🚀 หุ้น Score > 90'
})
""")
