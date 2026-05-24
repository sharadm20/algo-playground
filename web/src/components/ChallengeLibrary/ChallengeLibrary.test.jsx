import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import ChallengeLibrary from './ChallengeLibrary';

const mockChallenges = [
  {
    id: 'two-sum',
    title: 'Two Sum',
    difficulty: 'easy',
    language: 'java',
    topic: 'Array',
    tags: ['hash-map'],
    description: 'Find two numbers that add up to target',
    sourcePath: 'java/TwoSum.java',
    dayIds: [1],
    type: 'problem',
  },
  {
    id: 'binary-search',
    title: 'Binary Search',
    difficulty: 'medium',
    language: 'java',
    topic: 'Binary Search',
    tags: ['binary-search'],
    description: 'Search for target in sorted array',
    sourcePath: 'java/BinarySearch.java',
    dayIds: [16],
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

it('renders challenge cards after loading', async () => {
  render(
    <MemoryRouter>
      <ChallengeLibrary />
    </MemoryRouter>
  );
  expect(await screen.findByRole('heading', { name: 'Two Sum' })).toBeInTheDocument();
  expect(await screen.findByRole('heading', { name: 'Binary Search' })).toBeInTheDocument();
});

it('shows challenge count', async () => {
  render(
    <MemoryRouter>
      <ChallengeLibrary />
    </MemoryRouter>
  );
  expect(await screen.findByText(/2 challenges/)).toBeInTheDocument();
});

it('shows loading state initially', () => {
  global.fetch = vi.fn(() => new Promise(() => {}));
  render(
    <MemoryRouter>
      <ChallengeLibrary />
    </MemoryRouter>
  );
  expect(screen.getByText(/loading/i)).toBeInTheDocument();
});
