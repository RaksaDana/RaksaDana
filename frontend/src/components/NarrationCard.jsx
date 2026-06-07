import styles from './NarrationCard.module.css';

export default function NarrationCard({ text }) {
  if (!text) return null;

  return (
    <aside className={styles.card} aria-label="Analisis AI">
      <div className={styles.label}>
        <span className={styles.labelDot} />
        Analisis AI
      </div>
      <p className={styles.text}>{text}</p>
    </aside>
  );
}
