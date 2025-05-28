// src/api/user.js
import axios from './axios'

// 비밀번호 변경
export async function changePassword(currentPassword, newPassword) {
  return await axios.post('/change-password/', {
    current_password: currentPassword,
    new_password: newPassword,
  })
}

// 계정 삭제
export async function deleteAccount() {
  return await axios.delete('/delete-account/')
}
