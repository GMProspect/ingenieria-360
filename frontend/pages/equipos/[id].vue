<template>
  <div class="page-container">
    <NuxtLink to="/equipos" class="back-link">← Volver al Inventario</NuxtLink>
    <h1 class="title">✏️ Editar Equipo</h1>
    
    <div v-if="loadingData" class="loading-state">
      <div class="spinner"></div>
      <p>Cargando datos...</p>
    </div>

    <EquipoForm 
      v-else
      :initialData="equipo"
      :isEdit="true"
      :loading="saving"
      @submit="actualizarEquipo" 
    />
  </div>
</template>

<script setup>
import axios from 'axios';
import { useRoute, useRouter } from 'vue-router';

const route = useRoute();
const router = useRouter();
const equipo = ref({});
const loadingData = ref(true);
const saving = ref(false);

const id = route.params.id;

onMounted(async () => {
  try {
    const response = await axios.get(`http://localhost:8000/api/equipos/${id}/`);
    equipo.value = response.data;
  } catch (error) {
    console.error('Error cargando equipo:', error);
    alert('No se pudo cargar el equipo.');
    router.push('/equipos');
  } finally {
    loadingData.value = false;
  }
});

const actualizarEquipo = async (formData) => {
  saving.value = true;
  try {
    await axios.put(`http://localhost:8000/api/equipos/${id}/`, formData);
    alert('¡Equipo actualizado con éxito!');
    router.push('/equipos');
  } catch (error) {
    console.error('Error actualizando:', error);
    alert('Error al actualizar.');
  } finally {
    saving.value = false;
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

.loading-state {
  text-align: center;
  padding: 50px;
  color: var(--text-muted);
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(255, 255, 255, 0.1);
  border-top-color: var(--primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
