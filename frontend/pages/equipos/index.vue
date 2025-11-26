<template>
  <div class="page-container">
    <NuxtLink to="/" class="back-link">← Volver al Inicio</NuxtLink>
    <h1 class="title">📦 Inventario de Equipos</h1>
    
    <!-- Barra de Acciones y Búsqueda -->
    <div class="controls-bar">
      <div class="search-box">
        <span class="search-icon">🔍</span>
        <input 
          v-model="searchQuery" 
          placeholder="Buscar por nombre, marca o modelo..." 
          class="search-input"
        >
      </div>
      
      <NuxtLink to="/equipos/crear" class="btn-add">
        + Nuevo Equipo
      </NuxtLink>
    </div>

    <!-- Estado de Carga -->
    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>Cargando inventario...</p>
    </div>

    <!-- Tabla de Datos -->
    <div v-else-if="filteredEquipos.length > 0" class="table-container cyber-card">
      <table class="cyber-table">
        <thead>
          <tr>
            <th>Nombre</th>
            <th>Marca</th>
            <th>Modelo</th>
            <th>Especificaciones</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="equipo in filteredEquipos" :key="equipo.id">
            <td>{{ equipo.nombre }}</td>
            <td>{{ equipo.marca }}</td>
            <td>{{ equipo.modelo }}</td>
            <td>
              <div class="specs-preview">
                <span v-for="(val, key) in equipo.especificaciones" :key="key" class="spec-tag">
                  {{ key }}: {{ val }}
                </span>
              </div>
            </td>
            <td class="actions-cell">
              <NuxtLink :to="`/equipos/${equipo.id}`" class="btn-icon edit" title="Editar">
                ✏️
              </NuxtLink>
              <button @click="deleteEquipo(equipo.id)" class="btn-icon delete" title="Eliminar">
                🗑️
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Estado Vacío -->
    <div v-else class="empty-state">
      <div class="empty-icon">📭</div>
      <h3>No se encontraron equipos</h3>
      <p v-if="searchQuery">Intenta con otra búsqueda.</p>
      <p v-else>¡Tu inventario está vacío! Agrega el primer equipo.</p>
    </div>

  </div>
</template>

<script setup>
import axios from 'axios';

const equipos = ref([]);
const loading = ref(true);
const searchQuery = ref('');

// Cargar Equipos
const fetchEquipos = async () => {
  loading.value = true;
  try {
    const response = await axios.get('http://localhost:8000/api/equipos/');
    equipos.value = response.data;
  } catch (error) {
    console.error('Error cargando equipos:', error);
    alert('Error de conexión con el servidor.');
  } finally {
    loading.value = false;
  }
};

onMounted(fetchEquipos);

// Filtrado en Tiempo Real
const filteredEquipos = computed(() => {
  if (!searchQuery.value) return equipos.value;
  
  const query = searchQuery.value.toLowerCase();
  return equipos.value.filter(eq => 
    eq.nombre.toLowerCase().includes(query) ||
    eq.marca.toLowerCase().includes(query) ||
    eq.modelo.toLowerCase().includes(query)
  );
});

// Eliminar Equipo
const deleteEquipo = async (id) => {
  if (!confirm('¿Estás seguro de eliminar este equipo? Esta acción no se puede deshacer.')) return;

  try {
    await axios.delete(`http://localhost:8000/api/equipos/${id}/`);
    // Eliminar localmente para feedback instantáneo
    equipos.value = equipos.value.filter(e => e.id !== id);
  } catch (error) {
    console.error(error);
    alert('Error al eliminar el equipo.');
  }
};
</script>

<style scoped>
.page-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.title {
  text-align: center;
  margin-bottom: 30px;
  color: var(--primary);
  text-shadow: 0 0 10px rgba(0, 242, 255, 0.3);
}

/* Controls Bar */
.controls-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  gap: 20px;
  flex-wrap: wrap;
}

.search-box {
  flex: 1;
  position: relative;
  max-width: 400px;
}

.search-icon {
  position: absolute;
  left: 15px;
  top: 50%;
  transform: translateY(-50%);
  opacity: 0.7;
}

.search-input {
  width: 100%;
  padding: 12px 12px 12px 45px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 25px;
  color: white;
  font-size: 1em;
  transition: all 0.3s ease;
}

.search-input:focus {
  border-color: var(--primary);
  box-shadow: 0 0 15px rgba(0, 242, 255, 0.2);
  outline: none;
  background: rgba(255, 255, 255, 0.1);
}

.btn-add {
  background: var(--primary);
  color: black;
  padding: 12px 25px;
  text-decoration: none;
  border-radius: 25px;
  font-weight: bold;
  transition: all 0.3s ease;
  box-shadow: 0 0 10px rgba(0, 242, 255, 0.2);
  white-space: nowrap;
}

.btn-add:hover {
  background: white;
  box-shadow: 0 0 20px rgba(0, 242, 255, 0.5);
  transform: translateY(-2px);
}

/* Table Styles */
.table-container {
  overflow-x: auto;
  padding: 0; /* Clean edges */
  border-radius: 10px;
  overflow: hidden;
}

.cyber-table {
  width: 100%;
  border-collapse: collapse;
  color: var(--text-main);
}

.cyber-table th {
  background: rgba(0, 242, 255, 0.15);
  color: var(--primary);
  padding: 18px;
  text-align: left;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 1px;
  font-size: 0.9em;
}

.cyber-table td {
  padding: 15px 18px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  vertical-align: middle;
}

.cyber-table tr:last-child td {
  border-bottom: none;
}

.cyber-table tr:hover td {
  background: rgba(255, 255, 255, 0.03);
}

/* Specs Tags */
.specs-preview {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
}

.spec-tag {
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.1);
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.8em;
  color: var(--text-muted);
}

/* Actions */
.actions-cell {
  white-space: nowrap;
}

.btn-icon {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.2em;
  padding: 5px;
  margin-right: 10px;
  transition: transform 0.2s;
  text-decoration: none;
  display: inline-block;
}

.btn-icon:hover {
  transform: scale(1.2);
}

.btn-icon.delete:hover {
  filter: drop-shadow(0 0 5px red);
}

.btn-icon.edit:hover {
  filter: drop-shadow(0 0 5px yellow);
}

/* States */
.loading-state, .empty-state {
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

.empty-icon {
  font-size: 4em;
  margin-bottom: 20px;
  opacity: 0.5;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@media (max-width: 768px) {
  .controls-bar {
    flex-direction: column;
    align-items: stretch;
  }
  
  .search-box {
    max-width: 100%;
  }
}
</style>
