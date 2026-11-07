import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

import AppRoutes from './routes/AppRoutes';
import style from './index.module.css';
import logo from './assets/in-yn.jpeg'
import RegisterModal from './pages/RegPage';
import LoginPage from './pages/LoginPage';
import { checkAuth } from './components/ChekAuth/ChekAuth';


function App() {
  const navigate = useNavigate();

  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userName, setUserName] = useState('');
  const [userEmail, setUserEmail] = useState('');
  const [isRegisterModalOpen, setIsRegisterModalOpen] = useState(false);
  const [isLoginModalOpen, setIsLoginModalOpen] = useState(false);


  const applyUser = (user) => {
    if (user) {
      setIsLoggedIn(true);
      setUserName(user.nickname || 'Пользователь');
      setUserEmail(user.email || '');
    } else {
      setIsLoggedIn(false);
      setUserName('');
      setUserEmail('');
    }
  };

  // Авторизация
  useEffect(()=>{
    checkAuth(applyUser);
  }, []);

  const handleLogout = ()=>{
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    applyUser(null)
    // window.location.href = '/login';
  };

  const handleLoginSuccess = async () => {
    setIsLoginModalOpen(false);
    await checkAuth(applyUser);
    navigate('/', { replace: true });
  };

  const handleRegisterSuccess = () => {
    setIsRegisterModalOpen(false);
    checkAuth(applyUser )
  }

  return (
    <>
      <div className={style.container}>
        <header className={style.header}>
          {/* Логотип */}
          <img src={logo} alt="Логотип" className={style.logo}/>
          
          {/* управление */}
          {/* логин/логаут */}
          
          {isLoggedIn ? (
            <div className={style.userMenu}>
              <span className={style.username}>{userName}</span>
              <button 
                onClick={handleLogout}
                className={style.logoutBtn}
                type='button'
              >Выйти</button>
            </div>
          ) : (
            <div className={style.authLinks}>
              <button                           
                onClick={() => setIsLoginModalOpen(true)}
                className={style.authLink}
                type='button'
              >Вход</button>
              <button
                onClick={() => setIsRegisterModalOpen(true)}
                className={style.authLink}
                style={{ textDecoration: 'underline', cursor: 'pointer' }}
                type='button'
              >Регистрация</button>
            </div>
          )}
        </header>
        <main className={style.main}>
          <AppRoutes isLoggedIn={isLoggedIn} userEmail={userEmail} handleLogout={handleLogout}/>
        </main>
      </div>
      <RegisterModal 
        isOpen={isRegisterModalOpen}
        onClose={() => setIsRegisterModalOpen(false)}
        onSuccess={handleRegisterSuccess}
      />
      <LoginPage
        isOpen={isLoginModalOpen}
        onClose={() => setIsLoginModalOpen(false)}
        onSuccess={handleLoginSuccess}
      />
    </>
  )
}

export default App