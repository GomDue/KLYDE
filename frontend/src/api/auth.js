import axios from './axios'

// 회원가입
export async function register({ username, email, password1, password2 }) {
  const res = await axios.post('/auth/registration/', {
    username,
    email,
    password1,
    password2
  })

  const access = res.data.access
  const refresh = res.data.refresh

  // 로컬 스토리지 저장
  localStorage.setItem('access', access)
  localStorage.setItem('refresh', refresh)

  // axios 기본 헤더 설정
  axios.defaults.headers.common['Authorization'] = `Bearer ${access}`

  return res.data.user
}

export async function login({ email, password }) {
  // ✅ 기존 access / refresh 토큰 제거
  localStorage.removeItem('access')
  localStorage.removeItem('refresh')
  delete axios.defaults.headers.common['Authorization']

  // 로그인 요청 (Authorization 헤더 제거 상태에서 요청)
  const res = await axios.post(
    '/users/login/',
    { email, password },
    {
      headers: {
        Authorization: ''  // interceptor 방어용
      }
    }
  )

  const access = res.data.access
  const refresh = res.data.refresh

  // ✅ 로그인 성공 후 토큰 저장
  localStorage.setItem('access', access)
  localStorage.setItem('refresh', refresh)

  // ✅ 이후 요청을 위한 기본 헤더 설정
  axios.defaults.headers.common['Authorization'] = `Bearer ${access}`

  return {
    id: res.data.user_id,
    email: res.data.email
  }
}

// 로그아웃
export function logout() {
  localStorage.removeItem('access')
  localStorage.removeItem('refresh')

  // axios 헤더 제거
  delete axios.defaults.headers.common['Authorization']
}
