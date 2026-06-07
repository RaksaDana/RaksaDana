import { NavLink } from 'react-router-dom';
import { LayoutDashboard, Calculator } from 'lucide-react';
import styles from './BottomNav.module.css';

export default function BottomNav() {
  return (
    <nav className={styles.nav} aria-label="Navigasi mobile">
      <NavLink
        to="/"
        end
        className={({ isActive }) =>
          `${styles.navItem} ${isActive ? styles.active : ''}`
        }
      >
        <LayoutDashboard size={20} />
        Dashboard
      </NavLink>

      <NavLink
        to="/kalkulator"
        className={({ isActive }) =>
          `${styles.navItem} ${isActive ? styles.active : ''}`
        }
      >
        <Calculator size={20} />
        Kalkulator
      </NavLink>
    </nav>
  );
}
