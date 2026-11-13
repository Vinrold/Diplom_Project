// Адреса API
export const API_URL = 'http://127.0.0.1:8000';
export const COMICS_ENDPOINT = `${API_URL}/comics`;

export const INITIAL_COMICS_FORM = {
    name: '',
    description: '',
    image_url: '',
    genre_ids: [],
    tag_ids: [],
};

// Лимиты
export const COMICS_LIMITS = {
    name: 255,
    description: 5000,
    image_url: 512,
};

// Тексты для интерфейса
export const COMICS_LABELS = {
    title: 'Добавление комикса',
    name: 'Название',
    namePlaseholder: 'Введите название комикса',
    description: 'Описание',
    descriptionPlaceholder: 'Введите описание комикса',
    imageUrl: 'Ссылка на обложку',
    imageUrlPlaceholder: 'https://example.com/cover.jpg',
    submit: 'Добавить комикс',
    submitting: 'Добавляем...',
};

// Сообщения
export const COMICS_MESSAGES = {
    requiredName: 'Название обязательно для добавления',
    nameTooLong: `Название не должно быть длинее ${COMICS_LIMITS.name} символов`,
    descriptionTooLong: `Описание не должно быть длинее ${COMICS_LIMITS.description} символов`,
    urlTooLong: `Ссылка на изображение не должна быть длинее ${COMICS_LIMITS.image_url} символов`,
    invalidUrl: 'Ссылка на изображение должна начинаться с http:// или https://',
    networkError: 'Ошибка соединения с сервером',
    submitError: 'Не удалось добавить комикс',
    success: 'Коммикс успешно добавлен',

};

// После успешного добавления
export const COMICS_ROUTES = {
    home: '/',
    detail: (id)=> `/comics/${id}`
};