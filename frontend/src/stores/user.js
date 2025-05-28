import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    email: '',
  }),
  actions: {
    setEmail(email) {
      this.email = email
    }
  },
  persist: true
})
