import { useState, useMemo } from 'react';
import { queries, domainSchemas, categories, domains } from '../../data/sqlStreamQueries';
import SqlStreamCard from '../SqlStreamCard/SqlStreamCard';
import SqlStreamFilters from '../SqlStreamFilters/SqlStreamFilters';
import styles from './SqlStreamsPage.module.css';

export default function SqlStreamsPage() {
  const [search, setSearch] = useState('');
  const [categoryFilter, setCategoryFilter] = useState('All');
  const [domainFilter, setDomainFilter] = useState('All');
  const [difficultyFilter, setDifficultyFilter] = useState('All');

  const filtered = useMemo(() => {
    return queries.filter(q => {
      const matchSearch = !search
        || q.title.toLowerCase().includes(search.toLowerCase())
        || q.description.toLowerCase().includes(search.toLowerCase())
        || q.sqlQuery.toLowerCase().includes(search.toLowerCase())
        || q.javaStreamCode.toLowerCase().includes(search.toLowerCase());
      const matchCategory = categoryFilter === 'All' || q.category === categoryFilter;
      const matchDomain = domainFilter === 'All' || q.domain === domainFilter;
      const matchDifficulty = difficultyFilter === 'All' || q.difficulty === difficultyFilter;
      return matchSearch && matchCategory && matchDomain && matchDifficulty;
    });
  }, [search, categoryFilter, domainFilter, difficultyFilter]);

  return (
    <div className={styles.page}>
      <h1 className={styles.title}>SQL ↔ Java Streams</h1>
      <p className={styles.subtitle}>
        {filtered.length} of {queries.length} queries — Learn how SQL patterns translate to Java Stream API
      </p>
      <SqlStreamFilters
        search={search}
        onSearchChange={setSearch}
        categoryFilter={categoryFilter}
        onCategoryChange={setCategoryFilter}
        domainFilter={domainFilter}
        onDomainChange={setDomainFilter}
        difficultyFilter={difficultyFilter}
        onDifficultyChange={setDifficultyFilter}
        categories={categories}
        domains={domains}
      />
      {filtered.length === 0 ? (
        <div className={styles.empty}>
          <div className={styles.emptyIcon} aria-hidden="true">🔍</div>
          <p className={styles.emptyText}>No queries match your filters.</p>
        </div>
      ) : (
        filtered.map(q => (
          <SqlStreamCard
            key={q.id}
            query={q}
            schema={domainSchemas[q.domain]}
          />
        ))
      )}
    </div>
  );
}
