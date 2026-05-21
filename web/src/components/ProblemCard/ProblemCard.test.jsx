import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
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


});
