<script setup>
import { ref } from 'vue'
import axios from 'axios'

const props = defineProps(['modelValue'])
const emit = defineEmits(['update:modelValue'])
const form = props.modelValue

const updateField = (key, value) => {
  form[key] = value
}

</script>

<template>
  <div>
    <h3>Información del padre de familia</h3>
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
  </div>
</template>
