import styles from './SkeletonLoader.module.css';

/**
 * Reusable skeleton loader shapes.
 * Each variant maps to a different visual size/shape.
 */

export function SkeletonSignalCard() {
  return <span className={`${styles.block} ${styles.signalCard}`} aria-hidden="true" />;
}

export function SkeletonLine({ width = '100%' }) {
  return (
    <span
      className={`${styles.block} ${styles.line}`}
      style={{ width }}
      aria-hidden="true"
    />
  );
}

export function SkeletonLineSm() {
  return <span className={`${styles.block} ${styles.lineSm}`} aria-hidden="true" />;
}

export function SkeletonMetricsRow() {
  return (
    <div className={styles.row} aria-hidden="true">
      {[0, 1, 2, 3].map((i) => (
        <span key={i} className={`${styles.block} ${styles.metricCard}`} />
      ))}
    </div>
  );
}

export function SkeletonChart() {
  return <span className={`${styles.block} ${styles.chartBlock}`} aria-hidden="true" />;
}

export function SkeletonNarration() {
  return <span className={`${styles.block} ${styles.narrationBlock}`} aria-hidden="true" />;
}

export function SkeletonGroup({ count = 3 }) {
  return (
    <div className={styles.group} aria-hidden="true">
      {Array.from({ length: count }).map((_, i) => (
        <SkeletonLine key={i} width={i % 2 === 0 ? '100%' : '75%'} />
      ))}
    </div>
  );
}
