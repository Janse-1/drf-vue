<template>
  <div class="periodos-wrapper">
    <h2>Periodos Académicos</h2>
    <div v-if="loading" class="loading">Cargando periodos...</div>
    <div v-else>
      <ul class="periodos-list">
        <li v-for="periodo in periodos" :key="periodo.id" :class="{ activo: periodo.activo }">
          <span>
            {{ periodo.nombre }} ({{ periodo.anio }})
            <span v-if="periodo.activo" class="badge-activo">Activo</span>
          </span>
        </li>
      </ul>
      <div v-if="!validoUnSoloActivo" class="error">
        <span>⚠️ Debe haber solo un periodo activo. Revise la configuración.</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { toast } from 'vue3-toastify'

const periodos = ref([])
const loading = ref(true)

const validoUnSoloActivo = computed(() => periodos.value.filter(p => p.activo).length === 1)

async function cargarPeriodos() {
  loading.value = true
  try {
    const token = localStorage.getItem('access_token')
    const res = await axios.get('http://localhost:8000/api/periodo-actual/', {
      headers: { Authorization: `Bearer ${token}` }
    })
    periodos.value = res.data.todos_los_periodos  // ✅ Asignar solo el array
    loading.value = false
  } catch (err) {
    toast.error('Error al cargar los periodos académicos')
    loading.value = false
  }
}


onMounted(cargarPeriodos)
</script>

<style scoped>
.periodos-wrapper {
  max-width: 500px;
  margin: 2rem auto;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(27,27,30,0.07);
  padding: 2rem 1.5rem;
}
.periodos-list {
  list-style: none;
  padding: 0;
  margin: 0;
}
.periodos-list li {
  padding: 0.7rem 1rem;
  border-radius: 8px;
  margin-bottom: 0.7rem;
  background: #f3f4f6;
  font-size: 1.08rem;
  display: flex;
  align-items: center;
}
.periodos-list li.activo {
  background: #dbeafe;
  font-weight: bold;
  color: #2563eb;
}
.badge-activo {
  background: #34d399;
  color: #fff;
  border-radius: 6px;
  padding: 0.2rem 0.7rem;
  font-size: 0.95rem;
  margin-left: 1rem;
}
.loading {
  color: #2563eb;
  font-weight: 500;
}
.error {
  color: #ef4444;
  margin-top: 1rem;
  font-weight: 600;
}
</style>
