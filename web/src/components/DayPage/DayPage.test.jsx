import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import { ThemeProvider } from '../../context/ThemeContext';
import { ProgressProvider } from '../../context/ProgressContext';
import DayPage from './DayPage';

vi.mock('../../content/day-01.mdx', () => ({ default: () => null }));
vi.mock('../../content/day-02.mdx', () => ({ default: () => null }));
vi.mock('../../content/day-03.mdx', () => ({ default: () => null }));
vi.mock('../../content/day-04.mdx', () => ({ default: () => null }));
vi.mock('../../content/day-05.mdx', () => ({ default: () => null }));
vi.mock('../../content/day-06.mdx', () => ({ default: () => null }));
vi.mock('../../content/day-07.mdx', () => ({ default: () => null }));
vi.mock('../../content/day-08.mdx', () => ({ default: () => null }));
vi.mock('../../content/day-09.mdx', () => ({ default: () => null }));
vi.mock('../../content/day-10.mdx', () => ({ default: () => null }));
vi.mock('../../content/day-11.mdx', () => ({ default: () => null }));
vi.mock('../../content/day-12.mdx', () => ({ default: () => null }));
vi.mock('../../content/day-13.mdx', () => ({ default: () => null }));
vi.mock('../../content/day-14.mdx', () => ({ default: () => null }));
vi.mock('../../content/day-15.mdx', () => ({ default: () => null }));
vi.mock('../../content/day-16.mdx', () => ({ default: () => null }));
vi.mock('../../content/day-17.mdx', () => ({ default: () => null }));
vi.mock('../../content/day-18.mdx', () => ({ default: () => null }));
vi.mock('../../content/day-19.mdx', () => ({ default: () => null }));
vi.mock('../../content/day-20.mdx', () => ({ default: () => null }));
vi.mock('../../content/day-21.mdx', () => ({ default: () => null }));
vi.mock('../../content/day-22.mdx', () => ({ default: () => null }));
vi.mock('../../content/day-23.mdx', () => ({ default: () => null }));
vi.mock('../../content/day-24.mdx', () => ({ default: () => null }));
vi.mock('../../content/day-25.mdx', () => ({ default: () => null }));
vi.mock('../../content/day-26.mdx', () => ({ default: () => null }));
vi.mock('../../content/day-27.mdx', () => ({ default: () => null }));
vi.mock('../../content/day-28.mdx', () => ({ default: () => null }));
vi.mock('../../content/day-29.mdx', () => ({ default: () => null }));
vi.mock('../../content/day-30.mdx', () => ({ default: () => null }));

function renderAtRoute(route) {
  return render(
    <MemoryRouter initialEntries={[route]}>
      <ThemeProvider>
        <ProgressProvider>
          <Routes>
            <Route path="/day/:dayId" element={<DayPage />} />
          </Routes>
        </ProgressProvider>
      </ThemeProvider>
    </MemoryRouter>
  );
}

describe('DayPage', () => {
  beforeEach(() => {
    localStorage.clear();
  });

  it('shows "Day not found" for invalid day', () => {
    renderAtRoute('/day/999');
    expect(screen.getByText('Day not found')).toBeInTheDocument();
  });

  it('shows correct day title for valid day', async () => {
    renderAtRoute('/day/1');
    expect(screen.getByText(/Arrays & Hashing/)).toBeInTheDocument();
  });

  it('shows prev/next navigation links', () => {
    renderAtRoute('/day/2');
    expect(screen.getByText(/Day 1/)).toBeInTheDocument();
    expect(screen.getByText(/Day 3/)).toBeInTheDocument();
  });

  it('disables prev link on day 1', () => {
    renderAtRoute('/day/1');
    expect(screen.getByText(/Prev/)).toBeInTheDocument();
  });

  it('disables next link on day 30', () => {
    renderAtRoute('/day/30');
    expect(screen.getByText(/Next/)).toBeInTheDocument();
  });

  it('shows "Mark Complete" button when day not completed', () => {
    renderAtRoute('/day/1');
    expect(screen.getByText(/Mark Day 1 Complete/)).toBeInTheDocument();
  });

  it('shows "Redo" button when day is completed', () => {
    localStorage.setItem('dsaProgress', JSON.stringify({ completedDays: [1], startedAt: new Date().toISOString() }));
    renderAtRoute('/day/1');
    expect(screen.getByText(/Redo Day 1/)).toBeInTheDocument();
  });
});
