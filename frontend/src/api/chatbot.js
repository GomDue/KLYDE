// src/api/chatbot.js
import axios from './axios'

export async function fetchChatbotResponse({ article_id, question }) {
  const res = await axios.post('/chatbot/', {
    article_id,
    question
  })
  return res.data.response
}
