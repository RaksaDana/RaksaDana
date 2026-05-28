import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from src.inference import (
    predict_next_day,
    forecast_30d,
    get_metrics,
    calculate_profit_loss,
    calculate_profit_loss_from_prices,
)

# ──────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="RaksaDana — Dashboard Investasi",
    page_icon="assets/favicon.ico" if False else None,  # swap when asset is ready
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────
# GLOBAL CSS
# ──────────────────────────────────────────────
st.markdown(
    """
    <style>
    /* ── Base ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {
        background-color: #1E3A5F;
    }
    section[data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }
    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span {
        color: #CBD5E1 !important;
    }
    section[data-testid="stSidebar"] .stSelectbox > div > div {
        background-color: #253F6E;
        color: #FFFFFF;
        border: 1px solid #3B5A8A;
        border-radius: 6px;
    }

    /* ── Page header ── */
    .page-header {
        padding: 1.5rem 0 0.5rem 0;
        border-bottom: 2px solid #E2E8F0;
        margin-bottom: 1.5rem;
    }
    .page-header h1 {
        font-size: 1.75rem;
        font-weight: 700;
        color: #1E3A5F;
        margin: 0;
        letter-spacing: -0.3px;
    }
    .page-header p {
        font-size: 0.875rem;
        color: #64748B;
        margin: 0.25rem 0 0 0;
    }

    /* ── Section title ── */
    .section-title {
        font-size: 1rem;
        font-weight: 600;
        color: #1E3A5F;
        margin: 0 0 0.25rem 0;
    }
    .section-subtitle {
        font-size: 0.8rem;
        color: #94A3B8;
        margin: 0 0 1rem 0;
    }

    /* ── Metric cards ── */
    .metric-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 1.1rem 1.25rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .metric-card .label {
        font-size: 0.75rem;
        font-weight: 500;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.3rem;
    }
    .metric-card .value {
        font-size: 1.35rem;
        font-weight: 700;
        color: #1E3A5F;
        line-height: 1.2;
    }
    .metric-card .delta {
        font-size: 0.78rem;
        margin-top: 0.25rem;
        font-weight: 500;
    }
    .delta-up   { color: #4CAF50; }
    .delta-down { color: #F44336; }
    .delta-flat { color: #FF9800; }

    /* ── Signal card ── */
    .signal-card {
        border-radius: 10px;
        padding: 1.1rem 1.25rem;
        border-left: 5px solid;
        display: flex;
        flex-direction: column;
        gap: 0.2rem;
    }
    .signal-buy  { background: #F0FDF4; border-color: #4CAF50; }
    .signal-sell { background: #FFF5F5; border-color: #F44336; }
    .signal-hold { background: #FFFBEB; border-color: #FF9800; }

    .signal-card .sig-label {
        font-size: 0.72rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        color: #64748B;
    }
    .signal-card .sig-text {
        font-size: 2rem;
        font-weight: 800;
        letter-spacing: 1px;
        line-height: 1.1;
    }
    .sig-text-buy  { color: #4CAF50; }
    .sig-text-sell { color: #F44336; }
    .sig-text-hold { color: #FF9800; }

    .signal-card .sig-desc {
        font-size: 0.78rem;
        color: #64748B;
        margin-top: 0.1rem;
    }

    /* ── Chart container ── */
    .chart-container {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1.5rem;
    }

    /* ── Performance metric chip ── */
    .perf-chip {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 0.85rem 1rem;
        text-align: center;
    }
    .perf-chip .chip-label {
        font-size: 0.72rem;
        font-weight: 500;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.4px;
    }
    .perf-chip .chip-value {
        font-size: 1.2rem;
        font-weight: 700;
        color: #1E3A5F;
        margin-top: 0.15rem;
    }

    /* ── Calculator result card ── */
    .calc-result {
        border-radius: 10px;
        border: 1px solid #E2E8F0;
        padding: 1.25rem;
        background: #FFFFFF;
    }
    .calc-result .cr-header {
        font-size: 0.75rem;
        font-weight: 600;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        border-bottom: 1px solid #E2E8F0;
        padding-bottom: 0.6rem;
        margin-bottom: 0.8rem;
    }
    .calc-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.3rem 0;
        font-size: 0.85rem;
    }
    .calc-row .cr-label { color: #64748B; }
    .calc-row .cr-value { font-weight: 600; color: #1E3A5F; }
    .calc-divider {
        border: none;
        border-top: 1px solid #E2E8F0;
        margin: 0.6rem 0;
    }
    .calc-status-profit { color: #4CAF50; font-weight: 700; font-size: 1rem; }
    .calc-status-loss   { color: #F44336; font-weight: 700; font-size: 1rem; }
    .calc-status-even   { color: #FF9800; font-weight: 700; font-size: 1rem; }

    /* ── Analyst note (Gemini) ── */
    .analyst-note {
        background: #F8FAFC;
        border: 1px solid #CBD5E1;
        border-radius: 10px;
        padding: 1.4rem 1.5rem;
    }
    .analyst-note .note-header {
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        color: #2196F3;
        margin-bottom: 0.6rem;
    }
    .analyst-note .note-title {
        font-size: 1rem;
        font-weight: 600;
        color: #1E3A5F;
        margin-bottom: 0.6rem;
    }
    .analyst-note .note-body {
        font-size: 0.875rem;
        color: #475569;
        line-height: 1.7;
    }
    .analyst-note .note-disclaimer {
        font-size: 0.72rem;
        color: #94A3B8;
        margin-top: 1rem;
        border-top: 1px solid #E2E8F0;
        padding-top: 0.6rem;
    }

    /* ── Button ── */
    div.stButton > button {
        background-color: #2196F3;
        color: #FFFFFF;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        font-size: 0.875rem;
        padding: 0.55rem 1.4rem;
        cursor: pointer;
        transition: background 0.2s;
    }
    div.stButton > button:hover {
        background-color: #1976D2;
    }

    /* ── Hide Streamlit chrome ── */
    #MainMenu { visibility: hidden; }
    footer    { visibility: hidden; }
    header    { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)


# ──────────────────────────────────────────────
# HELPERS — formatting
# ──────────────────────────────────────────────
def fmt_idr(value: float) -> str:
    """Format a float as Indonesian Rupiah with period thousand separators and comma decimal."""
    # e.g. 7784.24 → Rp 7.784,24
    abs_val = abs(value)
    integer_part = int(abs_val)
    decimal_part = round((abs_val - integer_part) * 100)
    int_str = f"{integer_part:,}".replace(",", ".")
    sign = "-" if value < 0 else ""
    return f"{sign}Rp {int_str},{decimal_part:02d}"


def fmt_pct(value: float, decimals: int = 2) -> str:
    sign = "+" if value > 0 else ""
    return f"{sign}{value:.{decimals}f}%"


# ──────────────────────────────────────────────
# CACHED DATA FETCHERS
# ──────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def cached_predict(ticker: str) -> dict:
    return predict_next_day(ticker)


@st.cache_data(show_spinner=False)
def cached_forecast(ticker: str, days: int = 30) -> list:
    return forecast_30d(ticker, days=days)


@st.cache_data(show_spinner=False)
def cached_metrics(ticker: str) -> dict:
    return get_metrics(ticker)


# ──────────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        """
        <div style="padding: 0.5rem 0 1.5rem 0;">
            <div style="font-size:1.4rem; font-weight:800; letter-spacing:-0.5px;">RaksaDana</div>
            <div style="font-size:0.78rem; color:#93C5FD; margin-top:0.25rem; line-height:1.5;">
                Analisis prediktif saham IDX berbasis model LSTM ensemble
            </div>
        </div>
        <hr style="border-color:#253F6E; margin-bottom:1.25rem;"/>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div style="font-size:0.75rem; font-weight:600; text-transform:uppercase; '
        'letter-spacing:0.5px; color:#93C5FD; margin-bottom:0.4rem;">Pilih Saham</div>',
        unsafe_allow_html=True,
    )
    ticker = st.selectbox(
        label="Saham",
        options=["BBCA.JK", "BBRI.JK", "BMRI.JK"],
        label_visibility="collapsed",
    )

    st.markdown(
        """
        <hr style="border-color:#253F6E; margin: 1.5rem 0 1rem 0;"/>
        <div style="font-size:0.72rem; color:#64748B; line-height:1.6;">
            Data historis diperbarui setiap hari bursa.<br>
            Prediksi bersifat indikatif dan bukan rekomendasi investasi.
        </div>
        """,
        unsafe_allow_html=True,
    )


