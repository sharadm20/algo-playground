import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import StatsRow from './StatsRow';

describe('StatsRow', () => {
  it('renders completed count', () => {
    render(<StatsRow completed={5} total={30} />);
    expect(screen.getByText('5')).toBeInTheDocument();
    expect(screen.getByText('Completed')).toBeInTheDocument();
  });

  it('renders remaining count', () => {
    render(<StatsRow completed={5} total={30} />);
    expect(screen.getByText('25')).toBeInTheDocument();
    expect(screen.getByText('Remaining')).toBeInTheDocument();
  });

  it('renders percentage', () => {
    render(<StatsRow completed={15} total={30} />);
    expect(screen.getByText('50%')).toBeInTheDocument();
    expect(screen.getByText('Progress')).toBeInTheDocument();
  });

  it('renders problems count', () => {
    render(<StatsRow completed={0} total={30} />);
    expect(screen.getByText('170+')).toBeInTheDocument();
    expect(screen.getByText('Problems')).toBeInTheDocument();
  });
});
