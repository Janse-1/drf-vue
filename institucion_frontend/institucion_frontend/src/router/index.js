import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import MainView from '@/views/MainView.vue'
import RegistroView from '@/views/RegistroView.vue'

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

   {
    path: '/MainView',
    name: 'MainView',
    component: MainView
   },

   {
    path: '/RegistroView',
    name: 'RegistroView',
    component: RegistroView
   },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
