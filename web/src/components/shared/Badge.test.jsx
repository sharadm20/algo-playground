import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import Badge from './Badge';

describe('Badge', () => {
  it('renders label text', () => {
    render(<Badge label="Easy" />);
    expect(screen.getByText('Easy')).toBeInTheDocument();
  });

  it('applies custom background and color', () => {
    render(<Badge label="Hard" bg="#f8d7da" color="#721c24" />);
    const span = screen.getByText('Hard');
    expect(span).toHaveStyle({ background: '#f8d7da', color: '#721c24' });
  });

  it('renders with default styles when no bg/color provided', () => {
    render(<Badge label="Default" />);
    const span = screen.getByText('Default');
    expect(span).toHaveStyle({ background: '#e9ecef', color: '#495057' });
  });
});
