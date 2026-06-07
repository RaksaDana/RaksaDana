import { TrendingUp, TrendingDown, Minus } from 'lucide-react';
import styles from './SignalCard.module.css';

/** Format a number as Indonesian Rupiah: "Rp 1.234,56" */
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

/** Format a date string to "20 Jan 2026" in Indonesian */
function formatDate(dateStr) {
  if (!dateStr) return '-';
  const date = new Date(dateStr);
  return new Intl.DateTimeFormat('id-ID', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
  }).format(date);
}

const SIGNAL_MAP = {
  BUY:  { label: 'BELI',  cls: 'buy',  Icon: TrendingUp },
  SELL: { label: 'JUAL',  cls: 'sell', Icon: TrendingDown },
  HOLD: { label: 'TAHAN', cls: 'hold', Icon: Minus },
};

export default function SignalCard({ data }) {
  const { label, cls, Icon } = SIGNAL_MAP[data?.signal] ?? SIGNAL_MAP.HOLD;
  const logReturn = data?.predicted_log_return ?? 0;
  const returnPct = (Math.exp(logReturn) - 1) * 100;
  const returnCls =
    returnPct > 0 ? 'positive' : returnPct < 0 ? 'negative' : 'neutral';

  // Map signal class → left-border class (CSS only, no logic change)
  const borderCls = { buy: styles.borderBuy, sell: styles.borderSell, hold: styles.borderHold }[cls] ?? '';

  return (
    <article className={`${styles.card} ${borderCls}`} aria-label="Sinyal perdagangan">
      <div className={styles.header}>
        <div>
          <div className={`${styles.signalBadge} ${styles[cls]}`}>
            <span className={`${styles.signalDot} ${styles[cls]}`} />
            <Icon size={16} />
            {label}
          </div>
          <p className={styles.signalDate}>
            Tanggal sinyal: {formatDate(data?.signal_date)}
          </p>
        </div>
      </div>

      <div className={styles.divider} />

      <div className={styles.priceRow}>
        <div className={styles.priceBlock}>
          <span className={styles.priceLabel}>Harga Penutupan</span>
          <span className={styles.priceValue}>
            {formatRupiah(data?.base_close)}
          </span>
        </div>
        <div className={styles.priceBlock}>
          <span className={styles.priceLabel}>Prediksi Harga</span>
          <span className={`${styles.priceValueAccent} ${styles[cls]}`}>
            {formatRupiah(data?.predicted_close)}
          </span>
        </div>
      </div>

      <div className={styles.divider} />

      <div className={styles.returnRow}>
        <span className={styles.returnLabel}>Perkiraan imbal hasil:</span>
        <span className={`${styles.returnValue} ${styles[returnCls]}`}>
          {returnPct >= 0 ? '+' : ''}
          {returnPct.toFixed(2)}%
        </span>
      </div>
    </article>
  );
}
