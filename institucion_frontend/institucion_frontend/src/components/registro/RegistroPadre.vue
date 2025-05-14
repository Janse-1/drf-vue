<script setup>
import { computed } from 'vue';
import { useVModel } from '@vueuse/core';

const props = defineProps(['modelValue']);
const emit = defineEmits(['update:modelValue']);
const form = useVModel(props, 'modelValue', emit);
</script>

<template>
  <div>
    <h3>Información del padre de familia</h3>
    <input v-model="form.ocupacion" placeholder="Ocupación" />
    <input v-model="form.telefono" placeholder="Teléfono" />
    <input v-model="form.direccion" placeholder="Dirección" />
  </div>
</template>
