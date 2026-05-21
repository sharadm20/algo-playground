import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { ThemeProvider } from '../../context/ThemeContext';
import { ProgressProvider } from '../../context/ProgressContext';
import ExportPage from './ExportPage';

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

describe('ExportPage', () => {
  beforeEach(() => {
    localStorage.clear();
    vi.stubGlobal('URL', { createObjectURL: vi.fn(() => 'blob:url'), revokeObjectURL: vi.fn() });
  });

  it('renders title', () => {
    renderWithProviders(<ExportPage />);
    expect(screen.getByText('Export Progress')).toBeInTheDocument();
  });

  it('renders subtitle', () => {
    renderWithProviders(<ExportPage />);
    expect(screen.getByText(/Download or copy your progress/)).toBeInTheDocument();
  });

  it('renders markdown card', () => {
    renderWithProviders(<ExportPage />);
    expect(screen.getByText('Markdown Report')).toBeInTheDocument();
  });

  it('renders JSON card', () => {
    renderWithProviders(<ExportPage />);
    expect(screen.getByText('JSON Data')).toBeInTheDocument();
  });

  it('renders download buttons', () => {
    renderWithProviders(<ExportPage />);
    expect(screen.getByText(/Download .md/)).toBeInTheDocument();
    expect(screen.getByText(/Download .json/)).toBeInTheDocument();
  });
});
