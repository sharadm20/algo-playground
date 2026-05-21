import styles from './CodePlayground.module.css';

export default function OutputPanel({ output, error, running }) {
  if (running) {
    return <div className={styles.output}>Running...</div>;
  }

  if (error) {
    return <div className={styles.output}><span className={styles.error}>Error: {error}</span></div>;
  }

  if (!output) return null;

  return (
    <div className={styles.output}>
      {output.stdout && <div>{output.stdout}</div>}
      {output.stderr && <div className={styles.error}>{output.stderr}</div>}
      {output.tests && output.tests.map((t, i) => (
        <div key={i} className={`${styles.testResult} ${t.passed ? styles.success : styles.error}`}>
          {t.passed ? '\u2705' : '\u274C'} {t.name}
        </div>
      ))}
      <div className={styles.timing}>{output.timing_ms}ms</div>
    </div>
  );
}
