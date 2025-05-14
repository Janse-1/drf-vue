<script setup>
import { computed } from 'vue';
import { useVModel } from '@vueuse/core';

const props = defineProps(['modelValue']);
const emit = defineEmits(['update:modelValue']);
const form = useVModel(props, 'modelValue', emit);
</script>

<template>
  <div>
    <h3>Información del estudiante</h3>
    <input v-model="form.codigo_estudiante" placeholder="Código del estudiante" />
    <input v-model="form.telefono" placeholder="Teléfono" />
    <input v-model="form.direccion" placeholder="Dirección" />
  </div>
</template>
