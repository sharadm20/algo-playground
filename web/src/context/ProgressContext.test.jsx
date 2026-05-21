import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { useContext } from 'react';
import { ProgressContext, ProgressProvider } from './ProgressContext';

function TestComponent() {
  const ctx = useContext(ProgressContext);
  return (
    <div>
      <div data-testid="days">{JSON.stringify(ctx.progress.completedDays)}</div>
      <button onClick={() => ctx.markComplete(1)}>Mark 1</button>
      <button onClick={() => ctx.markComplete(2)}>Mark 2</button>
      <button onClick={() => ctx.markIncomplete(1)}>Unmark 1</button>
      <button onClick={() => ctx.resetDay(2)}>Reset 2</button>
    </div>
  );
}

describe('ProgressContext', () => {
  beforeEach(() => {
    localStorage.clear();
    vi.stubGlobal('location', { pathname: '/' });
  });

  it('wraps child component and provides context', () => {
    render(<ProgressProvider><TestComponent /></ProgressProvider>);
    expect(screen.getByTestId('days')).toBeInTheDocument();
  });

  it('markComplete adds day to completedDays', async () => {
    const user = userEvent.setup();
    render(<ProgressProvider><TestComponent /></ProgressProvider>);
    await user.click(screen.getByText('Mark 1'));
    expect(screen.getByTestId('days').textContent).toContain('1');
  });

  it('markComplete does not duplicate day', async () => {
    const user = userEvent.setup();
    render(<ProgressProvider><TestComponent /></ProgressProvider>);
    await user.click(screen.getByText('Mark 1'));
    await user.click(screen.getByText('Mark 1'));
    const days = JSON.parse(screen.getByTestId('days').textContent);
    expect(days).toEqual([1]);
  });

  it('markIncomplete removes day from completedDays', async () => {
    const user = userEvent.setup();
    render(<ProgressProvider><TestComponent /></ProgressProvider>);
    await user.click(screen.getByText('Mark 1'));
    await user.click(screen.getByText('Unmark 1'));
    expect(screen.getByTestId('days').textContent).not.toContain('1');
  });

  it('resetDay removes day from completedDays', async () => {
    const user = userEvent.setup();
    render(<ProgressProvider><TestComponent /></ProgressProvider>);
    await user.click(screen.getByText('Mark 2'));
    await user.click(screen.getByText('Reset 2'));
    expect(screen.getByTestId('days').textContent).not.toContain('2');
  });

  it('progress is persisted to localStorage', async () => {
    const user = userEvent.setup();
    render(<ProgressProvider><TestComponent /></ProgressProvider>);
    await user.click(screen.getByText('Mark 1'));
    const stored = JSON.parse(localStorage.getItem('dsaProgress'));
    expect(stored.completedDays).toContain(1);
  });
});
