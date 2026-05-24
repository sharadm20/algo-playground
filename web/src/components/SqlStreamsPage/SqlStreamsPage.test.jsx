import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import SqlStreamsPage from './SqlStreamsPage';

describe('SqlStreamsPage', () => {
  it('renders the page title', () => {
    render(<SqlStreamsPage />);
    expect(screen.getByText('SQL ↔ Java Streams')).toBeInTheDocument();
  });

  it('renders all query cards', () => {
    render(<SqlStreamsPage />);
    expect(screen.getByText('Find Customers with High Purchase Amounts')).toBeInTheDocument();
    expect(screen.getByText('Multi-Condition Filter with OR/AND Logic')).toBeInTheDocument();
  });

  it('shows result count', () => {
    render(<SqlStreamsPage />);
    expect(screen.getByText(/18 queries/)).toBeInTheDocument();
  });

  it('filters results by search', () => {
    render(<SqlStreamsPage />);
    fireEvent.change(screen.getByPlaceholderText('Search queries...'), { target: { value: 'rank' } });
    expect(screen.getByText('Rank Students by Grade per Subject')).toBeInTheDocument();
    expect(screen.queryByText('Find Customers with High Purchase Amounts')).not.toBeInTheDocument();
  });

  it('shows empty state when no results match', () => {
    render(<SqlStreamsPage />);
    fireEvent.change(screen.getByPlaceholderText('Search queries...'), { target: { value: 'zzzznotfound' } });
    expect(screen.getByText(/no queries match/i)).toBeInTheDocument();
  });

  it('clears filters and restores all results', () => {
    render(<SqlStreamsPage />);
    fireEvent.change(screen.getByPlaceholderText('Search queries...'), { target: { value: 'rank' } });
    expect(screen.getByText((_, el) => el.tagName === 'P' && el.textContent.includes('of 18 queries'))).toBeInTheDocument();
    expect(screen.queryByText('Find Customers with High Purchase Amounts')).not.toBeInTheDocument();
    fireEvent.change(screen.getByPlaceholderText('Search queries...'), { target: { value: '' } });
    expect(screen.getByText((_, el) => el.tagName === 'P' && el.textContent.includes('of 18 queries'))).toBeInTheDocument();
    expect(screen.getByText('Find Customers with High Purchase Amounts')).toBeInTheDocument();
  });
});
