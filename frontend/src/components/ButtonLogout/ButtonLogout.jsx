import { useNavigate } from 'react-router-dom';
import styles from './ButtonLogout.module.css';

function LogoutButton({ children, onClick, type = 'button', disabled = false }) {
  const navigate = useNavigate();

  const handleLogout = () => {
    // 1. Удаляем токены
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token'); // если есть

    // 2. Перенаправляем на страницу входа
    navigate('/login');
  };

  return (
    <button 
      type="button" 
      onClick={handleLogout} 
      disabled={disabled}
      className={styles.button}
    >
      {children}
    </button>
  );
};

export default LogoutButton