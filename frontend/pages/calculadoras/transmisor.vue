<template>
  <div class="calc-container">
    <NuxtLink to="/" class="back-link">← Volver al Inicio</NuxtLink>
    <h1 class="title">🎛️ Conversor de Transmisores</h1>
    <p class="subtitle">Escala lineal de señal (4-20mA) a Variable de Proceso (PV)</p>

    <div class="cyber-card">
      
      <!-- Rango del Instrumento -->
      <div class="section-title">Calibración del Instrumento</div>
      <div class="input-row">
        <div class="input-group">
          <label>Valor a 4mA (Mínimo)</label>
          <input v-model="lrv" type="number" placeholder="Ej: 0">
        </div>
        <div class="input-group">
          <label>Valor a 20mA (Máximo)</label>
          <input v-model="urv" type="number" placeholder="Ej: 100">
        </div>
        <div class="input-group">
          <label>Unidad</label>
          <input v-model="unit" type="text" placeholder="PSI, °C...">
        </div>
      </div>

      <div class="span-info">
        Alcance (Span): <strong>{{ span }}</strong> {{ unit }}
      </div>

      <div class="divider"></div>

      <!-- Conversión Bidireccional -->
      <div class="section-title">Conversión en Tiempo Real</div>
      <div class="conversion-row">
        
        <!-- Entrada mA -->
        <div class="input-group main-input">
          <label>Señal (mA)</label>
          <input 
            v-model="ma" 
            type="number" 
            step="0.01" 
            @input="calcFromMA"
            :class="{ active: lastEdited === 'ma' }"
          >
        </div>

        <div class="arrow">⇄</div>

        <!-- Entrada PV -->
        <div class="input-group main-input">
          <label>Variable Física ({{ unit || 'PV' }})</label>
          <input 
            v-model="pv" 
            type="number" 
            step="0.1" 
            @input="calcFromPV"
            :class="{ active: lastEdited === 'pv' }"
          >
        </div>

      </div>

      <!-- Barra Visual de Porcentaje -->
      <div class="progress-container">
        <!-- Barra visual (Clamped 0-100%) -->
        <div class="progress-bar" :style="{ width: visualPercentage + '%', background: statusColor }"></div>
        <!-- Texto Real (Unclamped) -->
        <span class="progress-text">{{ rawPercentage }}%</span>
      </div>

      <!-- Mensaje de Diagnóstico -->
      <div v-if="diagnosticMessage" class="diagnostic-box" :style="{ borderColor: statusColor, color: statusColor }">
        {{ diagnosticMessage }}
      </div>

      <div class="divider"></div>

      <!-- Tabla de Puntos de Calibración -->
      <div class="section-title">Puntos de Calibración (Check Points)</div>
      <div class="calibration-table">
        <div v-for="point in calibrationPoints" :key="point.pct" class="cal-row">
          <div class="cal-col pct">● {{ point.pct }}%</div>
          <div class="cal-col arrow">→</div>
          <div class="cal-col val">{{ point.pv }} {{ unit }}</div>
          <div class="cal-col arrow">→</div>
          <div class="cal-col ma">{{ point.ma }} mA</div>
        </div>
      </div>

    </div>

    <!-- Botonera -->
    <div class="actions">
      <div class="save-group">
        <input v-model="etiqueta" placeholder="Etiqueta (Ej: PT-101)" class="tag-input">
        <button @click="guardar" :disabled="!puedeGuardar" class="btn-save">
          💾 Guardar
        </button>
      </div>
    </div>

  </div>
</template>

<script setup>
import axios from 'axios';

const lrv = ref(0);
const urv = ref(100);
const unit = ref('');
const ma = ref('');
const pv = ref('');
const etiqueta = ref('');
const rawPercentage = ref('0.0'); // Porcentaje real (puede ser negativo o >100)
const lastEdited = ref('');

// Computed para el Span
const span = computed(() => {
  const min = parseFloat(lrv.value);
  const max = parseFloat(urv.value);
  if (isNaN(min) || isNaN(max)) return 0;
  return parseFloat((max - min).toFixed(4));
});

// Computed para Puntos de Calibración (0, 25, 50, 75, 100%)
const calibrationPoints = computed(() => {
  const min = parseFloat(lrv.value);
  const max = parseFloat(urv.value);
  
  if (isNaN(min) || isNaN(max)) return [];

  const points = [0, 25, 50, 75, 100];
  return points.map(pct => {
    const valMA = 4 + (16 * (pct / 100));
    const valPV = min + ((max - min) * (pct / 100));
    return {
      pct: pct,
      ma: valMA.toFixed(2),
      pv: valPV.toFixed(2)
    };
  });
});

// Computed para el ancho visual de la barra (0-100%)
const visualPercentage = computed(() => {
  const val = parseFloat(rawPercentage.value);
  if (isNaN(val)) return 0;
  return Math.min(Math.max(val, 0), 100);
});

// Lógica de Diagnóstico
const diagnosticMessage = computed(() => {
  const valMA = parseFloat(ma.value);
  if (isNaN(valMA)) return '';

  if (valMA < 3.8) return '⚠️ FALLA: Lazo Abierto / Sensor Dañado (< 3.8mA)';
  if (valMA >= 3.8 && valMA < 4.0) return '⚠️ ALERTA: Sub-rango (Under-range)';
  if (valMA > 20.0 && valMA <= 20.5) return '⚠️ ALERTA: Sobre-rango (Over-range)';
  if (valMA > 20.5) return '⚠️ FALLA: Saturación / Cortocircuito (> 20.5mA)';
  
  return ''; // Operación Normal
});

