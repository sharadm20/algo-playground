import styles from './HomePage.module.css';

export default function StatsRow({ completed, total }) {
  const pct = total > 0 ? Math.round((completed / total) * 100) : 0;
  return (
    <div className={styles.stats}>
      <div className={styles.statCard}>
        <div className={styles.statNumber}>{completed}</div>
        <div className={styles.statLabel}>Completed</div>
      </div>
      <div className={styles.statCard}>
        <div className={styles.statNumber}>{total - completed}</div>
        <div className={styles.statLabel}>Remaining</div>
      </div>
      <div className={styles.statCard}>
        <div className={styles.statNumber}>{pct}%</div>
        <div className={styles.statLabel}>Progress</div>
      </div>
      <div className={styles.statCard}>
        <div className={styles.statNumber}>170+</div>
        <div className={styles.statLabel}>Problems</div>
      </div>
    </div>
  );
}
