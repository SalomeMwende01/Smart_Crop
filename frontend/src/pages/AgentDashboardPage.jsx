import { useEffect, useState } from 'react'

import {
  STAGE_OPTIONS,
  createFieldUpdate,
  fetchDashboard,
  fetchFieldUpdates,
  fetchFields,
} from '../api/monitoring'
import StatCard from '../components/StatCard'
import StatusBadge from '../components/StatusBadge'

function AgentDashboardPage() {
  const [dashboard, setDashboard] = useState(null)
  const [fields, setFields] = useState([])
  const [fieldUpdates, setFieldUpdates] = useState({})
  const [formState, setFormState] = useState({})
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const loadData = async () => {
    setLoading(true)
    setError('')

    try {
      const [dashboardData, fieldData] = await Promise.all([fetchDashboard(), fetchFields()])
      setDashboard(dashboardData)
      setFields(fieldData)

      const initialForm = {}
      fieldData.forEach((field) => {
        initialForm[field.id] = {
          stage: field.current_stage,
          note: '',
          submitting: false,
          success: '',
        }
      })
      setFormState(initialForm)
    } catch {
      setError('Unable to load your assigned fields.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    loadData()
  }, [])

  const loadUpdates = async (fieldId) => {
    try {
      const updates = await fetchFieldUpdates(fieldId)
      setFieldUpdates((prev) => ({ ...prev, [fieldId]: updates }))
    } catch {
      setError('Unable to load field updates.')
    }
  }

  const setFieldForm = (fieldId, changes) => {
    setFormState((prev) => ({
      ...prev,
      [fieldId]: {
        ...prev[fieldId],
        ...changes,
      },
    }))
  }

  const submitUpdate = async (event, fieldId) => {
    event.preventDefault()
    const fieldForm = formState[fieldId]

    setFieldForm(fieldId, { submitting: true, success: '' })
    setError('')

    try {
      await createFieldUpdate(fieldId, {
        stage: fieldForm.stage,
        note: fieldForm.note,
      })

      setFieldForm(fieldId, { note: '', submitting: false, success: 'Update submitted.' })
      await Promise.all([loadData(), loadUpdates(fieldId)])
    } catch {
      setFieldForm(fieldId, { submitting: false })
      setError('Could not submit update. Please retry.')
    }
  }

  if (loading) {
    return <section className="placeholder-panel">Loading assigned fields...</section>
  }

  return (
    <section className="dashboard-stack">
      <div className="stats-grid">
        <StatCard title="Assigned Fields" value={dashboard?.total_fields ?? 0} />
        <StatCard title="Active" value={dashboard?.status_breakdown?.ACTIVE ?? 0} tone="active" />
        <StatCard title="At Risk" value={dashboard?.status_breakdown?.AT_RISK ?? 0} tone="risk" />
        <StatCard title="Completed" value={dashboard?.status_breakdown?.COMPLETED ?? 0} tone="done" />
      </div>

      {error ? <p className="form-error">{error}</p> : null}

      <section className="field-grid">
        {fields.map((field) => {
          const currentForm = formState[field.id] || {
            stage: field.current_stage,
            note: '',
            submitting: false,
            success: '',
          }
          const updates = fieldUpdates[field.id] || []

          return (
            <article className="content-card" key={field.id}>
              <div className="section-head">
                <h2>{field.name}</h2>
                <StatusBadge
                  statusCode={field.computed_status.code}
                  statusLabel={field.computed_status.label}
                />
              </div>

              <p className="muted">
                {field.crop_type} · Planted on {field.planting_date}
              </p>

              <form className="field-form" onSubmit={(event) => submitUpdate(event, field.id)}>
                <select
                  value={currentForm.stage}
                  onChange={(event) => setFieldForm(field.id, { stage: event.target.value })}
                >
                  {STAGE_OPTIONS.map((stage) => (
                    <option key={stage.value} value={stage.value}>
                      {stage.label}
                    </option>
                  ))}
                </select>

                <textarea
                  placeholder="Observation or note"
                  value={currentForm.note}
                  onChange={(event) => setFieldForm(field.id, { note: event.target.value })}
                  rows={3}
                />

                <button type="submit" disabled={currentForm.submitting}>
                  {currentForm.submitting ? 'Sending...' : 'Submit update'}
                </button>
                {currentForm.success ? <p className="success-text">{currentForm.success}</p> : null}
              </form>

              <button className="ghost-btn" type="button" onClick={() => loadUpdates(field.id)}>
                Refresh updates
              </button>

              {updates.length > 0 ? (
                <ul className="updates-list">
                  {updates.slice(0, 4).map((update) => (
                    <li key={update.id}>
                      <strong>{update.stage}</strong>
                      <span>{update.note || 'No note added.'}</span>
                    </li>
                  ))}
                </ul>
              ) : (
                <p className="muted">No updates loaded yet.</p>
              )}
            </article>
          )
        })}
      </section>
    </section>
  )
}

export default AgentDashboardPage
