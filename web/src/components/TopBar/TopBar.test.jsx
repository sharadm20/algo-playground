import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { ThemeProvider } from '../../context/ThemeContext';
import TopBar from './TopBar';

function renderWithTheme(ui) {
  return render(<ThemeProvider>{ui}</ThemeProvider>);
}

describe('TopBar', () => {
  beforeEach(() => {
    localStorage.clear();
  });

  it('renders theme toggle button', () => {
    renderWithTheme(<TopBar onToggleSidebar={() => {}} />);
    expect(screen.getByRole('button', { name: /toggle/i })).toBeInTheDocument();
  });

  it('renders hamburger button', () => {
    renderWithTheme(<TopBar onToggleSidebar={() => {}} />);
    const buttons = screen.getAllByRole('button');
    expect(buttons.length).toBe(2);
  });

  it('shows correct theme label when theme is light', () => {
    localStorage.setItem('dsaTheme', 'light');
    renderWithTheme(<TopBar onToggleSidebar={() => {}} />);
    expect(screen.getByText(/Dark/)).toBeInTheDocument();
  });

  it('fires onToggleSidebar when hamburger clicked', async () => {
    const onToggle = vi.fn();
    const user = userEvent.setup();
    renderWithTheme(<TopBar onToggleSidebar={onToggle} />);
    const btns = screen.getAllByRole('button');
    await user.click(btns[0]);
    expect(onToggle).toHaveBeenCalledTimes(1);
  });
});
