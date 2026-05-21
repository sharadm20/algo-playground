import * as React from 'react';
import { useParams, Link } from 'react-router-dom';
import { studyDays } from '../../data/navigation';
import { useProgress } from '../../hooks/useProgress';
import styles from './DayPage.module.css';

const dayModules = {
  1: React.lazy(() => import('../../content/day-01.mdx')),
  2: React.lazy(() => import('../../content/day-02.mdx')),
  3: React.lazy(() => import('../../content/day-03.mdx')),
  4: React.lazy(() => import('../../content/day-04.mdx')),
  5: React.lazy(() => import('../../content/day-05.mdx')),
  6: React.lazy(() => import('../../content/day-06.mdx')),
  7: React.lazy(() => import('../../content/day-07.mdx')),
  8: React.lazy(() => import('../../content/day-08.mdx')),
  9: React.lazy(() => import('../../content/day-09.mdx')),
  10: React.lazy(() => import('../../content/day-10.mdx')),
  11: React.lazy(() => import('../../content/day-11.mdx')),
  12: React.lazy(() => import('../../content/day-12.mdx')),
  13: React.lazy(() => import('../../content/day-13.mdx')),
  14: React.lazy(() => import('../../content/day-14.mdx')),
  15: React.lazy(() => import('../../content/day-15.mdx')),
  16: React.lazy(() => import('../../content/day-16.mdx')),
  17: React.lazy(() => import('../../content/day-17.mdx')),
  18: React.lazy(() => import('../../content/day-18.mdx')),
  19: React.lazy(() => import('../../content/day-19.mdx')),
  20: React.lazy(() => import('../../content/day-20.mdx')),
  21: React.lazy(() => import('../../content/day-21.mdx')),
  22: React.lazy(() => import('../../content/day-22.mdx')),
  23: React.lazy(() => import('../../content/day-23.mdx')),
  24: React.lazy(() => import('../../content/day-24.mdx')),
  25: React.lazy(() => import('../../content/day-25.mdx')),
  26: React.lazy(() => import('../../content/day-26.mdx')),
  27: React.lazy(() => import('../../content/day-27.mdx')),
  28: React.lazy(() => import('../../content/day-28.mdx')),
  29: React.lazy(() => import('../../content/day-29.mdx')),
  30: React.lazy(() => import('../../content/day-30.mdx')),
};

export default function DayPage() {
  const { dayId } = useParams();
  const day = parseInt(dayId);
  const { markComplete, resetDay, progress } = useProgress();
  const dayInfo = studyDays.find(d => d.day === day);
  const isComplete = progress.completedDays.includes(day);

  const prevDay = day > 1 ? day - 1 : null;
  const nextDay = day < 30 ? day + 1 : null;
  const DayContent = dayModules[day];

  if (!dayInfo || !DayContent) {
    return <div className={styles.page}><h2>Day not found</h2></div>;
  }

  return (
    <div className={styles.page}>
      <div className={styles.nav}>
        <div>
          <h1 className={styles.title}>Day {day}: {dayInfo.title}</h1>
          <p style={{ color: 'var(--color-text-secondary)', margin: 0, fontSize: 'var(--font-size-sm)' }}>
            {dayInfo.weekTitle}
          </p>
        </div>
        <div className={styles.navLinks}>
          {prevDay ? (
            <Link to={`/day/${prevDay}`} className={styles.navLink}>&larr; Day {prevDay}</Link>
          ) : (
            <span className={`${styles.navLink} ${styles.navLinkDisabled}`}>&larr; Prev</span>
          )}
          {nextDay ? (
            <Link to={`/day/${nextDay}`} className={styles.navLink}>Day {nextDay} &rarr;</Link>
          ) : (
            <span className={`${styles.navLink} ${styles.navLinkDisabled}`}>Next &rarr;</span>
          )}
        </div>
      </div>

      <React.Suspense fallback={<div>Loading content...</div>}>
        <DayContent />
      </React.Suspense>

      <div className={styles.actions}>
        {!isComplete ? (
          <button
            onClick={() => markComplete(day)}
            style={{
              padding: '10px 24px',
              background: 'var(--color-success)',
              color: 'white',
              border: 'none',
              borderRadius: 'var(--radius-md)',
              fontWeight: 600,
              cursor: 'pointer',
            }}
          >
            {'\u2713'} Mark Day {day} Complete
          </button>
        ) : (
          <button
            onClick={() => resetDay(day)}
            style={{
              padding: '10px 24px',
              background: 'var(--color-danger)',
              color: 'white',
              border: 'none',
              borderRadius: 'var(--radius-md)',
              fontWeight: 600,
              cursor: 'pointer',
            }}
          >
            {'\u21BA'} Redo Day {day}
          </button>
        )}
      </div>
    </div>
  );
}
