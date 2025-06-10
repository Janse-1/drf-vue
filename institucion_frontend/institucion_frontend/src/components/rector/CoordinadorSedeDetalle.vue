<template>
  <div class="coordinador-detalle-card" v-if="coordinador">
    <h2 class="coordinador-title">Coordinador</h2>
    <div v-if="!editandoDatos">
      <div class="coordinador-info">
        <p><strong>Nombre:</strong> {{ coordinador.nombres + ' ' + coordinador.apellidos }}</p>
        <p><strong>Email:</strong> {{ coordinador.correo?.trim() !== '' ? coordinador.correo : 'No disponible' }}</p>
        <p><strong>Teléfono:</strong> {{ coordinador.telefono?.trim() !== '' ? coordinador.telefono : 'No disponible' }}</p>

      </div>
      <div class="coordinador-actions">
        <button class="btn-cambiar" @click.stop="mostrarFormCambiar = !mostrarFormCambiar">Cambiar coordinador</button>
        <button class="btn-editar" @click.stop="editandoDatos = true">Editar datos</button>
        <button class="btn-eliminar" @click.stop="confirmarEliminar">Eliminar coordinador</button>
      </div>
      <div v-if="mostrarFormCambiar" class="cambiar-coord-form">
        <form @submit.prevent="cambiarCoordinador">
          <label>Selecciona un nuevo coordinador:</label>
          <select v-model="nuevoCoordinadorId" required>
            <optgroup label="Disponibles">
              <option v-for="coord in coordinadoresDisponibles" :key="coord.id" :value="coord.id">
                {{ coord.nombres }} {{ coord.apellidos }} (Disponible)
              </option>
            </optgroup>
            <optgroup label="Ocupados">
              <option v-for="coord in coordinadoresOcupados" :key="coord.id" :value="coord.id">
                {{ coord.nombres }} {{ coord.apellidos }} (Asignado a otra sede)
              </option>
            </optgroup>
          </select>
          <button class="btn-guardar" type="submit">Confirmar cambio</button>
          <button class="btn-cancelar" type="button" @click="mostrarFormCambiar = false">Cancelar</button>
        </form>
      </div>
    </div>
    <div v-else>
      <form @submit.prevent="guardarEdicion">
        <h4 class="info-obligatoria">Los campos con <span class="obligatorio">*</span> son obligatorios</h4>
        <div class="form-group">
          <label>Tipo de documento<span class="obligatorio">*</span></label>
          <input v-model="form.tipo_documento" required />
        </div>
        <div class="form-group">
          <label>Número de documento<span class="obligatorio">*</span></label>
          <input v-model="form.numero_documento" required />
        </div>
        <div class="form-group">
          <label>Nombres<span class="obligatorio">*</span></label>
          <input v-model="form.nombres" required />
        </div>
        <div class="form-group">
          <label>Apellidos<span class="obligatorio">*</span></label>
          <input v-model="form.apellidos" required />
        </div>
        <div class="form-group">
          <label>Sexo<span class="obligatorio">*</span></label>
          <select v-model="form.sexo" required>
            <option value="M">Masculino</option>
            <option value="F">Femenino</option>
            <option value="O">Otro</option>
          </select>
        </div>
        <div class="form-group">
          <label>Teléfono<span class="obligatorio">*</span></label>
          <input v-model="form.telefono" />
        </div>
        <div class="form-group">
          <label>Email<span class="obligatorio">*</span></label>
          <input v-model="form.correo" type="email" required />
        </div>
        <div class="form-group">
          <label>Dirección<span class="obligatorio">*</span></label>
          <input v-model="form.direccion" />
        </div>
        <div class="form-group">
          <label>Fecha de nacimiento<span class="obligatorio">*</span></label>
          <input v-model="form.fecha_nacimiento" required />
        </div>
        <div class="form-group">
          <label>Estado<span class="obligatorio">*</span></label>
          <select v-model="form.estado" required>
            <option value="activo">Activo</option>
            <option value="inactivo">Inactivo</option>
          </select>
        </div>
        <button class="btn-guardar" type="submit">Guardar</button>
        <button class="btn-cancelar" type="button" @click="cancelarEdicion">Cancelar</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import axios from 'axios'
import { toast } from 'vue3-toastify'
const props = defineProps({
  coordinador: { type: Object, required: true },
  sedeCodigoDane: { type: String, required: true }
})

const emit = defineEmits(['actualizar'])

const coordinadoresDisponibles = ref([])
const coordinadoresOcupados = ref([])
const mostrarFormCambiar = ref(false)
const nuevoCoordinadorId = ref('')
const editandoDatos = ref(false)
const form = ref({
  tipo_documento: '',
  numero_documento: '',
  nombres: '',
  apellidos: '',
  sexo: '',
  telefono: '',
  correo: '',
  direccion: '',
  fecha_nacimiento: '',
  estado: 'activo',
})

