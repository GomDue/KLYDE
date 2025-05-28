<template>
  <div class="container">
    <h1 class="logo">📰 KLYDE</h1>
    <p class="subtitle">Personalized AI News Curation</p>

    <div class="card">
      <h2>SIGN UP <span class="emoji clap">👏</span></h2>
      <p class="desc">Welcome to KLYDE Service</p>

      <form @submit.prevent="handleSubmit">
        <input v-model="form.email" type="email" placeholder="Email" required />
        <input v-model="form.password1" type="password" placeholder="Password" required />
        <input v-model="form.password2" type="password" placeholder="Confirm Password" required />
        <button type="submit">SIGN UP</button>
      </form>

      <p class="login-text">
        Already have an account?
        <router-link to="/login">LOG IN</router-link>
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
import axios from '@/api/axios';

const router = useRouter()
const form = reactive({
  email: '',
  password1: '',
  password2: ''
})

async function handleSubmit() {
  try {
    if (!validatePassword(form.password1)) {
      alert('Your password must be at least 8 characters long and include at least one letter, one number, and one special character.')
      return
    }

    if (form.password1 !== form.password2) {
      alert('Passwords do not match.')
      return
    }

    await axios.post('/auth/registration/', {
      email: form.email,
      password1: form.password1,
      password2: form.password2,
    });

    alert('Welcome! Your account has been created. Please log in to continue.');
    router.push('/login');
  } catch (err) {
    console.error('❌ Signup error:', err.response?.data || err.message);
    alert('Signup failed: ' + JSON.stringify(err.response?.data));
  }
}

function validatePassword(password) {
  const lengthOk = password.length >= 8
  const hasNumber = /[0-9]/.test(password)
  const hasLetter = /[a-zA-Z]/.test(password)
  const hasSpecial = /[!@#$%^&*(),.?":{}|<>]/.test(password)
  return lengthOk && hasNumber && hasLetter && hasSpecial
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
  text-align: center;
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
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 6px;
}

.emoji {
  font-size: 1.2rem;
}

.clap {
  display: inline-block;
  animation: clap-motion 0.6s ease-in-out infinite;
  transform-origin: center;
}

@keyframes clap-motion {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.25);
  }
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
