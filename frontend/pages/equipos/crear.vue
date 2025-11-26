<template>
  <div style="font-family: sans-serif; padding: 20px; max-width: 600px; margin: 0 auto;">
    <h1>➕ Agregar Nuevo Equipo</h1>
    
    <form @submit.prevent="guardarEquipo">
      <!-- Datos Básicos -->
      <div style="margin-bottom: 15px;">
        <label>Nombre:</label><br>
        <input v-model="form.nombre" type="text" required style="width: 100%; padding: 8px;">
      </div>
      <div style="margin-bottom: 15px;">
        <label>Marca:</label><br>
        <input v-model="form.marca" type="text" required style="width: 100%; padding: 8px;">
      </div>
      <div style="margin-bottom: 15px;">
        <label>Modelo:</label><br>
        <input v-model="form.modelo" type="text" required style="width: 100%; padding: 8px;">
      </div>
      <div style="margin-bottom: 15px;">
        <label>Fecha Adquisición:</label><br>
        <input v-model="form.fecha_adquisicion" type="date" required style="width: 100%; padding: 8px;">
      </div>

      <hr>

      <!-- Constructor de Especificaciones Dinámicas -->
      <h3>🛠️ Especificaciones Técnicas</h3>
      <p style="font-size: 0.9em; color: #666;">Agrega las características que quieras. No hay límites.</p>

      <div v-for="(spec, index) in dynamicSpecs" :key="index" style="display: flex; gap: 10px; margin-bottom: 10px;">
        <input v-model="spec.key" placeholder="Nombre (Ej: Voltaje)" style="flex: 1; padding: 5px;">
        <input v-model="spec.value" placeholder="Valor (Ej: 220V)" style="flex: 1; padding: 5px;">
        <button type="button" @click="removeSpec(index)" style="background: #ff4444; color: white; border: none; padding: 5px 10px; cursor: pointer;">X</button>
      </div>

      <button type="button" @click="addSpec" style="background: #28a745; color: white; border: none; padding: 5px 10px; cursor: pointer; margin-bottom: 20px;">
        + Agregar Característica
      </button>

      <hr>

      <button type="submit" style="background: #007bff; color: white; padding: 10px 20px; border: none; font-size: 1.1em; cursor: pointer; width: 100%;">
        💾 Guardar Equipo
      </button>
    </form>
  </div>
</template>

<script setup>
import axios from 'axios';
import { useRouter } from 'vue-router';

const router = useRouter();

// Estado del formulario básico
const form = ref({
  nombre: '',
  marca: '',
  modelo: '',
  fecha_adquisicion: '',
});

// Estado para las especificaciones dinámicas (Array temporal)
const dynamicSpecs = ref([
  { key: '', value: '' } // Empezamos con una fila vacía
]);

const addSpec = () => {
  dynamicSpecs.value.push({ key: '', value: '' });
};

const removeSpec = (index) => {
  dynamicSpecs.value.splice(index, 1);
};

const guardarEquipo = async () => {
  try {
    // 1. Convertir el Array de specs a un Objeto JSON real
    const especificacionesJSON = {};
    dynamicSpecs.value.forEach(spec => {
      if (spec.key && spec.value) {
        especificacionesJSON[spec.key] = spec.value;
      }
    });

    // 2. Preparar el payload final
    const payload = {
      ...form.value,
      especificaciones: especificacionesJSON
    };

    // 3. Enviar al Backend
    await axios.post('http://localhost:8000/api/equipos/', payload);
    
    alert('¡Equipo guardado con éxito!');
    router.push('/equipos'); // Volver a la lista

  } catch (error) {
    console.error('Error guardando:', error);
    alert('Error al guardar. Revisa la consola.');
  }
};
</script>
