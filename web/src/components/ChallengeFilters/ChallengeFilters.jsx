import styles from './ChallengeFilters.module.css';

export default function ChallengeFilters({
  search,
  onSearchChange,
  topicFilter,
  onTopicChange,
  languageFilter,
  onLanguageChange,
  difficultyFilter,
  onDifficultyChange,
  topics = [],
  languages = [],
}) {
  return (
    <div className={styles.filters}>
      <input
        type="text"
        className={styles.search}
        placeholder="Search challenges..."
        value={search}
        onChange={e => onSearchChange(e.target.value)}
      />
      <select
        className={styles.select}
        value={topicFilter}
        onChange={e => onTopicChange(e.target.value)}
      >
        <option value="All">All Topics</option>
        {topics.map(t => (
          <option key={t} value={t}>{t}</option>
        ))}
      </select>
      <select
        className={styles.select}
        value={languageFilter}
        onChange={e => onLanguageChange(e.target.value)}
      >
        <option value="All">All Languages</option>
        {languages.map(l => (
          <option key={l} value={l}>{l}</option>
        ))}
      </select>
      <select
        className={styles.select}
        value={difficultyFilter}
        onChange={e => onDifficultyChange(e.target.value)}
      >
        <option value="All">All Difficulties</option>
        <option value="easy">Easy</option>
        <option value="medium">Medium</option>
        <option value="hard">Hard</option>
      </select>
    </div>
  );
}
