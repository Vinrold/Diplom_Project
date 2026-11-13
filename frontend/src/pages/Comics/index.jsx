import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import styles from './index.module.css';
import ChapterModal from '../../components/ChapterModal/ChapterModal';
import { API_URL } from '../../constants/comics';

function ComicPage() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [comic, setComic] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);
  const [currentUser, setCurrentUser] = useState(null);
  const [isChapterModalOpen, setIsChapterModalOpen] = useState(false);

  const load = async () => {
    try {
      const res = await fetch(`${API_URL}/comics/${id}`);
      const data = await res.json();

      if (res.ok) {
        setComic(data);
      } else {
        setError(data.detail || 'Комикс не найден');
      }
    } catch {
      setError('Ошибка соединения с сервером');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, [id]);

  // Кто залогинен
  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (!token) return;

    fetch(`${API_URL}/users/me`, {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((res) => (res.ok ? res.json() : null))
      .then((user) => setCurrentUser(user))
      .catch(() => setCurrentUser(null));
  }, []);

  if (loading) {
    return <div className={styles.status}>Загружаем комикс...</div>;
  }

  if (error) {
    return (
      <div className={styles.status}>
        <p>{error}</p>
        <button className={styles.backBtn} onClick={() => navigate(-1)}>
          Назад
        </button>
      </div>
    );
  }

  const isOwner = currentUser?.id === comic.owner_id;

  return (
    <div className={styles.page}>
      {/* Верхняя часть: обложка + информация */}
      <section className={styles.header}>
        <div className={styles.coverSide}>
          <img
            src={comic.image_url ? `${API_URL}${comic.image_url}` : '/placeholder.png'}
            alt={`Обложка: ${comic.name}`}
            className={styles.cover}
          />
          <button className={styles.readBtn}>Читать</button>
          <button className={styles.bookmarkBtn}>В закладки</button>
        </div>

        <div className={styles.infoSide}>
          
          <h1 className={styles.title}>{comic.name}</h1>

          <div className={styles.stats}>
            <span>❤️ Лайков: {comic.likes_count ?? 0}</span>
            <span>👁️ Просмотров: {comic.views_count ?? 0}</span>
            <span>🔖 Закладок: {comic.bookmarks_count ?? 0}</span>
          </div>

          {/* Описание — сразу после названия */}
          <div className={styles.description}>
            <h2 className={styles.descriptionTitle}>Описание</h2>
            <p className={styles.descriptionText}>
              {comic.description || 'Описание пока не добавлено.'}
            </p>
          </div>

          {/* жанры */}
          {comic.genres?.length > 0 && (
            <div className={styles.tags}>
              {comic.genres.map((t) => (
                <span key={t.id} className={styles.tag}>{t.name}</span>
              ))}
            </div>
          )}

          {/* Тэги под описанием */}
          {comic.tags?.length > 0 && (
            <div className={styles.tags}>
              {comic.tags.map((t) => (
                <span key={t.id} className={styles.tag}>{t.name}</span>
              ))}
            </div>
          )}
        </div>
      </section>

      {/* Главы — ниже шапки, на всю ширину */}
      <section className={styles.chaptersSection}>
        <div className={styles.chaptersHeader}>
          <h2 className={styles.chaptersTitle}>Главы</h2>

          {isOwner && (
            <button
              className={styles.addChapterBtn}
              onClick={() => setIsChapterModalOpen(true)}
            >
              + Добавить главу
            </button>
          )}
        </div>

        {comic.chapters?.length > 0 ? (
          <div className={styles.chaptersList}>
            {comic.chapters.map((chapter) => (
              <div key={chapter.id} className={styles.chapterItem}>
                <span className={styles.chapterName}>
                  Глава {chapter.number}{chapter.title ? ` — ${chapter.title}` : ''}
                </span>
                <span className={styles.chapterDate}>{chapter.created_at || ''}</span>
              </div>
            ))}
          </div>
        ) : (
          <p className={styles.noChapters}>Главы пока не добавлены</p>
        )}
      </section>

      {isOwner && (
        <ChapterModal
          isOpen={isChapterModalOpen}
          onClose={() => setIsChapterModalOpen(false)}
          comicsId={comic.id}
          onCreated={load}
        />
      )}

    </div>
  );
}

export default ComicPage;