import { useEffect, useMemo, useState } from 'react'

import api from '../api/client'
import {
  STAGE_OPTIONS,
  createField,
  fetchDashboard,
  fetchFields,
  updateField,
} from '../api/monitoring'
import StatCard from '../components/StatCard'
import StatusBadge from '../components/StatusBadge'

const EMPTY_FORM = {
  name: '',
  crop_type: '',
  planting_date: '',
  current_stage: 'PLANTED',
  assigned_agent_id: '',
}

function AdminDashboardPage() {
  const [dashboard, setDashboard] = useState(null)
  const [fields, setFields] = useState([])
  const [agents, setAgents] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [formData, setFormData] = useState(EMPTY_FORM)
  const [submitting, setSubmitting] = useState(false)

  const loadData = async () => {
    setLoading(true)
    setError('')

    try {
      const [dashboardData, fieldData, agentsData] = await Promise.all([
        fetchDashboard(),
        fetchFields(),
        api.get('/auth/agents/').then((response) => response.data),
      ])

      setDashboard(dashboardData)
      setFields(fieldData)
      setAgents(agentsData)
    } catch (requestError) {
      setError(requestError.response?.data?.detail || 'Unable to load dashboard data.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    loadData()
  }, [])

  const summary = useMemo(() => {
    if (!dashboard) {
      return {
        total: 0,
        active: 0,
        atRisk: 0,
        completed: 0,
      }
    }

    return {
      total: dashboard.total_fields,
      active: dashboard.status_breakdown.ACTIVE,
      atRisk: dashboard.status_breakdown.AT_RISK,
      completed: dashboard.status_breakdown.COMPLETED,
    }
  }, [dashboard])

  const onCreateField = async (event) => {
    event.preventDefault()
    setError('')
    setSubmitting(true)

    try {
      await createField({
        ...formData,
        assigned_agent_id: formData.assigned_agent_id || null,
      })

      setFormData(EMPTY_FORM)
      await loadData()
    } catch (requestError) {
      setError(requestError.response?.data?.detail || 'Unable to create field.')
    } finally {
      setSubmitting(false)
    }
  }

  const onStageChange = async (fieldId, stage) => {
    try {
      await updateField(fieldId, { current_stage: stage })
      await loadData()
    } catch {
      setError('Unable to update field stage.')
    }
  }

  if (loading) {
    return <section className="placeholder-panel">Loading dashboard...</section>
  }

  return (
    <section className="dashboard-stack">
      <div className="stats-grid">
        <StatCard title="Total Fields" value={summary.total} />
        <StatCard title="Active" value={summary.active} tone="active" />
        <StatCard title="At Risk" value={summary.atRisk} tone="risk" />
        <StatCard title="Completed" value={summary.completed} tone="done" />
      </div>

      <section className="content-card">
        <h2>Create Field</h2>
        <form className="field-form" onSubmit={onCreateField}>
          <input
            placeholder="Field name"
            value={formData.name}
            onChange={(event) => setFormData((prev) => ({ ...prev, name: event.target.value }))}
            required
          />
          <input
            placeholder="Crop type"
            value={formData.crop_type}
            onChange={(event) => setFormData((prev) => ({ ...prev, crop_type: event.target.value }))}
            required
          />
          <input
            type="date"
            value={formData.planting_date}
            onChange={(event) => setFormData((prev) => ({ ...prev, planting_date: event.target.value }))}
            required
          />

          <select
            value={formData.current_stage}
            onChange={(event) => setFormData((prev) => ({ ...prev, current_stage: event.target.value }))}
          >
            {STAGE_OPTIONS.map((stage) => (
              <option key={stage.value} value={stage.value}>
                {stage.label}
              </option>
            ))}
          </select>

          <select
            value={formData.assigned_agent_id}
            onChange={(event) => setFormData((prev) => ({ ...prev, assigned_agent_id: event.target.value }))}
          >
            <option value="">Assign later</option>
            {agents.map((agent) => (
              <option key={agent.id} value={agent.id}>
                {agent.username}
              </option>
            ))}
          </select>

          <button type="submit" disabled={submitting}>
            {submitting ? 'Saving...' : 'Create field'}
          </button>
        </form>
      </section>

      <section className="content-card">
        <div className="section-head">
          <h2>All Fields</h2>
          <p className="muted">Assign agents, monitor current stage, and track computed risk.</p>
        </div>

        {error ? <p className="form-error">{error}</p> : null}

        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Field</th>
                <th>Crop</th>
                <th>Planted</th>
                <th>Stage</th>
                <th>Status</th>
                <th>Agent</th>
              </tr>
            </thead>
            <tbody>
              {fields.map((field) => (
                <tr key={field.id}>
                  <td>{field.name}</td>
                  <td>{field.crop_type}</td>
                  <td>{field.planting_date}</td>
                  <td>
                    <select
                      value={field.current_stage}
                      onChange={(event) => onStageChange(field.id, event.target.value)}
                    >
                      {STAGE_OPTIONS.map((stage) => (
                        <option key={stage.value} value={stage.value}>
                          {stage.label}
                        </option>
                      ))}
                    </select>
                  </td>
                  <td>
                    <StatusBadge
                      statusCode={field.computed_status.code}
                      statusLabel={field.computed_status.label}
                    />
                  </td>
                  <td>{field.assigned_agent?.username || 'Unassigned'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </section>
  )
}

export default AdminDashboardPage
