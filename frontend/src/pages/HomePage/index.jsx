import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import style from './index.module.css'


function HomePage() {
  const navigate = useNavigate();
  const [comics, setComics] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (!token){
      navigate('/login');
      return;
    }

    const fetchComics = async () => {
      try {
        const res = await fetch('/comics/', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
          },
        });

        // Читаем текст ДО попытки парсить JSON — это спасёт от «Unexpected token '<'»
        const text = await res.text();

        if (!res.ok) {
          console.error('❌ Status:', res.status);
          console.error('❌ Response body:', text); // тут будет HTML или JSON с ошибкой

        if (res.status === 401) {
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          navigate('/login');
          return;
        }

        throw new Error(`Ошибка сервера: ${res.status}`);
        }   

        const data = JSON.parse(text);
        setComics(Array.isArray(data) ? data : []);
      } catch (err) {
        console.error('💥 Fetch error:', err);
        setError(err instanceof Error ? err.message : 'Произошла ошибка при загрузке комиксов');
      } finally {
        setLoading(false);
      }
    };

    fetchComics()
  }, [navigate]);

  const getImageUrl = (url) => {
    if (!url) return 'https://via.placeholder.com/240x340?text=No+Image';
    if (url.startsWith('http://') || url.startsWith('https://')) return url;
    if (url.startsWith('/uploads/')) {
      return 'http://127.0.0.1:8000'+url;
    }
    return url;
  };

  const handleLogout = ()=>{
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    navigate('/login');
  };

  if (loading) {
    return <div className={style.loading}>Загрузка списка комиксов</div>;
  }

  if (error) {
    return <div className={style.error}>{error}</div>
  }

  return (
    <div className={style.container}>
      <header className={style.header}>
        <h1 className={style.title}>Мои комиксы</h1>
        <button
          onClick={handleLogout}
          className={style.logoutBtn}
          type='button' 
        >Выйти</button>
      </header>

      {comics.length === 0 ? (
        <div className={style.emptyState}>
          <h3>У вас пока нет комиксов</h3>
          <p>Добавьте первый комикс, чтобы он появился здесь</p>
        </div>
      ) : (
        <div className={style.comicsGrid}>
          {comics.map((comic)=>(
            <article key={comic.id} className={style.comicCard}>

              <img 
                src={getImageUrl(comic.image_url) }
                alt={comic.name}
                className={style.comicImage} 
              />

              <div className={style.comicInfo}>
                <h3 className={style.comicTitle}>{comic.name}</h3>
                <p className={style.comicSubtitle}>
                  {comic.author || 'Автор не известен'}
                </p>
                <div className={style.comicMeta}>
                  <span>Год: {comic.year || '-'}</span>
                  {comic.genre && <span>Жанр: {comic.genre}</span>}
                </div>
              </div>
            </article>
          ))}
        </div>
      )}
    </div>
  )

}

export default HomePage