import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import CalendarGrid from './CalendarGrid';
import { studyDays } from '../../data/navigation';

describe('CalendarGrid', () => {
  it('renders all 30 days', () => {
    render(
      <MemoryRouter>
        <CalendarGrid completedDays={[]} currentDay={1} />
      </MemoryRouter>
    );
    studyDays.forEach(d => {
      expect(screen.getByText(String(d.day))).toBeInTheDocument();
    });
  });

  it('shows completed day with completed class', () => {
    const { container } = render(
      <MemoryRouter>
        <CalendarGrid completedDays={[1, 2]} currentDay={3} />
      </MemoryRouter>
    );
    const dayLinks = container.querySelectorAll('a');
    const firstTwo = Array.from(dayLinks).slice(0, 2);
    firstTwo.forEach(el => {
      expect(el.className).toMatch(/completed/);
    });
  });

  it('shows current day with current class', () => {
    const { container } = render(
      <MemoryRouter>
        <CalendarGrid completedDays={[]} currentDay={5} />
      </MemoryRouter>
    );
    const dayLinks = container.querySelectorAll('a');
    const current = dayLinks[4];
    expect(current.className).toMatch(/current/);
  });

  it('shows upcoming day with upcoming class', () => {
    const { container } = render(
      <MemoryRouter>
        <CalendarGrid completedDays={[]} currentDay={1} />
      </MemoryRouter>
    );
    const dayLinks = container.querySelectorAll('a');
    for (let i = 1; i < dayLinks.length; i++) {
      expect(dayLinks[i].className).toMatch(/upcoming/);
    }
  });

  it('creates links to /day/:id for each day', () => {
    render(
      <MemoryRouter>
        <CalendarGrid completedDays={[]} currentDay={1} />
      </MemoryRouter>
    );
    studyDays.forEach(d => {
      const link = screen.getByText(String(d.day)).closest('a');
      expect(link).toHaveAttribute('href', `/day/${d.day}`);
    });
  });
});