# ──────────────────────────────────────────────
# PAGE HEADER
# ──────────────────────────────────────────────
stock_label = ticker.replace(".JK", "")
st.markdown(
    f"""
    <div class="page-header">
        <h1>Dashboard Investasi — {stock_label}</h1>
        <p>Model LSTM Ensemble &nbsp;|&nbsp; Prediksi harga dan sinyal perdagangan berbasis data historis</p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ──────────────────────────────────────────────
# FETCH DATA
# ──────────────────────────────────────────────
with st.spinner("Mengambil data prediksi model..."):
    result = cached_predict(ticker)

with st.spinner("Mengambil data ramalan 30 hari..."):
    forecast = cached_forecast(ticker, days=30)

with st.spinner("Memuat metrik performa model..."):
    metrics = cached_metrics(ticker)


# ──────────────────────────────────────────────
# SECTION 1 — PRICE SNAPSHOT + SIGNAL
# ──────────────────────────────────────────────
st.markdown(
    '<p class="section-title">Ringkasan Harga &amp; Sinyal</p>'
    '<p class="section-subtitle">Perbandingan harga penutupan terakhir dengan estimasi model untuk hari bursa berikutnya</p>',
    unsafe_allow_html=True,
)

price_change = result["predicted_close"] - result["base_close"]
price_change_pct = (price_change / result["base_close"]) * 100
signal = result["signal"]

# Determine signal CSS class and description
if signal == "BUY":
    sig_cls = "signal-buy"
    sig_txt_cls = "sig-text-buy"
    sig_desc = "Model memprediksi kenaikan harga yang signifikan pada hari bursa berikutnya."
elif signal == "SELL":
    sig_cls = "signal-sell"
    sig_txt_cls = "sig-text-sell"
    sig_desc = "Model memprediksi penurunan harga yang signifikan pada hari bursa berikutnya."
else:
    sig_cls = "signal-hold"
    sig_txt_cls = "sig-text-hold"
    sig_desc = "Prediksi pergerakan harga masih dalam rentang netral. Tidak ada aksi yang disarankan."

delta_cls = "delta-up" if price_change >= 0 else "delta-down"
delta_sign = "+" if price_change >= 0 else ""

col_price1, col_price2, col_signal = st.columns([1, 1, 1])

with col_price1:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="label">Harga Penutupan Terakhir</div>
            <div class="value">{fmt_idr(result['base_close'])}</div>
            <div class="delta" style="color:#94A3B8;">Data per tanggal sinyal</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col_price2:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="label">Estimasi Harga Besok ({result['signal_date']})</div>
            <div class="value">{fmt_idr(result['predicted_close'])}</div>
            <div class="delta {delta_cls}">{delta_sign}{fmt_idr(price_change)} &nbsp;({fmt_pct(price_change_pct)})</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col_signal:
    st.markdown(
        f"""
        <div class="signal-card {sig_cls}">
            <div class="sig-label">Sinyal Perdagangan</div>
            <div class="sig-text {sig_txt_cls}">{signal}</div>
            <div class="sig-desc">{sig_desc}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# SECTION 2 — FORECAST CHART
# ──────────────────────────────────────────────
st.markdown(
    '<p class="section-title">Ramalan Harga 30 Hari ke Depan</p>'
    '<p class="section-subtitle">Proyeksi harga penutupan berbasis rekursi model LSTM. '
    'Garis putus-putus menunjukkan harga penutupan terakhir sebagai acuan.</p>',
    unsafe_allow_html=True,
)

df_forecast = pd.DataFrame(forecast)
df_forecast["date"] = pd.to_datetime(df_forecast["date"])

base_close = result["base_close"]

fig_forecast = go.Figure()

# Forecast line
fig_forecast.add_trace(
    go.Scatter(
        x=df_forecast["date"],
        y=df_forecast["predicted_close"],
        mode="lines+markers",
        name="Estimasi Harga",
        line=dict(color="#2196F3", width=2.5),
        marker=dict(size=4, color="#2196F3"),
        hovertemplate="<b>%{x|%d %b %Y}</b><br>Estimasi: Rp %{y:,.2f}<extra></extra>",
    )
)

# Reference line — current price
fig_forecast.add_hline(
    y=base_close,
    line_dash="dot",
    line_color="#94A3B8",
    line_width=1.5,
    annotation_text=f"Harga Terakhir: {fmt_idr(base_close)}",
    annotation_position="bottom right",
    annotation_font=dict(size=11, color="#64748B"),
)

# Shading above/below reference
fig_forecast.add_trace(
    go.Scatter(
        x=pd.concat([df_forecast["date"], df_forecast["date"][::-1]]),
        y=pd.concat([df_forecast["predicted_close"],
                     pd.Series([base_close] * len(df_forecast))[::-1]]),
        fill="toself",
        fillcolor="rgba(33, 150, 243, 0.07)",
        line=dict(width=0),
        showlegend=False,
        hoverinfo="skip",
    )
)

fig_forecast.update_layout(
    xaxis=dict(
        title="Tanggal",
        title_font=dict(size=11, color="#64748B"),
        tickfont=dict(size=10, color="#94A3B8"),
        showgrid=True,
        gridcolor="#F1F5F9",
        linecolor="#E2E8F0",
    ),
    yaxis=dict(
        title="Harga (IDR)",
        title_font=dict(size=11, color="#64748B"),
        tickfont=dict(size=10, color="#94A3B8"),
        showgrid=True,
        gridcolor="#F1F5F9",
        linecolor="#E2E8F0",
        tickformat=",",
    ),
    hovermode="x unified",
    height=380,
    margin=dict(l=10, r=10, t=20, b=10),
    plot_bgcolor="#FFFFFF",
    paper_bgcolor="#FFFFFF",
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.01,
        xanchor="left",
        x=0,
        font=dict(size=11, color="#64748B"),
    ),
)

