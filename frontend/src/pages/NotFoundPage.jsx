import { Link } from 'react-router-dom'

function NotFoundPage() {
  return (
    <section className="placeholder-panel">
      <h2>Page not found</h2>
      <p>The page you requested does not exist.</p>
      <Link to="/">Back to dashboard</Link>
    </section>
  )
}

export default NotFoundPage
