import api from './client'

export const STAGE_OPTIONS = [
  { value: 'PLANTED', label: 'Planted' },
  { value: 'GROWING', label: 'Growing' },
  { value: 'READY', label: 'Ready' },
  { value: 'HARVESTED', label: 'Harvested' },
]

export async function fetchDashboard() {
  const { data } = await api.get('/monitoring/dashboard/')
  return data
}

export async function fetchFields() {
  const { data } = await api.get('/monitoring/fields/')
  return data
}

export async function createField(payload) {
  const { data } = await api.post('/monitoring/fields/', payload)
  return data
}

export async function updateField(fieldId, payload) {
  const { data } = await api.patch(`/monitoring/fields/${fieldId}/`, payload)
  return data
}

export async function fetchFieldUpdates(fieldId) {
  const { data } = await api.get(`/monitoring/fields/${fieldId}/updates/`)
  return data
}

export async function createFieldUpdate(fieldId, payload) {
  const { data } = await api.post(`/monitoring/fields/${fieldId}/updates/`, payload)
  return data
}
