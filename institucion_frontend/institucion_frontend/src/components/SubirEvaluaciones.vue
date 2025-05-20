<template>
  <div class="subir-evaluaciones-container">
    <h2>Subir Notas</h2>
    <h4>Puedes crear nuevas actividades en el botón "Agregar Evaluacion"</h4>
    <p>Nota: Recuerda ingresar valores entre 0.0 a 5.0</p>

    <div v-for="(grupo, index) in asignaturasGrupos" :key="grupo.id" class="bloque-asignatura">
      <button @click="toggleGrupo(index)">
        {{ grupo.asignatura.nombre }} - Grupo: {{ grupo.grupo.nombre }}
      </button>

      <div v-if="grupo.abierto">
        <button @click="abrirModal(grupo)">Agregar evaluación</button>

        <table>
          <thead>
            <tr>
              <th>Estudiante</th>
              <th v-for="evaluar in grupo.evaluaciones" :key="evaluar.id">
                {{ evaluar.nombre }} ({{ evaluar.tipo }})
              </th>
              <th>Asistencia</th>
              <th>Disciplina</th>
              <th>Nota Final</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="est in grupo.estudiantes" :key="est.id">
              <td>{{ est.nombres }} {{ est.apellidos }}</td>
              <td v-for="evalua in grupo.evaluaciones" :key="evalua.id">
                <input type="number" min="0" max="5" step="0.1"
                  v-model.number="grupo.notas[`${est.id}-${evalua.id}`]" />
              </td>
              <td><input type="number" min="0" max="5" step="0.1" v-model.number="grupo.asistencia[est.id]" /></td>
              <td><input type="number" min="0" max="5" step="0.1" v-model.number="grupo.disciplina[est.id]" /></td>
              <td>{{ calcularNotaFinal(grupo, est.id) }}</td>
            </tr>
          </tbody>
        </table>

        <button @click="guardarNotas(grupo)">Guardar calificaciones</button>
      </div>
    </div>

    <!-- Modal -->
    <div v-if="mostrarModal">
      <div class="modal">
        <h3>Nueva evaluación para {{ modalContext.asignatura.nombre }} - {{ modalContext.grupo.nombre }}</h3>
        <input v-model="nuevaEval.nombre" placeholder="Nombre" />
        <select v-model="nuevaEval.tipo">
          <option value="actividad">Actividad</option>
          <option value="examen_final">Examen Final</option>
        </select>
        <input type="date" v-model="nuevaEval.fecha" />
        <button @click="crearEvaluacion">Crear</button>
        <button @click="cerrarModal">Cancelar</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const asignaturasGrupos = ref([])
const mostrarModal = ref(false)
const modalContext = ref(null)
const nuevaEval = ref({ nombre: '', tipo: 'actividad', fecha: '' })

const toggleGrupo = (index) => {
  asignaturasGrupos.value[index].abierto = !asignaturasGrupos.value[index].abierto
 if (asignaturasGrupos.value[index].abierto && asignaturasGrupos.value[index].evaluaciones.length === 0) {
  cargarDatosGrupo(index)
}
  }


const abrirModal = (grupo) => {
  modalContext.value = grupo
  mostrarModal.value = true
}

const cerrarModal = () => {
  mostrarModal.value = false
  nuevaEval.value = { nombre: '', tipo: 'actividad', fecha: '' }
  modalContext.value = null
}

const cargarAsignaciones = async () => {
  const token = localStorage.getItem('access_token')
  const headers = { Authorization: `Bearer ${token}` }

  const res = await axios.get('http://127.0.0.1:8000/api/docente/asignaturas-grupos/', { headers })
  asignaturasGrupos.value = res.data.map(item => ({
    ...item,
    abierto: false,
    evaluaciones: [],
    estudiantes: [],
    notas: {},
    asistencia: {},
    disciplina: {},
  }))
}

