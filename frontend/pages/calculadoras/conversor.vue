<template>
  <div class="calc-container">
    <NuxtLink to="/" class="back-link">← Volver al Inicio</NuxtLink>
    <h1 class="title">🔄 Conversor Universal</h1>
    <p class="subtitle">Herramienta de conversión para ingeniería</p>

    <div class="cyber-card">
      
      <!-- Selector de Categoría -->
      <div class="category-selector">
        <button 
          v-for="(cat, key) in categories" 
          :key="key"
          :class="['cat-btn', { active: currentCategory === key }]"
          @click="currentCategory = key"
        >
          {{ cat.icon }} {{ cat.name }}
        </button>
      </div>

      <div class="divider"></div>

      <!-- Área de Conversión -->
      <div class="conversion-area">
        
        <!-- Lado Izquierdo (FROM) -->
        <div class="input-group">
          <label>De:</label>
          <input 
            v-model="valFrom" 
            type="number" 
            placeholder="0"
            @input="convert('from')"
          >
          <select v-model="unitFrom" @change="convert('from')">
            <option v-for="(u, k) in currentUnits" :key="k" :value="k">
              {{ u.name }} ({{ u.symbol }})
            </option>
          </select>
        </div>

        <div class="arrow">➔</div>

        <!-- Lado Derecho (TO) -->
        <div class="input-group">
          <label>A:</label>
          <input 
            v-model="valTo" 
            type="number" 
            placeholder="0"
            @input="convert('to')"
          >
          <select v-model="unitTo" @change="convert('from')"> <!-- Recalc from source when target unit changes -->
            <option v-for="(u, k) in currentUnits" :key="k" :value="k">
              {{ u.name }} ({{ u.symbol }})
            </option>
          </select>
        </div>

      </div>

    </div>

    <!-- Botonera -->
    <div class="actions">
      <div class="save-group">
        <input v-model="etiqueta" placeholder="Etiqueta (Ej: Presión Caldera)" class="tag-input">
        <button @click="guardar" :disabled="!puedeGuardar" class="btn-save">
          💾 Guardar Conversión
        </button>
      </div>
    </div>

  </div>
</template>

<script setup>
import axios from 'axios';

const config = useRuntimeConfig();
const apiBase = config.public.apiBase;

// --- Configuración de Unidades ---
const categories = {
  pressure: {
    name: 'Presión',
    icon: '🌡️',
    units: {
      bar: { name: 'Bar', symbol: 'bar', factor: 1 },
      psi: { name: 'PSI', symbol: 'psi', factor: 0.0689476 },
      kpa: { name: 'Kilopascal', symbol: 'kPa', factor: 0.01 },
      atm: { name: 'Atmósfera', symbol: 'atm', factor: 1.01325 },
      mmhg: { name: 'mmHg', symbol: 'mmHg', factor: 0.00133322 }
    }
  },
  temperature: {
    name: 'Temperatura',
    icon: '🔥',
    units: {
      c: { name: 'Celsius', symbol: '°C' },
      f: { name: 'Fahrenheit', symbol: '°F' },
      k: { name: 'Kelvin', symbol: 'K' }
    }
  },
  length: {
    name: 'Longitud',
    icon: '📏',
    units: {
      m: { name: 'Metro', symbol: 'm', factor: 1 },
      cm: { name: 'Centímetro', symbol: 'cm', factor: 0.01 },
      mm: { name: 'Milímetro', symbol: 'mm', factor: 0.001 },
      in: { name: 'Pulgada', symbol: 'in', factor: 0.0254 },
      ft: { name: 'Pie', symbol: 'ft', factor: 0.3048 },
      mils: { name: 'Mils', symbol: 'mil', factor: 0.0000254 }
    }
  },
  weight: {
    name: 'Peso',
    icon: '⚖️',
    units: {
      kg: { name: 'Kilogramo', symbol: 'kg', factor: 1 },
      lb: { name: 'Libra', symbol: 'lb', factor: 0.453592 },
      g: { name: 'Gramo', symbol: 'g', factor: 0.001 },
      oz: { name: 'Onza', symbol: 'oz', factor: 0.0283495 }
    }
  }
};

// --- Estado ---
const currentCategory = ref('pressure');
const valFrom = ref('');
const valTo = ref('');
const unitFrom = ref('');
const unitTo = ref('');
const etiqueta = ref('');

// --- Computed ---
const currentUnits = computed(() => categories[currentCategory.value].units);

// --- Watchers ---
// Resetear unidades al cambiar de categoría
watch(currentCategory, (newCat) => {
  const keys = Object.keys(categories[newCat].units);
  unitFrom.value = keys[0];
  unitTo.value = keys[1] || keys[0];
  valFrom.value = '';
  valTo.value = '';
}, { immediate: true });

