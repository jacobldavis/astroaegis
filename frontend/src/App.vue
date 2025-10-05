<template>
  <component :is="currentHeader" />
  <div :class="{ 'colorblind-mode': accessibility.colorblindMode }">
    <router-view />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useAccessibilityStore } from './stores/accessibilityStore.js'
import Header from './components/Header.vue'
import HeaderDark from './components/HeaderDark.vue'

const accessibility = useAccessibilityStore()
const route = useRoute()

const currentHeader = computed(() => {
  return route.path === '/' ? Header : HeaderDark
})
</script>

<style>
</style>