st.plotly_chart(fig_forecast, use_container_width=True)


# ──────────────────────────────────────────────
# SECTION 3 — MODEL PERFORMANCE
# ──────────────────────────────────────────────
st.markdown(
    '<p class="section-title">Performa Model LSTM</p>'
    '<p class="section-subtitle">Metrik evaluasi pada data uji (test set). '
    'Nilai MAPE rendah dan R² mendekati 1 menandakan akurasi model yang baik.</p>',
    unsafe_allow_html=True,
)

if metrics:
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)

    perf_items = [
        (m_col1, "MAPE", f"{metrics['mape']:.2f}%",
         "Mean Absolute Percentage Error — semakin kecil semakin akurat"),
        (m_col2, "R\u00b2 (Koefisien Determinasi)", f"{metrics['r2']:.4f}",
         "Seberapa baik model menjelaskan variasi harga"),
        (m_col3, "Akurasi Arah", f"{metrics['direction_accuracy']:.1f}%",
         "Persentase prediksi arah naik/turun yang benar"),
        (m_col4, "Return RMSE", f"{metrics['return_rmse']:.6f}",
         "Root Mean Squared Error pada log-return"),
    ]

    for col, label, value, tooltip in perf_items:
        with col:
            st.markdown(
                f"""
                <div class="perf-chip" title="{tooltip}">
                    <div class="chip-label">{label}</div>
                    <div class="chip-value">{value}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
else:
    st.info("Metrik model belum tersedia untuk saham ini. Jalankan notebook pelatihan terlebih dahulu.")

st.markdown("<br>", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# SECTION 4 — PROFIT / LOSS CALCULATOR
# ──────────────────────────────────────────────
st.markdown(
    '<p class="section-title">Kalkulator Estimasi Profit / Loss</p>'
    '<p class="section-subtitle">Masukkan harga beli dan jumlah lot untuk menghitung estimasi hasil investasi. '
    'Biaya transaksi menggunakan tarif standar broker IDX (beli 0.15%, jual 0.25%).</p>',
    unsafe_allow_html=True,
)

calc_col_left, calc_col_right = st.columns([1, 1], gap="large")

with calc_col_left:
    st.markdown(
        '<div style="font-size:0.8rem; font-weight:600; color:#1E3A5F; margin-bottom:0.5rem;">Parameter Posisi</div>',
        unsafe_allow_html=True,
    )

    buy_price = st.number_input(
        label="Harga Beli per Saham (IDR)",
        min_value=1,
        value=int(result["base_close"]),
        step=10,
        help="Harga per lembar saham pada saat pembelian.",
    )
    lots = st.number_input(
        label="Jumlah Lot (1 lot = 100 lembar saham)",
        min_value=1,
        value=1,
        step=1,
        help="Masukkan jumlah lot yang ingin diinvestasikan.",
    )
    sell_price_input = st.number_input(
        label="Harga Jual Manual (IDR) — kosongkan / isi 0 untuk gunakan prediksi model",
        min_value=0,
        value=0,
        step=10,
        help="Isi angka ini jika Anda memiliki target harga jual. "
             "Biarkan 0 untuk menggunakan estimasi harga besok dari model.",
    )

    run_calc = st.button("Hitung Estimasi Profit / Loss", use_container_width=True)

with calc_col_right:
    st.markdown(
        '<div style="font-size:0.8rem; font-weight:600; color:#1E3A5F; margin-bottom:0.5rem;">Hasil Kalkulasi</div>',
        unsafe_allow_html=True,
    )

    if run_calc:
        with st.spinner("Menghitung..."):
            try:
                if sell_price_input > 0:
                    calc = calculate_profit_loss_from_prices(
                        ticker=ticker,
                        buy_price=buy_price,
                        sell_price=sell_price_input,
                        lots=lots,
                    )
                else:
                    calc = calculate_profit_loss(
                        ticker=ticker,
                        buy_price=buy_price,
                        lots=lots,
                    )

                # Determine status style
                status_raw = calc["status"]
                if status_raw == "PROFIT":
                    status_html = '<span class="calc-status-profit">PROFIT</span>'
                elif status_raw == "LOSS":
                    status_html = '<span class="calc-status-loss">LOSS</span>'
                else:
                    status_html = '<span class="calc-status-even">BREAK-EVEN</span>'

                net_pl = calc["net_profit_loss"]
                net_cls = "delta-up" if net_pl >= 0 else "delta-down"

                price_src_label = {
                    "manual": "Manual",
                    "model_next_day": "Estimasi Model (besok)",
                }.get(calc.get("price_source", ""), calc.get("price_source", ""))

                st.markdown(
                    f"""
                    <div class="calc-result">
                        <div class="cr-header">Ringkasan Transaksi &nbsp;&mdash;&nbsp; {price_src_label}</div>

                        <div class="calc-row">
                            <span class="cr-label">Jumlah Saham</span>
                            <span class="cr-value">{calc['quantity']['shares']:,} lembar ({calc['quantity']['lots']:.0f} lot)</span>
                        </div>
                        <div class="calc-row">
                            <span class="cr-label">Total Modal Beli</span>
                            <span class="cr-value">{fmt_idr(calc['total_cost'])}</span>
                        </div>
                        <div class="calc-row">
                            <span class="cr-label">Biaya Pembelian (0,15%)</span>
                            <span class="cr-value">{fmt_idr(calc['buy_fee'])}</span>
                        </div>
                        <hr class="calc-divider"/>
                        <div class="calc-row">
                            <span class="cr-label">Harga Jual</span>
                            <span class="cr-value">{fmt_idr(calc['sell_price'])}</span>
                        </div>
                        <div class="calc-row">
                            <span class="cr-label">Gross Penjualan</span>
                            <span class="cr-value">{fmt_idr(calc['gross_sell_value'])}</span>
                        </div>
                        <div class="calc-row">
                            <span class="cr-label">Biaya Penjualan (0,25%)</span>
                            <span class="cr-value">{fmt_idr(calc['sell_fee'])}</span>
                        </div>
                        <div class="calc-row">
                            <span class="cr-label">Gross Profit / Loss</span>
                            <span class="cr-value">{fmt_idr(calc['gross_profit_loss'])}</span>
                        </div>
                        <hr class="calc-divider"/>
                        <div class="calc-row">
                            <span class="cr-label">Net Profit / Loss</span>
                            <span class="cr-value {net_cls}" style="font-size:1.05rem;">{fmt_idr(net_pl)}</span>
                        </div>
                        <div class="calc-row">
                            <span class="cr-label">Return Bersih</span>
                            <span class="cr-value">{fmt_pct(calc['net_return_pct'])}</span>
                        </div>
                        <div class="calc-row">
                            <span class="cr-label">Harga Impas (Breakeven)</span>
                            <span class="cr-value">{fmt_idr(calc['breakeven_sell_price'])}</span>
                        </div>
                        <hr class="calc-divider"/>
                        <div class="calc-row">
                            <span class="cr-label" style="font-weight:600; color:#1E3A5F;">Status</span>
                            <span>{status_html}</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            except Exception as exc:
                st.error(f"Gagal menghitung: {exc}")
    else:
        st.markdown(
            """
            <div style="border:1px dashed #CBD5E1; border-radius:10px; padding:2rem 1.5rem;
                        text-align:center; color:#94A3B8; font-size:0.85rem;">
                Tekan tombol <strong style="color:#2196F3;">Hitung Estimasi Profit / Loss</strong>
                untuk melihat hasil kalkulasi di sini.
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("<br>", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# SECTION 5 — GEMINI ANALYST NOTE
# ──────────────────────────────────────────────
st.markdown(
    '<p class="section-title">Catatan Analis AI</p>'
    '<p class="section-subtitle">Narasi ringkasan kondisi saham berdasarkan output model — '
    'dihasilkan oleh Google Gemini AI.</p>',
    unsafe_allow_html=True,
)

# ── PLACEHOLDER: Ganti blok di bawah dengan pemanggilan Gemini API ──────────
# Contoh integrasi (uncomment dan sesuaikan):
#
#   import google.generativeai as genai
#   genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
#   model_gemini = genai.GenerativeModel("gemini-1.5-flash")
#
#   prompt = f"""
#   Kamu adalah analis investasi saham Indonesia yang profesional.
#   Tulis ringkasan singkat (3-4 paragraf) dalam bahasa Indonesia formal
#   berdasarkan data berikut untuk saham {ticker}:
#   - Harga terakhir  : Rp {result['base_close']:,.2f}
#   - Estimasi besok  : Rp {result['predicted_close']:,.2f}
#   - Sinyal          : {result['signal']}
#   - MAPE model      : {metrics.get('mape', 'N/A')}%
#   - R²              : {metrics.get('r2', 'N/A')}
#   - Akurasi arah    : {metrics.get('direction_accuracy', 'N/A')}%
#   Jangan sertakan kata "AI" atau "model". Gunakan bahasa analis profesional.
#   """
#
#   gemini_response = model_gemini.generate_content(prompt)
#   analyst_body = gemini_response.text

# Teks placeholder sementara:
analyst_body = (
    f"Berdasarkan analisis model LSTM ensemble terhadap data historis <strong>{stock_label}</strong>, "
    f"harga penutupan terakhir berada di level <strong>{fmt_idr(result['base_close'])}</strong>. "
    f"Model memproyeksikan harga untuk hari bursa berikutnya ({result['signal_date']}) "
    f"di kisaran <strong>{fmt_idr(result['predicted_close'])}</strong>, "
    f"menghasilkan sinyal <strong>{signal}</strong>."
    "<br><br>"
    f"Tingkat akurasi model pada data uji mencapai MAPE {metrics.get('mape', '—'):.2f}% "
    f"dengan koefisien determinasi R² sebesar {metrics.get('r2', '—'):.4f}, "
    f"menunjukkan bahwa model mampu menangkap pola pergerakan harga dengan baik. "
    f"Akurasi arah prediksi tercatat {metrics.get('direction_accuracy', '—'):.1f}%, "
    "yang mengindikasikan kehandalan model dalam menentukan arah naik atau turun harga."
    "<br><br>"
    "Investor disarankan untuk mempertimbangkan kondisi pasar secara lebih luas, "
    "termasuk sentimen makroekonomi, kebijakan suku bunga, dan laporan keuangan emiten "
    "sebelum mengambil keputusan investasi. Proyeksi ini bersifat indikatif dan tidak "
    "menggantikan analisis fundamental maupun teknikal secara menyeluruh."
) if metrics else (
    f"Berdasarkan analisis model LSTM ensemble terhadap data historis <strong>{stock_label}</strong>, "
    f"sinyal perdagangan saat ini adalah <strong>{signal}</strong>. "
    "Metrik performa model belum tersedia — jalankan notebook pelatihan untuk memperoleh data evaluasi lengkap."
)
# ── END PLACEHOLDER ──────────────────────────────────────────────────────────

st.markdown(
    f"""
    <div class="analyst-note">
        <div class="note-header">Catatan Analis &nbsp;|&nbsp; Didukung Google Gemini AI</div>
        <div class="note-title">Ringkasan Investasi — {stock_label}</div>
        <div class="note-body">{analyst_body}</div>
        <div class="note-disclaimer">
            Narasi ini dihasilkan secara otomatis oleh model bahasa AI dan bersifat indikatif.
            Bukan merupakan rekomendasi investasi. Keputusan investasi sepenuhnya ada pada investor.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)