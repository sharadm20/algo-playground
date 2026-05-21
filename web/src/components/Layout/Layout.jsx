import { Outlet } from 'react-router-dom';
import Sidebar from '../Sidebar/Sidebar';
import TopBar from '../TopBar/TopBar';
import { ThemeProvider } from '../../context/ThemeContext';
import { ProgressProvider } from '../../context/ProgressContext';
import styles from './Layout.module.css';

export default function Layout() {
  return (
    <ThemeProvider>
      <ProgressProvider>
        <div className={styles.layout}>
          <Sidebar />
          <div className={styles.main}>
            <TopBar />
            <Outlet />
          </div>
        </div>
      </ProgressProvider>
    </ThemeProvider>
  );
}
