import { NavLink } from 'react-router-dom';
import { LayoutDashboard, Calculator } from 'lucide-react';
import styles from './Sidebar.module.css';

export default function Sidebar() {
  return (
    <aside className={styles.sidebar} aria-label="Navigasi utama">
      <div className={styles.logo}>
        <div className={styles.logoText}>RaksaDana</div>
        <div className={styles.logoSub}>Platform Investasi Saham AI</div>
      </div>

      <nav className={styles.nav}>
        <NavLink
          to="/"
          end
          className={({ isActive }) =>
            `${styles.navItem} ${isActive ? styles.active : ''}`
          }
        >
          <LayoutDashboard size={18} />
          Dashboard
        </NavLink>

        <NavLink
          to="/kalkulator"
          className={({ isActive }) =>
            `${styles.navItem} ${isActive ? styles.active : ''}`
          }
        >
          <Calculator size={18} />
          Kalkulator
        </NavLink>
      </nav>

      <div className={styles.footer}>
        <p className={styles.footerText}>
          Data bersumber dari model prediksi AI.<br />
          Bukan merupakan saran investasi resmi.
        </p>
      </div>
    </aside>
  );
}
