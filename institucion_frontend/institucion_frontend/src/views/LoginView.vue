<template>
  <div class="login-container">
    <h2>Iniciar Sesión</h2>
    <form @submit.prevent="login">
      <div>
        <label for="username">Usuario</label>
        <input v-model="username" type="text" id="username" required />
      </div>
      <div>
        <label for="password">Contraseña</label>
        <input v-model="password" type="password" id="password" required />
      </div>
      <button type="submit">Ingresar</button>
      <p v-if="error" style="color:red;">{{ error }}</p>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const username = ref('')
const password = ref('')
const error = ref('')
const router = useRouter()

const login = async () => {
  error.value = ''
  try {
    // 1. Enviar usuario y contraseña al backend
    const response = await fetch('http://localhost:8000/auth/jwt/create/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username: username.value,
        password: password.value,
      }),
    })

    const data = await response.json()

    if (!response.ok) {
      error.value = data.detail || 'Error al iniciar sesión'
      return
    }

    const accessToken = data.access
    localStorage.setItem('access_token', accessToken)
    localStorage.setItem('refresh_token', data.refresh)

    // 2. Obtener información del usuario usando el token
    const userResponse = await fetch('http://localhost:8000/auth/users/me/', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${accessToken}`,
      },
    })

    const userInfo = await userResponse.json()

    if (!userResponse.ok) {
      error.value = 'Error al obtener la información del usuario'
      return
    }

    // 3. Guardar nombre, apellido y tipo de usuario en localStorage
    localStorage.setItem('first_name', userInfo.first_name)
    localStorage.setItem('last_name', userInfo.last_name)
    localStorage.setItem('tipo_usr', userInfo.tipo_usr)

    // 4. Redirigir a la vista principal
    router.push('/MainView')
  } catch (err) {
    error.value = 'Error de red o del servidor'
  }
}
</script>


<style scoped>
.login-container {
  max-width: 400px;
  margin: 80px auto;
  padding: 2rem;
  border: 1px solid #ccc;
  border-radius: 12px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}
input {
  display: block;
  width: 100%;
  margin-top: 4px;
  margin-bottom: 16px;
  padding: 8px;
}
button {
  padding: 10px 20px;
  cursor: pointer;
}
</style>