const statusColor = computed(() => {
  const valMA = parseFloat(ma.value);
  if (isNaN(valMA)) return 'var(--primary)'; // Default Cyan

  if (valMA < 3.8 || valMA > 20.5) return 'var(--accent-danger)'; // Rojo Falla
  if (valMA < 4.0 || valMA > 20.0) return '#ffcc00'; // Amarillo Alerta
  
  return 'var(--accent-success)'; // Verde Normal (o Cyan si prefieres)
});

// Calcular PV desde mA
const calcFromMA = () => {
  lastEdited.value = 'ma';
  const valMA = parseFloat(ma.value);
  const min = parseFloat(lrv.value);
  const max = parseFloat(urv.value);

  if (!isNaN(valMA) && !isNaN(min) && !isNaN(max)) {
    // Cálculo de porcentaje real
    let pct = ((valMA - 4) / 16) * 100;
    rawPercentage.value = pct.toFixed(2);

    const result = ((valMA - 4) / 16) * (max - min) + min;
    pv.value = result.toFixed(2);
  }
};

// Calcular mA desde PV
const calcFromPV = () => {
  lastEdited.value = 'pv';
  const valPV = parseFloat(pv.value);
  const min = parseFloat(lrv.value);
  const max = parseFloat(urv.value);

  if (!isNaN(valPV) && !isNaN(min) && !isNaN(max)) {
    let pct = ((valPV - min) / (max - min)) * 100;
    rawPercentage.value = pct.toFixed(2);

    const result = ((valPV - min) / (max - min)) * 16 + 4;
    ma.value = result.toFixed(2);
  }
};

const puedeGuardar = computed(() => {
  return etiqueta.value && ma.value && pv.value;
});

const guardar = async () => {
  try {
    const payload = {
      tipo: 'TRANSMISOR',
      etiqueta: etiqueta.value,
      datos_entrada: { 
        lrv: lrv.value, 
        urv: urv.value, 
        unit: unit.value,
        input_type: lastEdited.value, // 'ma' o 'pv'
        input_value: lastEdited.value === 'ma' ? ma.value : pv.value
      },
      resultado: { 
        ma: ma.value, 
        pv: pv.value, 
        percentage: rawPercentage.value 
      }
    };
    await axios.post('http://localhost:8000/api/history/', payload);
    alert('¡Calibración guardada!');
    etiqueta.value = '';
  } catch (error) {
    console.error(error);
    alert('Error al guardar');
  }
};
</script>

<style scoped>
.calc-container {
  max-width: 700px;
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

.section-title {
  color: var(--primary);
  font-size: 0.9em;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 15px;
  font-weight: bold;
}

.input-row {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
}

.input-group {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.input-group label {
  color: var(--text-muted);
  font-size: 0.8em;
  margin-bottom: 5px;
}

.input-group input {
  width: 100%; /* Fix overflow */
  padding: 10px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: white;
  border-radius: 5px;
  font-size: 1em;
}

.input-group input:focus {
  border-color: var(--primary);
  box-shadow: 0 0 10px rgba(0, 242, 255, 0.2);
  outline: none;
}

.span-info {
  text-align: center;
  color: var(--text-muted);
  margin-bottom: 10px;
  font-size: 0.9em;
}

.span-info strong {
  color: var(--secondary);
  font-size: 1.1em;
}

.divider {
  height: 1px;
  background: rgba(255, 255, 255, 0.1);
  margin: 20px 0;
}

.conversion-row {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 30px;
}

.arrow {
  font-size: 2em;
  color: var(--secondary);
  animation: pulse 2s infinite;
}

.main-input input {
  font-size: 1.5em;
  text-align: center;
  font-weight: bold;
  border: 2px solid rgba(255, 255, 255, 0.1);
}

.main-input input.active {
  border-color: var(--primary);
  background: rgba(0, 242, 255, 0.05);
}

.progress-container {
  height: 20px;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 10px;
  overflow: hidden;
  position: relative;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.progress-bar {
  height: 100%;
  /* El color se controla dinámicamente */
  transition: width 0.3s ease, background-color 0.3s ease;
}

.progress-text {
  position: absolute;
  width: 100%;
  text-align: center;
  top: 0;
  line-height: 20px;
  font-size: 0.8em;
  font-weight: bold;
  text-shadow: 0 0 5px black;
}

.diagnostic-box {
  margin-top: 15px;
  padding: 10px;
  border: 1px solid;
  border-radius: 5px;
  background: rgba(0, 0, 0, 0.2);
  text-align: center;
  font-weight: bold;
  animation: fadeIn 0.3s ease-out;
}

.calibration-table {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 10px;
  padding: 10px;
}

.cal-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.cal-row:last-child {
  border-bottom: none;
}

.cal-col {
  flex: 1;
  text-align: center;
}

.cal-col.pct {
  color: var(--secondary);
  font-weight: bold;
}

.cal-col.val {
  color: white;
}

.cal-col.ma {
  color: var(--primary);
  font-family: monospace;
}

.cal-col.arrow {
  color: var(--text-muted);
  font-size: 0.8em;
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

@keyframes pulse {
  0% { opacity: 0.5; }
  50% { opacity: 1; }
  100% { opacity: 0.5; }
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-5px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
