<script setup>
const props = defineProps(['modelValue'])
const emit = defineEmits(['update:modelValue'])

const form = props.modelValue

const updateField = (key, value) => {
  emit('update:modelValue', { ...form, [key]: value })
}
</script>

<template>
  <div>
    <h3>Información del padre de familia</h3>
    <input :value="form.telefono" @input="updateField('telefono', $event.target.value)" placeholder="Teléfono" />
    <input :value="form.direccion" @input="updateField('direccion', $event.target.value)" placeholder="Dirección" />
  </div>
</template>
