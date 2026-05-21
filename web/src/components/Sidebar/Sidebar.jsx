import { Link } from 'react-router-dom';
import { studyDays } from '../../data/navigation';
import WeekGroup from './WeekGroup';
import styles from './Sidebar.module.css';

function groupByWeek(days) {
  const weeks = {};
  days.forEach(d => {
    if (!weeks[d.week]) weeks[d.week] = { title: d.weekTitle, days: [] };
    weeks[d.week].days.push(d);
  });
  return Object.entries(weeks).sort(([a], [b]) => Number(a) - Number(b));
}

export default function Sidebar({ completedDays = [], currentDay = 0 }) {
  const weeks = groupByWeek(studyDays);
  const total = studyDays.length;
  const done = completedDays.length;
  const pct = total > 0 ? Math.round((done / total) * 100) : 0;

  return (
    <aside className={styles.sidebar}>
      <div className={styles.header}>
        <Link to="/" style={{ color: 'inherit', textDecoration: 'none' }}>
          <h1>DSA Study Plan</h1>
          <p>30 Days to Mastery</p>
        </Link>
      </div>
      <div className={styles.progressSummary}>
        {done}/{total} days completed ({pct}%)
      </div>
      {weeks.map(([week, w]) => (
        <WeekGroup
          key={week}
          weekTitle={w.title}
          days={w.days}
          completedDays={completedDays}
          currentDay={currentDay}
        />
      ))}
    </aside>
  );
}
