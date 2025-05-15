<template>
  <div class="registro-container">
    <h1 class="titulo">Registro de Usuario</h1>
    <form @submit.prevent="registrarUsuario" class="formulario">
      <div class="form-grid">
        <input v-model="form.username" type="text" placeholder="Nombre de usuario" required />
        <input v-model="form.first_name" type="text" placeholder="Nombres" required />
        <input v-model="form.last_name" type="text" placeholder="Apellidos" required />
        <input v-model="form.email" type="email" placeholder="Correo electrónico" required />
        <div class="password-field">
         <input :type="mostrarPassword ? 'text' : 'password'" v-model="form.password" placeholder="Contraseña" required />
            <button type="button" @click="mostrarPassword = !mostrarPassword">
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

      <!-- Campos dinámicos según tipo de usuario -->
      <RegistroEstudiante v-if="form.tipo_usr === 'estudiante'" v-model="form" />
      <RegistroDocente v-if="form.tipo_usr === 'docente'" v-model="form" />
      <RegistroCoordinador v-if="form.tipo_usr === 'coordinador'" v-model="form" />
      <RegistroPadre v-if="form.tipo_usr === 'padre'" v-model="form" />

      <button type="submit" class="boton-registrar">Registrar</button>
    </form>

    <div v-if="error" class="error">{{ error }}</div>
    <div v-if="mensajeExito" class="exito">{{ mensajeExito }}</div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import axios from 'axios'

// Importa los componentes específicos
import CamposComunes from '@/components/registro/CamposComunes.vue'
import RegistroEstudiante from '@/components/registro/RegistroEstudiante.vue'
import RegistroDocente from '@/components/registro/RegistroDocente.vue'
import RegistroCoordinador from '@/components/registro/RegistroCoordinador.vue'
import RegistroPadre from '@/components/registro/RegistroPadre.vue'


const mostrarPassword = ref(false);
// Objeto reactivo para el formulario
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

//limpiar formulario
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
    console.log('Formulario que se envía:', JSON.parse(JSON.stringify(form)))

    const response = await axios.post('http://127.0.0.1:8000/api/registro/', form)
    mensajeExito.value = 'Usuario registrado con éxito'
    resetUsuario();
    
  } catch (err) {
    if (err.response?.data) {
      const data = err.response.data
      // Muestra el primer error si hay varios
      const firstKey = Object.keys(data)[0]
      error.value = `${firstKey}: ${data[firstKey]}`
    } else {
      error.value = 'Error al registrar usuario'
    }
  }
}
</script>

<style scoped>
.registro-container {
  max-width: 600px;
  margin: auto;
  padding: 2rem;
  background: #f9f9f9;
  border-radius: 12px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.titulo {
  text-align: center;
  font-size: 1.8rem;
  margin-bottom: 1.5rem;
}

.formulario {
  display: flex;
  flex-direction: column;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
  margin-bottom: 1rem;
}

input, select {
  padding: 0.6rem;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 1rem;
}

.boton-registrar {
  margin-top: 1rem;
  padding: 0.75rem;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
}

.boton-registrar:hover {
  background-color: #0056b3;
}

.error {
  margin-top: 1rem;
  color: red;
  font-weight: bold;
  text-align: center;
}

.exito {
  margin-top: 1rem;
  color: green;
  font-weight: bold;
  text-align: center;
}
</style>
