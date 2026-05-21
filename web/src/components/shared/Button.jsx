export default function Button({ children, variant = 'primary', onClick, disabled, style }) {
  const variants = {
    primary: { background: 'var(--color-accent)', color: 'white', borderColor: 'var(--color-accent)' },
    secondary: { background: 'transparent', color: 'var(--color-accent)', borderColor: 'var(--color-accent)' },
    success: { background: 'var(--color-success)', color: 'white', borderColor: 'var(--color-success)' },
    danger: { background: 'var(--color-danger)', color: 'white', borderColor: 'var(--color-danger)' },
  };

  const v = variants[variant] || variants.primary;

  return (
    <button
      onClick={onClick}
      disabled={disabled}
      style={{
        display: 'inline-flex',
        alignItems: 'center',
        gap: '8px',
        padding: '10px 20px',
        border: '2px solid',
        borderRadius: 'var(--radius-md)',
        fontWeight: 600,
        fontSize: '0.95rem',
        cursor: disabled ? 'not-allowed' : 'pointer',
        opacity: disabled ? 0.5 : 1,
        transition: 'all 0.2s',
        ...v,
        ...style,
      }}
    >
      {children}
    </button>
  );
}
