import { useState, useEffect } from 'react';
import { getTickers, postProfitLoss } from '../api';
import NarrationCard from '../components/NarrationCard';
import { SkeletonNarration } from '../components/SkeletonLoader';
import styles from './Calculator.module.css';

const DEFAULT_TICKERS = ['BBCA.JK', 'BBRI.JK', 'BMRI.JK'];

/** Format number as Indonesian Rupiah "Rp 1.234,56" */
function formatRupiah(value) {
  if (value == null) return '-';
  return new Intl.NumberFormat('id-ID', {
    style: 'currency',
    currency: 'IDR',
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  })
    .format(value)
    .replace('IDR', 'Rp')
    .trim();
}

/** Format percentage with 2 decimal places */
function formatPct(value) {
  if (value == null) return '-';
  return `${value >= 0 ? '+' : ''}${Number(value).toFixed(2)}%`;
}

/** Determine CSS class suffix from status string */
function statusClass(status) {
  if (status === 'PROFIT') return 'profit';
  if (status === 'LOSS') return 'loss';
  return 'breakEven';
}

/** Indonesian label for status */
function statusLabel(status) {
  if (status === 'PROFIT') return 'Untung';
  if (status === 'LOSS') return 'Rugi';
  return 'Impas';
}

const INITIAL_FORM = {
  ticker: DEFAULT_TICKERS[0],
  buy_price: '',
  lots: '',
  sell_price: '',
  forecast_days: '30',
};

