import { api } from './client'

export const dashboardApi = {
  summary: () => api.get('/dashboard/summary'),
  lessonStats: () => api.get('/dashboard/lesson-stats'),
}

export const studentApi = {
  list: () => api.get('/students'),
  create: (payload) => api.post('/students', payload),
}

export const coachApi = {
  list: () => api.get('/coaches'),
  create: (payload) => api.post('/coaches', payload),
  setActive: (id, active) => api.patch(`/coaches/${id}/active?active=${active}`, {}),
}

export const appointmentApi = {
  list: () => api.get('/appointments'),
  create: (payload) => api.post('/appointments', payload),
  cancel: (id, reason) => api.post(`/appointments/${id}/cancel`, { reason }),
}

export const reminderApi = {
  list: () => api.get('/reminders'),
  listUpcoming: (hoursAhead = 24) => api.get(`/reminders/upcoming?hours_ahead=${hoursAhead}`),
  get: (id) => api.get(`/reminders/${id}`),
  send: (id) => api.post(`/reminders/${id}/send`),
  read: (id) => api.post(`/reminders/${id}/read`),
}
