import { Navigate, Route, Routes } from 'react-router-dom'

import ProtectedRoute from './components/ProtectedRoute'
import useAuth from './context/useAuth'
import AppShell from './layouts/AppShell'
import AdminDashboardPage from './pages/AdminDashboardPage'
import AgentDashboardPage from './pages/AgentDashboardPage'
import LoginPage from './pages/LoginPage'
import NotFoundPage from './pages/NotFoundPage'

function RoleRedirect() {
  const { loading, isAuthenticated, user } = useAuth()

  if (loading) {
    return <div className="screen-center">Preparing dashboard...</div>
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }

  return <Navigate to={user.role === 'ADMIN' ? '/admin' : '/agent'} replace />
}

function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />

      <Route
        element={
          <ProtectedRoute>
            <AppShell />
          </ProtectedRoute>
        }
      >
        <Route
          path="/admin"
          element={
            <ProtectedRoute allowedRoles={['ADMIN']}>
              <AdminDashboardPage />
            </ProtectedRoute>
          }
        />

        <Route
          path="/agent"
          element={
            <ProtectedRoute allowedRoles={['AGENT']}>
              <AgentDashboardPage />
            </ProtectedRoute>
          }
        />
      </Route>

      <Route path="/" element={<RoleRedirect />} />
      <Route path="*" element={<NotFoundPage />} />
    </Routes>
  )
}

export default App
