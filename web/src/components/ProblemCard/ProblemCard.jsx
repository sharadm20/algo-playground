import Badge from '../shared/Badge';
import styles from './ProblemCard.module.css';

const DIFFICULTY_COLORS = {
  easy: { bg: '#d4edda', color: '#155724' },
  medium: { bg: '#fff3cd', color: '#856404' },
  hard: { bg: '#f8d7da', color: '#721c24' },
};

export default function ProblemCard({ title, difficulty = 'easy', pattern, children }) {
  return (
    <div className={styles.card}>
      <div className={styles.header}>
        <h4>{title}</h4>
        <Badge
          label={difficulty}
          bg={DIFFICULTY_COLORS[difficulty]?.bg || '#e9ecef'}
          color={DIFFICULTY_COLORS[difficulty]?.color || '#495057'}
        />
      </div>
      {pattern && <div className={styles.pattern}>Pattern: {pattern}</div>}
      <div className={styles.description}>{children}</div>
    </div>
  );
}
