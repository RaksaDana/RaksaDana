import styles from './MetricsRow.module.css';

const METRICS_CONFIG = [
  {
    key: 'mape',
    label: 'MAPE',
    format: (v) => `${v.toFixed(2)}%`,
    description: 'Rata-rata persentase kesalahan prediksi harga.',
  },
  {
    key: 'r2',
    label: 'R²',
    format: (v) => v.toFixed(4),
    description: 'Seberapa baik model menjelaskan variasi harga (0–1).',
  },
  {
    key: 'direction_accuracy',
    label: 'Akurasi Arah',
    format: (v) => `${v.toFixed(1)}%`,
    description: 'Persentase prediksi arah naik/turun yang benar.',
  },
  {
    key: 'return_rmse',
    label: 'Return RMSE',
    format: (v) => v.toFixed(6),
    description: 'Kesalahan akar rata-rata kuadrat imbal hasil prediksi.',
  },
];

export default function MetricsRow({ data }) {
  return (
    <div className={styles.row} role="list" aria-label="Metrik kinerja model">
      {METRICS_CONFIG.map(({ key, label, format, description }) => {
        const raw = data?.[key];
        const value = raw != null ? format(raw) : '—';

        return (
          <div key={key} className={styles.card} role="listitem">
            <div className={styles.accentBar} />
            <span className={styles.label}>{label}</span>
            <span className={styles.value}>{value}</span>
            <p className={styles.description}>{description}</p>
          </div>
        );
      })}
    </div>
  );
}
