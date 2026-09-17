import { useState, useEffect } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import { getUser } from '../../api/users'

function UserPage() {
  const { id } = useParams() 
  const navigate = useNavigate()
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    const loadUser = async () => {
      try {
        setLoading(true)
        const data = await getUser(id)
        setUser(data)
      } catch (err) {
        setError('Пользователь не найден или произошла ошибка')
        console.error(err)
      } finally {
        setLoading(false)
      }
    }
    loadUser()
  }, [id])

  if (loading) return <p>Загрузка...</p>
  if (error) return <p style={{ color: 'red' }}>{error}</p>

  return (
    <div>
      <Link to="/" style={{ marginBottom: '1rem', display: 'inline-block' }}>
        ← Назад к списку
      </Link>
      <h2>Детали пользователя</h2>
      <div style={{ padding: '1rem', border: '1px solid #ccc', borderRadius: '8px', maxWidth: '400px' }}>
        <p><strong>ID:</strong> {user.id}</p>
        <p><strong>Никнейм:</strong> {user.nickname}</p>
        <p><em>(Пароль скрыт в целях безопасности)</em></p>
      </div>
    </div>
  )
}

export default UserPage