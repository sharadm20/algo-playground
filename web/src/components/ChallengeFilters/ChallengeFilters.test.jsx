import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import ChallengeFilters from './ChallengeFilters';

const defaultProps = {
  search: '',
  onSearchChange: vi.fn(),
  topicFilter: 'All',
  onTopicChange: vi.fn(),
  languageFilter: 'All',
  onLanguageChange: vi.fn(),
  difficultyFilter: 'All',
  onDifficultyChange: vi.fn(),
  topics: ['Array', 'String', 'Tree'],
  languages: ['java', 'python'],
};

it('renders search input and filter dropdowns', () => {
  render(<ChallengeFilters {...defaultProps} />);
  expect(screen.getByPlaceholderText(/Search challenges/i)).toBeInTheDocument();
  expect(screen.getByDisplayValue('All Topics')).toBeInTheDocument();
  expect(screen.getByDisplayValue('All Languages')).toBeInTheDocument();
  expect(screen.getByDisplayValue('All Difficulties')).toBeInTheDocument();
});

it('calls onSearchChange when typing', () => {
  const onSearchChange = vi.fn();
  render(<ChallengeFilters {...defaultProps} onSearchChange={onSearchChange} />);
  fireEvent.change(screen.getByPlaceholderText(/Search challenges/i), { target: { value: 'two' } });
  expect(onSearchChange).toHaveBeenCalledWith('two');
});

it('calls onTopicChange when selecting topic', () => {
  const onTopicChange = vi.fn();
  render(<ChallengeFilters {...defaultProps} onTopicChange={onTopicChange} topics={['Array', 'String']} />);
  fireEvent.change(screen.getByDisplayValue('All Topics'), { target: { value: 'Array' } });
  expect(onTopicChange).toHaveBeenCalledWith('Array');
});

it('calls onDifficultyChange when selecting difficulty', () => {
  const onDifficultyChange = vi.fn();
  render(<ChallengeFilters {...defaultProps} onDifficultyChange={onDifficultyChange} />);
  fireEvent.change(screen.getByDisplayValue('All Difficulties'), { target: { value: 'easy' } });
  expect(onDifficultyChange).toHaveBeenCalledWith('easy');
});

it('renders topic dropdown options', () => {
  render(<ChallengeFilters {...defaultProps} topics={['Array', 'String', 'Tree']} />);
  expect(screen.getByText('Array')).toBeInTheDocument();
  expect(screen.getByText('String')).toBeInTheDocument();
  expect(screen.getByText('Tree')).toBeInTheDocument();
});
