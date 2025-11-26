<template>
  <div style="font-family: sans-serif; padding: 20px;">
    <h1>📦 Inventario de Equipos</h1>
    <div style="margin-bottom: 20px;">
      <NuxtLink to="/equipos/crear" style="background: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">
        + Agregar Nuevo Equipo
      </NuxtLink>
    </div>

    <table border="1" cellpadding="10" style="width: 100%; border-collapse: collapse;">
      <thead>
        <tr style="background: #f0f0f0;">
          <th>Nombre</th>
          <th>Marca</th>
          <th>Modelo</th>
          <th>Especificaciones (JSON)</th>
          <th>Fecha Adquisición</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="equipo in equipos" :key="equipo.id">
          <td>{{ equipo.nombre }}</td>
          <td>{{ equipo.marca }}</td>
          <td>{{ equipo.modelo }}</td>
          <td>
            <pre style="text-align: left; font-size: 0.8em;">{{ JSON.stringify(equipo.especificaciones, null, 2) }}</pre>
          </td>
          <td>{{ equipo.fecha_adquisicion }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import axios from 'axios';

const equipos = ref([]);

onMounted(async () => {
  try {
    // Usamos la IP de la máquina host o configuramos un proxy. 
    // Para simplificar en desarrollo local, usaremos localhost del navegador.
    const response = await axios.get('http://localhost:8000/api/equipos/');
    equipos.value = response.data;
  } catch (error) {
    console.error('Error cargando equipos:', error);
    alert('Error cargando equipos. Asegúrate de que el backend esté corriendo.');
  }
});
</script>
