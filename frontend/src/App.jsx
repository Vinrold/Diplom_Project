import { useState, useEffect } from 'react';
import { BrowserRouter } from 'react-router-dom';

import AppRoutes from './routes/AppRoutes';
import style from './index.module.css';
import logo from './assets/in-yn.jpeg'
import RegisterModal from './pages/RegPage';


function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userName, setUserName] = useState('');
  const [isRegisterModalOpen, setIsRegisterModalOpen] = useState(false);


  // Авторизация
  useEffect(()=>{
    const token = localStorage.getItem('access_token');
    if (!token){
      setIsLoggedIn(false);
      setUserName('');
      return;
    }
    setIsLoggedIn(true);

    // Запрос на текущего пользователя
    fetch('http://127.0.0.1:8000/users/me', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
    })
      .then((res)=>{
        // Если токен истек выходим
        if (!res.ok){
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          setIsLoggedIn(false);
          setUserName('');
          return;
        }
        return res.json();
      })
      .then((user)=>{
        setUserName(user.nickname || 'Пользователь')
        setIsLoggedIn(true);
      })
      .catch(()=>{
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        setIsLoggedIn(false);
        setUserName('');
      });
  }, []);

  const handleLogout = ()=>{
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    setIsLoggedIn(false);
    setUserName('');
    // window.location.href = '/login';
  };

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
              <a href="/login" className={style.authLink}>Вход</a>
              {/* Кнопка регистрации */}
              <button 
                onClick={() => setIsRegisterModalOpen(true)}
                className={style.authLink}
                style={{ textDecoration: 'underline', cursor: 'pointer'}}
              >
                Регистрация
              </button>
            </div>
          )}
        </header>
        <main className={style.main}>
          <AppRoutes isLoggedIn={isLoggedIn} userName={userName} handleLogout={handleLogout}/>
        </main>
      </div>
      <RegisterModal 
        isOpen={isRegisterModalOpen}
        onClose={() => setIsRegisterModalOpen(false)}
      />
    </>
  )
}

export default App