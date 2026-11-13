import { useState, useEffect } from "react";
import styles from './index.module.css'
import { 
  INITIAL_COMICS_FORM, COMICS_LIMITS, COMICS_LABELS, COMICS_MESSAGES, COMICS_ENDPOINT, COMICS_ROUTES, API_URL
 } from "../../constants/comics";

function NewComics({ onSuccess, onClose }) {
  const [form, setForm] = useState(INITIAL_COMICS_FORM);
  const [genres, setGenres] = useState([]);
  const [tags, setTags] = useState([]);
  const [imageUrl, setImageUrl] = useState('');
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(()=>{
    fetch(`${API_URL}/genre`)
      .then((res) => res.json())
      .then(setGenres)
      .catch(()=>{});

    fetch(`${API_URL}/tag`)
      .then((res) => res.json())
      .then(setTags)
      .catch(()=>{}); 
  },[]);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  // 
  const  toggleInList = (field, id) => {
    const list = form[field];
    setForm({
      ...form, [field]: list.includes(id) ? list.filter((x) => x !== id) : [...list, id]
    });
  };

  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    if (file.size > 5 * 1024 * 1024) {
      setError('Файл больше 5 МБ');
      return;
    }

    setIsUploading(true);
    setError('');

    try {
      const formData = new FormData();
      formData.append('file', file);

      const res = await fetch(`${API_URL}/uploads`, {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access_token')}`,
        },
        body: formData,
      });

      const data = await res.json();

      if (res.ok) {
        setImageUrl(data.url);
      } else {
        setError(data.detail || 'Не удалось загрузить изображение')
      }
    } catch (err) {
      setError('Не удалось загрузить изображение')
    } finally {
      setIsUploading(false);
    }
  };

  const validate = () => {
    if (!form.name.trim()) return COMICS_MESSAGES.requiredName;
    
    if (form.name.length > COMICS_LIMITS.name) return COMICS_MESSAGES.nameTooLong

    if (form.description.length > COMICS_LIMITS.description) return COMICS_MESSAGES.descriptionTooLong

    return '';
  }

  const handleSubmit = async (e) => {
    e.preventDefault();

    const validationError = validate();
    if (validationError) {
      setError(validationError);
      return
    }

    setError('');
    setIsSubmitting(true);

    try {
      const res = await fetch(COMICS_ENDPOINT,{
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('access_token')}`,
        },
        body: JSON.stringify({
          name: form.name,
          description: form.description || null,
          image_url: imageUrl || null,
          genre_ids: form.genre_ids,
          tag_ids: form.tag_ids,
        }),
      });

      const data = await res.json();

      if (res.ok) {
        if (onSuccess) onSuccess(data);
        if (onClose) onClose();
      } else {
        setError(data.detail || COMICS_MESSAGES.submitError);
      }
    } catch (err) {
      setError(COMICS_MESSAGES.networkError)
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className={styles.form}>
      {error && <p className={styles.error}>{error}</p>}

      <label className={styles.field}>
        {COMICS_LABELS.name}
        <input 
          name="name"
          value={form.name}
          onChange={handleChange}
          maxLength={COMICS_LIMITS.name}
          placeholder={COMICS_LABELS.namePlaseholder}
        />
      </label>

      <label className={styles.field}>
        {COMICS_LABELS.description}
        <textarea 
          name="description"
          value={form.description}
          onChange={handleChange}
          maxLength={COMICS_LIMITS.description}
          placeholder={COMICS_LABELS.descriptionPlaceholder}
        />
      </label>
      
      <label className={styles.field}>
        {COMICS_LABELS.imageUrl}
        <input 
          type="file"
          accept="image/*"
          onChange={handleFileChange}
          disabled={isUploading}
        />
        {isUploading && <span>Загружаем...</span>}
        {imageUrl && (
          <img
            src={`${API_URL}${imageUrl}`}
            alt="Превью обложки"
            className={styles.preview}
          />
        )}
      </label>

      <fieldset className={styles.group}>
        <legend>Жанры</legend>
        {genres.map((genre)=>(
          <label key={genre.id} className={styles.check}>
            <input
              type="checkbox"
              checked={form.genre_ids.includes(genre.id)}
              onChange={()=> toggleInList('genre_ids', genre.id)}
            />
            {genre.name}
          </label>
        ))}
      </fieldset>

      <fieldset className={styles.group}>
        <legend>Тэги</legend>
        {tags.map((tag)=>(
          <label key={tag.id} className={styles.check}>
            <input
              type="checkbox"
              checked={form.tag_ids.includes(tag.id)}
              onChange={()=> toggleInList('tag_ids', tag.id)}
            />
            {tag.name}
          </label>
        ))}
      </fieldset>

      <button
        type="submit"
        disabled={isSubmitting || isUploading}
      >
        {isSubmitting ? COMICS_LABELS.submitting : COMICS_LABELS.submit}
      </button>
    </form>
  );

}

export default NewComics;