<template>
  <div class="page-container">
    <NuxtLink to="/equipos" class="back-link">← Volver al Inventario</NuxtLink>
    <h1 class="title">✏️ Editar Equipo</h1>
    
    <div v-if="loadingData" class="loading-state">
      <div class="spinner"></div>
      <p>Cargando datos...</p>
    </div>

    <div v-else>
      <EquipoForm 
        :initialData="equipo"
        :isEdit="true"
        :loading="saving"
        :isAdmin="isAdmin"
        @submit="actualizarEquipo" 
      />

      <div class="actions-footer" v-if="isAdmin">
        <button type="button" @click="deleteEquipo" class="btn-delete">
          🗑️ Eliminar Equipo
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios';

const route = useRoute();
const router = useRouter();
const id = route.params.id;

const isAdmin = useState('isAdmin');
const equipo = ref({});
const loadingData = ref(true);
const saving = ref(false);

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
  if (!isAdmin.value) {
    alert('No tienes permisos para editar.');
    return;
  }
  
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

const deleteEquipo = async () => {
  if (!confirm('¿Estás seguro de eliminar este equipo? Esta acción no se puede deshacer.')) return;

  try {
    await axios.delete(`http://localhost:8000/api/equipos/${id}/`);
    alert('Equipo eliminado.');
    router.push('/equipos');
  } catch (error) {
    console.error('Error eliminando:', error);
    alert('Error al eliminar.');
  }
};
</script>

<style scoped>
.page-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.back-link {
  color: var(--text-muted);
  text-decoration: none;
  margin-bottom: 20px;
  display: inline-block;
}

.back-link:hover {
  color: var(--primary);
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

.actions-footer {
  margin-top: 30px;
  display: flex;
  justify-content: center;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  padding-top: 20px;
}

.btn-delete {
  background: rgba(255, 50, 50, 0.1);
  color: #ff5555;
  border: 1px solid #ff5555;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-delete:hover {
  background: rgba(255, 50, 50, 0.2);
  box-shadow: 0 0 10px rgba(255, 85, 85, 0.3);
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
