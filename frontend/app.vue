<template>
  <div class="app-container">
    <!-- Barra de Navegación -->
    <nav class="navbar">
      <NuxtLink to="/" class="nav-brand">
        🏗️ Ingeniería 360
      </NuxtLink>
      <div class="nav-links">
        <NuxtLink to="/equipos" class="nav-item">
          Inventario
        </NuxtLink>
        <NuxtLink to="/calculadoras/ohm" class="nav-item">
          ⚡ Ley de Ohm
        </NuxtLink>
      </div>
    </nav>

    <!-- Aquí se renderizan las páginas -->
    <div class="page-content">
      <NuxtPage />
    </div>
  </div>
</template>

<style scoped>
.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.navbar {
  background: rgba(10, 14, 23, 0.95);
  border-bottom: 1px solid rgba(0, 242, 255, 0.1);
  padding: 15px 30px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  backdrop-filter: blur(10px);
  position: sticky;
  top: 0;
  z-index: 100;
}

.nav-brand {
  font-size: 1.5em;
  font-weight: bold;
  color: var(--primary);
  text-shadow: 0 0 10px rgba(0, 242, 255, 0.3);
}

.nav-links {
  display: flex;
  gap: 20px;
}

.nav-item {
  color: var(--text-muted);
  font-weight: 500;
  transition: all 0.3s;
}

.nav-item:hover {
  color: var(--primary);
  text-shadow: 0 0 8px var(--primary);
}

.router-link-active {
  color: var(--primary);
  border-bottom: 2px solid var(--primary);
}

.page-content {
  flex: 1;
  padding: 20px;
}
</style>
