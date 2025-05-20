<template>
  <div>
    <h2>Docente: {{ docenteNombre }}</h2>
    <h3>Asignatura: {{ asignaturaNombre }}</h3>
    <ul>
      <li v-for="grupo in grupos" :key="grupo.id">
        <button @click="seleccionarGrupo(grupo.id)">{{ grupo.nombre }}</button>
      </li>
    </ul>
    <div v-if="estudiantes.length">
      <h4>Estudiantes del Grupo</h4>
      <ul>
        <li v-for="estudiante in estudiantes" :key="estudiante.id">
          {{ estudiante.nombre }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const docenteNombre = ref('')
const asignaturaNombre = ref('')
const grupos = ref([])
const estudiantes = ref([])

onMounted(async () => {
  const token = localStorage.getItem('access_token')
  const headers = { Authorization: `Bearer ${token}` }

  // Obtener información del docente y asignaturas
  const response = await axios.get('http://127.0.0.1:8000/api/docente/asignaturas-grupos/', { headers })
  docenteNombre.value = response.data.nombre
  asignaturaNombre.value = response.data.asignatura
  grupos.value = response.data.grupos
})

const seleccionarGrupo = async (grupoId) => {
  const token = localStorage.getItem('access_token')
  const headers = { Authorization: `Bearer ${token}` }

  const response = await axios.get(`http://localhost:8000/api/estudiante-asignatura-curso-grado/?grupo=${grupoId}&asignatura=${asigId}`, { headers })
  estudiantes.value = response.data
}
</script>
