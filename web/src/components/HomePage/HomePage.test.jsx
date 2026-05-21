import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { ThemeProvider } from '../../context/ThemeContext';
import { ProgressProvider } from '../../context/ProgressContext';
import HomePage from './HomePage';

function renderWithProviders(ui) {
  return render(
    <MemoryRouter>
      <ThemeProvider>
        <ProgressProvider>
          {ui}
        </ProgressProvider>
      </ThemeProvider>
    </MemoryRouter>
  );
}

describe('HomePage', () => {
  beforeEach(() => {
    localStorage.clear();
  });

  it('renders title', () => {
    renderWithProviders(<HomePage />);
    expect(screen.getByText('30-Day DSA Study Plan')).toBeInTheDocument();
  });

  it('renders subtitle', () => {
    renderWithProviders(<HomePage />);
    expect(screen.getByText(/mastering Data Structures/)).toBeInTheDocument();
  });

  it('renders StatsRow (Completed label)', () => {
    renderWithProviders(<HomePage />);
    expect(screen.getByText('Completed')).toBeInTheDocument();
  });

  it('renders CalendarGrid with Calendar heading', () => {
    renderWithProviders(<HomePage />);
    expect(screen.getByText('Calendar')).toBeInTheDocument();
  });

  it('renders export link', () => {
    renderWithProviders(<HomePage />);
    const link = screen.getByText('Export Progress Report');
    expect(link).toBeInTheDocument();
    expect(link.closest('a')).toHaveAttribute('href', '/export');
  });
});
