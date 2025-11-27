<template>
  <form @submit.prevent="handleSubmit" class="cyber-form">
    <!-- Datos Básicos -->
    <div class="form-section">
      <div class="input-group">
        <label>Nombre del Equipo</label>
        <input v-model="form.nombre" type="text" required placeholder="Ej: Transmisor de Presión PT-101">
      </div>
      
      <div class="row">
        <div class="input-group">
          <label>Marca</label>
          <input v-model="form.marca" type="text" required placeholder="Ej: Rosemount">
        </div>
        <div class="input-group">
          <label>Modelo</label>
          <input v-model="form.modelo" type="text" required placeholder="Ej: 3051S">
        </div>
      </div>

      <div class="row">
        <div class="input-group">
          <label>Cantidad</label>
          <input v-model="form.cantidad" type="number" min="0" required placeholder="1">
        </div>
        <div class="input-group">
          <label>Fecha de Adquisición</label>
          <input v-model="form.fecha_adquisicion" type="date" required>
        </div>
        <div class="input-group">
          <label>Última Revisión</label>
          <input v-model="form.ultima_revision" type="date">
        </div>
      </div>
    </div>

    <div class="divider"></div>

    <!-- Componente de Specs -->
    <SpecBuilder v-model="dynamicSpecs" />

    <div class="divider"></div>

    <button type="submit" class="btn-submit" :disabled="loading || (isEdit && !isAdmin)">
      {{ loading ? 'Guardando...' : (isEdit ? (isAdmin ? '💾 Actualizar Equipo' : '🔒 Solo Admin puede editar') : '💾 Guardar Equipo') }}
    </button>
  </form>
</template>

<script setup>
const props = defineProps({
  initialData: {
    type: Object,
    default: () => ({})
  },
  isEdit: {
    type: Boolean,
    default: false
  },
  loading: {
    type: Boolean,
    default: false
  },
  isAdmin: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['submit']);

const form = ref({
  nombre: '',
  marca: '',
  modelo: '',
  cantidad: 1,
  fecha_adquisicion: '',
  ultima_revision: '',
});

const dynamicSpecs = ref([
  { key: '', value: '' }
]);

// Cargar datos iniciales si existen
watch(() => props.initialData, (newData) => {
  if (newData && Object.keys(newData).length > 0) {
    form.value = {
      nombre: newData.nombre || '',
      marca: newData.marca || '',
      modelo: newData.modelo || '',
      cantidad: newData.cantidad || 1,
      fecha_adquisicion: newData.fecha_adquisicion || '',
      ultima_revision: newData.ultima_revision || ''
    };

    // Convertir objeto specs a array para el builder
    if (newData.especificaciones) {
      dynamicSpecs.value = Object.entries(newData.especificaciones).map(([key, value]) => ({
        key,
        value
      }));
    }
  }
}, { immediate: true });

const handleSubmit = () => {
  // Convertir specs array a objeto
  const specsObj = {};
  dynamicSpecs.value.forEach(spec => {
    if (spec.key && spec.value) {
      specsObj[spec.key] = spec.value;
    }
  });

  emit('submit', {
    ...form.value,
    especificaciones: specsObj
  });
};
</script>

<style scoped>
.cyber-form {
  background: var(--bg-card);
  padding: 30px;
  border-radius: 15px;
  border: 1px solid rgba(0, 242, 255, 0.1);
  box-shadow: var(--glow-card);
}

.input-group {
  margin-bottom: 20px;
  display: flex;
  flex-direction: column;
}

.input-group label {
  color: var(--primary);
  margin-bottom: 8px;
  font-size: 0.9em;
  font-weight: bold;
}

.input-group input {
  padding: 12px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 5px;
  color: white;
  font-size: 1em;
  transition: all 0.3s;
}

.input-group input:focus {
  border-color: var(--primary);
  box-shadow: 0 0 10px rgba(0, 242, 255, 0.2);
  outline: none;
}

.row {
  display: flex;
  gap: 20px;
}

.row .input-group {
  flex: 1;
}

.divider {
  height: 1px;
  background: rgba(255, 255, 255, 0.1);
  margin: 30px 0;
}

.btn-submit {
  width: 100%;
  padding: 15px;
  background: var(--primary);
  color: black;
  border: none;
  border-radius: 5px;
  font-size: 1.1em;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-submit:hover:not(:disabled) {
  box-shadow: 0 0 20px rgba(0, 242, 255, 0.5);
  transform: translateY(-2px);
}

.btn-submit:disabled {
  background: #555;
  cursor: not-allowed;
}
</style>
