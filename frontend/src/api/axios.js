import axios from 'axios'

const instance = axios.create({
  baseURL: 'http://localhost:8000',  // 실제 배포 시 백엔드 주소로 변경
  headers: {
    'Content-Type': 'application/json',
  },
})

instance.interceptors.request.use(config => {
  const token = localStorage.getItem('access')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export default instance
