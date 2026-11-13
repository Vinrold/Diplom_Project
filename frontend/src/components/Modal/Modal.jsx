import styles from './Modal.module.css';

function Modal({ isOpen, onClose, title, children }) {
  if (!isOpen) return null; // модалка не открыта — ничего не рендерим

  return (
    <div className={styles.overlay} onClick={onClose}>
      <div className={styles.content} onClick={(e) => e.stopPropagation()}>
        <div className={styles.header}>
          <h2>{title}</h2>
          <button className={styles.close} onClick={onClose}>
            ✕
          </button>
        </div>
        <div className={styles.body}>{children}</div>
      </div>
    </div>
  );
}

export default Modal;