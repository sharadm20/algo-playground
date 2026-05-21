import { Link } from 'react-router-dom';
import { useProgress } from '../../hooks/useProgress';
import StatsRow from './StatsRow';
import CalendarGrid from './CalendarGrid';
import styles from './HomePage.module.css';

export default function HomePage() {
  const { progress, currentDay } = useProgress();
  const completed = progress.completedDays.length;

  return (
    <div className={styles.page}>
      <h1 className={styles.title}>30-Day DSA Study Plan</h1>
      <p className={styles.subtitle}>Your journey to mastering Data Structures & Algorithms</p>

      <StatsRow completed={completed} total={30} />

      <h2>Calendar</h2>
      <p style={{ marginBottom: 'var(--space-md)', color: 'var(--color-text-secondary)' }}>
        Click any day to start learning.
      </p>

      <CalendarGrid completedDays={progress.completedDays} currentDay={currentDay} />

      <div style={{ marginTop: 'var(--space-xl)', textAlign: 'center' }}>
        <Link
          to="/export"
          style={{
            display: 'inline-block',
            padding: 'var(--space-sm) var(--space-lg)',
            background: 'var(--color-accent)',
            color: 'white',
            borderRadius: 'var(--radius-md)',
            fontWeight: 600,
            textDecoration: 'none',
          }}
        >
          Export Progress Report
        </Link>
      </div>
    </div>
  );
}
