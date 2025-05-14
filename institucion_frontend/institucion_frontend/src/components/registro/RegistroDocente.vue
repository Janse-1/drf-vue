<script setup>
import { computed } from 'vue';
import { useVModel } from '@vueuse/core';

const props = defineProps(['modelValue']);
const emit = defineEmits(['update:modelValue']);
const form = useVModel(props, 'modelValue', emit);
</script>

<template>
  <div>
    <h3>Información del docente</h3>
    <input v-model="form.codigo_docente" placeholder="Código del docente" />
    <input v-model="form.titulo" placeholder="Título profesional" />
  </div>
</template>

<style scoped></style>