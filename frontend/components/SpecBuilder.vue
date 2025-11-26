<template>
  <div>
    <h3>🛠️ Especificaciones Técnicas</h3>
    <p style="font-size: 0.9em; color: #666;">Agrega las características que quieras. No hay límites.</p>

    <div v-for="(spec, index) in modelValue" :key="index" style="display: flex; gap: 10px; margin-bottom: 10px;">
      <input 
        :value="spec.key" 
        @input="updateSpec(index, 'key', $event.target.value)"
        placeholder="Nombre (Ej: Voltaje)" 
        style="flex: 1; padding: 5px;"
      >
      <input 
        :value="spec.value" 
        @input="updateSpec(index, 'value', $event.target.value)"
        placeholder="Valor (Ej: 220V)" 
        style="flex: 1; padding: 5px;"
      >
      <button type="button" @click="removeSpec(index)" style="background: #ff4444; color: white; border: none; padding: 5px 10px; cursor: pointer;">X</button>
    </div>

    <button type="button" @click="addSpec" style="background: #28a745; color: white; border: none; padding: 5px 10px; cursor: pointer; margin-bottom: 20px;">
      + Agregar Característica
    </button>
  </div>
</template>

<script setup>
const props = defineProps({
  modelValue: {
    type: Array,
    required: true,
    default: () => []
  }
});

const emit = defineEmits(['update:modelValue']);

const addSpec = () => {
  const newSpecs = [...props.modelValue, { key: '', value: '' }];
  emit('update:modelValue', newSpecs);
};

const removeSpec = (index) => {
  const newSpecs = [...props.modelValue];
  newSpecs.splice(index, 1);
  emit('update:modelValue', newSpecs);
};

const updateSpec = (index, field, value) => {
  const newSpecs = [...props.modelValue];
  newSpecs[index] = { ...newSpecs[index], [field]: value };
  emit('update:modelValue', newSpecs);
};
</script>
