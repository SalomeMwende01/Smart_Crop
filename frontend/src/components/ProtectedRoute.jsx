import { Navigate, useLocation } from 'react-router-dom'

import useAuth from '../context/useAuth'

function ProtectedRoute({ children, allowedRoles }) {
  const { loading, isAuthenticated, user } = useAuth()
  const location = useLocation()

  if (loading) {
    return <div className="screen-center">Loading your workspace...</div>
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />
  }

  if (allowedRoles && !allowedRoles.includes(user.role)) {
    const fallback = user.role === 'ADMIN' ? '/admin' : '/agent'
    return <Navigate to={fallback} replace />
  }

  return children
}

export default ProtectedRoute
