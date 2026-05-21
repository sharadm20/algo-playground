export default function Badge({ label, bg = '#e9ecef', color = '#495057' }) {
  return (
    <span style={{
      fontSize: '0.75rem',
      padding: '3px 10px',
      borderRadius: '12px',
      textTransform: 'uppercase',
      fontWeight: 600,
      background: bg,
      color,
    }}>
      {label}
    </span>
  );
}
