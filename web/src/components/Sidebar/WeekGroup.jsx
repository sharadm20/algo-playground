import DayLink from './DayLink';
import styles from './Sidebar.module.css';

export default function WeekGroup({ weekTitle, days, completedDays, currentDay }) {
  return (
    <nav className={styles.nav}>
      <div className={styles.weekTitle}>{weekTitle}</div>
      <ul className={styles.dayList}>
        {days.map(d => (
          <DayLink
            key={d.day}
            day={d.day}
            title={d.title}
            isComplete={completedDays.includes(d.day)}
            isCurrent={d.day === currentDay}
          />
        ))}
      </ul>
    </nav>
  );
}
