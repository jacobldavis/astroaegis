<script setup>
import { ref, onMounted, onBeforeUnmount, reactive } from 'vue'
import { useAccessibilityStore } from '../stores/accessibilityStore.js'
import { rule } from 'postcss'

const accessibility = useAccessibilityStore()
accessibility.initLanguage()
const showAccessibilityMenu = ref(false)

const translations = reactive({
  en: { accessibility: "Accessibility Menu", learnMore: "Learn More", colorblindMode: "Colorblind Mode"},
  es: { accessibility: "Menú de Accesibilidad", learnMore: "Aprende Más", colorblindMode: "Modo Daltonismo"},
  fr: { accessibility: "Menu Accessibilité", learnMore: "En Savoir Plus", colorblindMode: "Mode Daltonien",},
  ru: { accessibility: "Меню доступности", learnMore: "Узнать больше", colorblindMode: "Режим для дальтоников"},
  zh: { accessibility: "无障碍菜单", learnMore: "了解更多", colorblindMode: "色盲模式"},
  ar: { accessibility: "قائمة الوصول", learnMore: "معرفة المزيد", colorblindMode: "وضع عمى الألوان"}
})

const t = (key) => translations[accessibility.language][key] || key

const headerOpaque = ref(false)
const heroSection = ref(null)

onMounted(() => {
  const observer = new IntersectionObserver(
    ([entry]) => {
      headerOpaque.value = !entry.isIntersecting
    },
    { threshold: 0.1 }
  )
  if (heroSection.value) observer.observe(heroSection.value)
})
</script>

<template>
  <section ref="heroSection" class="absolute top-0 left-0 w-full h-[80vh] pointer-events-none"></section>

  <header
  class="app-header fixed top-0 left-0 w-full flex items-center justify-between px-4 py-2 z-50 transition-colors duration-300 shadow-md"
  :style="{
    backgroundColor: accessibility.colorblindMode ? 'white' : (headerOpaque ? 'black' : 'transparent'),
    color: accessibility.colorblindMode ? 'black' : 'white'
  }"
>
  <router-link
    class="flex items-center space-x-2 font-bold"
    :style="{ color: accessibility.colorblindMode ? 'black' : 'white' }"
    to="/"
  >
    <span class="text-lg">AstroAegis</span>
  </router-link>

  <div class="flex items-center space-x-4 relative">
    <router-link
      to="/info"
      class="px-3 py-2 rounded transition"
      :class="{
        'bg-white text-black hover:bg-black hover:text-white': !accessibility.colorblindMode,
        'bg-black text-white hover:bg-gray-800 hover:text-white': accessibility.colorblindMode
      }"
    >
      {{ t('learnMore') }}
    </router-link>

    <div class="relative">
      <button
        @click="showAccessibilityMenu = !showAccessibilityMenu"
        class="p-2 rounded transition"
        :style="{ color: accessibility.colorblindMode ? 'black' : 'white' }"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none"
             viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M4 6h16M4 12h16M4 18h16"/>
        </svg>
      </button>

      <ul v-if="showAccessibilityMenu"
          class="absolute right-0 mt-2 w-48 bg-white text-black rounded shadow-lg py-1">
        <li class="px-4 py-2">
          <label class="block text-sm font-medium mb-1">{{ t('accessibility') }}</label>
          <select v-model="accessibility.language"
                  @change="accessibility.setLanguage(accessibility.language)"
                  class="w-full border rounded p-1 text-black">
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
