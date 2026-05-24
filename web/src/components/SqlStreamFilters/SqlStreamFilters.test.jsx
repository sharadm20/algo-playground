import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import SqlStreamFilters from './SqlStreamFilters';

const defaultProps = {
  search: '',
  onSearchChange: vi.fn(),
  categoryFilter: 'All',
  onCategoryChange: vi.fn(),
  domainFilter: 'All',
  onDomainChange: vi.fn(),
  difficultyFilter: 'All',
  onDifficultyChange: vi.fn(),
  categories: ['Filtering & Conditionals', 'Window Functions'],
  domains: ['ecommerce', 'hr'],
};

describe('SqlStreamFilters', () => {
  it('renders search input and filter dropdowns', () => {
    render(<SqlStreamFilters {...defaultProps} />);
    expect(screen.getByPlaceholderText(/Search queries/i)).toBeInTheDocument();
    expect(screen.getByDisplayValue('All Categories')).toBeInTheDocument();
    expect(screen.getByDisplayValue('All Domains')).toBeInTheDocument();
    expect(screen.getByDisplayValue('All Difficulties')).toBeInTheDocument();
  });

  it('calls onSearchChange when typing', () => {
    const onSearchChange = vi.fn();
    render(<SqlStreamFilters {...defaultProps} onSearchChange={onSearchChange} />);
    fireEvent.change(screen.getByPlaceholderText(/Search queries/i), { target: { value: 'filter' } });
    expect(onSearchChange).toHaveBeenCalledWith('filter');
  });

  it('calls onCategoryChange when selecting category', () => {
    const onCategoryChange = vi.fn();
    render(<SqlStreamFilters {...defaultProps} onCategoryChange={onCategoryChange} categories={['Filtering & Conditionals']} />);
    fireEvent.change(screen.getByDisplayValue('All Categories'), { target: { value: 'Filtering & Conditionals' } });
    expect(onCategoryChange).toHaveBeenCalledWith('Filtering & Conditionals');
  });

  it('calls onDifficultyChange when selecting difficulty', () => {
    const onDifficultyChange = vi.fn();
    render(<SqlStreamFilters {...defaultProps} onDifficultyChange={onDifficultyChange} />);
    fireEvent.change(screen.getByDisplayValue('All Difficulties'), { target: { value: 'beginner' } });
    expect(onDifficultyChange).toHaveBeenCalledWith('beginner');
  });

  it('calls onDomainChange when selecting domain', () => {
    const onDomainChange = vi.fn();
    render(<SqlStreamFilters {...defaultProps} onDomainChange={onDomainChange} domains={['ecommerce', 'hr']} />);
    fireEvent.change(screen.getByDisplayValue('All Domains'), { target: { value: 'ecommerce' } });
    expect(onDomainChange).toHaveBeenCalledWith('ecommerce');
  });
});
