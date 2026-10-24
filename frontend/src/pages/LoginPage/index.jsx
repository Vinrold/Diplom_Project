import { useNavigate } from "react-router-dom";
import { useState } from "react";
import styles from './index.module.css'


function LoginPage() {
  const navigate = useNavigate('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    try {
      const res = await fetch('http://127.0.0.1:8000/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      });

      const data = await res.json();

      if (res.ok) {
        localStorage.setItem('access_token', data.access_token);
        navigate('/');
      } else {
        setError(data.detail || 'Ошибка авторизации');
      }
    } catch (err) {
      setError('Ошибка соединения с сервером')
    }
  };

  return (
    <div className={styles.container}>
      <form onSubmit={handleSubmit} className={styles.form}>
        <h2 className={styles.title}>Страница входа</h2>
          {error && <p style={{color: 'red'}}> {error} </p>}
        <div className={styles.field}>
          <label className={styles.label}>Email</label>
          <input 
            type="email"
            value={email}
            className={styles.input}
            onChange={(e) => setEmail(e.target.value)}
            required />
        </div>
        <div className={styles.field}>
          <label className={styles.label}>Пароль</label>
          <input 
            type="password"
            value={password}
            className={styles.input}
            onChange={(e) => setPassword(e.target.value)}
            required/>
        </div>
        <button type="submit" className={styles.submitBtn}>Войти</button>
        <div className={styles.registerLinkWrapper}>
          Нет аккаунта?{' '}
          <span
            className={styles.registerLink}
            onClick={() => navigate('/register')}
            role="button"
            tabIndex={0}
            onKeyDown={(e) => {
              if (e.key === 'Enter') navigate('/register');
            }}
          >
            Зарегистрироваться
          </span>
        </div>
      </form>
    </div>
  )
}

export default LoginPage