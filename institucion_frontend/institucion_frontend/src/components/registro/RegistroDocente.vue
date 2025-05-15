<template>
  <div class="mb-4">
    <h3>Información adicional del docente</h3>

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
    <label>Estado del docente</label><br>
    <select :value="form.estado" @change="updateField('estado', $event.target.value)">
      <option disabled value="">Seleccione estado</option>
      <option v-for="estado in estados" :key="estado" :value="estado">
        {{ estado }}
      </option>
    </select> <br>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const props = defineProps(['modelValue'])
const emit = defineEmits(['update:modelValue'])
const form = props.modelValue

const updateField = (key, value) => {
  form[key] = value
}

// Estado: opciones fijas
const estados = ['activo', 'inactivo']

</script>