// --- Lógica de Conversión ---
const convert = (direction) => {
  const isTemp = currentCategory.value === 'temperature';
  
  if (direction === 'from') {
    // Calculando TO basado en FROM
    const val = parseFloat(valFrom.value);
    if (isNaN(val)) {
      valTo.value = '';
      return;
    }

    if (isTemp) {
      valTo.value = convertTemp(val, unitFrom.value, unitTo.value);
    } else {
      // Factor base: Convertir a unidad base (factor 1) y luego a destino
      const factorFrom = currentUnits.value[unitFrom.value].factor;
      const factorTo = currentUnits.value[unitTo.value].factor;
      const baseVal = val * factorFrom;
      valTo.value = (baseVal / factorTo).toFixed(4);
    }
  } else {
    // Calculando FROM basado en TO
    const val = parseFloat(valTo.value);
    if (isNaN(val)) {
      valFrom.value = '';
      return;
    }

    if (isTemp) {
      valFrom.value = convertTemp(val, unitTo.value, unitFrom.value);
    } else {
      const factorFrom = currentUnits.value[unitFrom.value].factor;
      const factorTo = currentUnits.value[unitTo.value].factor;
      const baseVal = val * factorTo;
      valFrom.value = (baseVal / factorFrom).toFixed(4);
    }
  }
};

// Helper para Temperatura (No lineal)
const convertTemp = (val, from, to) => {
  if (from === to) return val;

  let celsius;
  // 1. Todo a Celsius
  if (from === 'c') celsius = val;
  else if (from === 'f') celsius = (val - 32) * 5/9;
  else if (from === 'k') celsius = val - 273.15;

  // 2. Celsius a Destino
  if (to === 'c') return celsius.toFixed(2);
  if (to === 'f') return ((celsius * 9/5) + 32).toFixed(2);
  if (to === 'k') return (celsius + 273.15).toFixed(2);
};

// --- Guardar ---
const puedeGuardar = computed(() => {
  return etiqueta.value && valFrom.value && valTo.value;
});

const guardar = async () => {
  try {
    const payload = {
      tipo: 'CONVERSOR',
      etiqueta: etiqueta.value,
      datos_entrada: { 
        category: currentCategory.value,
        unit_from: unitFrom.value,
        unit_to: unitTo.value,
        val_from: valFrom.value
      },
      resultado: { 
        val_to: valTo.value
      }
    };
    await axios.post(`${apiBase}/api/history/`, payload);
    alert('¡Conversión guardada!');
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
  margin-bottom: 30px;
}

.cyber-card {
  background: var(--bg-card);
  border: 1px solid rgba(0, 242, 255, 0.1);
  border-radius: 15px;
  padding: 30px;
  box-shadow: var(--glow-card);
}

/* Category Selector */
.category-selector {
  display: flex;
  justify-content: center;
  gap: 10px;
  flex-wrap: wrap;
  margin-bottom: 20px;
}

.cat-btn {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: var(--text-muted);
  padding: 10px 20px;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.cat-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  color: white;
}

.cat-btn.active {
  background: var(--primary);
  color: black;
  border-color: var(--primary);
  box-shadow: var(--glow-primary);
  font-weight: bold;
}

.divider {
  height: 1px;
  background: rgba(255, 255, 255, 0.1);
  margin: 20px 0;
}

.conversion-area {
  display: flex;
  align-items: center;
  gap: 20px;
  justify-content: space-between;
}

.input-group {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.input-group label {
  color: var(--text-muted);
  font-size: 0.9em;
}

.input-group input, .input-group select {
  width: 100%;
  padding: 15px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: white;
  border-radius: 5px;
  font-size: 1.2em;
}

.input-group select option {
  background-color: var(--bg-card);
  color: white;
}

.input-group input:focus, .input-group select:focus {
  border-color: var(--primary);
  box-shadow: 0 0 10px rgba(0, 242, 255, 0.2);
  outline: none;
}

.arrow {
  font-size: 2em;
  color: var(--secondary);
}

.actions {
  margin-top: 30px;
  display: flex;
  justify-content: center;
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
  transition: all 0.3s ease;
}

.btn-save:hover {
  box-shadow: var(--glow-primary);
}

.btn-save:disabled {
  background: #555;
  cursor: not-allowed;
  box-shadow: none;
}

/* Mobile Responsive */
@media (max-width: 600px) {
  .conversion-area {
    flex-direction: column;
  }
  
  .arrow {
    transform: rotate(90deg);
  }
}
</style>
