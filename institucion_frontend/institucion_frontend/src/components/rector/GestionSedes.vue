<template>
  <div class="p-4 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
    <div
      v-for="sede in sedes"
      :key="sede.id"
      class="bg-white rounded-2xl shadow p-4 hover:shadow-xl transition cursor-pointer"
      @click="verDetalle(sede.id)"
    >
      <h2 class="text-xl font-bold mb-2">{{ sede.nombre }}</h2>
      <p class="text-sm text-gray-600 mb-2">👩‍🏫 Coordinador: {{ sede.coordinador }}</p>

      <apexchart
        type="radialBar"
        :options="chartOptions"
        :series="[sede.docentes, sede.grados, sede.grupos, sede.estudiantes]"
        height="250"
      ></apexchart>

      <ul class="text-sm mt-2 space-y-1">
        <li>📚 Docentes: {{ sede.docentes }}</li>
        <li>🎓 Grados: {{ sede.grados }}</li>
        <li>👥 Grupos: {{ sede.grupos }}</li>
        <li>👨‍🎓 Estudiantes: {{ sede.estudiantes }}</li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import VueApexCharts from 'vue3-apexcharts'

const sedes = ref([])

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

onMounted(async () => {
  const res = await axios.get('/api/sedes/resumen/')
  sedes.value = res.data
})

function verDetalle(sedeId) {
  // Redirige a la vista detallada (puedes usar router)
  console.log('Ver detalles de sede:', sedeId)
}
</script>

<style scoped>
/* Puedes mejorar con Tailwind directamente */
</style>
