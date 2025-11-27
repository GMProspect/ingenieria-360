<template>
  <div class="calc-container">
    <NuxtLink to="/" class="back-link">← Volver al Inicio</NuxtLink>
    <h1 class="title">⚡ Ley de Ohm</h1>
    <p class="subtitle">
      Ingresa 2 valores para calcular el 3ro. <br>
      <span class="hint">(Deja vacío el que quieres descubrir)</span>
    </p>

    <!-- Contenedor Principal Centrado -->
    <div class="triangle-wrapper">
      
      <!-- El Triángulo Mágico -->
      <div class="triangle-container">
        
        <!-- Fondo y Forma del Triángulo -->
        <div class="triangle-shape"></div>
        
        <!-- Líneas Divisorias -->
        <div class="divider-horizontal"></div>
        <div class="divider-vertical"></div>

        <!-- INPUT: Voltaje (Arriba) -->
        <div class="input-group top">
          <label>V</label>
          <input 
            v-model="v" 
            type="number" 
            placeholder="?" 
            @input="recalc('v')"
            :class="{ result: isResult === 'v' }"
          >
          <span class="unit">Volts</span>
        </div>

        <!-- INPUT: Resistencia (Izquierda) -->
        <div class="input-group left">
          <label>R</label>
          <input 
            v-model="r" 
            type="number" 
            placeholder="?" 
            @input="recalc('r')"
            :class="{ result: isResult === 'r' }"
          >
          <span class="unit">Ohms</span>
        </div>

        <!-- INPUT: Corriente (Derecha) -->
        <div class="input-group right">
          <label>I</label>
          <input 
            v-model="i" 
            type="number" 
            placeholder="?" 
            @input="recalc('i')"
            :class="{ result: isResult === 'i' }"
          >
          <span class="unit">Amps</span>
        </div>

      </div>
    </div>

    <!-- Botonera de Acciones -->
    <div class="actions">
      <button @click="limpiar" class="btn-clear">
        🧹 Limpiar
      </button>
      
      <div class="save-group">
        <input v-model="etiqueta" placeholder="Etiqueta (Ej: Motor 1)" class="tag-input">
        <button @click="guardar" :disabled="!puedeGuardar" class="btn-save">
          💾 Guardar
        </button>
      </div>
    </div>

  </div>
</template>

<script setup>
import axios from 'axios';

const config = useRuntimeConfig();
const apiBase = config.public.apiBase;

const v = ref('');
const i = ref('');
const r = ref('');
const etiqueta = ref('');
const isResult = ref(''); // 'v', 'i', 'r', or ''

// Lógica Fluida: "El vacío manda, el conflicto se resuelve"
const recalc = (source) => {
  const valV = v.value;
  const valI = i.value;
  const valR = r.value;

  // 1. Detección Agresiva
  if (valV && valI && !valR) isResult.value = 'r';
  else if (valV && valR && !valI) isResult.value = 'i';
  else if (valI && valR && !valV) isResult.value = 'v';
  
  // 2. Resolución de Conflictos
  else if (valV && valI && valR) {
    if (isResult.value === source) {
      if (source === 'v') isResult.value = 'i';
      else if (source === 'i') isResult.value = 'r';
      else if (source === 'r') isResult.value = 'v';
    }
  }
  
  // 3. Reset
  if (!valV && !valI && !valR) isResult.value = '';

  // --- CÁLCULO ---
  const numV = parseFloat(v.value) || 0;
  const numI = parseFloat(i.value) || 0;
  const numR = parseFloat(r.value) || 0;

  if (isResult.value === 'v' && source !== 'v') {
    v.value = (numI * numR).toFixed(2);
    if (v.value === '0.00') v.value = '';
  }
  else if (isResult.value === 'i' && source !== 'i') {
    if (numR !== 0) {
      i.value = (numV / numR).toFixed(2);
      if (i.value === '0.00') i.value = '';
    }
  }
  else if (isResult.value === 'r' && source !== 'r') {
    if (numI !== 0) {
      r.value = (numV / numI).toFixed(2);
      if (r.value === '0.00') r.value = '';
    }
  }
};

const limpiar = () => {
  v.value = '';
  i.value = '';
  r.value = '';
  isResult.value = '';
};

const puedeGuardar = computed(() => {
  return etiqueta.value && v.value && i.value && r.value;
});

