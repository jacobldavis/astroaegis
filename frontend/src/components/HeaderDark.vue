<script setup>
import { ref, reactive } from 'vue'
import { useAccessibilityStore } from '../stores/accessibilityStore.js'

const accessibility = useAccessibilityStore()
accessibility.initLanguage()
const showAccessibilityMenu = ref(false)

const translations = reactive({
  en: { 
    accessibility: "Accessibility Menu", 
    backHome: "Back Home",
    colorblindMode: "Colorblind Mode"
  },
  es: { 
    accessibility: "Menú de Accesibilidad", 
    backHome: "Volver a Inicio",
    colorblindMode: "Modo Daltonismo"
  },
  fr: { 
    accessibility: "Menu Accessibilité", 
    backHome: "Retour à l’Accueil",
    colorblindMode: "Mode Daltonien",
  },
  ru: { 
    accessibility: "Меню доступности", 
    backHome: "Назад на главную",
    colorblindMode: "Режим для дальтоников"
  },
  zh: { 
    accessibility: "无障碍菜单", 
    backHome: "返回主页",
    colorblindMode: "色盲模式"
  },
  ar: { 
    accessibility: "قائمة الوصول", 
    backHome: "العودة إلى الصفحة الرئيسية",
    colorblindMode: "وضع عمى الألوان"
  }
})

const t = (key) => translations[accessibility.language][key] || key
</script>

<template>
  <header
    class="app-header fixed top-0 left-0 w-full flex items-center justify-between px-4 py-3 z-50 bg-white text-black shadow-md"
  >
    <router-link class="flex items-center space-x-2" to="/">
      <span class="text-lg font-bold">AstroAegis</span>
    </router-link>

    <div class="flex items-center space-x-4 relative">

      <router-link
        to="/"
        class="px-3 py-2 bg-black hover:bg-gray-800 text-white rounded transition"
      >
        {{ t('backHome') }}
      </router-link>

      <div class="relative">
        <button 
          @click="showAccessibilityMenu = !showAccessibilityMenu"
          class="p-2 rounded hover:bg-gray-200 transition"
          aria-label="Accessibility Menu"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none"
               viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M4 6h16M4 12h16M4 18h16"/>
          </svg>
        </button>

        <ul 
          v-if="showAccessibilityMenu"
          class="absolute right-0 mt-2 w-48 bg-white text-black rounded shadow-lg py-2 border border-gray-200"
        >
          <li class="px-4 py-2">
            <label class="block text-sm font-medium mb-1">{{ t('accessibility') }}</label>
            <select 
              v-model="accessibility.language"
              @change="accessibility.setLanguage(accessibility.language)"
              class="w-full border rounded p-1 text-black"
            >
              <option value="en">English</option>
              <option value="es">Español</option>
              <option value="fr">Français</option>
              <option value="ru">Русский</option>
              <option value="zh">中文</option>
              <option value="ar">العربية</option>
            </select>
          </li>

          <li class="px-4 py-2 flex items-center justify-between">
            <span class="text-sm font-medium">{{t('colorblindMode')}}</span>
            <input type="checkbox"
                   v-model="accessibility.colorblindMode"
                   class="ml-2 h-5 w-5 accent-blue-600 rounded"/>
          </li>
        </ul>
      </div>
    </div>
  </header>
</template>
