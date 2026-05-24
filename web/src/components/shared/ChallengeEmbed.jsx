import { useState, useEffect } from 'react';
import ProblemCard from '../ProblemCard/ProblemCard';

const API_BASE = import.meta.env.VITE_API_BASE || '';

export default function ChallengeEmbed({ id }) {
  const [challenge, setChallenge] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    let cancelled = false;
    setError(null);
    fetch(`${API_BASE}/api/challenges`)
      .then(r => {
        if (!r.ok) throw new Error('Failed to load challenges');
        return r.json();
      })
      .then(data => {
        if (cancelled) return;
        const found = data.find(c => c.id === id);
        if (found) setChallenge(found);
        else setError(`Challenge "${id}" not found`);
      })
      .catch(() => {
        if (!cancelled) setError('Failed to load challenges');
      });
    return () => { cancelled = true; };
  }, [id]);

  if (error) return <p style={{ color: 'var(--color-danger)' }}>{error}</p>;
  if (!challenge) return <p>Loading challenge...</p>;

  return (
    <ProblemCard
      title={challenge.title}
      difficulty={challenge.difficulty}
      pattern={challenge.tags?.[0]}
      solutionId={challenge.id}
      solutionLanguage={challenge.language}
    >
      {challenge.description}
    </ProblemCard>
  );
}