const guardar = async () => {
  try {
    const payload = {
      tipo: 'OHM',
      etiqueta: etiqueta.value,
      datos_entrada: { v: v.value, i: i.value, r: r.value },
      resultado: { v: v.value, i: i.value, r: r.value }
    };
    await axios.post(`${apiBase}/api/history/`, payload);
    alert('¡Guardado!');
    etiqueta.value = '';
  } catch (error) {
    console.error(error);
    alert('Error al guardar');
  }
};
</script>

<style scoped>
.calc-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.title {
  text-align: center;
  margin-bottom: 5px;
}

.subtitle {
  text-align: center;
  color: var(--text-muted);
  margin-bottom: 40px;
}

.hint {
  font-size: 0.9em;
  color: var(--secondary);
}

.triangle-wrapper {
  display: flex;
  justify-content: center;
  margin-bottom: 50px;
  padding: 20px;
}

.triangle-container {
  position: relative;
  width: 440px; /* Aumentado de 360px */
  height: 380px; /* Aumentado de 310px */
}

/* La forma del triángulo */
.triangle-shape {
  position: absolute;
  top: 0;
  left: 0;
  width: 0;
  height: 0;
  border-left: 220px solid transparent; /* Mitad del ancho */
  border-right: 220px solid transparent;
  border-bottom: 380px solid rgba(0, 242, 255, 0.1); /* Cyan transparente */
  filter: drop-shadow(0 0 20px rgba(0, 242, 255, 0.2));
  z-index: 0;
}

/* Borde brillante inferior */
.triangle-shape::after {
  content: '';
  position: absolute;
  top: 380px;
  left: -220px;
  width: 440px;
  height: 2px;
  background: var(--primary);
  box-shadow: 0 0 15px var(--primary);
}

/* Líneas divisorias */
.divider-horizontal {
  position: absolute;
  top: 190px; /* Mitad de altura */
  left: 110px; /* Ajustado */
  width: 220px;
  height: 2px;
  background: var(--primary);
  box-shadow: 0 0 10px var(--primary);
  z-index: 1;
}

.divider-vertical {
  position: absolute;
  top: 190px;
  left: 220px; /* Centro */
  width: 2px;
  height: 190px;
  background: var(--primary);
  box-shadow: 0 0 10px var(--primary);
  z-index: 1;
}

/* Estilos comunes para los grupos de input */
.input-group {
  position: absolute;
  display: flex;
  flex-direction: column;
  align-items: center;
  z-index: 2;
  width: 120px;
}

.input-group label {
  font-size: 2em;
  font-weight: 900;
  color: white;
  text-shadow: 0 0 10px var(--primary);
  margin-bottom: 5px;
}

.input-group input {
  width: 100px;
  background: rgba(0, 0, 0, 0.6);
  border: 1px solid var(--primary);
  border-radius: 8px;
  padding: 8px;
  text-align: center;
  font-size: 1.2em;
  font-weight: bold;
  color: white;
  outline: none;
  transition: all 0.2s;
}

.input-group input:focus {
  background: rgba(0, 242, 255, 0.1);
  transform: scale(1.1);
  box-shadow: 0 0 15px rgba(0, 242, 255, 0.3);
}

/* Estilo especial para el resultado calculado */
.input-group input.result {
  background: var(--accent-success);
  color: black;
  border-color: var(--accent-success);
  box-shadow: 0 0 20px var(--accent-success);
}

.input-group .unit {
  font-size: 0.8em;
  color: var(--text-muted);
  margin-top: 5px;
}

/* Posicionamiento exacto (Recalculado para 440x380) */
.top {
  top: 70px;
  left: 160px; /* (440 - 120) / 2 */
}

.left {
  top: 250px;
  left: 40px;
}

.right {
  top: 250px;
  left: 280px;
}

.actions {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 20px;
}

.btn-clear {
  background: rgba(255, 255, 255, 0.1);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.2);
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-clear:hover {
  background: rgba(255, 255, 255, 0.2);
}

.save-group {
  display: flex;
  gap: 10px;
}

.tag-input {
  padding: 10px;
  width: 200px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: white;
  border-radius: 5px;
}

.btn-save {
  background: var(--primary);
  color: black;
  border: none;
  padding: 10px 25px;
  border-radius: 5px;
  font-weight: bold;
  cursor: pointer;
}

.btn-save:disabled {
  background: #555;
  cursor: not-allowed;
}
</style>
