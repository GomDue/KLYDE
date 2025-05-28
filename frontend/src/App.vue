<script setup>
import { useRoute } from 'vue-router'
import { computed, ref, onMounted } from 'vue'
import TheHeader from '@/components/TheHeader.vue'
import TheFooter from '@/components/TheFooter.vue'
import ChatBotLauncher from '@/components/ChatBotLauncher.vue'
import LoadingSpinner from '@/components/LoadingSpinner.vue'

const route = useRoute()

const isLoading = ref(true)

onMounted(() => {
  // TOSS 스타일: 첫 진입 시만 부드럽게 로딩
  setTimeout(() => {
    isLoading.value = false
  }, 1500)
})
</script>

<template>
  <div v-if="isLoading" class="fullscreen-loader">
    <LoadingSpinner />
  </div>

  <div v-else>
    <TheHeader
      v-if="route.path !== '/' && route.path !== '/login' && route.path !== '/register'"
    />

    <main>
      <RouterView />
    </main>

    <TheFooter
      v-if="route.path !== '/' && route.path !== '/login' && route.path !== '/register'"
    />

    <ChatBotLauncher v-if="route.name === 'newsDetail'" />
  </div>
</template>

<style lang="scss">
main {
  max-width: 1280px;
  min-width: 360px;
  min-height: 100vh;
  margin: 0 auto;
  padding: 50px 15px;
}

html, body, #app {
  height: auto;
  overflow: visible;
}

.fullscreen-loader {
  position: fixed;
  inset: 0;
  z-index: 9999;
  background-color: white;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
