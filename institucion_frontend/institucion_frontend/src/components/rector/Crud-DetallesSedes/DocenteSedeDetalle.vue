<template>
  <div class="docente-detalle-wrapper">
    <h2>Docentes asignados a la sede</h2>
    <div v-if="loading" class="loading">Cargando docentes...</div>
    <div v-else>
      <button class="btn-asignar" @click="mostrarFormNuevo ? cancelarEdicion() : abrirAsignar()">
        <span v-if="!mostrarFormNuevo"> + Asignar docentes a esta sede </span>
        <span v-else>Cancelar</span>
      </button>
      <!-- Modal de asignación de docentes -->
      <div v-if="mostrarFormNuevo" class="asignar-modal">
        <h3>Asignar docentes a esta sede</h3>
        <div v-if="loadingDisponibles" class="loading">Cargando docentes disponibles...</div>
        <div v-else class="docentes-grid">
          <div v-for="doc in docentesDisponibles || []" :key="doc.id" class="docente-box">
            <label>
              <input type="checkbox" v-model="seleccionados" :value="doc.id" />
              <div class="docente-info">
                <div class="docente-nombre">{{ doc.nombres }} {{ doc.apellidos }}</div>
                <div class="docente-email">{{ doc.correo }}</div>
              </div>
            </label>
          </div>
        </div>
        <div class="form-actions">
          <button class="btn-guardar" @click="asignarDocentes">Guardar</button>
          <button class="btn-cancelar" @click="cancelarEdicion">Cancelar</button>
        </div>
      </div>
      <table class="tabla-docentes">
        <thead>
          <tr>
            <th>#</th>
            <th>Nombre</th>
            <th>Email</th>
            <th>Estado</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(docente, idx) in docentes || []" :key="docente.id">
            <td>{{ idx + 1 }}</td>
            <td>{{ docente.nombres }} {{ docente.apellidos }}</td>
            <td>{{ docente.correo }}</td>
            <td>
              <span :class="['docente-estado', docente.estado === 'activo' ? 'activo' : 'inactivo']">
                {{ docente.estado }}
              </span>
            </td>
            <td class="acciones-td">
              <button class="btn-icon" @click="editarDocente(docente)" title="Editar">
                <svg width="20" height="20" fill="none" viewBox="0 0 24 24"><path stroke="#2563eb" stroke-width="2" d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4 12.5-12.5Z"/></svg>
              </button>
              <button class="btn-icon eliminar" @click="eliminarDocente(docente)" title="Eliminar">
                <svg width="20" height="20" fill="none" viewBox="0 0 24 24"><path stroke="#ef4444" stroke-width="2" d="M6 7h12M9 7V5a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2m2 0v12a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2V7h12Z"/></svg>
              </button>
              <button class="btn-icon rendimiento" @click="verRendimiento(docente)" title="Ver rendimiento">
                <svg width="20" height="20" fill="none" viewBox="0 0 24 24"><path stroke="#34d399" stroke-width="2" d="M4 17v2a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1v-2M7 11l3 3 7-7"/></svg>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      
      <div v-if="docenteEditando" class="form-modal">
        <form @submit.prevent="guardarDocente">
          <h3>Editar docente</h3>
          <div class="form-group">
            <label>Nombres</label>
            <input v-model="form.nombres" required />
          </div>
          <div class="form-group">
            <label>Apellidos</label>
            <input v-model="form.apellidos" required />
          </div>
          <div class="form-group">
            <label>Email</label>
            <input v-model="form.correo" type="email" required />
          </div>
          <div class="form-group">
            <label>Tipo de documento</label>
            <input v-model="form.tipo_documento" required />
          </div>
          <div class="form-group">
            <label>Número de documento</label>
            <input v-model="form.numero_documento" required />
          </div>
          <div class="form-group">
            <label>Sexo</label>
            <select v-model="form.sexo" required>
              <option value="M">Masculino</option>
              <option value="F">Femenino</option>
              <option value="O">Otro</option>
            </select>
          </div>
          <div class="form-group">
            <label>Teléfono</label>
            <input v-model="form.telefono" />
          </div>
          <div class="form-group">
            <label>Dirección</label>
            <input v-model="form.direccion" />
          </div>
          <div class="form-group">
            <label>Fecha de nacimiento</label>
            <input v-model="form.fecha_nacimiento" type="date" required />
          </div>
          <div class="form-group">
            <label>Estado</label>
            <select v-model="form.estado" required>
              <option value="activo">Activo</option>
              <option value="inactivo">Inactivo</option>
            </select>
          </div>
          <!-- <div class="form-group">
            <label>Sedes asignadas</label>
            <div class="checkbox-grid">
              <label v-for="sede in sedes || []" :key="sede.codigo_dane">
                <input
                  type="checkbox"
                  :value="sede.codigo_dane"
                  v-model="form.sedes"
                />
                {{ sede.nombre }}
              </label>
            </div>
          </div>
          <div class="form-group">
            <label>Materias a asignar</label>
            <div class="checkbox-grid">
              <label v-for="asig in asignaturas || []" :key="asig.id">
                <input
                  type="checkbox"
                  :value="asig.id"
                  v-model="form.materias"
                />
                {{ asig.nombre }}
              </label>
            </div>
          </div>
          <div class="form-group">
            <label>Grupos a asignar</label>
            <div class="checkbox-grid">
              <label v-for="grupo in grupos || []" :key="grupo.id">
                <input
                  type="checkbox"
                  :value="grupo.id"
                  v-model="form.grupos"
                />
                {{ grupo.nombre }} ({{ grupo.grado_nombre }})
              </label>
            </div>
          </div> -->
          <div class="form-actions">
            <button class="btn-guardar" type="submit">Guardar</button>
            <button class="btn-cancelar" type="button" @click="cancelarEdicion">Cancelar</button>
          </div>
        </form>
      </div>
      <div v-if="docenteRendimiento && docenteRendimiento.rendimiento" class="rendimiento-modal">
        <h3>Rendimiento de {{ docenteRendimiento.nombres }} {{ docenteRendimiento.apellidos }}</h3>
        <ul>
          <li v-for="item in docenteRendimiento.rendimiento || []" :key="item.id">
            {{ item.descripcion }}: <strong>{{ item.valor }}</strong>
          </li>
        </ul>
        <button @click="docenteRendimiento = null">Cerrar</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import axios from 'axios'
