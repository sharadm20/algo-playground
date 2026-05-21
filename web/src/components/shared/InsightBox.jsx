export default function InsightBox({ title = 'Key Insights', children }) {
  return (
    <div style={{
      background: 'linear-gradient(135deg, #667eea, #764ba2)',
      color: 'white',
      padding: 'var(--space-lg)',
      borderRadius: 'var(--radius-md)',
      margin: 'var(--space-lg) 0',
    }}>
      {title && <h3 style={{ color: 'white', marginBottom: 'var(--space-md)' }}>{title}</h3>}
      {children}
    </div>
  );
}
