<template>
  <div style="font-family: sans-serif;">
    <!-- Barra de Navegación Simple -->
    <nav style="background: #333; color: white; padding: 15px;">
      <NuxtLink to="/" style="color: white; text-decoration: none; margin-right: 20px; font-weight: bold;">
        🏗️ Ingeniería 360
      </NuxtLink>
      <NuxtLink to="/equipos" style="color: #ddd; text-decoration: none;">
        Inventario
      </NuxtLink>
    </nav>

    <!-- Aquí se renderizan las páginas (index.vue, crear.vue, etc.) -->
    <NuxtPage />
  </div>
</template>
