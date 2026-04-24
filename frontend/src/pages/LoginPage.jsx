import { useState } from 'react'
import { Navigate, useLocation, useNavigate } from 'react-router-dom'

import useAuth from '../context/useAuth'

function LoginPage() {
  const { login, isAuthenticated, user } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()

  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [submitting, setSubmitting] = useState(false)

  if (isAuthenticated) {
    const route = user?.role === 'ADMIN' ? '/admin' : '/agent'
    return <Navigate to={route} replace />
  }

  const onSubmit = async (event) => {
    event.preventDefault()
    setError('')
    setSubmitting(true)

    try {
      const loggedInUser = await login(username, password)
      const route = loggedInUser.role === 'ADMIN' ? '/admin' : '/agent'
      const from = location.state?.from?.pathname
      navigate(from || route, { replace: true })
    } catch (requestError) {
      setError(requestError.response?.data?.detail || 'Login failed. Check your credentials and try again.')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="auth-wrap">
      <section className="auth-card">
        <p className="eyebrow">SmartSeason Assessment</p>
        <h1>FieldPulse Monitoring</h1>
        <p className="muted">Track every field stage, note, and risk signal from one shared command center.</p>

        <form onSubmit={onSubmit} className="auth-form">
          <label>
            Username
            <input
              type="text"
              value={username}
              onChange={(event) => setUsername(event.target.value)}
              required
              autoComplete="username"
            />
          </label>

          <label>
            Password
            <input
              type="password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              required
              autoComplete="current-password"
            />
          </label>

          {error ? <p className="form-error">{error}</p> : null}

          <button type="submit" disabled={submitting}>
            {submitting ? 'Signing in...' : 'Sign in'}
          </button>
        </form>
      </section>
    </div>
  )
}

export default LoginPage
