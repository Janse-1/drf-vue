<template>
  <header class="header-public">
    <div class="header-container">
      <div class="logo-section" @click="$router.push('/')" style="cursor: pointer;">
        <img src="../assets/images/logo.png" alt="Logo IEI" class="logo" />
        <span class="nombre-sistema">Institución Educativa Indigena N1 </span>
      </div>

      <nav class="navbar">
        <a v-if="!isHomeView" href="/" title="Inicio">  
          <i class="fa-solid fa-house"></i> Inicio
        </a>
        <div class="dropdown" @mouseenter="mostrarDropdown = true" @mouseleave="mostrarDropdown = false">
          <a href="/QuienesSomosView" title="¿Quiénes somos?" class="dropdown-toggle">
            <i class="fa-solid fa-users"></i> Quiénes somos <i class="fa-solid fa-caret-down"></i>
          </a>
          <div v-if="mostrarDropdown" class="dropdown-menu">
            <a href="MvView" class="dropdown-item">Misión y Visión</a>
            <a href="SimbolosView" class="dropdown-item">Símbolos</a>
          </div>
        </div>
        <!-- <a href="#" title="Noticias">
          <i class="fa-solid fa-newspaper"></i> Noticias
        </a> -->
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
import { ref } from 'vue'
import { useRoute } from 'vue-router'
const route = useRoute()

const mostrarDropdown = ref(false)

// Ocultar La seccion si ya estás en la vista 
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
  /* Imagen de fondo con superposición de color institucional */
  background-image:
    linear-gradient(rgba(215,38,56,0.92), rgba(215,38,56,0.92)),
    url('../assets/images/fondo-header.png');
  background-size: 100% 100%; /* Ajusta la imagen para que ocupe todo el ancho y alto del header */
  background-position: center;
  background-repeat: no-repeat;
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

.dropdown {
  position: relative;
  display: inline-block;
}
.dropdown-toggle {
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
}
.dropdown-menu {
  position: absolute;
  top: 110%;
  left: 0;
  background: #D72638;;
  color: #ffff;
  min-width: 180px;
  border-radius: 8px;
  box-shadow: 0 4px 16px rgba(27,27,30,0.12);
  z-index: 100;
  display: flex;
  flex-direction: column;
  padding: 0.5rem 0;
}
.dropdown-item {
  color: #D72638;
  padding: 0.7rem 1.2rem;
  text-decoration: none;
  font-weight: 500;
  transition: background 0.2s, color 0.2s;
  border: none;
  background: none;
  text-align: left;
  cursor: pointer;
}
.dropdown-item:hover {
  background: #FFBA08;
  color: #fff;
}
</style>
