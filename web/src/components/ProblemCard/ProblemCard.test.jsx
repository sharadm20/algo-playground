import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import ProblemCard from './ProblemCard';

describe('ProblemCard', () => {
  it('renders title', () => {
    render(<ProblemCard title="Two Sum">description</ProblemCard>);
    expect(screen.getByText('Two Sum')).toBeInTheDocument();
  });

  it('renders difficulty badge for easy', () => {
    render(<ProblemCard title="Test" difficulty="easy">desc</ProblemCard>);
    expect(screen.getByText('easy')).toBeInTheDocument();
  });

  it('renders difficulty badge for medium', () => {
    render(<ProblemCard title="Test" difficulty="medium">desc</ProblemCard>);
    expect(screen.getByText('medium')).toBeInTheDocument();
  });

  it('renders difficulty badge for hard', () => {
    render(<ProblemCard title="Test" difficulty="hard">desc</ProblemCard>);
    expect(screen.getByText('hard')).toBeInTheDocument();
  });

  it('renders pattern text', () => {
    render(<ProblemCard title="Test" pattern="Hash Map">desc</ProblemCard>);
    expect(screen.getByText('Pattern: Hash Map')).toBeInTheDocument();
  });

  it('renders children description', () => {
    render(<ProblemCard title="Test">Solve this problem</ProblemCard>);
    expect(screen.getByText('Solve this problem')).toBeInTheDocument();
  });

  it('toggles solution details on click', async () => {
    const user = userEvent.setup();
    render(<ProblemCard title="Test">desc</ProblemCard>);
    const summary = screen.getByText('Show Solution');
    await user.click(summary);
    expect(screen.getByText('Hide Solution')).toBeInTheDocument();
    await user.click(screen.getByText('Hide Solution'));
    expect(screen.getByText('Show Solution')).toBeInTheDocument();
  });
});
