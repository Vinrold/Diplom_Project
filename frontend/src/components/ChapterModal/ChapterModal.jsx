import { useState } from 'react';
import Modal from '../Modal/Modal';
import styles from './ChapterModal.module.css';
import { API_URL } from '../../constants/comics';

function ChapterModal({ isOpen, onClose, comicsId, onCreated }) {
  const [number, setNumber] = useState('');
  const [title, setTitle] = useState('');
  const [files, setFiles] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const formData = new FormData();
      formData.append('number', number);
      if (title) formData.append('title', title);
      for (const file of files) {
        formData.append('pages', file);
      }

      const token = localStorage.getItem('access_token');
      const res = await fetch(`${API_URL}/comics/${comicsId}/chapters`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${token}` },
        body: formData,
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Не удалось добавить главу');

      onCreated();
      onClose();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Новая глава">
      <form onSubmit={handleSubmit} className={styles.form}>
        {error && <p className={styles.error}>{error}</p>}

        <div className={styles.field}>
          <label htmlFor="ch-number">Номер главы</label>
          <input
            id="ch-number"
            type="number"
            min="1"
            value={number}
            onChange={(e) => setNumber(e.target.value)}
            required
            className={styles.input}
          />
        </div>

        <div className={styles.field}>
          <label htmlFor="ch-title">Название (необязательно)</label>
          <input
            id="ch-title"
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className={styles.input}
          />
        </div>

        <div className={styles.field}>
          <label htmlFor="ch-pages">Страницы (можно выбрать несколько)</label>
          <input
            id="ch-pages"
            type="file"
            accept="image/*"
            multiple
            onChange={(e) => setFiles(e.target.files)}
            required
            className={styles.fileInput}
          />
        </div>

        <button type="submit" disabled={loading} className={styles.submitBtn}>
          {loading ? 'Загружаем...' : 'Добавить главу'}
        </button>
      </form>
    </Modal>
  );
}

export default ChapterModal;
