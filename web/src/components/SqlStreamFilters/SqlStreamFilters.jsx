import styles from './SqlStreamFilters.module.css';

export default function SqlStreamFilters({
  search,
  onSearchChange,
  categoryFilter,
  onCategoryChange,
  domainFilter,
  onDomainChange,
  difficultyFilter,
  onDifficultyChange,
  categories = [],
  domains = [],
}) {
  return (
    <div className={styles.filters}>
      <input
        type="text"
        className={styles.search}
        placeholder="Search queries..."
        value={search}
        onChange={e => onSearchChange(e.target.value)}
      />
      <select className={styles.select} value={categoryFilter} onChange={e => onCategoryChange(e.target.value)}>
        <option value="All">All Categories</option>
        {categories.map(c => <option key={c} value={c}>{c}</option>)}
      </select>
      <select className={styles.select} value={domainFilter} onChange={e => onDomainChange(e.target.value)}>
        <option value="All">All Domains</option>
        {domains.map(d => <option key={d} value={d}>{d}</option>)}
      </select>
      <select className={styles.select} value={difficultyFilter} onChange={e => onDifficultyChange(e.target.value)}>
        <option value="All">All Difficulties</option>
        <option value="beginner">Beginner</option>
        <option value="intermediate">Intermediate</option>
        <option value="advanced">Advanced</option>
      </select>
    </div>
  );
}
