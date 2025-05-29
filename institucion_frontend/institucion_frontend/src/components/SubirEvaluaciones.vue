<template>
  <div class="subir-evaluaciones-container">
    <h2 v-if="periodoActual">
      Registro de Nota Final - {{ periodoActual.nombre }} ({{ periodoActual.representacion }}) - Año {{ periodoActual.anio }}
    </h2>
    <p>Ingresa notas válidas entre 0.0 y 5.0 usando punto decimal (ej. 3.5)</p>
     <h4 class="info-aviso">Recuerda que una vez guardas las notas no pueden ser modificadas, sé cuidadoso antes de enviarlas.</h4>


    <div v-for="(grupo, index) in asignaturasGrupos" :key="grupo.id" class="bloque-asignatura">
      <button @click="toggleGrupo(index)" class="btn-grupo">
        {{ grupo.asignatura.nombre }} - Grupo: {{ grupo.grupo.nombre }}
        <span v-if="grupo.enviado" style="color: green; font-weight: bold;">
          ✔ Notas registradas
        </span>
      </button>


      <div v-if="grupo.abierto">
        <table>
          <thead>
            <tr>
              <th>Número</th>
              <th>Nombres</th>
              <th>Nota del {{ periodoActual.representacion }}</th>
              <th>Observaciones</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(est, idx) in grupo.estudiantes"
              :key="est.id"
              :class="{
                'verde': getColor(grupo.notasFinales[est.id]) === 'verde',
                'rojo': getColor(grupo.notasFinales[est.id]) === 'rojo',
                'amarillo': getColor(grupo.notasFinales[est.id]) === 'amarillo'
              }"
            >
              <td>{{ idx + 1 }}</td>
              <td>{{ est.apellidos }} {{ est.nombres }}</td>
              <td>
                <div style="position: relative;">
                  <span
                    v-if="erroresNotas[`${grupo.id}-${est.id}`]"
                    class="error-text"
                    style="position: absolute; top: -1.2rem; font-size: 0.75rem;"
                  >
                    {{ erroresNotas[`${grupo.id}-${est.id}`] }}
                  </span>
                  <input
                    type="text"
                    v-model="grupo.notasFinales[est.id]"
                    @input="validarNota(est.id, grupo)"
                    :class="{ 'input-error': erroresNotas[`${grupo.id}-${est.id}`] }"
                    :disabled="grupo.notasRegistradas[est.id] !== undefined"
                  />
                </div>
              </td>
              <td>
                <textarea v-model="grupo.observaciones[est.id]"></textarea>
              </td>
            </tr>

          </tbody>
        </table>

        <button
          @click="guardarNotas(grupo)"
          class="btn-grupo"
          :disabled="grupo.enviado || !hayNotasParaGuardar(grupo)"
        >
          Guardar calificaciones
        </button>
        <span v-if="grupo.enviado" style="color: green; font-weight: bold;">
           Ya has registrado las notas a este grupo ✔
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { toast } from "vue3-toastify"
import "vue3-toastify/dist/index.css"

const asignaturasGrupos = ref([])
const erroresNotas = ref({})
const periodoActual = ref(null)


const toggleGrupo = async (index) => {
  const grupo = asignaturasGrupos.value[index]
  grupo.abierto = !grupo.abierto
  if (grupo.abierto && grupo.estudiantes.length === 0) {
    await cargarDatosGrupo(index)
  }
}

const getColor = (nota) => {
  const n = parseFloat(nota)
  if (isNaN(n)) return ''
  if (n >= 4.5) return 'verde'
  if (n <= 2.5) return 'rojo'
  return 'amarillo'
}

const cargarAsignaciones = async () => {
  const token = localStorage.getItem('access_token')
  const headers = { Authorization: `Bearer ${token}` }

  const res = await axios.get('http://127.0.0.1:8000/api/docente/asignaturas-grupos/', { headers })
  const periodoId = periodoActual.value?.id

  // Mapear asignaciones y verificar notas ya enviadas
  asignaturasGrupos.value = await Promise.all(res.data.map(async item => {
    const grupoId = item.grupo.id
    const asigId = item.asignatura.id

    let enviado = false
    let notasRegistradas = {}

    try {
      const notasRes = await axios.get(`http://127.0.0.1:8000/api/notas-finales/?grupo=${grupoId}&asignatura=${asigId}&periodo=${periodoId}`, { headers })
      notasRes.data.forEach(nota => {
        notasRegistradas[nota.estudiante] = nota.nota_final
      })
      // Solo marcar como "enviado" si todos los estudiantes tienen nota
      const estudiantesRes = await axios.get(
        `http://localhost:8000/api/estudiante-asignatura-curso-grado/?grupo=${grupoId}&asignatura=${asigId}`,
        { headers }
      )
      const totalEstudiantes = estudiantesRes.data.length
      const totalNotas = Object.keys(notasRegistradas).length
      enviado = totalEstudiantes > 0 && totalNotas === totalEstudiantes
    } catch (e) {
      console.error('Error al verificar notas existentes:', e)
    }


    return {
      ...item,
      abierto: false,
      estudiantes: [],
      notasFinales: {},
      observaciones: {},
      enviado,
      notasRegistradas,
    }
  }))
}


