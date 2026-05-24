import { useState } from 'react';
import Badge from '../shared/Badge';
import styles from './ProblemCard.module.css';

const DIFFICULTY_COLORS = {
  easy: { bg: '#d4edda', color: '#155724' },
  medium: { bg: '#fff3cd', color: '#856404' },
  hard: { bg: '#f8d7da', color: '#721c24' },
};

const API_BASE = import.meta.env.VITE_API_BASE || '';

export default function ProblemCard({
  title,
  difficulty = 'easy',
  pattern,
  children,
  solutionId,
  solutionLanguage,
}) {
  const [showSolution, setShowSolution] = useState(false);
  const [solutionCode, setSolutionCode] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleToggleSolution = async () => {
    if (showSolution) {
      setShowSolution(false);
      return;
    }
    if (solutionCode) {
      setShowSolution(true);
      return;
    }
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/api/challenges/${solutionId}/solution`);
      if (!res.ok) throw new Error('Failed to load solution');
      const data = await res.json();
      setSolutionCode(data.code);
      setShowSolution(true);
    } catch {
      setSolutionCode('// Failed to load solution');
      setShowSolution(true);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.card}>
      <div className={styles.header}>
        <h4>{title}</h4>
        <div className={styles.badges}>
          <Badge
            label={difficulty}
            bg={DIFFICULTY_COLORS[difficulty]?.bg || '#e9ecef'}
            color={DIFFICULTY_COLORS[difficulty]?.color || '#495057'}
          />
          {solutionLanguage && (
            <Badge label={solutionLanguage} bg="#e2e3f1" color="#4a4a6a" />
          )}
        </div>
      </div>
      {pattern && <div className={styles.pattern}>Pattern: {pattern}</div>}
      <div className={styles.description}>{children}</div>
      {solutionId && (
        <button
          className={styles.solutionBtn}
          onClick={handleToggleSolution}
          disabled={loading}
        >
          {loading ? 'Loading...' : showSolution ? 'Hide Solution' : 'Show Solution'}
        </button>
      )}
      {showSolution && solutionCode && (
        <pre className={styles.solutionBlock}>
          <code>{solutionCode}</code>
        </pre>
      )}
    </div>
  );
}
