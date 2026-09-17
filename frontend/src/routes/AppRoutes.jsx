import { Routes, Route } from 'react-router-dom'
import HomePage from '../pages/HomePage'
import LoginPage from '../pages/LoginPage'
import UserPage from '../pages/UserPage' 

function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/users/:id" element={<UserPage />} /> {}
    </Routes>
  )
}

export default AppRoutes