import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { fetchUsers, createUser, deleteUser } from '../../api/users'
import Button from '../../components/Button/Button'
import LogoutButton from '../../components/ButtonLogout/ButtonLogout'

function HomePage() {
  const [users, setUsers] = useState([])
  const [nickname, setNickname] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    loadUsers()
  }, [])

  const loadUsers = async () => {
    try {
      setLoading(true)
      const data = await fetchUsers()
      setUsers(data)
      setError('')
    } catch (err) {
      setError('Ошибка при загрузке пользователей')
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      await createUser({ email: nickname, password })
      setNickname('')
      setPassword('')
      loadUsers() 
    } catch (err) {
      let msg = 'Ошибк при создании пользователя'
      if (err instanceof Error) msg = err.message
      else if (typeof err === 'object' && err.detail) msg = err.detail
      setError(msg)
    }
  }

  const handleDelete = async (id, userNickname) => {
    
    if (!window.confirm(`Вы уверены, что хотите удалить пользователя "${userNickname}"?`)) {
      return
    }

    try {
      await deleteUser(id)
      loadUsers() 
    } catch (err) {
      setError('Ошибка при удалении пользователя')
    }
  }


  return (
    <div>
      
      <h2>Управление пользователями</h2>
      
      <LogoutButton>
        Выход
      </LogoutButton>

      {error && <p style={{ color: 'red', marginBottom: '1rem' }}>{error}</p>}
      
      {}
      <form onSubmit={handleSubmit} style={{ marginBottom: '2rem', display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
        <input 
          type="text" 
          placeholder="email" 
          value={nickname} 
          onChange={(e) => setNickname(e.target.value)} 
          required 
        />
        <input 
          type="password" 
          placeholder="Пароль" 
          value={password} 
          onChange={(e) => setPassword(e.target.value)} 
          required 
        />
        <Button type="submit" disabled={loading}>
          {loading ? 'Создание...' : 'Добавить'}
        </Button>
            
        
      </form>

      <h3>Список ({users.length})</h3>
      {users.length === 0 ? (
        <p>Пользователей пока нет. Добавьте первого!</p>
      ) : (
        <ul style={{ listStyle: 'none', padding: 0 }}>
          {users.map((user) => (
            <li 
              key={user.id} 
              style={{ 
                display: 'flex', 
                justifyContent: 'space-between', 
                alignItems: 'center', 
                padding: '10px', 
                borderBottom: '1px solid #eee' 
              }}
            >
              <div>
                <strong>{user.nickname}</strong> 
                <span style={{ color: '#888', marginLeft: '10px' }}>(ID: {user.id})</span>
              </div>
              
              <div style={{ display: 'flex', gap: '10px' }}>
                {}
                <Link to={`/users/${user.id}`}>
                  <Button type="button" style={{ backgroundColor: '#17a2b8' }}>
                    Просмотр
                  </Button>
                </Link>
                
                {}
                <Button 
                  type="button" 
                  onClick={() => handleDelete(user.id, user.nickname)}
                  style={{ backgroundColor: '#dc3545' }}
                >
                  Удалить
                </Button>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}

export default HomePage