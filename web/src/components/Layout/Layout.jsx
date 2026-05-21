import { useState, useCallback } from 'react';
import { Outlet } from 'react-router-dom';
import Sidebar from '../Sidebar/Sidebar';
import TopBar from '../TopBar/TopBar';
import { ThemeProvider } from '../../context/ThemeContext';
import { ProgressProvider } from '../../context/ProgressContext';
import styles from './Layout.module.css';

export default function Layout() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const toggleSidebar = useCallback(() => setSidebarOpen(o => !o), []);
  const closeSidebar = useCallback(() => setSidebarOpen(false), []);

  return (
    <ThemeProvider>
      <ProgressProvider>
        <div className={styles.layout}>
          <Sidebar open={sidebarOpen} onClose={closeSidebar} />
          <div className={styles.main}>
            <TopBar onToggleSidebar={toggleSidebar} />
            <Outlet />
          </div>
          {sidebarOpen && <div className={styles.overlay} onClick={closeSidebar} />}
        </div>
      </ProgressProvider>
    </ThemeProvider>
  );
}
