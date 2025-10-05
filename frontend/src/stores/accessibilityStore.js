import { defineStore } from 'pinia'

export const useAccessibilityStore = defineStore('accessibility', {
  state: () => ({
    language: 'en',
    colorblindMode: false,
  }),
  actions: {
    setLanguage(lang) {
      this.language = lang
      if (lang !== 'en') localStorage.setItem('language', lang)
      else localStorage.removeItem('language')
    },
    initLanguage() {
      const saved = localStorage.getItem('language')
      if (saved) this.language = saved
    },
    toggleColorblindMode() {
      this.colorblindMode = !this.colorblindMode
      localStorage.setItem('colorblindMode', this.colorblindMode)
    },
    initColorblindMode() {
      const mode = localStorage.getItem('colorblindMode')
      if (mode !== null) this.colorblindMode = mode === 'true'
    }
  },
  getters: {
    getLanguage: (state) => state.language
  }
})
