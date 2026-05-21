import { useState, useCallback } from 'react';
import { Outlet } from 'react-router-dom';
import Sidebar from '../Sidebar/Sidebar';
import TopBar from '../TopBar/TopBar';
import { ThemeProvider } from '../../context/ThemeContext';
import { ProgressProvider } from '../../context/ProgressContext';
import { useProgress } from '../../hooks/useProgress';
import styles from './Layout.module.css';

function LayoutInner() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const toggleSidebar = useCallback(() => setSidebarOpen(o => !o), []);
  const closeSidebar = useCallback(() => setSidebarOpen(false), []);
  const { progress, currentDay } = useProgress();

  return (
    <div className={styles.layout}>
      <Sidebar open={sidebarOpen} onClose={closeSidebar} completedDays={progress.completedDays} currentDay={currentDay} />
      <div className={styles.main}>
        <TopBar onToggleSidebar={toggleSidebar} />
        <Outlet />
      </div>
      {sidebarOpen && <div className={styles.overlay} onClick={closeSidebar} />}
    </div>
  );
}

export default function Layout() {
  return (
    <ThemeProvider>
      <ProgressProvider>
        <LayoutInner />
      </ProgressProvider>
    </ThemeProvider>
  );
}
