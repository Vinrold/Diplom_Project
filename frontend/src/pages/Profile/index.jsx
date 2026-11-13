import { useState, useEffect } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import Modal from '../../components/Modal/Modal';
import NewComics from '../NewComics';
import style from './index.module.css'


function Profile() {
  const [profile, setProfile] = useState(null);
  const [myComics, setMyComics] = useState([]);
  const [favorites, setFavorites] = useState([]);
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [error, setError] = useState('')

  const fetchWithAuth = async (url) => {
    const token = localStorage.getItem('access_token');
    const res = await fetch(url, {
      headers: {Authorization: `Bearer ${token}`},
    });
    if (!res.ok) {
      throw new Error('Не удалось загрузить данные');
    }
    return res.json();
  };

  const load = async () => {
    try {
      setProfile(await fetchWithAuth('http://127.0.0.1:8000/users/me'));
    } catch {setError('Не удалось загрузить профиль');}

    try {
      setMyComics(await fetchWithAuth('http://127.0.0.1:8000/users/me/comics'));
    } catch {setError('Не удалось загрузить комиксы');}

    try {
      setFavorites(await fetchWithAuth('http://127.0.0.1:8000/users/me/favorites'));
    } catch {setError('Не удалось загрузить избранное');}

  };

  useEffect(() => {
    load();
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

  if (error) return <p className={style.error}>{error}</p>
  if (!profile) return <p className={style.loading}>Загрузка...</p>

  return (
    <div className={style.pageContainer}>
      <section className={style.profileBlock}>
        <h1 className={style.pageTitle}>Личный кабинет</h1>
        <div className={style.profileCard}>
          <h2 className={style.profileName}>{profile.nickname}</h2>
          <p className={style.profileEmail}>{profile.email}</p>
        </div>
      </section>
      <section className={style.sectionBlock}>
        <div className={style.sectionHeader}>
          <h2 className={style.sectionTitle}>
            Мои комиксы <span className={style.countBadge}>({myComics.length})</span>
          </h2>
          <button
            className={style.addBtn}
            onClick={() => setIsModalOpen(true)}
          >
          + Добавить комикс
          </button>
        </div>
        {myComics.length === 0 ? (
          <div className={style.emptyState}>
            <h3>Пока нет комиксов</h3>
            <p>Создайте и опубликуйте первый комикс — он появится здесь.</p>
          </div>
        ):(
          <div className={style.gridView}>
            {myComics.map((comic) => (
              <article key={comic.id} className={style.card}>
                <Link to={`/comics/${comic.id}`} className={style.link}>
                  <img
                    src={getImageUrl(comic.image_url)}
                    alt={comic.name}
                    className={style.cardImage}
                  />
                  <div className={style.cardInfo}>
                    <h3 className={style.cardTitle}>{comic.name}</h3>
                    <div className={style.cardMeta}>
                      <span>{comic.is_published ? 'Опубликован' : 'Черновик'}</span>
                    </div>
                  </div>
                </Link>
              </article>
            ))}
          </div>
        )}

        {isModalOpen && (
          <Modal isOpen={isModalOpen} onClose={()=>setIsModalOpen(false)} title='Новый комикс'>
            <NewComics 
              onSuccess={()=>{
                load();
                setIsModalOpen(false)
              }}
              onClose={()=> setIsModalOpen(false)}
            />
          </Modal>
        )}
      </section>     
      <section className={style.sectionBlock}>
        <h2 className={style.sectionTitle}>
          Избранное <span className={style.countBadge}>({favorites.length})</span>
        </h2>

        {favorites.length === 0 ? (
          <div className={style.emptyState}>
            <h3>В избранном пока пусто</h3>
            <p>Добавляйте комиксы в избранное кнопкой на их странице.</p>
          </div>
        ) : (
          <div className={style.gridView}>
            {favorites.map((comic) => (
              <article key={comic.id} className={style.card}>
                <Link to={`/comics/${comic.id}`} className={style.link}>
                  <img
                    src={getImageUrl(comic.image_url)}
                    alt={comic.name}
                    className={style.cardImage}
                  />
                  <div className={style.cardInfo}>
                    <h3 className={style.cardTitle}>{comic.name}</h3>
                  </div>
                </Link>
              </article>
            ))}
          </div>
        )}
      </section>
      
    </div>
  )

}

export default Profile