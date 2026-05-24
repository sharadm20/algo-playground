import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import ChallengeEmbed from './ChallengeEmbed';

const mockChallenges = [
  {
    id: 'two-sum',
    title: 'Two Sum',
    difficulty: 'easy',
    topic: 'Array',
    tags: ['hash-map'],
    description: 'Find two numbers that add up to target',
    language: 'java',
    sourcePath: 'java/TwoSum.java',
    dayIds: [1],
    type: 'problem',
  },
];

beforeEach(() => {
  global.fetch = vi.fn(() =>
    Promise.resolve({
      ok: true,
      json: () => Promise.resolve(mockChallenges),
    })
  );
});

afterEach(() => {
  vi.restoreAllMocks();
});

it('renders ProblemCard for valid challenge id', async () => {
  render(<ChallengeEmbed id="two-sum" />);
  expect(await screen.findByText('Two Sum')).toBeInTheDocument();
  expect(await screen.findByText('easy')).toBeInTheDocument();
});

it('renders error message for unknown id', async () => {
  render(<ChallengeEmbed id="nonexistent" />);
  expect(await screen.findByText(/not found/i)).toBeInTheDocument();
});

it('shows loading state initially', () => {
  global.fetch = vi.fn(() => new Promise(() => {}));
  render(<ChallengeEmbed id="two-sum" />);
  expect(screen.getByText(/loading/i)).toBeInTheDocument();
});

it('handles fetch failure', async () => {
  global.fetch = vi.fn(() => Promise.reject(new Error('Network error')));
  render(<ChallengeEmbed id="two-sum" />);
  expect(await screen.findByText(/failed to load/i)).toBeInTheDocument();
});