export default function Calculator() {
  const [tickers, setTickers] = useState(DEFAULT_TICKERS);
  const [form, setForm] = useState(INITIAL_FORM);
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [submitError, setSubmitError] = useState(null);

  /* Fetch available tickers on mount */
  useEffect(() => {
    getTickers()
      .then((res) => {
        if (Array.isArray(res.data) && res.data.length > 0) {
          setTickers(res.data);
          setForm((f) => ({ ...f, ticker: res.data[0] }));
        }
      })
      .catch(() => {
        // Fall back to defaults if API unreachable
      });
  }, []);

  const hasSellPrice = form.sell_price.trim() !== '';

  /* Field change handler */
  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((f) => ({ ...f, [name]: value }));
    setErrors((er) => ({ ...er, [name]: undefined }));
  };

  /* Validate form and return error map */
  function validate() {
    const errs = {};
    if (!form.ticker) errs.ticker = 'Pilih saham terlebih dahulu.';
    if (!form.buy_price || Number(form.buy_price) <= 0)
      errs.buy_price = 'Masukkan harga beli yang valid (lebih dari 0).';
    if (!form.lots || !Number.isInteger(Number(form.lots)) || Number(form.lots) <= 0)
      errs.lots = 'Masukkan jumlah lot yang valid (bilangan bulat positif).';
    if (form.sell_price && Number(form.sell_price) <= 0)
      errs.sell_price = 'Harga jual harus lebih dari 0.';
    if (
      !hasSellPrice &&
      form.forecast_days &&
      (Number(form.forecast_days) <= 0 || !Number.isInteger(Number(form.forecast_days)))
    )
      errs.forecast_days = 'Hari proyeksi harus bilangan bulat positif.';
    return errs;
  }

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitError(null);
    setResult(null);

    const errs = validate();
    if (Object.keys(errs).length > 0) {
      setErrors(errs);
      return;
    }

    setLoading(true);

    // Build request body — omit optional fields if blank
    const body = {
      ticker: form.ticker,
      buy_price: Number(form.buy_price),
      lots: Number(form.lots),
    };
    if (form.sell_price.trim()) body.sell_price = Number(form.sell_price);
    if (!form.sell_price.trim() && form.forecast_days.trim())
      body.forecast_days = Number(form.forecast_days);

    try {
      const res = await postProfitLoss(body);
      setResult(res.data);
    } catch (err) {
      setSubmitError(
        err.response?.data?.detail ??
          err.message ??
          'Terjadi kesalahan. Pastikan server berjalan.'
      );
    } finally {
      setLoading(false);
    }
  };

  const cls = result ? statusClass(result.status) : null;

  return (
    <div className={styles.page}>
      <h1 className={styles.pageTitle}>Kalkulator Untung / Rugi</h1>

      {/* ── Form ── */}
      <div className={styles.formCard}>
        <form onSubmit={handleSubmit} noValidate>
          <div className={styles.formGrid}>
            {/* Ticker selector */}
            <div className={styles.fieldGroup}>
              <label className={styles.label} htmlFor="calc-ticker">
                Saham
              </label>
              <select
                id="calc-ticker"
                name="ticker"
                className={`${styles.select} ${errors.ticker ? styles.hasError : ''}`}
                value={form.ticker}
                onChange={handleChange}
              >
                {tickers.map((t) => (
                  <option key={t} value={t}>
                    {t}
                  </option>
                ))}
              </select>
              {errors.ticker && <span className={styles.fieldError}>{errors.ticker}</span>}
            </div>

            {/* Lots */}
            <div className={styles.fieldGroup}>
              <label className={styles.label} htmlFor="calc-lots">
                Jumlah Lot
              </label>
              <input
                id="calc-lots"
                name="lots"
                type="number"
                min="1"
                step="1"
                className={`${styles.input} ${errors.lots ? styles.hasError : ''}`}
                placeholder="cth. 10"
                value={form.lots}
                onChange={handleChange}
              />
              {errors.lots && <span className={styles.fieldError}>{errors.lots}</span>}
            </div>

            {/* Buy price */}
            <div className={styles.fieldGroup}>
              <label className={styles.label} htmlFor="calc-buy-price">
                Harga Beli (IDR)
              </label>
              <input
                id="calc-buy-price"
                name="buy_price"
                type="number"
                min="1"
                step="any"
                className={`${styles.input} ${errors.buy_price ? styles.hasError : ''}`}
                placeholder="cth. 9500"
                value={form.buy_price}
                onChange={handleChange}
              />
              {errors.buy_price && <span className={styles.fieldError}>{errors.buy_price}</span>}
            </div>

            {/* Sell price (optional) */}
            <div className={styles.fieldGroup}>
              <label className={styles.label} htmlFor="calc-sell-price">
                Harga Jual (IDR){' '}
                <span className={styles.labelOptional}>(opsional)</span>
              </label>
              <input
                id="calc-sell-price"
                name="sell_price"
                type="number"
                min="1"
                step="any"
                className={`${styles.input} ${errors.sell_price ? styles.hasError : ''}`}
                placeholder="Kosongkan untuk pakai prediksi model"
                value={form.sell_price}
                onChange={handleChange}
              />
              {errors.sell_price && (
                <span className={styles.fieldError}>{errors.sell_price}</span>
              )}
            </div>

            {/* Forecast days — only shown if sell price is empty */}
            {!hasSellPrice && (
              <div className={styles.fieldGroup}>
                <label className={styles.label} htmlFor="calc-forecast-days">
                  Hari Proyeksi
                </label>
                <input
                  id="calc-forecast-days"
                  name="forecast_days"
                  type="number"
                  min="1"
                  step="1"
                  className={`${styles.input} ${errors.forecast_days ? styles.hasError : ''}`}
                  placeholder="30"
                  value={form.forecast_days}
                  onChange={handleChange}
                />
                {errors.forecast_days ? (
                  <span className={styles.fieldError}>{errors.forecast_days}</span>
                ) : (
                  <span className={styles.hint}>
                    Harga jual diambil dari prediksi model pada hari ke-N.
                  </span>
                )}
              </div>
            )}

            {/* Submit */}
            <div className={`${styles.fieldGroup} ${styles.fullWidth}`}>
              <button
                id="calc-submit"
                type="submit"
                className={styles.submitBtn}
                disabled={loading}
              >
                {loading ? 'Menghitung...' : 'Hitung Sekarang'}
              </button>
            </div>
          </div>
        </form>
      </div>

      {/* ── Loading state ── */}
      {loading && <SkeletonNarration />}

      {/* ── Submit error ── */}
      {submitError && !loading && (
        <div className={styles.errorBox} role="alert">
          Gagal menghitung: {submitError}
        </div>
      )}

      {/* ── Result ── */}
      {result && !loading && (
        <div className={styles.resultCard}>
          {/* Status badge + net P&L */}
          <div className={styles.resultHeader}>
            <span className={`${styles.statusBadge} ${styles[cls]}`}>
              {statusLabel(result.status)}
            </span>
            <span className={`${styles.netValue} ${styles[cls]}`}>
              {formatRupiah(result.net_profit_loss)}
            </span>
          </div>

          <div className={styles.divider} />

          {/* Summary grid */}
          <p className={styles.sectionLabel}>Rincian Transaksi</p>
          <div className={styles.summaryGrid}>
            <SummaryItem label="Imbal Hasil Bersih" value={formatPct(result.net_return_pct)} />
            <SummaryItem label="Harga Beli" value={formatRupiah(result.buy_price)} />
            <SummaryItem label="Harga Jual" value={formatRupiah(result.sell_price)} />
            <SummaryItem label="Harga Impas" value={formatRupiah(result.breakeven_sell_price)} />
            <SummaryItem
              label="Total Saham"
              value={`${result.quantity?.shares?.toLocaleString('id-ID') ?? '-'} lembar`}
            />
            <SummaryItem label="Total Biaya Beli" value={formatRupiah(result.total_cost)} />
            <SummaryItem label="Hasil Bersih Jual" value={formatRupiah(result.net_proceeds)} />
            <SummaryItem label="Biaya Pembelian" value={formatRupiah(result.buy_fee)} />
            <SummaryItem label="Biaya Penjualan" value={formatRupiah(result.sell_fee)} />
          </div>

          {/* AI narration */}
          {result.narration && (
            <>
              <div className={styles.divider} />
              <NarrationCard text={result.narration} />
            </>
          )}
        </div>
      )}
    </div>
  );
}

/** Small summary key/value card */
function SummaryItem({ label, value }) {
  return (
    <div className={styles.summaryItem}>
      <span className={styles.summaryLabel}>{label}</span>
      <span className={styles.summaryValue}>{value}</span>
    </div>
  );
}
