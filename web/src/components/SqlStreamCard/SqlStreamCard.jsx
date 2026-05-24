import { useState } from 'react';
import Badge from '../shared/Badge';
import styles from './SqlStreamCard.module.css';

const DIFFICULTY_COLORS = {
  beginner: { bg: '#d4edda', color: '#155724' },
  intermediate: { bg: '#fff3cd', color: '#856404' },
  advanced: { bg: '#f8d7da', color: '#721c24' },
};

const DOMAIN_COLORS = {
  ecommerce: { bg: '#e3f2fd', color: '#0d47a1' },
  hr: { bg: '#fce4ec', color: '#880e4f' },
  'social-media': { bg: '#f3e5f5', color: '#4a148c' },
  student: { bg: '#fff3e0', color: '#e65100' },
};

export default function SqlStreamCard({ query, schema }) {
  const [expanded, setExpanded] = useState(false);
  const [showSchema, setShowSchema] = useState(false);
  const [schemaSection, setSchemaSection] = useState(null);

  const handleCopy = (text) => {
    navigator.clipboard.writeText(text);
  };

  const diffColor = DIFFICULTY_COLORS[query.difficulty] || { bg: '#e9ecef', color: '#495057' };
  const domainColor = DOMAIN_COLORS[query.domain] || { bg: '#e9ecef', color: '#495057' };

  return (
    <div className={styles.card}>
      <div className={styles.header} onClick={() => setExpanded(!expanded)} role="button" aria-label={expanded ? 'hide details' : 'show details'}>
        <div className={styles.headerContent}>
          <div className={styles.badges}>
            <Badge label={query.difficulty} bg={diffColor.bg} color={diffColor.color} />
            <Badge label={query.category} bg="#e9ecef" color="#495057" />
          </div>
          <h4 className={styles.title}>{query.title}</h4>
          <p className={styles.description}>{query.description}</p>
        </div>
        <span className={`${styles.chevron} ${expanded ? styles.chevronOpen : ''}`}>▼</span>
      </div>
      {expanded && (
        <div className={styles.body}>
          <div className={styles.codeGrid}>
            <div className={styles.codeBlock}>
              <div className={`${styles.codeHeader} ${styles.sqlHeader}`}>
                <span>SQL</span>
                <button className={styles.copyBtn} onClick={() => handleCopy(query.sqlQuery)}>Copy</button>
              </div>
              <pre className={`${styles.codeContent} ${styles.sqlCode}`}>{query.sqlQuery}</pre>
            </div>
            <div className={styles.codeBlock}>
              <div className={`${styles.codeHeader} ${styles.javaHeader}`}>
                <span>Java Stream</span>
                <button className={styles.copyBtn} onClick={() => handleCopy(query.javaStreamCode)}>Copy</button>
              </div>
              <pre className={`${styles.codeContent} ${styles.javaCode}`}>{query.javaStreamCode}</pre>
            </div>
          </div>

          <div className={`${styles.section} ${styles.explanation}`}>
            <div className={styles.explanationTitle}>📖 Explanation</div>
            <p className={styles.explanationText}>{query.explanation}</p>
          </div>

          <div className={`${styles.section} ${styles.output}`}>
            <div className={styles.outputTitle}>💻 Expected Output</div>
            <pre className={styles.outputContent}>{query.output}</pre>
          </div>

          <div className={styles.schemaToggle}>
            <button className={styles.schemaBtn} onClick={() => setShowSchema(!showSchema)}>
              {showSchema ? 'Hide Schema & Models' : 'Show Schema & Models'}
            </button>
          </div>

          {showSchema && schema && (
            <div className={styles.schemaPanel}>
              <div className={styles.schemaSubSection}>
                <div className={styles.schemaSubHeader} onClick={() => setSchemaSection(schemaSection === 'ddl' ? null : 'ddl')}>
                  <span>🗄️ Database Schema</span>
                  <button className={styles.copyBtn} onClick={(e) => { e.stopPropagation(); handleCopy(schema.ddl); }}>Copy</button>
                </div>
                {schemaSection === 'ddl' && <pre className={styles.schemaCode}>{schema.ddl}</pre>}
              </div>
              <div className={styles.schemaSubSection}>
                <div className={styles.schemaSubHeader} onClick={() => setSchemaSection(schemaSection === 'data' ? null : 'data')}>
                  <span>📊 Sample Data</span>
                  <button className={styles.copyBtn} onClick={(e) => { e.stopPropagation(); handleCopy(schema.sampleData); }}>Copy</button>
                </div>
                {schemaSection === 'data' && <pre className={styles.schemaCode}>{schema.sampleData}</pre>}
              </div>
              <div className={styles.schemaSubSection}>
                <div className={styles.schemaSubHeader} onClick={() => setSchemaSection(schemaSection === 'models' ? null : 'models')}>
                  <span>☕ Java Models</span>
                  <button className={styles.copyBtn} onClick={(e) => { e.stopPropagation(); handleCopy(schema.javaModels); }}>Copy</button>
                </div>
                {schemaSection === 'models' && <pre className={styles.schemaCode}>{schema.javaModels}</pre>}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
