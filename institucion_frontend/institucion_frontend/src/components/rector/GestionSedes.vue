<template>
  <div class="grid-container">
    <div class="sede-header">
      <div class="header-actions">
        <button class="btn-crear" @click="toggleForm">
          <span v-if="!showForm">+ Crear nueva sede</span>
          <span v-else>Cancelar</span>
        </button>
        <button class="btn-asignar" @click="toggleAsignar">
          <span v-if="!showAsignar">Asignar coordinador a sede</span>
          <span v-else>Cancelar</span>
        </button>
      </div>
      <transition name="slide-fade">
        <form v-if="showForm" class="form-sede" @submit.prevent="crearSede">
          <div class="form-group">
            <label for="codigo_dane">Código DANE</label>
            <input v-model="form.codigo_dane" id="codigo_dane" required maxlength="12" />
          </div>
          <div class="form-group">
            <label for="nombre">Nombre</label>
            <input v-model="form.nombre" id="nombre" required maxlength="100" />
          </div>
          <div class="form-group">
            <label for="direccion">Dirección</label>
            <input v-model="form.direccion" id="direccion" required maxlength="200" />
          </div>
          <button class="btn-guardar" type="submit">Guardar</button>
        </form>
      </transition>
      <transition name="slide-fade">
        <form v-if="showAsignar" class="form-sede" @submit.prevent="asignarCoordinador">
          <div class="form-group">
            <label for="coordinador">Coordinador</label>
            <select v-model="asignarForm.coordinador" id="coordinador" required>
              <option value="" disabled>Seleccione un coordinador</option>
              <option v-for="coord in coordinadoresDisponibles" :key="coord.id" :value="coord.id">
                {{ coord.nombres }} {{ coord.apellidos }}
              </option>
            </select>
          </div>
          <div class="form-group">
            <label for="sede">Sede</label>
            <select v-model="asignarForm.sede" id="sede" required>
              <option value="" disabled>Seleccione una sede</option>
              <option v-for="sede in sedesDisponibles" :key="sede.codigo_dane" :value="sede.codigo_dane">
                {{ sede.nombre }}
              </option>
            </select>
          </div>
          <button class="btn-guardar" type="submit">Asignar</button>
        </form>
      </transition>
    </div>
    <div
      v-for="sede in sedes"
      :key="sede.codigo_dane"
      class="card"
      @click="verDetalle(sede.codigo_dane)"
    >
      <h2 class="card-title">{{ sede.nombre }}</h2>
      <p class="coordinador">Coordinador: {{ sede.coordinador }}</p>
      <apexchart
        type="radialBar"
        :options="chartOptions"
        :series="[sede.docentes, sede.grados, sede.grupos, sede.estudiantes]"
        height="250"
      ></apexchart>
      <ul class="info-list">
        <li>Docentes: {{ sede.docentes }}</li>
        <li>Grados: {{ sede.grados }}</li>
        <li>Grupos: {{ sede.grupos }}</li>
        <li>Estudiantes: {{ sede.estudiantes }}</li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { toast } from 'vue3-toastify'
import 'vue3-toastify/dist/index.css'


const emit = defineEmits(['ver-detalle'])
const sedes = ref([])
const showForm = ref(false)
const showAsignar = ref(false)
const form = ref({ codigo_dane: '', nombre: '', direccion: '' })
const asignarForm = ref({ coordinador: '', sede: '' })
const coordinadoresDisponibles = ref([])
const sedesDisponibles = ref([])

const chartOptions = {
  chart: { type: 'radialBar' },
  plotOptions: {
    radialBar: {
      dataLabels: {
        name: { show: false },
        value: { show: true }
      }
    }
  },
  labels: ['Docentes', 'Grados', 'Grupos', 'Estudiantes'],
  colors: ['#34d399', '#60a5fa', '#fbbf24', '#ef4444']
}

function toggleForm() {
  showForm.value = !showForm.value
  if (!showForm.value) {
    form.value = { codigo_dane: '', nombre: '', direccion: '' }
  }
}
function toggleAsignar() {
  showAsignar.value = !showAsignar.value
  if (showAsignar.value) {
    cargarCoordinadoresYSedes()
  } else {
    asignarForm.value = { coordinador: '', sede: '' }
  }
}

async function cargarCoordinadoresYSedes() {
  const token = localStorage.getItem('access_token')
  try {
    const resCoord = await axios.get('http://localhost:8000/api/coordinadores-disponibles/', {
      headers: { Authorization: `Bearer ${token}` }
    })
    coordinadoresDisponibles.value = resCoord.data
    const resSede = await axios.get('http://localhost:8000/api/sedes-disponibles/', {
      headers: { Authorization: `Bearer ${token}` }
    })
    sedesDisponibles.value = resSede.data
  } catch (err) {
    toast.error('Error al cargar coordinadores o sedes disponibles.')
  }
}

