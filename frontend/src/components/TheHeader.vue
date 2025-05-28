<script setup>
import { RouterLink, useRoute, useRouter } from "vue-router";
import { computed } from "vue";

const route = useRoute();
const router = useRouter();

// 새로고침 로직
const refreshPage = (event) => {
  event.preventDefault();
  router.push("/").then(() => {
    window.location.reload();
  });
};

// 현재 경로가 일치하는지
const isActive = (path) => route.path === path;

// 로그인 여부
const isLoggedIn = computed(() => !!localStorage.getItem("access"));

// 로그아웃 함수
const handleLogout = () => {
  localStorage.removeItem("access");
  localStorage.removeItem("refresh");
  alert("You’re now logged out.");
  router.push("/login");
};
</script>

<template>
  <div class="header__container">
    <header>
      <router-link to="/news">
        <span class="logo"> 📰 KLYDE </span>
      </router-link>

      <nav class="menus">
        <router-link
          to="/news"
          :class="{ active: isActive('/news') }"
        >Personal News Curating</router-link>

        <router-link
          to="/dashboard"
          :class="{ active: isActive('/dashboard') }"
        >Dashboard</router-link>

        <router-link
          v-if="isLoggedIn"
          to="/settings"
          :class="{ active: isActive('/settings') }"
        >Settings</router-link>
        
        <button
          v-if="isLoggedIn"
          @click="handleLogout"
          class="logout"
        >Logout</button>

        <router-link v-else to="/login">Login</router-link>
      </nav>
    </header>
  </div>
</template>

<style scoped lang="scss">
.header__container {
  background-color: var(--color-primary-bg);
  border-bottom: 1px solid var(--color-border);

  header {
    max-width: 1280px;
    margin: 0 auto;
    height: 80px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 15px;
  }

  .logo {
    font-size: x-large;
    font-weight: 800;
    color: var(--color-primary);
  }

  .menus {
    display: flex;
    align-items: center;
    gap: 24px;
    margin-left: auto;

    a {
      color: var(--color-text);
      text-decoration: none;
      font-weight: 500;
      padding-bottom: 3px;
      border-bottom: 2px solid transparent;
      transition: all 0.2s ease;

      &.active {
        color: var(--color-primary);
        border-color: var(--color-primary);
        font-weight: 700;
      }

      &:hover {
        color: var(--color-primary);
      }
    }

    .logout {
      background: none;
      border: none;
      color: var(--color-text);
      cursor: pointer;
      font-weight: 600;

      &:hover {
        color: var(--color-primary);
      }
    }
  }
}
</style>
