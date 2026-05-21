import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import { useEffect } from 'react';
import { useCodeRunner } from './useCodeRunner';

function TestComponent({ code, lang, shouldRun }) {
  const { running, output, error, run } = useCodeRunner();
  useEffect(() => {
    if (shouldRun) run(code, lang);
  }, [shouldRun, code, lang, run]);
  return (
    <div>
      <div data-testid="running">{String(running)}</div>
      <div data-testid="output">{output ? JSON.stringify(output) : 'null'}</div>
      <div data-testid="error">{error || 'null'}</div>
    </div>
  );
}

const mockResponse = (data, ok = true) => {
  return Promise.resolve({
    ok,
    json: () => ok ? Promise.resolve(data) : Promise.resolve({ detail: data }),
  });
};

describe('useCodeRunner', () => {
  beforeEach(() => {
    global.fetch = vi.fn();
  });

  it('initial state is idle', () => {
    render(<TestComponent code="" lang="python" shouldRun={false} />);
    expect(screen.getByTestId('running').textContent).toBe('false');
    expect(screen.getByTestId('error').textContent).toBe('null');
  });

  it('sets running to true when run is called', async () => {
    global.fetch.mockImplementation(() => new Promise(() => {}));
    render(<TestComponent code="print(1)" lang="python" shouldRun={true} />);
    expect(screen.getByTestId('running').textContent).toBe('true');
  });

  it('on success, sets output and running to false', async () => {
    global.fetch.mockImplementation(() => mockResponse({ stdout: 'Hello', timing_ms: 10 }));
    render(<TestComponent code="print(1)" lang="python" shouldRun={true} />);
    await vi.waitFor(() => {
      expect(screen.getByTestId('running').textContent).toBe('false');
    });
    const outputText = screen.getByTestId('output').textContent;
    expect(outputText).toContain('Hello');
  });

  it('on error, sets error message and running to false', async () => {
    global.fetch.mockImplementation(() => mockResponse('Execution failed', false));
    render(<TestComponent code="bad code" lang="python" shouldRun={true} />);
    await vi.waitFor(() => {
      expect(screen.getByTestId('running').textContent).toBe('false');
    });
    expect(screen.getByTestId('error').textContent).toBe('Execution failed');
  });
});
