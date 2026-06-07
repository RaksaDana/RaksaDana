import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ReferenceLine,
} from 'recharts';
import styles from './ForecastChart.module.css';

/** Format date string to "20 Jan 2026" (id-ID short month) */
function formatDateShort(dateStr) {
  if (!dateStr) return '';
  const date = new Date(dateStr);
  return new Intl.DateTimeFormat('id-ID', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
  }).format(date);
}

/** Format date for X axis tick — show only "DD MMM" to save space */
function formatDateTick(dateStr) {
  if (!dateStr) return '';
  const date = new Date(dateStr);
  return new Intl.DateTimeFormat('id-ID', {
    day: '2-digit',
    month: 'short',
  }).format(date);
}

/** Format price as "Rp 1.234" (no decimals for axis) */
function formatRupiahShort(value) {
  if (value == null) return '';
  return `Rp ${new Intl.NumberFormat('id-ID').format(Math.round(value))}`;
}

/** Custom tooltip rendered inside the chart */
function CustomTooltip({ active, payload, label }) {
  if (!active || !payload?.length) return null;
  const price = payload[0]?.value;
  return (
    <div className={styles.tooltip}>
      <p className={styles.tooltipDate}>{formatDateShort(label)}</p>
      <p className={styles.tooltipPrice}>{formatRupiahShort(price)}</p>
    </div>
  );
}

export default function ForecastChart({ data, baseClose }) {
  // Reduce tick density: show every ~6th label on the x-axis
  const tickInterval = Math.max(1, Math.floor((data?.length ?? 0) / 5));

  return (
    <div className={styles.wrapper}>
      <div className={styles.header}>
        <h2 className={styles.title}>Proyeksi Harga 30 Hari</h2>
        <div className={styles.legend}>
          <div className={styles.legendItem}>
            <div className={styles.legendLine} />
            Prediksi
          </div>
          {baseClose != null && (
            <div className={styles.legendItem}>
              <div className={styles.legendDashed} />
              Harga saat ini
            </div>
          )}
        </div>
      </div>

      <div className={styles.chartArea}>
        <ResponsiveContainer width="100%" height="100%">
          <LineChart
            data={data ?? []}
            margin={{ top: 4, right: 16, left: 8, bottom: 4 }}
          >
            <CartesianGrid
              strokeDasharray="3 3"
              stroke="#F3F4F6"
              vertical={false}
            />
            <XAxis
              dataKey="date"
              tickFormatter={formatDateTick}
              interval={tickInterval}
              tick={{ fontSize: 11, fill: 'var(--color-text-muted)' }}
              axisLine={false}
              tickLine={false}
            />
            <YAxis
              tickFormatter={formatRupiahShort}
              tick={{ fontSize: 11, fill: 'var(--color-text-muted)' }}
              axisLine={false}
              tickLine={false}
              width={80}
              domain={['auto', 'auto']}
            />
            <Tooltip content={<CustomTooltip />} />

            {/* Dashed reference line at current (base) price */}
            {baseClose != null && (
              <ReferenceLine
                y={baseClose}
                stroke="var(--color-text-muted)"
                strokeDasharray="4 4"
                strokeWidth={1.5}
              />
            )}

            {/* Forecast line — no dots, smooth curve */}
            <Line
              type="monotone"
              dataKey="predicted_close"
              stroke="var(--color-accent)"
              strokeWidth={2}
              dot={false}
              activeDot={{ r: 4, strokeWidth: 0, fill: 'var(--color-accent)' }}
              isAnimationActive={false}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Static footnote below chart */}
      <p className={styles.chartNote}>
        Data model per 20 Januari 2026. Proyeksi dihitung dari tanggal tersebut.
      </p>
    </div>
  );
}