function cargarDatosForm() {
  if (!props.coordinador) return
  form.value = {
    tipo_documento: props.coordinador.tipo_documento || '',
    numero_documento: props.coordinador.numero_documento || '',
    nombres: props.coordinador.nombres || '',
    apellidos: props.coordinador.apellidos || '',
    sexo: props.coordinador.sexo || '',
    telefono: props.coordinador.telefono || '',
    correo: props.coordinador.correo || '',
    direccion: props.coordinador.direccion || '',
    fecha_nacimiento: props.coordinador.fecha_nacimiento || '',
    estado: props.coordinador.estado || 'activo',
  }
}

watch(() => props.coordinador, cargarDatosForm, { immediate: true })
onMounted(cargarDatosForm)


async function cargarCoordinadores() {
  try {
    const token = localStorage.getItem('access_token')
    const res = await axios.get('http://localhost:8000/api/coordinadores/disponibles-ocupados/', {
    headers: { Authorization: `Bearer ${token}` }
  })

    coordinadoresDisponibles.value = res.data.disponibles || res.data // soporta ambos formatos
    coordinadoresOcupados.value = res.data.ocupados || []
  } catch (err) {
    toast.error('Error al cargar coordinadores')
  }
}

watch(mostrarFormCambiar, (val) => {
  if (val) cargarCoordinadores()
})

async function cambiarCoordinador() {
  if (!nuevoCoordinadorId.value) return
  if (!window.confirm('¿Está seguro de cambiar el coordinador de esta sede?')) return
  try {
    const token = localStorage.getItem('access_token')
    await axios.post('http://localhost:8000/api/asignar-coordinador-sede/', {
      coordinador: nuevoCoordinadorId.value,
      sede: props.sedeCodigoDane
    }, {
      headers: { Authorization: `Bearer ${token}` }
    })
    toast.success('Coordinador cambiado correctamente')
    mostrarFormCambiar.value = false
    // Notificar al padre para que recargue los datos
    emit('actualizar')
  } catch (err) {
    toast.error('No se pudo cambiar el coordinador')
  }
}

function confirmarEliminar() {
  if (!window.confirm('¿Está seguro de dejar la sede sin coordinador?')) return
  eliminarCoordinador()
}

async function eliminarCoordinador() {
  try {
    const token = localStorage.getItem('access_token')
    await axios.post('http://localhost:8000/api/asignar-coordinador-sede/', {
      coordinador: null,
      sede: props.sedeCodigoDane
    }, {
      headers: { Authorization: `Bearer ${token}` }
    })
    toast.success('La sede ahora no tiene coordinador asignado')
    emit('actualizar')
  } catch (err) {
    toast.error('No se pudo eliminar el coordinador')
  }
}

function cancelarEdicion() {
  editandoDatos.value = false
}

async function guardarEdicion() {
  if (!window.confirm('¿Guardar cambios en los datos del coordinador?')) return
  try {
    const token = localStorage.getItem('access_token')
    await axios.put(`http://localhost:8000/api/coordinadores/${props.coordinador.id}/`, form.value, {
     headers: { Authorization: `Bearer ${token}` }
    })

    toast.success('Datos actualizados')
    editandoDatos.value = false
    emit('actualizar')
  } catch (err) {
    console.log('Datos enviados:', JSON.stringify(form.value, null, 2))
    console.error('Error al guardar:', err.response?.data || err)
    toast.error('No se pudieron guardar los cambios')
  }
}
</script>

<style scoped>
.coordinador-detalle-card {
  background: #f9fafb;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(27,27,30,0.07);
  padding: 1.5rem 1.2rem;
  margin: 1rem 0;
}
.coordinador-title {
  font-size: 1.2rem;
  font-weight: bold;
  color: var(--primary-color, #2563eb);
  margin-bottom: 1rem;
}
.coordinador-info p {
  margin: 0.2rem 0;
}
.coordinador-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}
.btn-editar, .btn-cambiar, .btn-eliminar, .btn-guardar, .btn-cancelar {
  border: none;
  border-radius: 8px;
  padding: 0.5rem 1.1rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}
.btn-editar {
  background: #60a5fa;
  color: #fff;
}
.btn-editar:hover {
  background: #2563eb;
}
.btn-cambiar {
  background: #fbbf24;
  color: #fff;
}
.btn-cambiar:hover {
  background: #f59e42;
}
.btn-eliminar {
  background: #ef4444;
  color: #fff;
}
.btn-eliminar:hover {
  background: #b91c1c;
}
.btn-guardar {
  background: #34d399;
  color: #fff;
}
.btn-guardar:hover {
  background: #059669;
}
.btn-cancelar {
  background: #d1d5db;
  color: #222;
}
.btn-cancelar:hover {
  background: #9ca3af;
}
.cambiar-coord-form {
  margin-top: 1rem;
  background: #f3f4f6;
  border-radius: 8px;
  padding: 1rem;
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
