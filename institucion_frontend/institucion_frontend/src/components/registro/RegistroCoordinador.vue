<template>
  <div class="space-y-4">
    <div>
      <h3>Información adicional del coordinador</h3>

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

     <label>Sexo</label><br>
      <select :value="form.sexo" @change="updateField('sexo', $event.target.value)">
        <option disabled value="">Seleccione el sexo</option>
        <option value="M">M (masculino)</option>
        <option value="F">F (Femenino)</option>
      </select><br>

     <label>Sedes disponibles</label><br>
    <select :value="form.sede" @change="updateField('sede', $event.target.value)">
      <option disabled value="">Seleccione la sede</option>
      <option v-for="sede in sedes" :key="sede.codigo_dane" :value="sede.codigo_dane">
        {{ sede.nombre }}
      </option>
    </select><br> 

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const props = defineProps(['modelValue'])
const emit = defineEmits(['update:modelValue'])
const form = props.modelValue

const updateField = (key, value) => {
  form[key] = value
}



const sedes = ref([])

onMounted(async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/api/sedes/') 
    sedes.value = response.data  // [{ codigo_dane, nombre }]
    console.log('Sedes cargadas:', response.data)

  } catch (error) {
    console.error('Error al cargar las sedes:', error)
  }

})
</script>
