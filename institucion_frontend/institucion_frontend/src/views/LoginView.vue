<template>
  <div class="login-box">
    <img src="@/assets/images/logo.png" alt="Logo IEI Wayuu" />
    <div class="decor-box">
      <img src="../assets/images/fondo_login.jpg" class="decor" />
      <img src="../assets/images/fondo_login.jpg" class="decor" />
    </div>

    <form @submit.prevent="login">
      <input
        v-model="username"
        type="text"
        class="input-field"
        placeholder="Usuario"
        required
      />

      <div class="password-wrapper">
        <input
          v-model="password"
          :type="showPassword ? 'text' : 'password'"
          class="input-field"
          placeholder="Contraseña"
          required
        />
        <button type="button" class="toggle-password" @click="togglePassword">
          <i :class="showPassword ? 'fa-solid fa-eye-slash' : 'fa-solid fa-eye'"></i>
        </button>
      </div>

      <p v-if="error" style="color: red; font-weight: bold;">{{ error }}</p>

      <button type="submit" class="button">INGRESAR</button>
      <a class="forgot-password" href="#">¿Olvidaste tu contraseña?</a>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const username = ref('')
const password = ref('')
const error = ref('')
const showPassword = ref(false)
const router = useRouter()

const togglePassword = () => {
  showPassword.value = !showPassword.value
}

const login = async () => {
  error.value = ''
  try {
    const response = await fetch('http://localhost:8000/auth/jwt/create/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: username.value, password: password.value }),
    })

    const data = await response.json()

    if (!response.ok) {
      error.value = data.detail || 'Usuario o contraseña incorrectos'
      return
    }

    const accessToken = data.access
    localStorage.setItem('access_token', accessToken)
    localStorage.setItem('refresh_token', data.refresh)

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

    localStorage.setItem('first_name', userInfo.first_name)
    localStorage.setItem('last_name', userInfo.last_name)
    localStorage.setItem('tipo_usr', userInfo.tipo_usr)

    router.push('/MainView')
  } catch (err) {
    error.value = 'Error de red o del servidor'
  }
}
</script>

<style scoped>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');

body {
  margin: 0;
  padding: 0;
  background-color: white;
}

.login-box {
  background: white;
  padding: 40px;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  width: 350px;
  margin: 80px auto;
  position: relative;
  z-index: 10;
  overflow: hidden;
  transform: scale(1.05);
  text-align: center;
}

.login-box img {
  width: 100px;
  display: block;
  margin: 0 auto 20px;
}

.input-field {
  width: 90%;
  padding: 12px;
  margin: 10px 0;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 16px;
  text-align: center;
  background-color: #f8d7da;
}

.password-wrapper {
  position: relative;
}

.toggle-password {
  position: absolute;
  top: 50%;
  right: 35px;
  transform: translateY(-50%);
  background: none;
  border: none;
  cursor: pointer;
  font-size: 18px;
  color: #333;
}

.button {
  background-color: green;
  color: white;
  padding: 10px 20px;
  margin-top: 10px;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
  transition: 0.3s;
}

.button:hover {
  opacity: 0.8;
}

.forgot-password {
  display: block;
  margin-top: 10px;
  color: blue;
  text-decoration: underline;
  cursor: pointer;
  font-size: 14px;
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
</style>
