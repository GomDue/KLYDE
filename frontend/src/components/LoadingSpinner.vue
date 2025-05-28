<!-- src/components/LoadingSpinner.vue -->
<template>
  <div class="spinner">
    <div class="dot" />
    <div class="dot" />
    <div class="dot" />
  </div>
</template>

<style scoped>
.spinner {
  display: flex;
  gap: 10px;
}

.dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background-color: #6366F1;
  animation: bounce 0.6s infinite alternate;
}

.dot:nth-child(2) {
  animation-delay: 0.2s;
}
.dot:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes bounce {
  to {
    transform: translateY(-10px);
    opacity: 0.5;
  }
}
</style>
