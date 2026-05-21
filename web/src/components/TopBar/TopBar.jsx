import { useTheme } from '../../context/ThemeContext';
import styles from './TopBar.module.css';

export default function TopBar() {
  const { theme, toggleTheme } = useTheme();

  return (
    <div className={styles.bar}>
      <button className={styles.themeBtn} onClick={toggleTheme}>
        {theme === 'light' ? '\uD83C\uDF19 Dark' : '\u2600\uFE0F Light'}
      </button>
    </div>
  );
}
