<template>
  <div class="perfil-container">
    <h2>Mi Perfil</h2>

    <div v-if="perfil" class="perfil-form">
      <p class="info-aviso">
        Para hacer otros cambios debe comunicarse con las personas autorizadas.
      </p>

      <div class="campo"><label>Nombre de usuario:</label><span>{{ perfil.username }}</span></div>
      <div class="campo"><label>Tipo de usuario:</label><span>{{ perfil.tipo_usr }}</span></div>
      <div class="campo"><label>Nombres:</label><span>{{ perfil.nombres }}</span></div>
      <div class="campo"><label>Apellidos:</label><span>{{ perfil.apellidos }}</span></div>
      <div class="campo"><label>Email:</label><span>{{ perfil.email }}</span></div>
      <div class="campo"><label>Teléfono:</label><span>{{ perfil.telefono }}</span></div>
      <div class="campo"><label>Dirección:</label><span>{{ perfil.direccion }}</span></div>

      <div v-if="perfil.fecha_nacimiento" class="campo">
        <label>Fecha de nacimiento:</label><span>{{ perfil.fecha_nacimiento }}</span>
      </div>

      <div v-if="perfil.sexo" class="campo">
        <label>Sexo:</label><span>{{ perfil.sexo }}</span>
      </div>

      <div v-if="perfil.estado" class="campo">
        <label>Estado:</label><span>{{ perfil.estado }}</span>
      </div>

      <button class="cambiar-password" @click="mostrarCambioPass = !mostrarCambioPass">
        Cambiar contraseña
      </button>

      <div v-if="mostrarCambioPass" class="cambio-password">
        <input
          :type="mostrarNueva ? 'text' : 'password'"
          v-model="nuevaPassword"
          placeholder="Nueva contraseña"
        />
        <input
          :type="mostrarNueva ? 'text' : 'password'"
          v-model="confirmarPassword"
          placeholder="Confirmar contraseña"
        />

        <div class="toggle-pass">
          <input type="checkbox" id="ver" v-model="mostrarNueva" />
          <label for="ver">Ver contraseña</label>
        </div>

        <button @click="confirmarCambio" class="cambiar-password">Guardar nueva contraseña</button>

        <p v-if="mensaje" class="mensaje">{{ mensaje }}</p>
        <p v-if="error" class="error">{{ error }}</p>
      </div>
    </div>

    <div v-else>
      <p>Cargando perfil...</p>
    </div>
  </div>
</template>


<script setup>
import { ref, onMounted } from 'vue'

const perfil = ref(null)
const mostrarCambioPass = ref(false)
const mostrarNueva = ref(false)
const nuevaPassword = ref('')
const confirmarPassword = ref('')
const mensaje = ref('')
const error = ref('')

const obtenerPerfil = async () => {
  try {
    const token = localStorage.getItem('access_token')
    const response = await fetch('http://localhost:8000/api/perfil-detallado/', {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    perfil.value = await response.json()
  } catch (err) {
    console.error('Error al obtener perfil:', err)
  }
}

const confirmarCambio = () => {
  if (confirm("¿Estás seguro de que deseas cambiar tu contraseña?")) {
    cambiarPassword()
  }
}

const cambiarPassword = async () => {
  error.value = ''
  mensaje.value = ''

  if (nuevaPassword.value !== confirmarPassword.value) {
    error.value = 'Las contraseñas no coinciden'
    return
  }

  // Opcional: pedir contraseña actual
  const current_password = prompt("Introduce tu contraseña actual para confirmar:")

  try {
    const token = localStorage.getItem('access_token')
    const response = await fetch('http://localhost:8000/auth/users/set_password/', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        current_password,
        new_password: nuevaPassword.value,
      }),
    })

    if (!response.ok) {
      const res = await response.json()
      error.value = res.new_password?.[0] || res.current_password?.[0] || 'Error al cambiar contraseña'
      return
    }

    mensaje.value = 'Contraseña actualizada con éxito'
    nuevaPassword.value = ''
    confirmarPassword.value = ''
    mostrarCambioPass.value = false
  } catch (err) {
    error.value = 'Error en el servidor'
  }
}

onMounted(() => {
  obtenerPerfil()
})
</script>


<style scoped>
.perfil-container {
  max-width: 600px;
  margin: auto;
  padding: 1rem;
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 0 8px rgba(0,0,0,0.1);
}

.perfil-container h2 {
  text-align: center;
  margin-bottom: 1rem;
}

.perfil-form .campo {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  border-bottom: 1px solid #eee;
}

.cambiar-password {
  margin-top: 1rem;
  background-color: #FFBA08;
  border: none;
  padding: 10px;
  font-weight: bold;
  cursor: pointer;
  border-radius: 6px;
}

.cambio-password {
  margin-top: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

input {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 6px;
}

.info-aviso {
  font-size: 0.9rem;
  color: #555;
  background-color: #fdf1c4;
  padding: 10px;
  border-left: 4px solid #FFBA08;
  margin-bottom: 1rem;
  border-radius: 6px;
}

.toggle-pass {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
}


.mensaje {
  color: green;
}

.error {
  color: red;
}
</style>
