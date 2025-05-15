<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const props = defineProps(['modelValue'])
const emit = defineEmits(['update:modelValue'])
const form = props.modelValue

const updateField = (key, value) => {
  form[key] = value
}

// Estado: opciones fijas
const estados = ['activo', 'inactivo', 'graduado']

// Grupo: se carga desde backend
const grupos = ref([])

onMounted(async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/api/grupos/') 
    grupos.value = response.data  // [{ id, nombre }]
    console.log('Grupos cargados:', response.data)

  } catch (error) {
    console.error('Error al cargar los grupos:', error)
  }

})
</script>

<template>
  <div>
    <h3>Información adicional del estudiante</h3>

    <label>Tipo de documento</label><br>
    <select :value="form.tipo_documento" @change="updateField('tipo_documento', $event.target.value)">
    <option disabled value="">Seleccione tipo de documento</option>
    <option value="C.C">C.C</option>
    <option value="T.I">T.I</option>
</select><br>

    <label>Número de documento</label><br>
    <input
      :value="form.documento"
      @input="updateField('documento', $event.target.value)"
      placeholder="Número de documento"
    /> <br>

    <label>Número de telefono</label><br>
    <input
      :value="form.telefono"
      @input="updateField('telefono', $event.target.value)"
      placeholder="Teléfono"
    /> <br>

    <label>Dirección</label><br>
    <input
      :value="form.direccion"
      @input="updateField('direccion', $event.target.value)"
      placeholder="Dirección"
    /> <br>

    <label>Fecha de nacimiento</label><br>
    <input
      :value="form.fecha_nacimiento"
      @input="updateField('fecha_nacimiento', $event.target.value)"
      type="date"
      placeholder="Fecha de nacimiento"
    /> <br>

    <!-- Select para estado -->
    <label>Estado del estudiante</label><br>
    <select :value="form.estado" @change="updateField('estado', $event.target.value)">
      <option disabled value="">Seleccione estado</option>
      <option v-for="estado in estados" :key="estado" :value="estado">
        {{ estado }}
      </option>
    </select> <br>

    <!-- Select para grupo -->
     <label>Grupo del estudiante</label><br>
    <select :value="form.grupo" @change="updateField('grupo', $event.target.value)">
      <option disabled value="">Seleccione grupo</option>
      <option v-for="grupo in grupos" :key="grupo.id" :value="grupo.id">
        {{ grupo.nombre }}
      </option>
    </select><br>
  </div>
</template>


<style scoped>
select option {
  color: black;
  background-color: white;
}
</style>