import { toast } from 'vue3-toastify'


const props = defineProps({ sedeCodigoDane: { type: String, required: true } })
const docentes = ref([])
const docentesDisponibles = ref([])
const seleccionados = ref([])
const sedes = ref([])
const asignaturas = ref([])
const grupos = ref([])
const loading = ref(true)
const mostrarFormNuevo = ref(false)
const docenteEditando = ref(null)
const docenteRendimiento = ref(null)
const loadingDisponibles = ref(false)
const form = ref({
  nombres: '',
  apellidos: '',
  correo: '',
  tipo_documento: '',
  numero_documento: '',
  sexo: '',
  telefono: '',
  direccion: '',
  fecha_nacimiento: '',
  estado: 'activo',
  sedes: [],
  materias: [],
  grupos: [],
})

async function cargarDatos() {
  loading.value = true
  try {
    const token = localStorage.getItem('access_token')
    // Solo docentes de la sede actual
    const resDoc = await axios.get(`http://localhost:8000/api/docentes/?sede=${props.sedeCodigoDane}`, { headers: { Authorization: `Bearer ${token}` } })
    const [resSedes, resAsig, resGrupos] = await Promise.all([
      axios.get('http://localhost:8000/api/sedes/', { headers: { Authorization: `Bearer ${token}` } }),
      axios.get('http://localhost:8000/api/asignaturas/', { headers: { Authorization: `Bearer ${token}` } }),
      axios.get(`http://localhost:8000/api/grupos/?sede=${props.sedeCodigoDane}`, { headers: { Authorization: `Bearer ${token}` } }),
    ])
    docentes.value = resDoc.data
    sedes.value = resSedes.data
    asignaturas.value = resAsig.data
    grupos.value = resGrupos.data.map(g => ({ ...g, grado_nombre: g.grado?.nombre || '' }))
    loading.value = false
  } catch (err) {
    toast.error('Error al cargar datos de docentes')
    loading.value = false
  }
}

function abrirAsignar() {
  mostrarFormNuevo.value = true
  seleccionados.value = []
}

async function cargarDocentesDisponibles() {
  loadingDisponibles.value = true
  try {
    const token = localStorage.getItem('access_token')
    const res = await axios.get(`http://localhost:8000/api/docentes/disponibles/?sede=${props.sedeCodigoDane}`, { headers: { Authorization: `Bearer ${token}` } })
    docentesDisponibles.value = res.data
    loadingDisponibles.value = false
  } catch (err) {
    toast.error('Error al cargar docentes disponibles')
    loadingDisponibles.value = false
  }
}

watch(mostrarFormNuevo, (nuevo) => {
  if (nuevo) {
    cargarDocentesDisponibles()
    seleccionados.value = []
  }
})

async function asignarDocentes() {
  if (!seleccionados.value.length) {
    toast.error('Seleccione al menos un docente')
    return
  }
  const token = localStorage.getItem('access_token')
  try {
    const response = await axios.post('http://localhost:8000/api/docentes/asignar-sede/', {
      sede: props.sedeCodigoDane,
      docentes: seleccionados.value
    }, {
      headers: { Authorization: `Bearer ${token}` }
    })

    toast.success('Docentes asignados')


    docentes.value = response.data.docentes

    mostrarFormNuevo.value = false
    seleccionados.value = []

  } catch (err) {
    console.error(err)
    toast.error('No se pudo asignar docentes')
  }
}


onMounted(cargarDatos)