async function crearSede() {
  // Validación básica en frontend
  if (!form.value.codigo_dane || !form.value.nombre || !form.value.direccion) {
    toast.error('Todos los campos son obligatorios.')
    return
  }
  if (!/^[0-9]{5,12}$/.test(form.value.codigo_dane)) {
    toast.error('El código DANE debe ser numérico y de 5 a 12 dígitos.')
    return
  }
  if (form.value.nombre.length < 3) {
    toast.error('El nombre debe tener al menos 3 caracteres.')
    return
  }
  if (form.value.direccion.length < 5) {
    toast.error('La dirección debe tener al menos 5 caracteres.')
    return
  }
  const token = localStorage.getItem('access_token')
  try {
    await axios.post('http://localhost:8000/api/sedes/', form.value, {
      headers: { Authorization: `Bearer ${token}` }
    })
    toast.success('Sede creada correctamente.')
    showForm.value = false
    form.value = { codigo_dane: '', nombre: '', direccion: '' }
    // Recargar sedes
    const res = await axios.get('http://localhost:8000/api/resumen-sedes/', {
      headers: { Authorization: `Bearer ${token}` }
    })
    sedes.value = res.data
  } catch (err) {
    if (err.response && err.response.data && err.response.data.codigo_dane) {
      toast.error('Ya existe una sede con ese código DANE.')
    } else {
      toast.error('Error al crear la sede.')
    }
  }
}

async function asignarCoordinador() {
  if (!asignarForm.value.coordinador || !asignarForm.value.sede) {
    toast.error('Debe seleccionar coordinador y sede.')
    return
  }
  const token = localStorage.getItem('access_token')
  try {
    await axios.post('http://localhost:8000/api/asignar-coordinador-sede/', asignarForm.value, {
      headers: { Authorization: `Bearer ${token}` }
    })
    toast.success('Coordinador asignado correctamente.')
    showAsignar.value = false
    asignarForm.value = { coordinador: '', sede: '' }
    // Recargar sedes
    const res = await axios.get('http://localhost:8000/api/resumen-sedes/', {
      headers: { Authorization: `Bearer ${token}` }
    })
    sedes.value = res.data
  } catch (err) {
    toast.error('Error al asignar coordinador.')
  }
}

function verDetalle(codigoDane) {
  emit('ver-detalle', codigoDane)
}

onMounted(async () => {
  const token = localStorage.getItem('access_token')
  if (!token) {
    toast.error('No hay token de autenticación. Inicia sesión.')
    return
  }
  try {
    const res = await axios.get('http://localhost:8000/api/resumen-sedes/', {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    sedes.value = res.data
  } catch (err) {
    toast.error('Error al cargar las sedes.')
    console.error(err)
  }
})
</script>

<style scoped>
.grid-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1rem;
  padding: 1rem;
}

.card {
  background-color: white;
  border-radius: 16px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  padding: 1rem;
  cursor: pointer;
  transition: box-shadow 0.3s ease;
}

.card:hover {
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15);
}

.card-title {
  font-size: 1.2rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
  color: var(--primary-color);
}

.coordinador {
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 0.5rem;
}

.info-list {
  font-size: 0.9rem;
  margin-top: 0.5rem;
  list-style: none;
  padding: 0;
}

.sede-header {
  grid-column: 1 / -1;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  margin-bottom: 1.5rem;
}
.header-actions {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}
.btn-crear, .btn-asignar {
  background: var(--primary-color, #2563eb);
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 0.6rem 1.2rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}
.btn-crear:hover, .btn-asignar:hover {
  background: var(--secondary-color);
}
.btn-guardar {
  background: var(--secondary-color);
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 0.5rem 1.2rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  margin-top: 0.5rem;
  transition: background 0.2s;
}
.btn-guardar:hover {
  background: #0ef119;
}
.form-sede {
  background: #f9fafb;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(27,27,30,0.07);
  padding: 1.2rem 1.5rem;
  width: 100%;
  max-width: 400px;
  margin-bottom: 1rem;
  animation: fadeInDown 0.4s;
}
.form-sede:hover {
  box-shadow: 0 4px 16px rgba(13, 13, 14, 0.12);
  
}
@keyframes fadeInDown {
  from { opacity: 0; transform: translateY(-30px); }
  to { opacity: 1; transform: translateY(0); }
}
.slide-fade-enter-active, .slide-fade-leave-active {
  transition: all 0.4s cubic-bezier(.55,0,.1,1);
}
.slide-fade-enter-from, .slide-fade-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}
.form-group {
  margin-bottom: 1rem;
}
.form-group label {
  font-weight: 600;
  margin-bottom: 0.3rem;
  display: block;
}
.form-group input, .form-group select {
  width: 100%;
  padding: 0.5rem;
  border-radius: 6px;
  border: 1px solid #d1d5db;
  font-size: 1rem;
}
</style>
