import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
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

  describe('ProblemCard with solution', () => {
    beforeEach(() => {
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve({ language: 'java', code: 'public class Solution {}' }),
        })
      );
    });

    afterEach(() => {
      vi.restoreAllMocks();
    });

    it('shows Show Solution button when solutionId is provided', () => {
      render(
        <ProblemCard title="Two Sum" solutionId="two-sum" solutionLanguage="java">
          description text
        </ProblemCard>
      );
      expect(screen.getByText('Show Solution')).toBeInTheDocument();
    });

    it('does not show Show Solution button when solutionId is not provided', () => {
      render(<ProblemCard title="Two Sum">description text</ProblemCard>);
      expect(screen.queryByText('Show Solution')).not.toBeInTheDocument();
    });

    it('shows solution code after clicking button', async () => {
      render(
        <ProblemCard title="Two Sum" solutionId="two-sum" solutionLanguage="java">
          description
        </ProblemCard>
      );
      fireEvent.click(screen.getByText('Show Solution'));
      expect(await screen.findByText(/public class Solution/)).toBeInTheDocument();
    });

    it('toggles solution visibility on re-click', async () => {
      render(
        <ProblemCard title="Two Sum" solutionId="two-sum" solutionLanguage="java">
          description
        </ProblemCard>
      );
      fireEvent.click(screen.getByText('Show Solution'));
      expect(await screen.findByText(/public class Solution/)).toBeInTheDocument();
      fireEvent.click(screen.getByText('Hide Solution'));
      expect(screen.queryByText(/public class Solution/)).not.toBeInTheDocument();
    });

    it('shows language badge when solutionLanguage is provided', () => {
      render(
        <ProblemCard title="Two Sum" solutionId="two-sum" solutionLanguage="java">
          description
        </ProblemCard>
      );
      expect(screen.getByText('java')).toBeInTheDocument();
    });
  });
});
