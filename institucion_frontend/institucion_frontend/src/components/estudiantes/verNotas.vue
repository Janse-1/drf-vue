<template>
  <div class="contenedor-notas">
    <h2>Mis Notas</h2>

    <div v-if="loading">Cargando información...</div>
    <div v-else>
      <div class="info-general">
        <p><strong>Grado:</strong> {{ grado }}</p>
        <p><strong>Grupo:</strong> {{ grupo.nombre || 'Sin grupo' }}</p>
        <p><strong>Director de grupo:</strong> {{ directorGrupo }}</p>
      </div>
      <table class="tabla-notas">
        <thead>
          <tr>
            <th>Materia</th>
            <th>1P</th>
            <th>2P</th>
            <th>3P</th>
            <th>4P</th>
            <th>Def</th>
            <th>Final</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(nota, index) in notas" :key="index">
            <td>{{ nota.asignatura.nombre }}</td>
            <td>{{ formatoNota(nota.notas_periodos['1P']) }}</td>
            <td>{{ formatoNota(nota.notas_periodos['2P']) }}</td>
            <td>{{ formatoNota(nota.notas_periodos['3P']) }}</td>
            <td>{{ formatoNota(nota.notas_periodos['4P']) }}</td>
            <td>{{ formatoNota(nota.notas_periodos['Def']) }}</td>
            <td><strong>{{ formatoNota(nota.notas_periodos['Final']) }}</strong></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import axios from 'axios'
import { toast } from 'vue3-toastify'
import 'vue3-toastify/dist/index.css'

const grupo = ref({})
const grado = ref('')
const directorGrupo = ref('No asignado')
const notas = ref([])
const loading = ref(true)

const token = localStorage.getItem('access_token')
const headers = { Authorization: `Bearer ${token}` }

const formatoNota = (valor) => {
  if (valor === null || valor === undefined || isNaN(valor)) return '—'
  return Number(valor).toFixed(2)
}

const obtenerDatos = async () => {
  try {
    const perfilRes = await axios.get('http://localhost:8000/api/perfil-detallado/', { headers })
    const estudiante = perfilRes.data
    const estudianteId = estudiante.id
    const grupoData = estudiante.grupo

    if (!grupoData) throw new Error('El estudiante no tiene grupo asignado')

    grupo.value = grupoData
    grado.value = grupoData.grado
    directorGrupo.value = grupoData.director?.nombre_completo || 'No asignado'

    const asignaturasRes = await axios.get(
      `http://localhost:8000/api/asignatura-docente-grupo/asignaturas-por-grupo/?grupo=${grupoData.id}`,
      { headers }
    )
    const asignaturas = asignaturasRes.data

    const materiasConNotas = []

    for (const asig of asignaturas) {
      const notasRes = await axios.get(
        `http://localhost:8000/api/notas-finales/?estudiante=${estudianteId}&grupo=${grupoData.id}&asignatura=${asig.id}`,
        { headers }
      )
      const todasNotas = notasRes.data || []
      // Mapeo de nombres reales a códigos internos
      const mapPeriodo = {
        'PRIMER PERIODO': '1P',
        'SEGUNDO PERIODO': '2P',
        'TERCER PERIODO': '3P',
        'CUARTO PERIODO': '4P',
      }


      // Inicializar contenedor de notas por periodo
      const notas_periodos = {
        '1P': null,
        '2P': null,
        '3P': null,
        '4P': null,
        'Def': null,
        'Final': null,
      }

      // Procesar cada nota
      for (const nota of todasNotas) {
        const nombrePeriodo = String(nota.periodo_nombre).toUpperCase().trim()
        const codigoPeriodo = mapPeriodo[nombrePeriodo]
        const valor = parseFloat(nota.nota_final)

        console.log(`Periodo detectado: ${nombrePeriodo} → ${codigoPeriodo} — Valor nota: ${valor}`)

        if (codigoPeriodo && !isNaN(valor)) {
          notas_periodos[codigoPeriodo] = valor
        }

      }

      // Calcular promedio
      const valoresCompletos = ['1P', '2P', '3P', '4P']
     .map(p => (typeof notas_periodos[p] === 'number' && !isNaN(notas_periodos[p])) ? notas_periodos[p] : 0.0)

      const suma = valoresCompletos.reduce((acc, val) => acc + val, 0)
      const promedio = valoresCompletos.length > 0 ? suma / valoresCompletos.length : 0.0


      notas_periodos['Def'] = promedio
      notas_periodos['Final'] = promedio // si hay diferencia con otra lógica, cámbiala aquí

      materiasConNotas.push({
        asignatura: asig,
        notas_periodos: { ...notas_periodos }, // copia plana
      })
    }

    notas.value = materiasConNotas
    console.log('Notas finales procesadas:', JSON.stringify(notas.value, null, 2))

  } catch (error) {
    console.error('Error al obtener notas:', error)
    toast.error('Hubo un error al cargar tus notas. Intenta más tarde.', {
      position: 'top-right',
      autoClose: 5000,
      closeOnClick: true,
      pauseOnHover: true,
      draggable: true,
    })
  } finally {
    loading.value = false
  }
}

onMounted(obtenerDatos)
</script>




<style scoped>
.contenedor-notas {
  padding: 2rem;
  background-color: #fff;
  border-left: #ffd700 5px solid;
  border-radius: 10px;
  box-shadow: 0 0 10px #ccc;
  max-width: 1100px;
  margin: 0 auto;
  font-family: 'Segoe UI', sans-serif;
}
.contenedor-notas:hover{
  box-shadow: 0 0 15px #aaa;

}
.contenedor-notas h2 {
  color: #f54646; 
  font-size: 24px;
  margin-bottom: 1rem;
  text-align: center;
}

.info-general {
  margin-bottom: 1rem;
  font-size: 16px;
}
.info-general p {
  color: #555;
}
.info-general p:hover {
  background-color: #fffae5; 
  transform: translateX(4px);
  transition: background-color 0.3s ease, transform 0.3s ease;
}
.info-general strong {
  color: #222;
}

.tabla-notas {
  width: 100%;
  border-collapse: collapse;
  font-size: 15px;
}

.tabla-notas th,
.tabla-notas td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: center;
}

.tabla-notas th {
  background-color: #ffd700; /* Amarillo institucional */
  color: #333;
}

.tabla-notas tbody tr:nth-child(even) {
  background-color: #fff8dc;
}

.tabla-notas tbody tr:hover {
  background-color: #fffae5;
}

.tabla-notas td strong {
  color: #d35400; /* Naranja fuerte para nota final */
}
</style>
