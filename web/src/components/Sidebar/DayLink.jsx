import { NavLink } from 'react-router-dom';

const statusIcon = {
  completed: '\u2713',
  current: '\u25CF',
  upcoming: '\u2192',
};

export default function DayLink({ day, title, isComplete, isCurrent }) {
  const status = isComplete ? 'completed' : isCurrent ? 'current' : 'upcoming';

  return (
    <li style={{ margin: '2px 0' }}>
      <NavLink
        to={`/day/${day}`}
        style={({ isActive }) => ({
          display: 'flex',
          alignItems: 'center',
          padding: '10px 20px',
          color: 'var(--color-sidebar-text)',
          textDecoration: 'none',
          borderLeft: '3px solid transparent',
          background: isActive ? 'rgba(52,152,219,0.2)' : 'transparent',
          borderLeftColor: isActive ? 'var(--color-accent)' : 'transparent',
        })}
      >
        <span style={{
          width: 28, height: 28, borderRadius: '50%',
          background: isComplete ? 'var(--color-success)' : isCurrent ? 'var(--color-accent)' : 'rgba(255,255,255,0.1)',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          fontSize: '0.75rem', fontWeight: 600, marginRight: 12, flexShrink: 0,
        }}>
          {day}
        </span>
        <span style={{ flex: 1, fontSize: '0.9rem' }}>{title}</span>
        <span style={{ fontSize: '0.9rem', opacity: isComplete ? 1 : 0.5 }}>
          {statusIcon[status]}
        </span>
      </NavLink>
    </li>
  );
}
