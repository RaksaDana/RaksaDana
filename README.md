# RaksaDana — Dashboard Investasi Saham Berbasis Multivariate LSTM dan Explainable AI

Dashboard investasi interaktif untuk memprediksi pergerakan harga saham BBCA, BBRI, dan BMRI dengan integrasi variabel fundamental (ROE, EPS, Dividend Yield) dan Explainable AI via Google Gemini API. Dibangun dengan Nuxt.js (frontend) dan FastAPI (backend).

🌐 **Live Demo:** [https://raksa-dana.vercel.app](https://raksa-dana.vercel.app)  
🔗 **API Backend:** [https://raksadana-raksadana-api.hf.space](https://raksadana-raksadana-api.hf.space)  
📖 **API Docs:** [https://raksadana-raksadana-api.hf.space/docs](https://raksadana-raksadana-api.hf.space/docs)

---

## Tentang Proyek

Investor ritel kesulitan menginterpretasikan data historis dan laporan keuangan secara terpadu. RaksaDana menjawab kebutuhan ini dengan menghadirkan sinyal investasi (Buy/Hold/Sell) berbasis model LSTM multivariate yang transparan dan dapat dijelaskan.

**Research Questions:**
1. Bagaimana pengaruh integrasi variabel fundamental (ROE, EPS, DY) terhadap akurasi LSTM dibanding model univariat?
2. Sejauh mana Google Gemini API efektif mentransformasi output numerik menjadi narasi investasi?
3. Apa faktor fundamental paling signifikan, dan bagaimana kalkulator profit/loss membantu mitigasi risiko?

---

## Fitur Utama

- **Sinyal Investasi** — BUY/HOLD/SELL berbasis prediksi model LSTM per ticker
- **Proyeksi Harga 30 Hari** — Grafik forecast interaktif dengan referensi harga terkini
- **Metrik Model** — MAPE, R², Direction Accuracy, Return RMSE
- **Kalkulator Profit/Loss** — Simulasi investasi dengan perhitungan biaya transaksi riil
- **Analisis AI** — Narasi rekomendasi investasi dalam Bahasa Indonesia via Google Gemini

---

## Alur Pipeline

```
Yahoo Finance (yfinance)
        ↓
  01. EDA & Eksplorasi
        ↓
  02. Preprocessing & Feature Engineering
      (OHLCV + MA + RSI + MACD + BB + ROE/EPS/DY → 18 fitur)
        ↓
  03–05. LSTM Modelling per Ticker
         Target: Next_Log_Return → rekonstruksi harga
         Baseline: Naive, MA5, Ridge, LSTM Univariat
        ↓
  06. Cross-Ticker Evaluation
        ↓
  FastAPI Backend (HuggingFace Spaces)
        ↓
  Nuxt.js Frontend (Vercel) + Gemini AI Narasi
```

---

## Struktur Proyek

```
RaksaDana/
├── data/
│   ├── raw/                         # CSV harga historis dari yfinance
│   └── processed/                   # Featured CSV per ticker
│       ├── BBCA_JK_featured.csv
│       ├── BBRI_JK_featured.csv
│       └── BMRI_JK_featured.csv
├── frontend/                        # Nuxt.js 3 frontend
│   ├── components/                  # Vue components
│   ├── composables/useApi.js        # Axios API calls
│   ├── pages/
│   │   ├── index.vue               # Dashboard
│   │   └── kalkulator.vue          # Kalkulator P/L
│   ├── layouts/default.vue
│   └── nuxt.config.js
├── models/
│   └── return_model/               # .keras models + scalers + feature config
├── notebook/
│   ├── 01.DataCollection&EDA.ipynb
│   ├── 02.preproccesing-and-feature-engineering.ipynb
│   ├── 03.BBCA-Modelling-Evaluation.ipynb
│   ├── 04.BBRI-Modelling-Evaluation.ipynb
│   ├── 05.BMRI-Modelling-Evaluation.ipynb
│   └── 06.Evaluation-Comparison.ipynb
├── outputs/figures/                # Plot PNG per ticker + evaluasi
├── reports/return_model/           # CSV metrics per ticker
├── src/
│   ├── inference.py                # Fungsi inferensi model
│   └── gemini_narration.py         # Integrasi Google Gemini API
├── assets/                         # Logo dan aset statis
├── main.py                         # FastAPI app
├── Dockerfile                      # Docker untuk deployment
├── requirements.txt                # Dependencies lengkap
└── requirements-prod.txt           # Dependencies untuk production
```

---

## Arsitektur Model

| Komponen | Detail |
|---|---|
| Input | 60 hari × 18 fitur (15 teknikal + ROE, EPS, DY) |
| Target | `Next_Log_Return = log(Close_t+1 / Close_t)` |
| Rekonstruksi harga | `Close_t × exp(predicted_return)` |
| Arsitektur | LSTM(32) → LayerNorm → Dropout(0.2) → Dense(16) → Dense(1) |
| Training | 3 seed ensemble (42, 123, 7), EarlyStopping, ReduceLROnPlateau |
| Validasi | Walk-forward TimeSeriesSplit (3 fold) |

---

## Hasil Evaluasi Model

| Ticker | MAPE | R² | Direction Accuracy |
|---|---|---|---|
| BBCA.JK | 1.18% | 0.9615 | 48.9% |
| BBRI.JK | 1.53% | 0.9747 | 44.7% |
| BMRI.JK | 1.52% | 0.9747 | 47.1% |

---

## Cara Mereplikasi Proyek

### Prasyarat

- Python 3.11 (wajib — TensorFlow belum support Python 3.12+)
- Node.js 22.x atau lebih baru
- Git

### 1. Clone Repository

```bash
git clone https://github.com/RaksaDana/RaksaDana.git
cd RaksaDana
```

### 2. Setup Backend (FastAPI)

```bash
# Buat virtual environment dengan Python 3.11
py -3.11 -m venv venv

# Aktifkan virtual environment
# Windows:
.\venv\Scripts\Activate.ps1
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Setup Environment Variables

Buat file `.env` di root folder:

```
GEMINI_API_KEY=your_google_gemini_api_key_here
```

Dapatkan API key gratis di: [https://aistudio.google.com/apikey](https://aistudio.google.com/apikey)

### 4. Jalankan Notebook Secara Berurutan

```bash
# Pastikan venv aktif
jupyter notebook

# Jalankan notebook berikut secara berurutan:
# 01.DataCollection&EDA.ipynb
# 02.preproccesing-and-feature-engineering.ipynb
# 03.BBCA-Modelling-Evaluation.ipynb
# 04.BBRI-Modelling-Evaluation.ipynb
# 05.BMRI-Modelling-Evaluation.ipynb
# 06.Evaluation-Comparison.ipynb
```

### 5. Jalankan Backend FastAPI

```bash
uvicorn main:app --reload
```

Backend berjalan di `http://127.0.0.1:8000`  
API docs tersedia di `http://127.0.0.1:8000/docs`

### 6. Setup Frontend (Nuxt.js)

```bash
cd frontend
npm install
```

Buat file `.env` di folder `frontend`:

```
NUXT_PUBLIC_API_BASE=http://127.0.0.1:8000
```

Jalankan frontend:

```bash
npm run dev
```

Frontend berjalan di `http://localhost:3000`

---

## Deployment

### Backend — HuggingFace Spaces

Backend di-deploy ke HuggingFace Spaces menggunakan Docker.

```bash
# Install HuggingFace CLI
pip install huggingface_hub hf_xet

# Login
hf auth login

# Upload ke HuggingFace Space
hf upload YOUR_USERNAME/raksadana-api . . --repo-type space
```

Tambahkan `GEMINI_API_KEY` di **Settings → Repository secrets** pada HuggingFace Space.

### Frontend — Vercel

1. Push repository ke GitHub
2. Buka [vercel.com](https://vercel.com) → Import project
3. Set **Root Directory** ke `frontend`
4. Tambahkan environment variable:
   ```
   NUXT_PUBLIC_API_BASE=https://your-space-url.hf.space
   ```
5. Deploy

---

## API Endpoints

| Method | Endpoint | Deskripsi |
|---|---|---|
| GET | `/api/v1/health` | Cek status backend |
| GET | `/api/v1/tickers` | Daftar ticker tersedia |
| GET | `/api/v1/predict/{ticker}` | Prediksi harga + sinyal |
| GET | `/api/v1/forecast/{ticker}` | Forecast 30 hari |
| GET | `/api/v1/metrics/{ticker}` | Metrik evaluasi model |
| POST | `/api/v1/profit-loss` | Kalkulasi profit/loss |

Tambahkan `?narrate=true` pada endpoint predict dan profit-loss untuk mengaktifkan narasi Gemini AI.

**Contoh penggunaan:**

```python
import requests

# Prediksi dengan narasi
response = requests.get(
    "https://raksadana-raksadana-api.hf.space/api/v1/predict/BBCA.JK",
    params={"narrate": True}
)
print(response.json())

# Kalkulator Profit/Loss
response = requests.post(
    "https://raksadana-raksadana-api.hf.space/api/v1/profit-loss",
    json={
        "ticker": "BBCA.JK",
        "buy_price": 7800.0,
        "lots": 2,
        "forecast_days": 30,
        "buy_fee_rate": 0.0015,
        "sell_fee_rate": 0.0025,
        "lot_size": 100
    }
)
print(response.json())
```

---

## Metodologi Evaluasi

- **Return RMSE** — error prediksi log return (metrik utama)
- **Price MAPE** — error harga rekonstruksi dalam persen
- **R²** — koefisien determinasi harga rekonstruksi
- **Direction Accuracy** — akurasi prediksi arah naik/turun
- **Fit Status** — rasio Test/Train RMSE: Good Fit (<1.25x), Mild Overfit (<1.75x), Overfit (>1.75x)

---

## Baseline Perbandingan

| Model | Deskripsi |
|---|---|
| Naive_Zero_Return | Prediksi return = 0 setiap hari |
| MA5_Return | Rata-rata 5 hari return terakhir |
| Ridge_Return | Ridge regression dengan 18 fitur |
| LSTM_Univariate | LSTM 1 fitur (Close_Log_Return_1) |
| LSTM_Return_Ensemble | Model utama, ensemble 3 seed ✅ |

---

## Tech Stack

| Layer | Teknologi |
|---|---|
| Frontend | Nuxt.js 3, Vue 3, TailwindCSS, ApexCharts, GSAP |
| Backend | FastAPI, Uvicorn, Python 3.11 |
| Model | TensorFlow/Keras, Scikit-learn, Pandas, NumPy |
| AI Narasi | Google Gemini API (gemini-2.0-flash) |
| Data | yfinance (Yahoo Finance) |
| Deployment | Vercel (frontend), HuggingFace Spaces (backend) |

---

## Catatan Penting

- Data model mencakup hingga **20 Januari 2026** — forecast dihitung dari tanggal tersebut
- Data fundamental (ROE, EPS, DY) menggunakan nilai snapshot terkini dari yfinance
- Direction Accuracy ~49% mendekati acak — sinyal BUY/HOLD/SELL perlu diinterpretasikan dengan hati-hati
- **Aplikasi ini bukan merupakan saran investasi resmi**

---

## Tim

| Nama | Role | Tanggung Jawab |
|---|---|---|
| Chelsa Yoga Permadany | ML Engineer | Feature Engineering, Integrasi Frontend-Backend |
| Fayola Saphira Zulkarnaen | Data Analyst | Data Collection & EDA, Testing & Bug Fixing |
| Muhammad Akbar Pradana | ML Engineer | Pembangunan Model LSTM, Deployment |
| Bima Mukhlisin Bil Sajjad | ML Engineer | Evaluasi & Tuning, Kalkulator Profit/Loss |
| Moch Mizan Ghodafail | Backend Engineer | FastAPI Backend, Integrasi Gemini API |
