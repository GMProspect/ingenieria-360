<template>
  <div class="page-container">
    <NuxtLink to="/equipos" class="back-link">← Volver al Inventario</NuxtLink>
    <h1 class="title">➕ Agregar Nuevo Equipo</h1>
    
    <EquipoForm 
      @submit="guardarEquipo" 
      :loading="loading"
    />
  </div>
</template>

<script setup>
import axios from 'axios';
import { useRouter } from 'vue-router';

const router = useRouter();
const config = useRuntimeConfig();
const apiBase = config.public.apiBase;
const loading = ref(false);

const guardarEquipo = async (formData) => {
  loading.value = true;
  try {
    await axios.post(`${apiBase}/api/equipos/`, formData);
    alert('¡Equipo guardado con éxito!');
    router.push('/equipos');
  } catch (error) {
    console.error('Error guardando:', error);
    alert('Error al guardar. Revisa la consola.');
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.page-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.title {
  text-align: center;
  margin-bottom: 30px;
  color: var(--primary);
  text-shadow: 0 0 10px rgba(0, 242, 255, 0.3);
}
</style>
