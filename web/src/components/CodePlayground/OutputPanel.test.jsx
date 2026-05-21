import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import OutputPanel from './OutputPanel';

describe('OutputPanel', () => {
  it('shows "Running..." when running prop is true', () => {
    render(<OutputPanel running={true} output={null} error={null} />);
    expect(screen.getByText('Running...')).toBeInTheDocument();
  });

  it('shows error message when error prop is set', () => {
    render(<OutputPanel running={false} output={null} error="SyntaxError" />);
    expect(screen.getByText(/Error: SyntaxError/)).toBeInTheDocument();
  });

  it('shows stdout when output has stdout', () => {
    const output = { stdout: 'Hello World', stderr: '', tests: [], timing_ms: 42 };
    render(<OutputPanel running={false} output={output} error={null} />);
    expect(screen.getByText('Hello World')).toBeInTheDocument();
  });

  it('shows stderr in error style when output has stderr', () => {
    const output = { stdout: '', stderr: 'Error message', tests: [], timing_ms: 42 };
    render(<OutputPanel running={false} output={output} error={null} />);
    expect(screen.getByText('Error message')).toBeInTheDocument();
  });

  it('shows test results with pass/fail indicators', () => {
    const output = {
      stdout: '', stderr: '', timing_ms: 50,
      tests: [
        { name: 'Test 1', passed: true },
        { name: 'Test 2', passed: false },
      ],
    };
    render(<OutputPanel running={false} output={output} error={null} />);
    expect(screen.getByText(/Test 1/)).toBeInTheDocument();
    expect(screen.getByText(/Test 2/)).toBeInTheDocument();
  });

  it('shows timing', () => {
    const output = { stdout: '', stderr: '', tests: [], timing_ms: 123 };
    render(<OutputPanel running={false} output={output} error={null} />);
    expect(screen.getByText('123ms')).toBeInTheDocument();
  });

  it('returns null when no output, error, or running', () => {
    const { container } = render(<OutputPanel running={false} output={null} error={null} />);
    expect(container.innerHTML).toBe('');
  });
});
