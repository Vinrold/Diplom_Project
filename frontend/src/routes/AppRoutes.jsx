import { Routes, Route, Navigate } from 'react-router-dom';
import ProtectedRoute from '../components/ProtectedRoute';
import HomePage from '../pages/HomePage';
import LoginPage from '../pages/LoginPage';
import UserPage from '../pages/UserPage';
import Profile from '../pages/Profile';

function AppRoutes({isLoggedIn, userName, handleLogout}) {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/" element={
        <HomePage
          isLoggedIn={isLoggedIn}
          userName={userName}
          handleLogout={handleLogout}
        />
      } />
      <Route path="/users/:id" element={
        <ProtectedRoute>
          <UserPage />
        </ProtectedRoute>
      } />
      <Route path='/account' element={
        localStorage.getItem('access_token') ? <Profile/> : <Navigate to='/' replace/>
      }
      />
    </Routes>

  )
}

export default AppRoutes