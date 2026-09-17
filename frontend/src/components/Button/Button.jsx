import styles from './Button.module.css'

function Button({ children, onClick, type = 'button', disabled = false }) {
  return (
    <button 
      type={type} 
      onClick={onClick} 
      disabled={disabled}
      className={styles.button}
    >
      {children}
    </button>
  )
}

export default Button