<template>
  <div class="spec-builder">
    <h3 class="section-title">🛠️ Especificaciones Técnicas</h3>
    <p class="section-subtitle">Agrega las características que quieras. No hay límites.</p>

    <div v-for="(spec, index) in modelValue" :key="index" class="spec-row">
      <input 
        :value="spec.key" 
        @input="updateSpec(index, 'key', $event.target.value)"
        placeholder="Nombre (Ej: Voltaje)" 
        class="cyber-input"
      >
      <input 
        :value="spec.value" 
        @input="updateSpec(index, 'value', $event.target.value)"
        placeholder="Valor (Ej: 220V)" 
        class="cyber-input"
      >
      <button type="button" @click="removeSpec(index)" class="btn-remove" title="Eliminar">✖</button>
    </div>

    <button type="button" @click="addSpec" class="btn-add-spec">
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

<style scoped>
.spec-builder {
  background: rgba(255, 255, 255, 0.02);
  padding: 20px;
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.section-title {
  color: var(--secondary);
  margin-top: 0;
  margin-bottom: 5px;
}

.section-subtitle {
  font-size: 0.9em;
  color: var(--text-muted);
  margin-bottom: 20px;
}

.spec-row {
  display: flex;
  gap: 10px;
  margin-bottom: 10px;
}

.cyber-input {
  flex: 1;
  padding: 10px;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: white;
  border-radius: 5px;
  transition: all 0.3s;
}

.cyber-input:focus {
  border-color: var(--secondary);
  outline: none;
  box-shadow: 0 0 10px rgba(0, 242, 255, 0.1);
}

.btn-remove {
  background: rgba(255, 0, 0, 0.2);
  color: #ff4444;
  border: 1px solid rgba(255, 0, 0, 0.3);
  padding: 0 15px;
  cursor: pointer;
  border-radius: 5px;
  transition: all 0.3s;
}

.btn-remove:hover {
  background: rgba(255, 0, 0, 0.4);
  color: white;
}

.btn-add-spec {
  background: rgba(0, 242, 255, 0.1);
  color: var(--primary);
  border: 1px solid var(--primary);
  padding: 10px 20px;
  border-radius: 20px;
  cursor: pointer;
  font-weight: bold;
  width: 100%;
  margin-top: 10px;
  transition: all 0.3s;
}

.btn-add-spec:hover {
  background: var(--primary);
  color: black;
  box-shadow: 0 0 15px rgba(0, 242, 255, 0.3);
}
</style>
