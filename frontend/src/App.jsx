import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import BottomNav from './components/BottomNav';
import Dashboard from './pages/Dashboard';
import Calculator from './pages/Calculator';
import styles from './App.module.css';
import './styles/global.css';

export default function App() {
  return (
    <BrowserRouter>
      <div className={styles.shell}>
        {/* Desktop sidebar */}
        <Sidebar />

        {/* Page content */}
        <main className={styles.main}>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/kalkulator" element={<Calculator />} />
          </Routes>
        </main>

        {/* Mobile bottom nav */}
        <BottomNav />
      </div>
    </BrowserRouter>
  );
}
