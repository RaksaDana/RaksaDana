import { useState, useEffect, useCallback } from 'react';
import { getPredict, getForecast, getMetrics } from '../api';
import SignalCard from '../components/SignalCard';
import MetricsRow from '../components/MetricsRow';
import ForecastChart from '../components/ForecastChart';
import NarrationCard from '../components/NarrationCard';
import {
  SkeletonSignalCard,
  SkeletonMetricsRow,
  SkeletonChart,
  SkeletonNarration,
} from '../components/SkeletonLoader';
import styles from './Dashboard.module.css';

const DEFAULT_TICKERS = ['BBCA.JK', 'BBRI.JK', 'BMRI.JK'];

export default function Dashboard() {
  const [tickers, setTickers] = useState(DEFAULT_TICKERS);
  const [activeTicker, setActiveTicker] = useState(DEFAULT_TICKERS[0]);

  // Per-section loading / error / data states
  const [predictState, setPredictState] = useState({ loading: true, error: null, data: null });
  const [metricsState, setMetricsState] = useState({ loading: true, error: null, data: null });
  const [forecastState, setForecastState] = useState({ loading: true, error: null, data: null });

  /** Fetch all three endpoints whenever the active ticker changes */
  const fetchAll = useCallback(async (ticker) => {
    setPredictState({ loading: true, error: null, data: null });
    setMetricsState({ loading: true, error: null, data: null });
    setForecastState({ loading: true, error: null, data: null });

    // Fire all three requests in parallel; handle each independently
    const [predictRes, metricsRes, forecastRes] = await Promise.allSettled([
      getPredict(ticker),
      getMetrics(ticker),
      getForecast(ticker, 30),
    ]);

    setPredictState(
      predictRes.status === 'fulfilled'
        ? { loading: false, error: null, data: predictRes.value.data }
        : { loading: false, error: predictRes.reason?.message ?? 'Gagal memuat sinyal', data: null }
    );

    setMetricsState(
      metricsRes.status === 'fulfilled'
        ? { loading: false, error: null, data: metricsRes.value.data }
        : { loading: false, error: metricsRes.reason?.message ?? 'Gagal memuat metrik', data: null }
    );

    setForecastState(
      forecastRes.status === 'fulfilled'
        ? { loading: false, error: null, data: forecastRes.value.data }
        : { loading: false, error: forecastRes.reason?.message ?? 'Gagal memuat proyeksi', data: null }
    );
  }, []);

  useEffect(() => {
    fetchAll(activeTicker);
  }, [activeTicker, fetchAll]);

  const handleTickerChange = (ticker) => {
    if (ticker !== activeTicker) setActiveTicker(ticker);
  };

  return (
    <div className={styles.page}>
      {/* ── Header / ticker selector ── */}
      <div className={styles.header}>
        <h1 className={styles.pageTitle}>Dashboard</h1>
        <div className={styles.tabs} role="tablist" aria-label="Pilih saham">
          {tickers.map((t) => (
            <button
              key={t}
              role="tab"
              aria-selected={t === activeTicker}
              className={`${styles.tab} ${t === activeTicker ? styles.active : ''}`}
              onClick={() => handleTickerChange(t)}
            >
              {t.replace('.JK', '')}
            </button>
          ))}
        </div>
      </div>

      {/* ── Signal Card ── */}
      <section aria-labelledby="signal-label">
        <p id="signal-label" className={styles.sectionLabel}>Sinyal Perdagangan</p>
        {predictState.loading && <SkeletonSignalCard />}
        {predictState.error && (
          <ErrorBox message={predictState.error} onRetry={() => fetchAll(activeTicker)} />
        )}
        {!predictState.loading && !predictState.error && predictState.data && (
          <SignalCard data={predictState.data} />
        )}
      </section>

      {/* ── AI Narration ── */}
      {!predictState.loading && predictState.data?.narration && (
        <NarrationCard text={predictState.data.narration} />
      )}
      {predictState.loading && <SkeletonNarration />}

      {/* ── Metrics Row ── */}
      <section aria-labelledby="metrics-label">
        <p id="metrics-label" className={styles.sectionLabel}>Kinerja Model</p>
        {metricsState.loading && <SkeletonMetricsRow />}
        {metricsState.error && (
          <ErrorBox message={metricsState.error} onRetry={() => fetchAll(activeTicker)} />
        )}
        {!metricsState.loading && !metricsState.error && metricsState.data && (
          <MetricsRow data={metricsState.data} />
        )}
      </section>

      {/* ── Forecast Chart ── */}
      <section aria-labelledby="forecast-label">
        <p id="forecast-label" className={styles.sectionLabel}>Proyeksi Harga</p>
        {forecastState.loading && <SkeletonChart />}
        {forecastState.error && (
          <ErrorBox message={forecastState.error} onRetry={() => fetchAll(activeTicker)} />
        )}
        {!forecastState.loading && !forecastState.error && forecastState.data && (
          <ForecastChart
            data={forecastState.data}
            baseClose={predictState.data?.base_close}
          />
        )}
      </section>
    </div>
  );
}

/** Inline error banner with retry button */
function ErrorBox({ message, onRetry }) {
  return (
    <div className={styles.errorBox} role="alert">
      <span className={styles.errorText}>Gagal memuat data: {message}</span>
      <button className={styles.retryBtn} onClick={onRetry}>
        Coba Lagi
      </button>
    </div>
  );
}
