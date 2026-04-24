function StatusBadge({ statusCode, statusLabel }) {
  const className = `status-badge status-${(statusCode || '').toLowerCase()}`
  return <span className={className}>{statusLabel || statusCode}</span>
}

export default StatusBadge
