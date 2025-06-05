<template>
  <div class="ver-estudiantes-container">
    <h2 class="info-division">Información del Docente</h2>
    <div class="info-docente">
      <p><strong>Nombre:</strong> {{ docente.nombres }} {{ docente.apellidos }}</p>
      <p><strong>Correo:</strong> {{ docente.email }}</p>
      <div v-for="(sede, index) in docente.sedes" :key="index" class="info-sede">
        <hr class="linea-divisora">
        <h4 class="info-division">Información de la sede</h4>
        <p><strong>Sede:</strong> {{ sede.nombre_sede }}</p>
        <div v-if="sede.coordinador">
          <p><strong>Coordinador de la sede:</strong> {{ sede.coordinador.nombre_completo }}</p>
          <p><strong>Correo del coordinador:</strong> {{ sede.coordinador.correo }}</p>
        </div>
        <div v-else>
          <p><em>No hay coordinador asignado.</em></p>
        </div>
      </div>
      <hr class="linea-divisora">
      <h4 class="info-division" >Información de sus grupos</h4>
      <p><strong>Materias que imparte:</strong> {{ materiasUnicas.join(', ') }}</p>
      <p><strong>Grupos asignados:</strong> {{ totalGrupos }}</p>
      <p><strong>Total de estudiantes:</strong> {{ totalEstudiantes }}</p>
    </div>

    <hr />

    <div v-for="(grupo, index) in asignaturasGrupos" :key="grupo.id" class="bloque-asignatura">
      <button @click="toggleGrupo(index)" class="btn-grupo">
        {{ grupo.asignatura.nombre }} - Grupo: {{ grupo.grupo.nombre }}
      </button>
      <div v-if="grupo.abierto" class="export-buttons">
        <button @click="exportarPDF(grupo)" class="btn-pdf">Exportar PDF</button>
        <button @click="exportarExcel(grupo)" class="btn-excel">Exportar Excel</button>
      </div>
      <div v-if="grupo.abierto">
        <div class="tabla-estudiantes-wrapper">
          <h3>Estudiantes del grupo</h3>
          <table class="tabla-estudiantes">
            <thead>
              <tr>
                <th>#</th>
                <th>Apellidos</th>
                <th>Nombres</th>
                <th>Correo</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(est, idx) in grupo.estudiantes" :key="est.id">
                <td>{{ idx + 1 }}</td>
                <td>{{ est.apellidos }}</td>
                <td>{{ est.nombres }}</td>
                <td>{{ est.correo }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import jsPDF from 'jspdf'
import autoTable from 'jspdf-autotable'
import * as XLSX from 'xlsx'
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { toast } from 'vue3-toastify'
import 'vue3-toastify/dist/index.css'
import escudo from '@/assets/images/logo.png'

const asignaturasGrupos = ref([])
const docente = ref({})
const totalEstudiantes = ref(0)
const totalGrupos = ref(0)
const materiasUnicas = ref([])

const token = localStorage.getItem('access_token')
const headers = { Authorization: `Bearer ${token}` }

const toggleGrupo = async (index) => {
  const grupo = asignaturasGrupos.value[index]
  grupo.abierto = !grupo.abierto
  if (grupo.abierto && grupo.estudiantes.length === 0) {
    await cargarDatosGrupo(index)
  }
}

const cargarDatosGrupo = async (index) => {
  try {
    const grupo = asignaturasGrupos.value[index]
    const grupoId = grupo.grupo.id
    const asigId = grupo.asignatura.id

    const res = await axios.get(
      `http://localhost:8000/api/estudiante-asignatura-curso-grado/?grupo=${grupoId}&asignatura=${asigId}`,
      { headers }
    )

    const estudiantesOrdenados = res.data
      .map(e => e.estudiante)
      .sort((a, b) => a.apellidos.localeCompare(b.apellidos))

    grupo.estudiantes.splice(0, grupo.estudiantes.length, ...estudiantesOrdenados)

    totalEstudiantes.value += estudiantesOrdenados.length
  } catch (err) {
    toast.error("Error al cargar estudiantes.")
    console.error(err)
  }
}

const cargarAsignaciones = async () => {
  try {
    const res = await axios.get('http://localhost:8000/api/docente/asignaturas-grupos/', { headers })
    totalGrupos.value = res.data.length

    const materias = new Set()

    asignaturasGrupos.value = res.data.map(item => {
      materias.add(item.asignatura.nombre)
      return {
        ...item,
        abierto: false,
        estudiantes: []
      }
    })

    materiasUnicas.value = Array.from(materias)

  } catch (err) {
    toast.error("Error al cargar asignaciones.")
    console.error(err)
  }
}

const cargarDatosDocente = async () => {
  try {
    const res = await axios.get('http://localhost:8000/api/perfil-detallado/', { headers })
    docente.value = res.data
  } catch (err) {
    toast.error("Error al obtener información del docente.")
    console.error(err)
  }
}

onMounted(() => {
  cargarDatosDocente()
  cargarAsignaciones()
})


const exportarPDF = (grupo) => {
  const doc = new jsPDF()

  doc.addImage(escudo, 'PNG', 15, 10, 25, 25)
  // Estilo institucional
  doc.setFontSize(16)
  doc.text('INSTITUCIÓN EDUCATIVA INDÍGENA N°1', 105, 20, { align: 'center' })
  doc.setFontSize(12)
  doc.text(`Listado de Estudiantes - ${grupo.asignatura.nombre}`, 105, 30, { align: 'center' })
  doc.text(`Grupo: ${grupo.grupo.nombre}`, 105, 38, { align: 'center' })
  doc.text(`Fecha: ${new Date().toLocaleDateString()}`, 14, 50)
  doc.text('Marque las asistencias en los campos A1 a A10', 14, 54)

  // Encabezados de la tabla: datos + 10 columnas de asistencia
  const asistenciaHeaders = Array.from({ length: 10 }, (_, i) => `A${i + 1}`)
  const tableHead = [['#', 'Apellidos', 'Nombres', 'Correo', ...asistenciaHeaders]]

  // Filas: datos + 10 celdas vacías
  const rows = grupo.estudiantes.map((est, i) => [
    i + 1,
    est.apellidos,
    est.nombres,
    est.correo,
    ...Array(10).fill('')
  ])

  autoTable(doc, {
    head: tableHead,
    body: rows,
    startY: 55,
    margin: { left: 14, right: 14 },
    styles: {
      fontSize: 10
    }
  })

  // Abrir en nueva pestaña
  const pdfBlob = doc.output('blob')
  const blobUrl = URL.createObjectURL(pdfBlob)
  window.open(blobUrl)
}



const exportarExcel = (grupo) => {
  const data = grupo.estudiantes.map((est, i) => ({
    '#': i + 1,
    Apellidos: est.apellidos,
    Nombres: est.nombres,
    Correo: est.correo
  }))

  const worksheet = XLSX.utils.json_to_sheet(data)
  const workbook = XLSX.utils.book_new()
  XLSX.utils.book_append_sheet(workbook, worksheet, 'Estudiantes')

  const nombreArchivo = `estudiantes_${grupo.grupo.nombre}_${grupo.asignatura.nombre}.xlsx`
  XLSX.writeFile(workbook, nombreArchivo)
}

</script>

<style scoped>
.ver-estudiantes-container {
  padding: 1rem;
  background-color: #f9f9f9;
  border-radius: 10px;
}
.info-docente {
  width: 900px;
  background-color: #fffaf7;
  padding: 24px;
  border-left: 4px solid #ffc107;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  transition: box-shadow 0.3s ease-in-out;
  margin-top: 1rem;

}
.info-docente:hover {
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}
.info-docente p {
  font-size: 1rem;
  color: #333;
  margin: 8px 0;
  transition: background-color 0.3s ease, transform 0.3s ease;
}

.info-docente p:hover {
  background-color: #fff3da;
  transform: translateX(4px);
}

.info-docente strong {
  color: #222;
}

.linea-divisora {
  border: none;
  border-top: 1px solid #ddd;
  margin: 16px 0;
}
.info-division{
  color: #f54646;
  position: relative;

}
.info-division:hover{
  color: #ffc107;
}

.info-sede {
  margin-top: 8px;
}
.bloque-asignatura {
  margin-bottom: 1.5rem;
  border: 1px solid #ccc;
  padding: 1rem;
  border-radius: 8px;
  
}
.bloque-asignatura:hover{
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  transition: box-shadow 0.3s ease-in-out;
}

.btn-grupo {
  margin: 1rem;
  background-color: #FFBA08;
  border: none;
  padding: 10px;
  font-weight: bold;
  cursor: pointer;
  border-radius: 6px;
}
.btn-grupo:hover{
  background-color: #f54646;
  color: #fff;
}
.tabla-estudiantes-wrapper {
  margin-top: 20px;
  background-color: #fffdf8;
  border-left: 4px solid #f54646;
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
  overflow-x: auto;
}

.tabla-estudiantes-wrapper h3 {
  margin-bottom: 12px;
  font-size: 1.2rem;
  color: #444;
}

.tabla-estudiantes {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.95rem;
  background-color: #fff;
}

.tabla-estudiantes th {
  background-color: #f9f9f9;
  color: #222;
  text-align: left;
  padding: 10px;
  font-weight: bold;
  border-bottom: 2px solid #ddd;
}

.tabla-estudiantes td {
  padding: 10px;
  border-bottom: 1px solid #eee;
  color: #333;
  transition: background-color 0.3s ease;
}

.tabla-estudiantes tr:hover td {
  background-color: #fff3da;
}

.export-buttons {
  margin-top: 10px;
}
.btn-pdf {
  background-color: #f54646;
  color: white;
  border: none;
  padding: 8px 12px;
  border-radius: 6px;
  cursor: pointer;
  margin-right: 10px;
}
.btn-excel {
  background-color: #008000;
  color: white;
  border: none;
  padding: 8px 12px;
  border-radius: 6px;
  cursor: pointer;
  margin-right: 10px;
} 
.btn-pdf:hover, .btn-excel:hover {
  opacity: 0.9;
  transform: translateY(-2px);
  background-color: #FFBA08;
}
@media (max-width: 600px) {
  .tabla-estudiantes th, .tabla-estudiantes td {
    padding: 8px 6px;
    font-size: 0.85rem;
  }
}

</style>
