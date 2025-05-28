<template>
  <div class="chat-popup-inner">
    <header>
      <h3>Newsie (Your AI News Assistant)</h3>
      <button @click="$emit('close')">✖</button>
    </header>

    <div class="chat-body">
      <div v-for="(m, i) in messages" :key="i" :class="['message', m.role]">
        <p>{{ m.text }}</p>
      </div>
    </div>

    <footer class="chat-input">
      <input v-model="userInput" @keydown.enter="sendMessage" placeholder="Ask something about the article..." />
      <button @click="sendMessage">Send</button>
    </footer>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { fetchChatbotResponse } from '@/api/chatbot'

const props = defineProps({ articleId: Number })
const userInput = ref('')
const messages = ref([{ role: 'bot', text: 'What can I help you with?' }])

async function sendMessage() {
  const input = userInput.value.trim()
  if (!input) return

  messages.value.push({ role: 'user', text: input })
  userInput.value = ''

  try {
    const response = await fetchChatbotResponse({
      article_id: props.articleId,
      question: input
    })
    messages.value.push({ role: 'bot', text: response })
  } catch (err) {
    console.error("❌ Chatbot error:", err)
    messages.value.push({ role: 'bot', text: "Sorry, something went wrong." })
  }
}
</script>

<style scoped>
.chat-popup-inner {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  background: white;
  border-radius: 12px;
  overflow: hidden;
  border: 2px solid #007bff;
}

header {
  background: #007bff;
  color: white;
  padding: 12px 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: bold;
  font-size: 16px;
}

header button {
  background: none;
  border: none;
  color: white;
  font-size: 20px;
  cursor: pointer;
  line-height: 1;
}

.chat-body {
  flex: 1;
  padding: 16px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.message {
  display: flex;
}

.message.user {
  justify-content: flex-end;
}

.message.user p {
  background: #e0f0ff;
  color: #000;
  padding: 10px 14px;
  border-radius: 16px 16px 0 16px;
  max-width: 75%;
}

.message.bot {
  justify-content: flex-start;
}

.message.bot p {
  background: #f1f1f1;
  color: #000;
  padding: 10px 14px;
  border-radius: 16px 16px 16px 0;
  max-width: 75%;
}

.chat-input {
  display: flex;
  gap: 8px;
  padding: 12px 16px;
  border-top: 1px solid #ccc;
}

.chat-input input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 8px;
}

.chat-input button {
  padding: 10px 14px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: bold;
}
</style>