import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'

const routes = [
  { path: '/',
    name: 'HomeView',
    component: HomeView
  },

  {
    path: '/loginView',
    name: 'LoginView',
    component: LoginView
   },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
