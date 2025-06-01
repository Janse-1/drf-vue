<template>
  <header class="header-public">
    <div class="header-container">
      <div class="logo-section">
        <img src="../assets/images/logo.png" alt="Logo IEI" class="logo" />
        <span class="nombre-sistema">Gestión de notas IEN1 Indigena</span>
      </div>

      <nav class="navbar">
        <a v-if="!isHomeView" href="/" title="Inicio">
          <i class="fa-solid fa-house"></i> Inicio
        </a>
        <a  href="#" title="¿Quiénes somos?">
          <i class="fa-solid fa-users"></i> Quiénes somos
        </a>
        <a  href="#" title="Noticias">
          <i class="fa-solid fa-newspaper"></i> Noticias
        </a>
        <a v-if="!isContactoView" href="ContactoView" title="Contacto">
          <i class="fa-solid fa-envelope"></i> Contacto
        </a>
        <a v-if="!isLoginView" href="/LoginView" title="Iniciar sesión">
          <i class="fa-solid fa-right-to-bracket"></i> Iniciar sesión
        </a>
      </nav>
    </div>
  </header>
</template>

<script setup>
import { useRoute } from 'vue-router'
const route = useRoute()

// Ocultar "Iniciar sesión" si ya estás en la vista Login
const isLoginView = route.path === '/LoginView'
const isHomeView = route.path === '/HomeView'
const isQuienesSomos = route.path === '/QuienesSomosView'
const isNoticiasView = route.path === '/NoticiasView'
const isContactoView = route.path === '/ContactoView'
</script>

<style scoped>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');

.header-public {
  background-color: #D72638;
  color: white;
  padding: 1rem 2rem;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.header-container {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
}

.logo-section {
  display: flex;
  align-items: center;
}

.logo {
  width: 50px;
  margin-right: 10px;
}

.nombre-sistema {
  font-size: 1.3rem;
  font-weight: bold;
  white-space: nowrap;
}

.navbar {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.navbar a {
  color: white;
  text-decoration: none;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 5px 10px;
  transition: 0.2s ease;
}

.navbar a:hover {
  background-color: #c31f2d;
  border-radius: 5px;
}
</style>
