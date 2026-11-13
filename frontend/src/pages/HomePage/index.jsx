import { useState, useEffect } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import style from './index.module.css'


function HomePage({ isLoggedIn, userName, handleLogout }) {
  const navigate = useNavigate();
  const [comics, setComics] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchComics = async () => {
      try {
        // Используем публичный эндпоинт — он не требует токена
        const res = await fetch('http://127.0.0.1:8000/comics/public', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
        });

        const text = await res.text();

        if (!res.ok) {
          console.error('❌ Status:', res.status);
          console.error('❌ Response body:', text);
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
  }, []);


  const getImageUrl = (path) => {
    // Если пути нет вообще — заглушка
    if (!path) {
      return 'https://via.placeholder.com/240x340?text=No+Image';
    }

    // Если уже полный URL (например, из стороннего источника) — возвращаем как есть
    if (path.startsWith('http://') || path.startsWith('https://')) {
      return path;
    }

    // Твой кейс: относительный путь вроде "/uploads/comics/..."
    // Формируем полный адрес. Для локальной разработки:
    const baseUrl = 'http://127.0.0.1:8000';
    
    // Убираем ведущий слэш у пути, чтобы не было двойного //
    const cleanPath = path.startsWith('/') ? path.slice(1) : path;

    return `${baseUrl}/${cleanPath}`;
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
        <h1 className={style.title}>Каталог комиксов</h1>
      </header>

      {comics.length === 0 ? (
        <div className={style.emptyState}>
          <h3>Пока нет опубликованных комиксов</h3>
          <p>Создайте и опубликуйте первый комикс — он появится здесь.</p>
        </div>
      ) : (
        <div className={style.comicsGrid}>
          {comics.map((comic) => (
            <article key={comic.id} className={style.comicCard}>
              <Link to={`/comics/${comic.id}`} className={style.link}>
                <img
                  src={getImageUrl(comic.image_url)}
                  alt={comic.name}
                  className={style.comicImage}
                />
                <div className={style.comicInfo}>
                  <h3 className={style.comicTitle}>{comic.name}</h3>
                  <p className={style.comicSubtitle}>
                    {comic.owner_id || 'Автор неизвестен'}
                  </p>
                  <div className={style.comicMeta}>
                    <span>ID: {comic.id}</span>
                    <span>{comic.is_published ? 'Опубликован' : 'Черновик'}</span>
                  </div>
                </div>
              </Link>
            </article>
          ))}
        </div>
      )}
    </div>
  );

}

export default HomePage