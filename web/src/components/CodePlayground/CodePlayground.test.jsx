import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import { ThemeProvider } from '../../context/ThemeContext';
import CodePlayground from './CodePlayground';

vi.mock('codemirror', () => {
  class MockEditorView {
    constructor() {
      this.destroy = vi.fn();
      this.update = vi.fn();
      this.state = { doc: { toString: () => '' } };
    }
  }
  return { EditorView: MockEditorView, basicSetup: [] };
});
vi.mock('@codemirror/state', () => ({ EditorState: { create: vi.fn() } }));
vi.mock('@codemirror/lang-python', () => ({ python: () => ({ extensions: [] }) }));
vi.mock('@codemirror/lang-javascript', () => ({ javascript: () => ({ extensions: [] }) }));
vi.mock('@codemirror/lang-rust', () => ({ rust: () => ({ extensions: [] }) }));
vi.mock('@codemirror/lang-java', () => ({ java: () => ({ extensions: [] }) }));
vi.mock('@codemirror/lang-cpp', () => ({ cpp: () => ({ extensions: [] }) }));
vi.mock('@codemirror/theme-one-dark', () => ({ oneDark: [] }));

function renderWithTheme(ui) {
  return render(<ThemeProvider>{ui}</ThemeProvider>);
}

describe('CodePlayground', () => {
  beforeEach(() => {
    localStorage.clear();
  });

  it('renders language selector', () => {
    renderWithTheme(<CodePlayground />);
    expect(screen.getByRole('combobox')).toBeInTheDocument();
  });

  it('renders run button', () => {
    renderWithTheme(<CodePlayground />);
    expect(screen.getByText('▶ Run')).toBeInTheDocument();
  });

  it('renders reset button', () => {
    renderWithTheme(<CodePlayground />);
    expect(screen.getByText('↺ Reset')).toBeInTheDocument();
  });

  it('renders OutputPanel area (Running... not initially shown)', () => {
    renderWithTheme(<CodePlayground />);
    expect(screen.queryByText('Running...')).not.toBeInTheDocument();
  });
});
