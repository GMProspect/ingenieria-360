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

      <!-- Componente Reutilizable -->
      <SpecBuilder v-model="dynamicSpecs" />

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
// Nuxt auto-imports components in /components, so no explicit import needed for SpecBuilder

const router = useRouter();

// Estado del formulario básico
const form = ref({
  nombre: '',
  marca: '',
  modelo: '',
  fecha_adquisicion: '',
});

// Estado para las especificaciones dinámicas
const dynamicSpecs = ref([
  { key: '', value: '' }
]);

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
