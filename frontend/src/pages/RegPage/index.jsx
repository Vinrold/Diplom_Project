import { useState } from "react";
import style from './index.module.css'


function RegisterModal({ isOpen, onClose, onSuccess}) {
    const [formData, setFormData] = useState({
        nickname: '',
        email: '',
        password: '',
    });
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const handleChange = (e) => {
        setFormData((prev) => ({
            ...prev,
            [e.target.name]: e.target.value,
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        try{
            const res = await fetch('http://127.0.0.1:8000/users/',{
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData),
            });

            const data = await res.json();

            if (!res.ok) {
                throw new Error(data.detail || 'Ошибка регистрации');
            }

            const loginRes = await fetch('http://127.0.0.1:8000/auth/login',{
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    email: formData.email,
                    password: formData.password,
                })
            });

            const loginData = await loginRes.json();

            if (!loginRes.ok){
                throw new Error(loginData.detail || 'Автовход после регистрации не удался')
            }

            localStorage.setItem('access_token', loginData.access_token);
            if (loginData.refresh_token) {
                localStorage.setItem('refresh_token', loginData.refresh_token);
            }

            onSuccess();
        } catch (err) {
            setError(err.message || 'Не удалось Зарегестрироваться');
        } finally {
            setLoading(false);
        }
    };

    if (!isOpen) return null;

    return (
        <div className={style.overlay} onClick={onClose}>
            <div className={style.modal} onClick={(e) => e.stopPropagation()}>
                <h2 className={style.title}>Регистрация</h2>
                
                {error && <p className={style.error}>{error}</p>}

                <form onSubmit={handleSubmit} className={style.form}>
                    <div className={style.field}>
                        <label htmlFor="nickname">Имя пользователя</label>
                        <input 
                            id="nickname"
                            name="nickname"
                            type="text"
                            value={formData.nickname}
                            onChange={handleChange}
                            required
                            className={style.input}
                        />
                    </div>

                    <div className={style.field}>
                        <label htmlFor="email">Email</label>
                        <input 
                            id="email"
                            name="email"
                            type="email"
                            value={formData.email}
                            onChange={handleChange}
                            required
                            className={style.input}
                        />
                    </div>

                    <div className={style.field}>
                        <label htmlFor="password">Пароль</label>
                        <input 
                            id="password"
                            name="password"
                            type="password"
                            value={formData.password}
                            onChange={handleChange}
                            minLength={6}
                            required
                            className={style.input}
                        />
                    </div>

                    <button type="submit" disabled={loading} className={style.submitBtn}>
                        {loading ? 'Регистрация...' : 'Зарегистрироваться'}
                    </button>
                </form>

                <button onClick={onClose} className={style.closeBtn}>
                    Закрыть
                </button>
            </div>
        </div>
    );
}

export default RegisterModal;