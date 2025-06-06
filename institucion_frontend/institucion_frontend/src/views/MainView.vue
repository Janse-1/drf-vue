<template>
  <div class="main-layout">
    <header class="encabezado">
      <img src="../assets/images/logo.png" class="logo" />
      <div class="user-info">
        <h2>Bienvenido, {{ user.first_name }} {{ user.last_name }}!</h2>
        <p class="rol">{{ user.tipo_usr }}</p>
      </div>


      <nav class="navbar-header">
        <a href="/"><i class="fa-solid fa-house"></i> Inicio</a>
        <a href="#"><i class="fa-solid fa-newspaper"></i> Noticias</a>
        <a href="/ContactoView"><i class="fa-solid fa-envelope"></i> Contacto</a>
        <button @click="cerrarSesion" class="logout-header">
          <i class="fa-solid fa-right-from-bracket"></i> Cerrar sesión
        </button>
      </nav>

    </header>

    <div class="contenido-total">
      <aside class="menu-lateral" v-if="user">
        
        <!-- Estudiante  -->
        <template v-if="user.tipo_usr === 'estudiante'">
          <a href="#" 
            @click.prevent="mostrarVista = 'perfil'" 
            :class="{ activo: mostrarVista === 'perfil' }">
            <i class="fa-solid fa-user"></i> Mi perfil
          </a>
          <a href="#"
            @click="mostrarVista = 'misNotas'"
            :class="{ activo: mostrarVista === 'misNotas'}"><i class="fa-solid fa-book"></i> Mis notas</a>
        </template>

        <!-- Docente -->
        <template v-else-if="user.tipo_usr === 'docente'">
           <a href="#" 
            @click.prevent="mostrarVista = 'perfil'" 
            :class="{ activo: mostrarVista === 'perfil' }">
            <i class="fa-solid fa-user"></i> Mi perfil
          </a>
          <a href="#" 
            @click.prevent="mostrarVista = 'subirEvaluacion'" 
            :class="{ activo: mostrarVista === 'subirEvaluacion' }">
            <i class="fa-solid fa-upload"></i> Subir notas
          </a>
          <a href="#" 
            @click.prevent="mostrarVista = 'verEstudiantes'" 
            :class="{ activo: mostrarVista === 'verEstudiantes' }">
            <i class="fa-solid fa-users"></i> Ver a Estudiantes
          </a>
        </template>

        <!-- Coordinador o Admin -->
        <template v-else-if="user.tipo_usr === 'coordinador' || user.tipo_usr === 'admin'">
          <a href="#" @click.prevent="mostrarVista = 'perfil'":class="{ activo: mostrarVista === 'perfil' }"><i class="fa-solid fa-user"></i> Mi perfil</a>
          <a href="#" @click.prevent="mostrarVista = 'subirEvaluacion'":class="{ activo: mostrarVista === 'subirEvaluacion'}"><i class="fa-solid fa-upload"></i> Subir notas</a>
          <a href="#" @click.prevent="mostrarVista = 'verEstudiantes'":class="{ activo: mostrarVista === 'verEstudiantes' }"><i class="fa-solid fa-users"></i> Ver estudiantes</a>
          <a href="#" @click.prevent="mostrarVista = 'registrar'":class="{ activo: mostrarVista === 'registrar' }"><i class="fa-solid fa-user-plus"></i> Registrar</a>
          <a href="#"><i class="fa-solid fa-school"></i> Mi sede</a>
        </template>

        <template v-else-if="user.tipo_usr === 'rector'">
          <a href="#" @click.prevent="mostrarVista = 'perfil'":class="{ activo: mostrarVista === 'perfil' }"><i class="fa-solid fa-user"></i> Mi perfil</a>
          <a href="#" @click.prevent="mostrarVista = 'subirEvaluacion'":class="{ activo: mostrarVista === 'subirEvaluacion' }"><i class="fa-solid fa-upload"></i> Subir notas</a>
          <a href="#" @click.prevent="mostrarVista = 'verEstudiantes'":class="{ activo: mostrarVista === 'verEstudiantes' }"><i class="fa-solid fa-users"></i> Ver estudiantes</a>
          <a href="#" @click.prevent="mostrarVista = 'registrar'":class="{ activo: mostrarVista === 'registrar' }"><i class="fa-solid fa-user-plus"></i> Registrar</a>
          <a href="#" @click.prevent="mostrarVista = 'gestionSedes'":class="{ activo: mostrarVista === 'gestionSedes'}"><i class="fa-solid fa-school"></i> Gestión de sedes</a>
        </template>

        <hr>
        
      </aside>

      <main class="seccion-dinamica">
        <MiPerfil v-if="mostrarVista=== 'perfil'" />
        <verNotas v-if="mostrarVista === 'misNotas'" />
        <SubirEvaluaciones v-if="mostrarVista === 'subirEvaluacion'" />
        <VerEstudiantes v-if="mostrarVista === 'verEstudiantes'" />
        <RegistroView v-if="mostrarVista === 'registrar'" />
        <GestionSedes v-if="mostrarVista === 'gestionSedes'" />

      </main>
    </div>

    <FooterComponent />
  </div>
