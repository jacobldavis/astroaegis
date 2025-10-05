import { createRouter, createWebHistory } from 'vue-router'

import Home from '../pages/Home.vue'
import Info from '../pages/Info.vue'
import Visualization from '../pages/Visualization.vue'

const routes = [
  {path: '/', name: 'Home', component: Home },
  {path: '/Info', name: 'Info', component: Info},
  {path: '/visualization', name: 'Visualization', component: Visualization}
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
