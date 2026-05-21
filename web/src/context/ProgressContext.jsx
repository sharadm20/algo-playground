import { createContext, useState, useCallback, useEffect } from 'react';

const STORAGE_KEY = 'dsaProgress';

function loadProgress() {
  try {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored) return JSON.parse(stored);
  } catch {}
  return { completedDays: [], startedAt: new Date().toISOString() };
}

function getCurrentDayFromPath() {
  const m = window.location.pathname.match(/\/day\/(\d+)/);
  return m ? Number(m[1]) : 0;
}

export const ProgressContext = createContext(null);

export function ProgressProvider({ children }) {
  const [progress, setProgress] = useState(loadProgress);
  const [currentDay, setCurrentDay] = useState(getCurrentDayFromPath);

  useEffect(() => {
    const handleLocationChange = () => setCurrentDay(getCurrentDayFromPath());
    window.addEventListener('popstate', handleLocationChange);
    return () => window.removeEventListener('popstate', handleLocationChange);
  }, []);

  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(progress));
  }, [progress]);

  const markComplete = useCallback((day) => {
    setProgress(p => ({
      ...p,
      completedDays: p.completedDays.includes(day) ? p.completedDays : [...p.completedDays, day].sort((a, b) => a - b),
    }));
  }, []);

  const markIncomplete = useCallback((day) => {
    setProgress(p => ({
      ...p,
      completedDays: p.completedDays.filter(d => d !== day),
    }));
  }, []);

  const resetDay = useCallback((day) => {
    setProgress(p => ({
      ...p,
      completedDays: p.completedDays.filter(d => d !== day),
    }));
  }, []);

  const resetAll = useCallback(() => {
    setProgress({ completedDays: [], startedAt: new Date().toISOString() });
  }, []);

  const exportProgress = useCallback(() => {
    return {
      ...progress,
      exportDate: new Date().toISOString(),
      totalDays: 30,
    };
  }, [progress]);

  return (
    <ProgressContext.Provider value={{
      progress, currentDay,
      markComplete, markIncomplete, resetDay, resetAll, exportProgress,
    }}>
      {children}
    </ProgressContext.Provider>
  );
}
