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
        <button @click="toggleAdmin" class="nav-item btn-admin" :title="isAdmin ? 'Bloquear Admin' : 'Desbloquear Admin'">
          {{ isAdmin ? '🔓' : '🔒' }}
        </button>
      </div>
    </nav>

    <!-- Aquí se renderizan las páginas -->
    <div class="page-content">
      <NuxtPage />
    </div>

    <!-- Footer -->
    <footer class="footer">
      <p>Desarrollado por <span class="author">Gustavo Matheus</span> | Ingeniería 360 © {{ new Date().getFullYear() }}</p>
    </footer>
  </div>
</template>

<script setup>
const isAdmin = useState('isAdmin', () => false);

const toggleAdmin = () => {
  if (isAdmin.value) {
    isAdmin.value = false;
    alert('Modo Admin: BLOQUEADO 🔒');
  } else {
    const password = prompt('Ingrese contraseña de administrador:');
    if (password === 'admin123') {
      isAdmin.value = true;
      alert('Modo Admin: DESBLOQUEADO 🔓');
    } else {
      alert('Contraseña incorrecta ❌');
    }
  }
};
</script>

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

.btn-admin {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.2em;
  padding: 0 10px;
}

.router-link-active {
  color: var(--primary);
  border-bottom: 2px solid var(--primary);
}

.page-content {
  flex: 1;
  padding: 20px;
}

.footer {
  text-align: center;
  padding: 20px;
  background: rgba(10, 14, 23, 0.95);
  border-top: 1px solid rgba(0, 242, 255, 0.1);
  color: var(--text-muted);
  font-size: 0.9em;
}

.author {
  color: var(--primary);
  font-weight: bold;
  text-shadow: 0 0 5px rgba(0, 242, 255, 0.3);
}
</style>
