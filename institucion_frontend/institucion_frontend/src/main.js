import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import { createPinia } from 'pinia';
import Vue3Toastify from 'vue3-toastify';
import 'vue3-toastify/dist/index.css'; // Importa los estilos mínimos

const app = createApp(App);

app.use(createPinia());
app.use(router);

// Opciones personalizadas para los toast
const toastOptions = {
  autoClose: 3000,
  theme: 'light',
  toastStyle: {
    fontFamily: 'inherit',      // Usa la fuente principal del sitio
    fontSize: '14px',
    padding: '10px',
    borderRadius: '8px',
    boxShadow: '0 2px 10px rgba(0, 0, 0, 0.1)',
  }
};

app.use(Vue3Toastify, toastOptions);

app.mount('#app');
