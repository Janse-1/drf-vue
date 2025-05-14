<script setup>
import { computed } from 'vue';
import { useVModel } from '@vueuse/core';

const props = defineProps(['modelValue']);
const emit = defineEmits(['update:modelValue']);
const form = useVModel(props, 'modelValue', emit);
</script>

<template>
  <div>
    <h3>Información del coordinador</h3>
    <input v-model="form.codigo_coordinador" placeholder="Código del coordinador" />
  </div>
</template>
