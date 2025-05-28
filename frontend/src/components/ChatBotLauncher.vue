<template>
  <div>
    <button class="chatbot-button" @click="toggleChat"></button>
    <div v-if="showChat" class="chat-popup">
      <ChatBotPopup :article-id="articleId" @close="toggleChat" />
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue"
import { useRoute } from "vue-router"
import ChatBotPopup from "./ChatBotPopup.vue"

const showChat = ref(false)
const toggleChat = () => (showChat.value = !showChat.value)

const route = useRoute()
const articleId = parseInt(route.params.id)
</script>

<style scoped>
.floating-button {
  position: fixed;
  bottom: 30px;
  right: 30px;
  background-color: #1d72b8;
  color: white;
  font-size: 24px;
  border: none;
  border-radius: 50%;
  width: 60px;
  height: 60px;
  cursor: pointer;
  z-index: 9999;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.chat-popup {
  position: fixed;
  bottom: 100px;
  right: 30px;
  width: 500px;
  height: 700px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25);
  overflow: hidden;
  z-index: 99999;
}

.chatbot-button {
  position: fixed;
  bottom: 30px;
  right: 30px;
  width: 64px;
  height: 64px;
  border: 2px solid #007aff;
  border-radius: 50%;
  background-image: url("@/assets/chatbot-avatar.png");
  background-size: 120%;
  background-position: center;
  background-repeat: no-repeat;
  box-shadow: 0 4px 16px rgba(29, 114, 184, 0.25);
  cursor: pointer;
  z-index: 99999;
  transition: all 0.2s ease;
}

.chatbot-button:hover {
  transform: scale(1.1);
  box-shadow: 0 6px 20px rgba(29, 114, 184, 0.35);
}
</style>