const hayNotasParaGuardar = (grupo) => {
  return grupo.estudiantes.some(est => {
    return grupo.notasRegistradas[est.id] === undefined && grupo.notasFinales[est.id] !== ''
  })
}


const obtenerPeriodoActual = async () => {
  try {
    const token = localStorage.getItem('access_token')
    const headers = { Authorization: `Bearer ${token}` }

    const res = await axios.get('http://127.0.0.1:8000/api/periodo-actual/', { headers })
    periodoActual.value = res.data
  } catch (err) {
    console.error('Error al obtener periodo actual:', err)
  }
}

const cargarDatosGrupo = async (index) => {
  try {
    const grupo = asignaturasGrupos.value[index]
    const token = localStorage.getItem('access_token')
    const headers = { Authorization: `Bearer ${token}` }

    const grupoId = grupo.grupo.id
    const asigId = grupo.asignatura.id

    const res = await axios.get(
      `http://localhost:8000/api/estudiante-asignatura-curso-grado/?grupo=${grupoId}&asignatura=${asigId}`,
      { headers }
    )

    // Ordenar por apellido
    const estudiantesOrdenados = res.data
      .map(e => e.estudiante)
      .sort((a, b) => a.apellidos.localeCompare(b.apellidos))

    // Asignar estudiantes
    grupo.estudiantes.splice(0, grupo.estudiantes.length, ...estudiantesOrdenados)

    // Llenar notas y observaciones
    estudiantesOrdenados.forEach(est => {
      const notaExistente = grupo.notasRegistradas[est.id]
      grupo.notasFinales[est.id] = notaExistente !== undefined ? notaExistente : ''
      grupo.observaciones[est.id] = ''
    })

    // 🔄 Verificar si todos los estudiantes tienen nota registrada
    const totalEstudiantesIds = estudiantesOrdenados.map(est => est.id)
    const estudiantesSinNota = totalEstudiantesIds.filter(id => grupo.notasRegistradas[id] === undefined)
    grupo.enviado = estudiantesSinNota.length === 0

  } catch (error) {
    console.error('Error al cargar estudiantes:', error)
    toast.error('Error al cargar estudiantes del grupo.')
  }
}



const validarNota = (estId, grupo) => {
  const key = `${grupo.id}-${estId}`
  const valor = grupo.notasFinales[estId]
  const num = parseFloat(valor)

  if (valor.includes(',')) {
    erroresNotas.value[key] = 'Usa punto (.) como separador decimal'
  } else if (isNaN(num)) {
    erroresNotas.value[key] = 'Debe ser un número'
  } else if (num < 0 || num > 5) {
    erroresNotas.value[key] = 'La nota debe estar entre 0.0 y 5.0'
  } else {
    delete erroresNotas.value[key]
  }
}

const guardarNotas = async (grupo) => {
  const token = localStorage.getItem('access_token')
  const headers = { Authorization: `Bearer ${token}` }

  const payload = []

  for (const est of grupo.estudiantes) {
    const key = `${grupo.id}-${est.id}`
    const nota = parseFloat(grupo.notasFinales[est.id])
    const observacion = grupo.observaciones[est.id] || ''

    if (erroresNotas.value[key]) {
      toast.error(`Error en la nota de ${est.nombres}. Corrige antes de guardar.`)
      return
    }

    if (isNaN(nota) || nota < 0 || nota > 5) {
      toast.error(`Nota inválida para ${est.nombres}. Debe estar entre 0.0 y 5.0`)
      return
    }

    payload.push({
      estudiante: est.id,
      asignatura: grupo.asignatura.id,
      grupo: grupo.grupo.id,
      periodo: periodoActual.value.id,
      nota_final: nota,
      observaciones: observacion
    })
  }

  try {
    await axios.post('http://127.0.0.1:8000/api/notas-finales/bulk_create/', payload, { headers })

    // Limpiar
    grupo.notasFinales = {}
    grupo.observaciones = {}

    // Cerrar grupo y marcar como enviado
    grupo.abierto = false
    grupo.enviado = true

    toast.success("Notas guardadas exitosamente.")
  } catch (error) {
    console.error('Error al guardar notas:', error)
    toast.error("Ocurrió un error al guardar las notas.")
  }
}



onMounted(() => {
  cargarAsignaciones()
  obtenerPeriodoActual()
})
</script>

<style scoped>
.subir-evaluaciones-container {
  padding: 1rem;
  background: #fff;
}
.bloque-asignatura {
  margin-bottom: 2rem;
  border: 1px solid #ccc;
  padding: 1rem;
  border-radius: 8px;
}
table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}
th, td {
  border: 1px solid #ddd;
  padding: 6px;
}
.input-error {
  border: 1px solid red;
}
.error-text {
  font-size: 0.8rem;
  color: red;
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
.btn-grupo {
  margin-top: 1rem;
  background-color: #FFBA08;
  border: none;
  padding: 10px;
  font-weight: bold;
  cursor: pointer;
  border-radius: 6px;
}

.verde {
  background-color: #e0ffe0;
}
.rojo {
  background-color: #ffe0e0;
}
.amarillo {
  background-color: #fff8dc;
}
button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

</style>
