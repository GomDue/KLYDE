<template>
  <div class="container">
    <h1 class="logo">📰 KLYDE</h1>
    <p class="subtitle">Personalized AI News Curation</p>

    <div class="card">
      <h2>
        Welcome Back <span class="wave">👋</span>
      </h2>
      <p class="desc">Log in to access your curated news feed</p>

      <form @submit.prevent="handleLogin">
        <input
          v-model="form.email"
          type="email"
          placeholder="Email"
          required
        />
        <input
          v-model="form.password"
          type="password"
          placeholder="Password"
          required
        />

        <button type="submit">LOG IN</button>
      </form>

      <p class="login-text">
        Don’t have an account yet?
        <router-link to="/register">SIGN UP</router-link>
      </p>
    </div>

    <footer>
      <p><span>Terms of Service</span> · <span>Privacy Policy</span></p>
      <p>© 2025 NEWSMATE. All rights reserved.</p>
    </footer>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import { useRouter } from 'vue-router'
import { login } from '@/api/auth'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

const form = reactive({
  email: '',
  password: '',
})

async function handleLogin() {
  try {
    if (!validatePassword(form.password)) {
      alert('Your password must be at least 8 characters long and include at least one letter, one number, and one special character.')
      return
    }

    const response = await login({
      email: form.email,
      password: form.password
    })

    userStore.setEmail(response.email)
    console.log('📌 저장된 이메일:', userStore.email)

    alert('Successfully logged in!')
    router.push('/news')

  } catch (err) {
    console.error('Login error:', err)
    const msg = err.response?.data?.detail || 'Login failed'
    alert(msg)
  }
}

function validatePassword(password) {
  return (
    password.length >= 8 &&
    /[0-9]/.test(password) &&
    /[a-zA-Z]/.test(password) &&
    /[!@#$%^&*(),.?":{}|<>]/.test(password)
  )
}
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  min-height: 100vh;
  padding: 250px 20px 40px;
  background-color: var(--color-bg);
  font-family: 'Pretendard', sans-serif;
}

.logo {
  font-size: 2rem;
  font-weight: 800;
  color: var(--color-primary);
  margin-bottom: 10px;
}

.subtitle {
  margin-bottom: 30px;
  color: var(--color-text-sub);
  font-size: 0.95rem;
}

.wave {
  display: inline-block;
  animation: wave 2s infinite;
  transform-origin: 70% 70%;
}

@keyframes wave {
  0% { transform: rotate(0deg); }
  10% { transform: rotate(14deg); }
  20% { transform: rotate(-8deg); }
  30% { transform: rotate(14deg); }
  40% { transform: rotate(-4deg); }
  50% { transform: rotate(10deg); }
  60% { transform: rotate(0deg); }
  100% { transform: rotate(0deg); }
}

.card {
  background-color: var(--color-surface);
  padding: 40px 30px;
  max-width: 420px;
  border-radius: 16px;
  box-shadow: 0 6px 24px rgba(0, 0, 0, 0.05);
  width: 100%;
  text-align: center;
}

.card h2 {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-text);
  margin-bottom: 8px;
  justify-content: center;
  align-items: center;
}

.card .desc {
  color: var(--color-text-sub);
  font-size: 0.95rem;
  margin-bottom: 24px;
}

input {
  width: 100%;
  padding: 14px 16px;
  margin-bottom: 16px;
  border: 1px solid var(--color-border);
  border-radius: 8px;
  font-size: 1rem;
  background-color: white;
  transition: border 0.2s;
}

input:focus {
  border-color: var(--color-primary);
  outline: none;
  box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2);
}

button {
  width: 100%;
  background-color: var(--color-primary);
  color: white;
  padding: 14px;
  font-weight: 600;
  font-size: 1rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.25s ease;
  text-align: center;
}

button:hover {
  background-color: #4f52d3;
}

.login-text {
  margin-top: 18px;
  font-size: 0.9rem;
  color: var(--color-text-sub);
}

.login-text a {
  font-weight: 600;
  color: var(--color-primary);
  text-decoration: none;
}

.login-text a:hover {
  text-decoration: underline;
}

footer {
  margin-top: 20px;
  padding: 20px 0;
  text-align: center;
  font-size: 0.8rem;
  color: var(--color-text-sub);
}

footer span {
  color: var(--color-text-sub);
  text-decoration: none;
  margin: 0 8px;
  cursor: pointer;
  transition: color 0.2s ease;
}

footer span:hover {
  color: var(--color-primary);
}

footer p {
  margin-top: 8px;
}
</style>
