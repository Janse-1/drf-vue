<template>
  <header>
    <h2 v-if="user">Bienvenido, {{ user.username }}!</h2>
    <nav v-if="user">
      <!-- Puedes hacer condiciones según el rol si lo agregas -->
      <a href="">Mi perfil</a>
      <a href="">Mis notas</a>
      <a href="">Mis cursos</a>
      <a href="">Estudiantes</a>
      <a href="">Sedes</a>
      <a href="">Subir notas</a>
    </nav>
  </header>

  <div>
    <ul>
      <li>
        <a href="">Revisar tareas pendientes</a>
        <a href="">Registrar estudiantes</a>
        <a href="">Registrar docentes</a>
      </li>
    </ul>
  </div>

  
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const user = ref(null)
const router = useRouter()

onMounted(async () => {
  const token = localStorage.getItem('access_token')

  try {
    const response = await fetch('http://localhost:8000/auth/users/me/', {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    })

    if (!response.ok) {
      throw new Error('No autorizado')
    }

    const data = await response.json()
    user.value = data
  } catch (error) {
    console.error('Error al obtener datos del usuario:', error)
    router.push('/LoginView')
  }
})

</script>

<style scoped>
/* Estilos básicos opcionales */
header {
  background-color: #f4f4f4;
  padding: 1rem;
  margin-bottom: 1rem;
}
nav a {
  margin-right: 1rem;
  text-decoration: none;
  color: #333;
}
footer {
  margin-top: 2rem;
  text-align: center;
  color: #666;
}
</style>
