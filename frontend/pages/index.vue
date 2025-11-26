<template>
  <div class="home-container">
    <div class="hero-section">
      <h1>🏗️ Ingeniería 360</h1>
      <p>Bienvenido a tu Entorno Técnico Inteligente</p>
    </div>

    <div class="tools-grid">
      
      <!-- Card: Inventario -->
      <NuxtLink to="/equipos" class="tool-card">
        <div class="card-icon">📦</div>
        <h3>Inventario</h3>
        <p>Gestión de activos y especificaciones dinámicas.</p>
      </NuxtLink>

      <!-- Card: Ley de Ohm -->
      <NuxtLink to="/calculadoras/ohm" class="tool-card">
        <div class="card-icon">⚡</div>
        <h3>Ley de Ohm</h3>
        <p>Cálculo de V, I, R con interfaz triangular.</p>
      </NuxtLink>

      <!-- Card: Transmisor 4-20mA -->
      <NuxtLink to="/calculadoras/transmisor" class="tool-card">
        <div class="card-icon">🎛️</div>
        <h3>Transmisor 4-20mA</h3>
        <p>Conversión de señales de instrumentación.</p>
      </NuxtLink>

      <!-- Card: Sondas de Vibración -->
      <NuxtLink to="/calculadoras/vibracion" class="tool-card">
        <div class="card-icon">📉</div>
        <h3>Sondas de Vibración</h3>
        <p>API 670: Voltaje de GAP a Mils/Micras.</p>
      </NuxtLink>

      <!-- Card: Conversor Universal -->
      <NuxtLink to="/calculadoras/conversor" class="tool-card">
        <div class="card-icon">🔄</div>
        <h3>Conversor Universal</h3>
        <p>Presión, Temperatura, Longitud y Peso.</p>
      </NuxtLink>

    </div>
  </div>
</template>

<style scoped>
.home-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
}

.hero-section {
  text-align: center;
  margin-bottom: 60px;
  animation: fadeIn 1s ease-out;
}

.hero-section h1 {
  font-size: 3.5em;
  margin-bottom: 10px;
  background: linear-gradient(to right, var(--primary), var(--secondary));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.hero-section p {
  font-size: 1.2em;
  color: var(--text-muted);
}

.tools-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
}

.tool-card {
  background: var(--bg-card);
  border: 1px solid rgba(0, 242, 255, 0.1);
  border-radius: 15px;
  padding: 30px;
  text-align: center;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  display: block; /* For NuxtLink */
}

.tool-card:hover {
  transform: translateY(-10px);
  box-shadow: var(--glow-card);
  border-color: var(--primary);
}

.tool-card:hover .card-icon {
  transform: scale(1.2) rotate(5deg);
}

.card-icon {
  font-size: 4em;
  margin-bottom: 20px;
  transition: all 0.3s ease;
}

.tool-card h3 {
  font-size: 1.5em;
  margin-bottom: 10px;
  color: var(--text-main);
}

.tool-card p {
  color: var(--text-muted);
  font-size: 0.95em;
}

/* Disabled State */
.tool-card.disabled {
  opacity: 0.6;
  cursor: not-allowed;
  filter: grayscale(0.8);
}

.tool-card.disabled:hover {
  transform: none;
  box-shadow: none;
  border-color: rgba(0, 242, 255, 0.1);
}

.badge {
  position: absolute;
  top: 15px;
  right: 15px;
  background: var(--secondary);
  color: white;
  font-size: 0.7em;
  padding: 5px 10px;
  border-radius: 20px;
  font-weight: bold;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
