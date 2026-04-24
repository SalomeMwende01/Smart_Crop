function StatCard({ title, value, tone = 'default' }) {
  return (
    <article className={`stat-card stat-${tone}`}>
      <p>{title}</p>
      <h3>{value}</h3>
    </article>
  )
}

export default StatCard
