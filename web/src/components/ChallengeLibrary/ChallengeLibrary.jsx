import { useState, useEffect } from 'react';
import ProblemCard from '../ProblemCard/ProblemCard';
import ChallengeFilters from '../ChallengeFilters/ChallengeFilters';
import styles from './ChallengeLibrary.module.css';

const API_BASE = import.meta.env.VITE_API_BASE || '';

export default function ChallengeLibrary() {
  const [challenges, setChallenges] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [topicFilter, setTopicFilter] = useState('All');
  const [languageFilter, setLanguageFilter] = useState('All');
  const [difficultyFilter, setDifficultyFilter] = useState('All');

  useEffect(() => {
    fetch(`${API_BASE}/api/challenges`)
      .then(r => r.json())
      .then(data => {
        setChallenges(data.filter(c => c.type === 'problem'));
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  const topics = [...new Set(challenges.map(c => c.topic))].sort();
  const languages = [...new Set(challenges.map(c => c.language))].sort();

  const filtered = challenges.filter(c => {
    const matchSearch = !search
      || c.title.toLowerCase().includes(search.toLowerCase())
      || c.tags?.some(t => t.includes(search.toLowerCase()));
    const matchTopic = topicFilter === 'All' || c.topic === topicFilter;
    const matchLang = languageFilter === 'All' || c.language === languageFilter;
    const matchDiff = difficultyFilter === 'All' || c.difficulty === difficultyFilter;
    return matchSearch && matchTopic && matchLang && matchDiff;
  });

  if (loading) return <div className={styles.page}><p>Loading challenges...</p></div>;

  return (
    <div className={styles.page}>
      <h1 className={styles.title}>Challenge Library</h1>
      <p className={styles.subtitle}>{filtered.length} challenge{filtered.length !== 1 ? 's' : ''}</p>
      <ChallengeFilters
        search={search}
        onSearchChange={setSearch}
        topicFilter={topicFilter}
        onTopicChange={setTopicFilter}
        languageFilter={languageFilter}
        onLanguageChange={setLanguageFilter}
        difficultyFilter={difficultyFilter}
        onDifficultyChange={setDifficultyFilter}
        topics={topics}
        languages={languages}
      />
      {filtered.length === 0 ? (
        <p>No challenges match your filters.</p>
      ) : (
        <div className={styles.grid}>
          {filtered.map(c => (
            <ProblemCard
              key={c.id}
              title={c.title}
              difficulty={c.difficulty}
              pattern={c.tags?.[0]}
              solutionId={c.id}
              solutionLanguage={c.language}
            >
              <div className={styles.meta}>
                <span className={styles.topic}>{c.topic}</span>
                {c.dayIds.length > 0 && (
                  <span>Day {c.dayIds.join(', ')}</span>
                )}
              </div>
              {c.description}
            </ProblemCard>
          ))}
        </div>
      )}
    </div>
  );
}