const cargarDatosGrupo = async (index) => {
  try{
  const grupo = asignaturasGrupos.value[index]
  const token = localStorage.getItem('access_token')
  const headers = { Authorization: `Bearer ${token}` }

  const grupoId = grupo.grupo.id
  const asigId = grupo.asignatura.id

  const res = await axios.get(`http://localhost:8000/api/estudiante-asignatura-curso-grado/?grupo=${grupoId}&asignatura=${asigId}`, { headers })
  console.log('Respuesta estudiantes asignados:', res.data)
  grupo.estudiantes.splice(0, grupo.estudiantes.length, ...res.data.map(e => e.estudiante))
  console.log("Estudiantes cargados para grupo:", grupo.grupo.nombre, grupo.estudiantes)
  console.log('Estudiantes asignados al grupo:', grupo.estudiantes)

 // Solo usamos el campo estudiante
  grupo.evaluaciones = []

  // Llenar asistencia y disciplina por defecto
  grupo.estudiantes.forEach(est => {
    grupo.asistencia[est.id] = 0
    grupo.disciplina[est.id] = 0
  })

  const evalRes = await axios.get(`http://localhost:8000/api/docente/evaluaciones/?grupo=${grupoId}&asignatura=${asigId}`, { headers })
  grupo.evaluaciones = evalRes.data

  } catch (error) {
    console.error('Error al cargar datos del grupo:', error)
  }
}



const crearEvaluacion = async () => {
  const token = localStorage.getItem('access_token')
  const headers = { Authorization: `Bearer ${token}` }

  const payload = {
    nombre: nuevaEval.value.nombre,
    tipo: nuevaEval.value.tipo,
    fecha: nuevaEval.value.fecha,
    grupo: modalContext.value.grupo.id,
    asignatura: modalContext.value.asignatura.id,
  }

   const grupoTemp = modalContext.value

  await axios.post('http://127.0.0.1:8000/api/docente/evaluaciones/', payload, { headers })
  cerrarModal()
  const idx = asignaturasGrupos.value.findIndex(
    ag => ag.grupo.id === grupoTemp.grupo.id && ag.asignatura.id === grupoTemp.asignatura.id
  )
  await cargarDatosGrupo(idx)
}

const guardarNotas = async (grupo) => {
  const token = localStorage.getItem('access_token')
  const headers = { Authorization: `Bearer ${token}` }

  for (const est of grupo.estudiantes) {
    for (const evaluacion of grupo.evaluaciones) {
      const key = `${est.id}-${evaluacion.id}`
      const nota = grupo.notas[key]
      if (nota !== undefined) {
        await axios.post('http://127.0.0.1:8000/api/docente/calificaciones/', {
          estudiante: est.id,
          evaluacion: evaluacion.id,
          nota,
        }, { headers })
      }
    }

    // Asistencia
    await axios.post('http://127.0.0.1:8000/api/docente/calificaciones/', {
      estudiante: est.id,
      evaluacion: null,
      tipo: "asistencia",
      nota: grupo.asistencia[est.id],
    }, { headers })

    // Disciplina
    await axios.post('http://127.0.0.1:8000/api/docente/calificaciones/', {
      estudiante: est.id,
      evaluacion: null,
      tipo: "disciplina",
      nota: grupo.disciplina[est.id],
    }, { headers })

    // Nota final calculada
    const notaFinal = calcularNotaFinal(grupo, est.id)
    await axios.post('http://127.0.0.1:8000/api/docente/calificaciones/', {
      estudiante: est.id,
      evaluacion: null,
      tipo: "final",
      nota: notaFinal,
    }, { headers })
  }

  alert('Notas guardadas con éxito')
}


const calcularNotaFinal = (grupo, estudianteId) => {
  const actividades = grupo.evaluaciones.filter(e => e.tipo === 'actividad')
  const examenes = grupo.evaluaciones.filter(e => e.tipo === 'examen_final')

  const avg = (arr, keyFn) => {
    const total = arr.reduce((acc, e) => acc + (keyFn(e) || 0), 0)
    return arr.length ? total / arr.length : 0
  }

  const notaActividad = avg(actividades, e => grupo.notas[`${estudianteId}-${e.id}`])
  const notaExamen = avg(examenes, e => grupo.notas[`${estudianteId}-${e.id}`])
  const notaAsistencia = grupo.asistencia[estudianteId] || 0
  const notaDisciplina = grupo.disciplina[estudianteId] || 0

  return (notaActividad * 0.6 + notaExamen * 0.2 + notaAsistencia * 0.1 + notaDisciplina * 0.1).toFixed(2)
}

onMounted(() => cargarAsignaciones())
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
.modal {
  background: rgba(255,255,255,0.9);
  padding: 1rem;
  border: 1px solid #999;
  margin-top: 1rem;
}
</style>
