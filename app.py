import os
import streamlit as st
from src.inference import predict_next_day, forecast_30d, get_metrics
from src.gemini_narration import generate_prediction_narration

st.set_page_config(
    page_title="RaksaDana",
    page_icon="📈",
    layout="wide"
)

st.title("📈 RaksaDana - Dashboard Investasi Saham")
st.caption("Analisis saham BBCA, BBRI, dan BMRI berbasis AI")

ticker = st.selectbox(
    "Pilih Saham",
    ["BBCA.JK", "BBRI.JK", "BMRI.JK"]
)

st.write(f"Ticker dipilih: **{ticker}**")

with st.spinner("Mengambil data prediksi..."):
    result = predict_next_day(ticker)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Harga Sekarang", f"Rp {result['base_close']:,.2f}")

with col2:
    st.metric("Prediksi Besok", f"Rp {result['predicted_close']:,.2f}")

with col3:
    signal = result['signal']
    color  = "🟢" if signal == "BUY" else "🔴" if signal == "SELL" else "🟡"
    st.metric("Sinyal", f"{color} {signal}")

import plotly.graph_objects as go
import pandas as pd

st.subheader("📊 Forecast 30 Hari ke Depan")

with st.spinner("Mengambil data forecast..."):
    forecast = forecast_30d(ticker, days=30)

df_forecast = pd.DataFrame(forecast)

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df_forecast['date'],
    y=df_forecast['predicted_close'],
    mode='lines+markers',
    name='Prediksi Harga',
    line=dict(color='#2196F3', width=2)
))

fig.update_layout(
    xaxis_title="Tanggal",
    yaxis_title="Harga (IDR)",
    hovermode="x unified",
    height=400
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("📐 Performa Model")

with st.spinner("Mengambil metrik model..."):
    metrics = get_metrics(ticker)

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric("MAPE", f"{metrics['mape']:.2f}%")
with m2:
    st.metric("R²", f"{metrics['r2']:.4f}")
with m3:
    st.metric("Direction Accuracy", f"{metrics['direction_accuracy']:.1f}%")
with m4:
    st.metric("Return RMSE", f"{metrics['return_rmse']:.4f}")

from src.inference import calculate_profit_loss

st.subheader("💰 Kalkulator Profit/Loss")

col_a, col_b = st.columns(2)

with col_a:
    buy_price = st.number_input("Harga Beli (IDR)", min_value=0, value=int(result['base_close']))
    lots      = st.number_input("Jumlah Lot", min_value=1, value=1)

with col_b:
    sell_price = st.number_input("Harga Jual Manual (isi 0 untuk pakai prediksi model)", min_value=0, value=0)

if st.button("Hitung Profit/Loss"):
    with st.spinner("Menghitung..."):
        if sell_price > 0:
            from src.inference import calculate_profit_loss_from_prices
            calc = calculate_profit_loss_from_prices(
                ticker=ticker,
                buy_price=buy_price,
                sell_price=sell_price,
                lots=lots
            )
        else:
            calc = calculate_profit_loss(
                ticker=ticker,
                buy_price=buy_price,
                lots=lots
            )

    st.write(f"**Status:** {calc['status']}")
    st.write(f"**Net Profit/Loss:** Rp {calc['net_profit_loss']:,.2f}")
    st.write(f"**Return:** {calc['net_return_pct']:.2f}%")
    st.write(f"**Breakeven Price:** Rp {calc['breakeven_sell_price']:,.2f}")

st.subheader("🤖 Analisis AI (Gemini)")

gemini_key = os.getenv("GEMINI_API_KEY", "")
if not gemini_key:
    st.info("Set environment variable `GEMINI_API_KEY` untuk mengaktifkan narasi AI.")
else:
    if st.button("Generate Narasi AI"):
        with st.spinner("Membuat narasi investasi..."):
            try:
                narration = generate_prediction_narration(ticker, result, metrics)
                st.markdown(narration)
            except Exception as e:
                st.error(f"Gagal membuat narasi: {e}")