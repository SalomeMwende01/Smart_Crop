import { Link, Outlet } from 'react-router-dom'

import useAuth from '../context/useAuth'

function AppShell() {
  const { user, logout } = useAuth()

  return (
    <div className="app-shell">
      <header className="topbar">
        <div>
          <p className="eyebrow">FieldPulse Monitoring</p>
          <h1>{user?.role === 'ADMIN' ? 'Coordinator Console' : 'Field Agent Desk'}</h1>
        </div>

        <nav className="topbar-nav">
          {user?.role === 'ADMIN' ? <Link to="/admin">Dashboard</Link> : <Link to="/agent">Dashboard</Link>}
          <button className="ghost-btn" onClick={logout} type="button">
            Logout
          </button>
        </nav>
      </header>

      <main>
        <Outlet />
      </main>
    </div>
  )
}

export default AppShell
