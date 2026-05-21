import { Link } from 'react-router-dom';
import { studyDays } from '../../data/navigation';
import styles from './HomePage.module.css';

export default function CalendarGrid({ completedDays, currentDay }) {
  return (
    <div className={styles.calendar}>
      {studyDays.map(d => {
        const isComplete = completedDays.includes(d.day);
        const isCurrent = d.day === currentDay;
        const statusClass = isComplete ? styles.completed : isCurrent ? styles.current : styles.upcoming;
        return (
          <Link
            key={d.day}
            to={`/day/${d.day}`}
            className={`${styles.day} ${statusClass}`}
          >
            <span className={styles.dayStatus}>
              {isComplete ? '\u2713' : isCurrent ? '\u25B6' : ''}
            </span>
            <span className={styles.dayNumber}>{d.day}</span>
            <span className={styles.dayTopic}>{d.title}</span>
          </Link>
        );
      })}
    </div>
  );
}
