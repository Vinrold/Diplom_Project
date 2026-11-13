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
          <div className={style.headerInner}>
            {/* Логотип */}
            <img
              src={logo}
              alt="Логотип"
              className={style.logo}
              onClick={() => navigate('/')}
            />

            {/* Навигация Пока не придумана  по этопу закоментирвана*/}
            <nav className={style.nav}>
              {/* <button
                className={style.navLink}
                type="button"
                onClick={() => navigate('/')}
              >
                Каталог
              </button>
              <button
                className={style.navLink}
                type="button"
                onClick={() => navigate('/account')}
              >
                Личный кабинет
              </button>
              <span className={style.navMore}>···</span> */}
            </nav>

            {/* Правая зона: поиск + вход/профиль */}
            <div className={style.rightZone}>
              <div className={style.search}>
                <svg
                  className={style.searchIcon}
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                >
                  <circle cx="11" cy="11" r="7" />
                  <line x1="21" y1="21" x2="16.5" y2="16.5" />
                </svg>
                <input
                  type="text"
                  placeholder="Что ищем, самурай?"
                  className={style.searchInput}
                />
              </div>

              {isLoggedIn ? (
                <div className={style.userMenu}>
                  <span className={style.username}>{userName}</span>
                  <button
                    onClick={() => navigate('/account')}
                    className={style.accountBtn}
                    type="button"
                  >
                    Личный кабинет
                  </button>
                  <button onClick={handleLogout} className={style.logoutBtn} type="button">
                    Выйти
                  </button>
                </div>
              ) : (
                <button
                  onClick={() => setIsLoginModalOpen(true)}
                  className={style.authBtn}
                  type="button"
                >
                  Вход/Регистрация
                </button>
              )}
            </div>
          </div>
        </header>

        <main className={style.main}>
          <AppRoutes isLoggedIn={isLoggedIn} userEmail={userEmail} handleLogout={handleLogout} />
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
  );
}

export default App