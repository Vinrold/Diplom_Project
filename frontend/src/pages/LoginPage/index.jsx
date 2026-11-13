import { useState, useEffect } from "react";
import styles from './index.module.css';
import Modal from "../../components/Modal/Modal";

function LoginPage({ isOpen, onClose, onSuccess, onOpenRegister }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (isOpen) {
      setEmail('');
      setPassword('');
      setError('');
      setLoading(false);
    }
  }, [isOpen]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const res = await fetch('http://127.0.0.1:8000/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      });

      const data = await res.json();

      if (res.ok) {
        localStorage.setItem('access_token', data.access_token);
        if (data.refresh_token) {
          localStorage.setItem('refresh_token', data.refresh_token);
        }
        onSuccess();
      } else {
        setError(data.detail || 'Ошибка авторизации');
      }
    } catch (err) {
      setError(err.message === 'Failed to fetch'
        ? 'Ошибка соединения с сервером'
        : (err.message || 'Не удалось выполнить вход'));
    } finally {
      setLoading(false);
    }
  };

  const handleRegisterClick = () => {
    onClose();          // закрываем модалку входа
    onOpenRegister();    // открываем модалку регистрации
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Вход в аккаунт">
      <form onSubmit={handleSubmit} className={styles.form}>
        {error && <p className={styles.error}>{error}</p>}

        <div className={styles.field}>
          <label htmlFor="login-email">Email</label>
          <input
            id="login-email"
            type="email"
            value={email}
            className={styles.input}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>

        <div className={styles.field}>
          <label htmlFor="login-password">Пароль</label>
          <input
            id="login-password"
            type="password"
            value={password}
            className={styles.input}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>

        <button type="submit" disabled={loading} className={styles.submitBtn}>
          {loading ? 'Вход...' : 'Войти'}
        </button>
      </form>

      {/* Кнопка-ссылка для перехода к регистрации */}
      <div className={styles.registerLinkWrapper}>
        <span className={styles.registerText}>Нет аккаунта?</span>
        <button
          type="button"
          onClick={handleRegisterClick}
          className={styles.registerLink}
        >
          Зарегистрироваться
        </button>
      </div>
    </Modal>
  );
}

export default LoginPage;