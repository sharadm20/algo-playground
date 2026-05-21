export default function DataTable({ headers, rows }) {
  return (
    <div style={{
      overflow: 'hidden',
      borderRadius: 'var(--radius-md)',
      boxShadow: 'var(--shadow-sm)',
      margin: 'var(--space-lg) 0',
    }}>
      <table style={{
        width: '100%',
        borderCollapse: 'collapse',
        background: 'var(--color-bg-card)',
      }}>
        <thead>
          <tr style={{ background: 'var(--color-primary)', color: 'white' }}>
            {headers.map((h, i) => (
              <th key={i} style={{
                padding: '12px 16px',
                textAlign: 'left',
                textTransform: 'uppercase',
                fontSize: '0.85rem',
                letterSpacing: '0.5px',
              }}>
                {h}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, i) => (
            <tr key={i} style={{ borderBottom: i < rows.length - 1 ? '1px solid var(--color-border)' : 'none' }}>
              {row.map((cell, j) => (
                <td key={j} style={{ padding: '12px 16px' }}>{cell}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
