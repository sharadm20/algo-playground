import { useState, useCallback } from 'react';

const API_BASE = import.meta.env.VITE_API_BASE || '';

export function useCodeRunner() {
  const [state, setState] = useState({ running: false, output: null, error: null });

  const run = useCallback(async (code, lang) => {
    setState({ running: true, output: null, error: null });
    try {
      const res = await fetch(`${API_BASE}/api/run`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code, lang }),
      });
      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || 'Execution failed');
      }
      const data = await res.json();
      setState({ running: false, output: data, error: null });
    } catch (e) {
      setState({ running: false, output: null, error: e.message });
    }
  }, []);

  return { ...state, run };
}
