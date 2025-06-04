import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import MainView from '@/views/MainView.vue'
import RegistroView from '@/views/RegistroView.vue'
import ContactoView from '@/views/info-institucion/ContactoView.vue'
import QuienesSomosView from '@/views/info-institucion/QuienesSomosView.vue'
import MisionVisionView from '@/views/info-institucion/MvView.vue'

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

   {
    path: '/ContactoView',
    name: 'ContactoView',
    component: ContactoView
   },

   {
    path: '/QuienesSomosView',
    name: 'QuienesSomosView',
    component: QuienesSomosView
   },

   {
    path: '/MvView',
    name: 'MvView',
    component: MisionVisionView
   },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
