<template>
    <div class="detalle-header">
      <button class="btn-volver" @click="$emit('volver')">← Volver</button>
    </div>
  <div class="detalle-sede-wrapper">
    <div class="detalle-card" v-if="sede">
        <h1 class="detalle-title">{{ sede?.nombre || 'Detalle de Sede' }}</h1>
      <ul class="info-list">
        <li class="info-item" @click.self="toggle('coordinador')">
          <strong>Coordinador:</strong> 
          {{ sede.coordinador ? (sede.coordinador.nombres + ' ' + sede.coordinador.apellidos) : 'Sin asignar' }}
          <div v-if="show.coordinador && sede.coordinador">
            <CoordinadorSedeDetalle
              :coordinador="sede.coordinador"
              :sede-codigo-dane="codigoDane"
              @actualizar="recargarSede"
              @editar="onEditarCoordinador"
              @eliminar="onEliminarCoordinador"
              @cambiar="onCambiarCoordinador"
            />
          </div>
        </li>
        <li class="info-item" @click="toggle('docentes')">
          <strong>Docentes:</strong> {{ sede.docentes.length }}
          <ul v-if="show.docentes" class="sub-list">
            <li v-for="doc in sede.docentes" :key="doc.id">{{ doc.nombres }} {{ doc.apellidos }}</li>
          </ul>
        </li>
        <li class="info-item" @click="toggle('grados')">
          <strong>Grados:</strong> {{ sede.grados.length }}
          <ul v-if="show.grados" class="sub-list">
            <li v-for="grado in sede.grados" :key="grado.id">{{ grado.nombre }}</li>
          </ul>
        </li>
        <li class="info-item" @click="toggle('grupos')">
          <strong>Grupos:</strong> {{ sede.grupos.length }}
          <ul v-if="show.grupos" class="sub-list">
            <li v-for="grupo in sede.grupos" :key="grupo.id">{{ grupo.nombre }}</li>
          </ul>
        </li>
        <li class="info-item" @click="toggle('estudiantes')">
          <strong>Estudiantes:</strong> {{ sede.estudiantes.length }}
          <ul v-if="show.estudiantes" class="sub-list">
            <li v-for="est in sede.estudiantes" :key="est.id">{{ est.nombres }} {{ est.apellidos }}</li>
          </ul>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { toast } from 'vue3-toastify'
import CoordinadorSedeDetalle from './Crud-DetallesSedes.vue/CoordinadorSedeDetalle.vue'

defineEmits(['volver'])
const sede = ref(null)
const show = ref({
  coordinador: false,
  docentes: false,
  grados: false,
  grupos: false,
  estudiantes: false
})
const mostrarCoordinadorDetalle = ref(false)

function toggle(key) {
  show.value[key] = !show.value[key]
  if (key === 'coordinador' && show.value[key] && sede.value?.coordinador) {
    mostrarCoordinadorDetalle.value = true
  } else if (key === 'coordinador') {
    mostrarCoordinadorDetalle.value = false
  }
}

function onEditarCoordinador(coord) {
  toast.info('Funcionalidad editar coordinador (por implementar)')
}
function onEliminarCoordinador(coord) {
  toast.info('Funcionalidad eliminar coordinador (por implementar)')
}
function onCambiarCoordinador(coord) {
  toast.info('Funcionalidad cambiar coordinador (por implementar)')
}

const props = defineProps(['codigoDane'])
function recargarSede() {
  cargarSede()
}

async function cargarSede() {
  const token = localStorage.getItem('access_token')
  try {
    const res = await axios.get(`http://localhost:8000/api/detalle-sede/${props.codigoDane}/`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    sede.value = res.data
  } catch (err) {
    toast.error('Error al cargar la información de la sede.')
  }
}

onMounted(cargarSede)
</script>

<style scoped>
.detalle-sede-wrapper {
  max-width: 700px;
  margin: 2rem auto;
  padding: 1rem;
}
.detalle-header {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}
.detalle-title {
  font-size: 1.6rem;
  font-weight: bold;
  color: var(--primary-color, #2563eb);
  margin: 0;
  margin-bottom: 30px;
}
.detalle-card {
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  padding: 2rem 1.5rem;
}
.info-list {
  list-style: none;
  padding: 0;
  margin: 0;
}
.info-item {
  margin-bottom: 1rem;
  cursor: pointer;
  background: #f3f4f6;
  border-radius: 8px;
  padding: 0.7rem 1rem;
  transition: background 0.2s;
  font-size: 1.05rem;
}
.info-item:hover {
  background: #e0e7ef;
}
.sub-list {
  margin-top: 0.5rem;
  margin-left: 1.5rem;
  list-style: disc;
  color: #444;
  font-size: 0.98rem;
}
.btn-volver {
  background: var(--primary-color, #2563eb);
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 0.5rem 1.2rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}
.btn-volver:hover {
  background: var(--secondary-color, #0ef119);
}
</style>