</template>


<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import FooterComponent from '@/components/FooterComponent.vue'
import MiPerfil from '@/components/MiPerfil.vue';
import SubirEvaluaciones from '@/components/docentes/SubirEvaluaciones.vue';
import VerEstudiantes from '@/components/docentes/VerEstudiantes.vue';
import RegistroView from './RegistroView.vue';
import verNotas from '@/components/estudiantes/verNotas.vue';
import GestionSedes from '@/components/rector/GestionSedes.vue';

const mostrarVista = ref(null);

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
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');

.main-layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.encabezado {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #D72638;
  color: white;
  padding: 1rem 2rem;
  flex-wrap: wrap;
}

.logo-area {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex: 1;
}

.logo {
  width: 60px;
}

.rol {
  font-size: 0.9rem;
  font-style: italic;
}

.navbar-header {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  align-items: center;
}

.navbar-header a,
.navbar-header button {
  color: white;
  text-decoration: none;
  font-weight: 500;
  background: none;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 6px 10px;
  font-size: 0.95rem;
  transition: background 0.2s;
}
.menu-lateral a.activo {
  border-left: 4px solid #ffc107; 
  background-color: #fff8dc;
  color: #D72638; 
  font-weight: bold;
}

.navbar-header a:hover,
.navbar-header button:hover {
  background-color: #c31f2d;
  border-radius: 5px;
}

.logout-header {
  background-color: #FFBA08;
  color: black;
  font-weight: bold;
  border-radius: 6px;
  padding: 6px 12px;
}

.logout-header:hover {
  background-color: #e0a800;
}


.user-info {
  flex: 1;
}

.rol {
  font-size: 0.9rem;
  font-style: italic;
}

.contenido-total {
  flex: 1;
  display: flex;
  background-color: #fff8f0;
}

.menu-lateral {
  width: 260px;
  background-color: #fff;
  border-right: 2px solid #ddd;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.menu-lateral a,
.menu-lateral button {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
  background: none;
  border: none;
  color: #333;
  text-align: left;
  text-decoration: none;
  font-weight: 500;
  font-size: 15px;
  cursor: pointer;
}

.menu-lateral a:hover,
.menu-lateral button:hover {
  background-color: #f3f3f3;
  color: #D72638;
}

.logout-button {
  margin-top: auto;
  color: black;
  font-weight: bold;
  background-color: #FFBA08;
  border-radius: 6px;
  transition: 0.3s;
  padding: 8px 12px;
}

.logout-button:hover {
  background-color: #e0a800;
}

.seccion-dinamica {
  flex: 1;
  padding: 2rem;
}


</style>
