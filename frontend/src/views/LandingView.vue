<script setup>
import { ref, onMounted } from "vue";

const show = ref(false);

onMounted(() => {
  setTimeout(() => {
    show.value = true;
  }, 100);
});
</script>

<template>
  <div class="landing-container">
    <transition name="fade-slide" appear>
      <div class="logo-section" v-if="show">
        <h1 class="logo-title">
          <span class="logo-icon">📰</span>
          <span class="typing">KLYDE&nbsp;</span>
        </h1>
        <p class="logo-subtitle">
          KLYDE curates the news that matters — clear, personal, and effortless.<br />
          Stay in flow with real-time updates, smart recommendations, and conversational insights.
        </p>
      </div>
    </transition>

    <transition name="fade-slide" appear>
      <div class="auth-links" v-if="show">
        <RouterLink to="/login">LOG IN</RouterLink>
        <RouterLink to="/register">SIGN UP</RouterLink>
      </div>
    </transition>
  </div>
</template>

<style scoped>
.landing-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  min-height: 100vh;
  padding-top: 450px;
  background-color: var(--color-bg);
}

/* 로고 */
.logo-section {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 24px;
  flex-direction: column;
  text-align: center;
}

.logo-icon {
  font-size: 56px;
  line-height: 1;
  align-self: center;
}

.logo-title {
  display: inline-flex;
  align-items: center;
  gap: 12px;
  font-size: 48px;
  font-weight: 800;
  font-family: "Pretendard", sans-serif;
  color: var(--color-primary);
  margin: 0 auto;
  line-height: 1;
}

/* 서브타이틀 */
.logo-subtitle {
  font-size: 16px;
  font-weight: 400;
  color: var(--color-text-sub);
  font-family: "Pretendard", sans-serif;
  margin: 10px 0 10px;
  text-align: center;
  max-width: 700px;
  line-height: 1.5;
}

/* 타이핑 효과 핵심 */
.typing {
  display: inline-block;
  overflow: hidden;
  white-space: nowrap;
  border-right: 3px solid var(--color-primary);
  width: 0;
  animation:
    typing 2s steps(10, end) forwards,
    blink 0.8s step-end infinite;
}

@keyframes typing {
  from {
    width: 0;
  }
  to {
    width: 5ch;
  }
}

@keyframes blink {
  50% {
    border-color: transparent;
  }
}

/* 로그인 / 회원가입 */
.auth-links {
  display: flex;
  gap: 40px;
}

.auth-links a {
  text-decoration: none;
  color: var(--color-text);
  font-size: 20px;
  font-weight: 600;
  transition: color 0.2s ease, text-decoration 0.2s ease;
}

.auth-links a:hover {
  color: var(--color-primary);
  text-decoration: underline;
}

/* 슬라이드 애니메이션 */
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: opacity 0.8s ease, transform 0.8s ease;
}

.fade-slide-enter-from {
  opacity: 0;
  transform: translateY(30px);
}

.fade-slide-enter-to {
  opacity: 1;
  transform: translateY(0);
}
</style>
