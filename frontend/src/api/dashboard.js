import axios from './axios'

export async function fetchDashboard() {
  const res = await axios.get('/dashboard')
  return res.data
}
