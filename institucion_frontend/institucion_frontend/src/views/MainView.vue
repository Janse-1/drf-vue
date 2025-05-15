<template>
  <div class="main-view">
    <header class="encabezado">
      <img src="../assets/images/logo.png" class="logo" />
      <div>
        <h2>Bienvenido, {{ user.first_name }} {{ user.last_name }}!</h2>
        <p class="rol">{{ user.tipo_usr }}</p>
      </div>
       <button class="logout-button" @click="cerrarSesion">Cerrar sesión</button>
    </header>

    <section class="contenido-principal">
      <aside class="menu-lateral" v-if="user">
        <!-- Estudiante y Padre -->
        <template v-if="user.tipo_usr === 'estudiante' || user.tipo_usr === 'padre'">
          <a href="#">Mi perfil</a>
          <a href="#">Mis notas</a>
          <a href="#">Descargar boletín</a>
        </template>

        <!-- Docente -->
        <template v-else-if="user.tipo_usr === 'docente'">
          <a href="#">Mi perfil</a>
          <a href="#">Mis notas</a>
          <a href="#">Subir notas</a>
          <a href="#">Estudiantes</a>
          <a href="#">Mis cursos</a>
        </template>

        <!-- Coordinador o Admin -->
        <template v-else-if="user.tipo_usr === 'coordinador' || user.tipo_usr === 'admin'">
          <a href="#">Mi perfil</a>
          <a href="#">Subir notas</a>
          <a href="#">Ver estudiantes</a>
          <a href="#">Registrar estudiantes</a>
          <a href="#">Registrar docentes</a>
          <a href="#">Gestión de sedes</a>
          <a href="#">Ver cursos</a>
        </template>
      </aside>

      <main class="seccion-dinamica">
        <!-- Aquí iría el contenido según la opción seleccionada -->
        <p>Selecciona una opción del menú para comenzar.</p>
      </main>
    </section>

    <FooterComponent />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import FooterComponent from '@/components/FooterComponent.vue'

const user = ref({
  username: '',
  first_name: '',
  last_name: '',
  email: '',
  tipo_usr: '',
})
const router = useRouter()


const cerrarSesion = () => {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  localStorage.removeItem('first_name')
  localStorage.removeItem('last_name')
  localStorage.removeItem('tipo_usr')
  router.push('/LoginView')
}


onMounted(async () => {
  const token = localStorage.getItem('access_token')

  if (!token) {
    router.push('/LoginView')
    return
  }

  try {
    const response = await fetch('http://localhost:8000/auth/users/me/', {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    })

    if (!response.ok) throw new Error('No autorizado')

    const data = await response.json()
    user.value = {
      username: data.username,
      first_name: data.first_name,
      last_name: data.last_name,
      email: data.email,
      tipo_usr: data.tipo_usr,
    }
  } catch (error) {
    console.error('Error al obtener datos del usuario:', error)
    cerrarSesion()
  }
})
</script>

<style scoped>
.main-view {
  font-family: 'Segoe UI', sans-serif;
  background-color: #fff8f0;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.encabezado {
  display: flex;
  align-items: center;
  background-color: #D72638;
  color: white;
  padding: 1rem 2rem;
}

.logo {
  width: 60px;
  margin-right: 1rem;
}

.rol {
  font-size: 0.9rem;
  font-style: italic;
}

.contenido-principal {
  display: flex;
  flex: 1;
  padding: 1rem;
}

.menu-lateral {
  width: 250px;
  padding: 1rem;
  background-color: #fff;
  border-right: 2px solid #ddd;
  display: flex;
  flex-direction: column;
}

.menu-lateral a {
  padding: 10px 0;
  text-decoration: none;
  color: #333;
  font-weight: 500;
  border-bottom: 1px solid #eee;
}

.menu-lateral a:hover {
  color: #D72638;
}

.seccion-dinamica {
  flex: 1;
  padding: 1rem 2rem;
}

.user-info {
  flex: 1;
}

.logout-button {
  background-color: #FFBA08;
  color: black;
  border: none;
  padding: 8px 16px;
  font-weight: bold;
  border-radius: 6px;
  cursor: pointer;
  transition: 0.3s;
  position: absolute;
  right: 0;
  margin-right: 20px;
}

.logout-button:hover {
  background-color: #e0a800;
}

</style>
