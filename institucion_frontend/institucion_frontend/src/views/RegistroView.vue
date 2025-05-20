<template>
  
  <div class="registro-box">
    <img src="../assets/images/logo.png" alt="Logo IEI Wayuu" />
    <div class="decor-box">
      <img src="../assets/images/fondo_login.jpg" class="decor" />
      <img src="../assets/images/fondo_login.jpg" class="decor" />
    </div>


    <h1 class="titulo">Registro de Usuario</h1>
    <form @submit.prevent="registrarUsuario">
      <div class="form-grid">
        <input v-model="form.username" type="text" placeholder="Nombre de usuario" required />
        <input v-model="form.first_name" type="text" placeholder="Nombres" required />
        <input v-model="form.last_name" type="text" placeholder="Apellidos" required />
        <input v-model="form.email" type="email" placeholder="Correo electrónico" required />

        <div class="password-field">
          <input :type="mostrarPassword ? 'text' : 'password'" v-model="form.password" placeholder="Contraseña" required />
          <button type="button" class="toggle-button" @click="mostrarPassword = !mostrarPassword">
            {{ mostrarPassword ? 'Ocultar' : 'Mostrar' }}
          </button>
        </div>

        <select v-model="form.tipo_usr" required>
          <option disabled value="">Seleccione tipo de usuario</option>
          <option value="estudiante">Estudiante</option>
          <option value="docente">Docente</option>
          <option value="coordinador">Coordinador</option>
          <option value="padre">Padre</option>
        </select>
      </div>

      <CamposComunes v-model="form" />
      <RegistroEstudiante v-if="form.tipo_usr === 'estudiante'" v-model="form" />
      <RegistroDocente v-if="form.tipo_usr === 'docente'" v-model="form" />
      <RegistroCoordinador v-if="form.tipo_usr === 'coordinador'" v-model="form" />
      <RegistroPadre v-if="form.tipo_usr === 'padre'" v-model="form" />

      <button type="submit" class="boton-registrar">Registrar</button>

      <div v-if="error" class="error">{{ error }}</div>
      <div v-if="mensajeExito" class="exito">{{ mensajeExito }}</div>
    </form>
  </div>

  
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
// import HeaderPublic from '@/components/HeaderPublic.vue'
// import FooterComponent from '@/components/FooterComponent.vue'

import CamposComunes from '@/components/registro/CamposComunes.vue'
import RegistroEstudiante from '@/components/registro/RegistroEstudiante.vue'
import RegistroDocente from '@/components/registro/RegistroDocente.vue'
import RegistroCoordinador from '@/components/registro/RegistroCoordinador.vue'
import RegistroPadre from '@/components/registro/RegistroPadre.vue'


const mostrarPassword = ref(false)
const router = useRouter()

const form = reactive({
  username: '',
  email: '',
  password: '',
  first_name: '',
  last_name: '',
  tipo_usr: '',
  documento: '0000000000',
  tipo_documento: 'N/A',
  fecha_nacimiento: '2000-01-01',
  telefono: '000000000',
  direccion: 'sin direccion',
  sexo: 'N',
  estado: 'activo',
})

const resetUsuario = () => {
  form.username = ''
  form.email = ''
  form.password = ''
  form.first_name = ''
  form.last_name = ''
  form.tipo_usr = ''
  form.documento = '0000000000'
  form.tipo_documento = 'N/A'
  form.fecha_nacimiento = '2000-01-01'
  form.telefono = '000000000'
  form.direccion = 'sin direccion'
  form.sexo = 'N'
  form.estado = 'activo'
  form.grupo = ''
}

const error = ref('')
const mensajeExito = ref('')

const registrarUsuario = async () => {
  error.value = ''
  mensajeExito.value = ''

  try {
    await axios.post('http://127.0.0.1:8000/api/registro/', form)
    mensajeExito.value = 'Usuario registrado con éxito'
    resetUsuario()
    setTimeout(() => {
      router.push('/RegistroView')
    }, 1000)
  } catch (err) {
    if (err.response?.data) {
      const data = err.response.data
      const firstKey = Object.keys(data)[0]
      error.value = `${firstKey}: ${data[firstKey]}`
    } else {
      error.value = 'Error al registrar usuario'
    }
  }
}
</script>

<style scoped>
.registro-box {
  background: white;
  padding: 40px;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  width: 700px;
  margin: 80px auto;
  position: relative;
  text-align: center;
}

.decor-box {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 100%;
  max-width: 300px;
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 100px;
  z-index: -1;
}

.decor {
  width: 80px;
}

img {
  width: 100px;
  margin-bottom: 20px;
}

.titulo {
  font-size: 1.8rem;
  margin-bottom: 1.5rem;
  color: #D72638;
}

input, select {
  padding: 0.6rem;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 1rem;
  width: 90%;
  margin: auto;
  margin-bottom: 12px;
}

.password-field {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
}

.password-field input {
  width: 80%;
}

.toggle-button {
  background: none;
  border: none;
  cursor: pointer;
  margin-left: 10px;
  color: #007bff;
}

.boton-registrar {
  margin-top: 1rem;
  padding: 0.75rem;
  background-color: green;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
}

.error {
  margin-top: 1rem;
  color: red;
  font-weight: bold;
}

.exito {
  margin-top: 1rem;
  color: green;
  font-weight: bold;
}
</style>