function editarDocente(docente) {
  docenteEditando.value = docente
  mostrarFormNuevo.value = false
  Object.assign(form.value, docente)
}

function cancelarEdicion() {
  docenteEditando.value = null
  mostrarFormNuevo.value = false
  form.value = {
    nombres: '', apellidos: '', correo: '', tipo_documento: '', numero_documento: '', sexo: '', telefono: '', direccion: '', fecha_nacimiento: '', estado: 'activo', sedes: [], materias: [], grupos: []
  }
}

async function guardarDocente() {
  const token = localStorage.getItem('access_token')
  try {
    if (docenteEditando.value) {
      await axios.put(`http://localhost:8000/api/docentes/${docenteEditando.value.id}/`, form.value, { headers: { Authorization: `Bearer ${token}` } })
      toast.success('Docente actualizado')
    } else {
      await axios.post('http://localhost:8000/api/docentes/', form.value, { headers: { Authorization: `Bearer ${token}` } })
      toast.success('Docente creado')
    }
    cancelarEdicion()
    cargarDatos()
  } catch (err) {
    toast.error('Error al guardar docente')
  }
}

async function eliminarDocente(docente) {
  if (!window.confirm('¿Eliminar este docente?')) return
  const token = localStorage.getItem('access_token')
  try {
    await axios.delete(`http://localhost:8000/api/docentes/${docente.id}/`, { headers: { Authorization: `Bearer ${token}` } })
    toast.success('Docente eliminado')
    cargarDatos()
  } catch (err) {
    toast.error('No se pudo eliminar el docente')
  }
}

async function verRendimiento(docente) {
  const token = localStorage.getItem('access_token')
  try {
    const res = await axios.get(`http://localhost:8000/api/docentes/${docente.id}/rendimiento/`, { headers: { Authorization: `Bearer ${token}` } })
    docenteRendimiento.value = { ...docente, rendimiento: res.data }
  } catch (err) {
    toast.error('No se pudo cargar el rendimiento')
  }
}
</script>

<style scoped>
.docente-detalle-wrapper {
  max-width: 900px;
  margin: 2rem auto;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(27,27,30,0.07);
  padding: 2rem 1.5rem;
}
.btn-asignar {
  background: var(--primary-color, #2563eb);
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 0.6rem 1.2rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  margin-bottom: 1.2rem;
  transition: background 0.2s;
}
.btn-asignar:hover {
  background: var(--secondary-color, #60a5fa);
}
.tabla-docentes {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 1.5rem;
}
.tabla-docentes th, .tabla-docentes td {
  padding: 0.7rem 1rem;
  border-bottom: 1px solid #e5e7eb;
  text-align: left;
}
.tabla-docentes th {
  background: #f3f4f6;
  color: #2563eb;
  font-weight: 700;
}
.tabla-docentes tr:last-child td {
  border-bottom: none;
}
.docente-estado.activo {
  color: #059669;
  font-weight: bold;
}
.docente-estado.inactivo {
  color: #ef4444;
  font-weight: bold;
}
.acciones-td {
  display: flex;
  gap: 0.5rem;
}
.btn-icon {
  background: none;
  border: none;
  padding: 0.2rem;
  cursor: pointer;
  border-radius: 50%;
  transition: background 0.2s;
}
.btn-icon:hover {
  background: #e0e7ff;
}
.btn-icon.eliminar:hover {
  background: #fee2e2;
}
.btn-icon.rendimiento:hover {
  background: #d1fae5;
}
.asignar-modal {
  background: #f9fafb;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(27,27,30,0.07);
  padding: 1.2rem 1.5rem;
  width: 100%;
  max-width: 600px;
  margin: 2rem auto;
}
.docentes-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1rem;
  margin-bottom: 1.2rem;
}
.docente-box {
  background: #fff;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  padding: 0.8rem 1rem;
  display: flex;
  align-items: center;
  transition: box-shadow 0.2s;
}
.docente-box:hover {
  box-shadow: 0 2px 8px rgba(27,27,30,0.10);
}
.docente-info {
  margin-left: 0.7rem;
}
.docente-nombre {
  font-weight: 600;
  color: #2563eb;
}
.docente-email {
  font-size: 0.95rem;
  color: #6b7280;
}
.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}
.btn-guardar {
  background: #34d399;
  color: #fff;
}
.btn-cancelar {
  background: #d1d5db;
  color: #222;
}
.loading {
  color: #2563eb;
  font-weight: 500;
}
.form-modal {
  background: #f9fafb;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(27,27,30,0.07);
  padding: 1.2rem 1.5rem;
  width: 100%;
  max-width: 500px;
  margin: 2rem auto;
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
.rendimiento-modal {
  background: #f3f4f6;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(27,27,30,0.07);
  padding: 1.2rem 1.5rem;
  width: 100%;
  max-width: 400px;
  margin: 2rem auto;
}
.checkbox-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 0.8rem;
}
</style>
