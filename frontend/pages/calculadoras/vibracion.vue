<template>
  <div class="calc-container">
    <NuxtLink to="/" class="back-link">← Volver al Inicio</NuxtLink>
    <h1 class="title">📉 Sonda de Vibración (API 670)</h1>
    <p class="subtitle">Conversión de Voltaje de GAP a Distancia (Mils/Micras)</p>

    <div class="cyber-card">
      
      <!-- Sensibilidad -->
      <div class="section-title">Configuración de Sonda</div>
      <div class="input-row">
        <div class="input-group">
          <label>
            Sensibilidad (mV/mil)
            <span @click="sensitivity = 200; calcFromVoltage()" class="reset-btn" title="Resetear a 200">↺</span>
          </label>
          <input v-model="sensitivity" type="number" placeholder="200" @input="calcFromVoltage">
        </div>
        <div class="input-group">
          <label>Unidad de Salida</label>
          <select v-model="unit">
            <option value="mils">Mils (milésimas de pulgada)</option>
            <option value="um">Micras (µm)</option>
          </select>
        </div>
      </div>

      <div class="divider"></div>

      <!-- Conversión Bidireccional -->
      <div class="section-title">Conversión en Tiempo Real</div>
      <div class="conversion-row">
        
        <!-- Entrada Voltaje -->
        <div class="input-group main-input">
          <label>Voltaje DC (V)</label>
          <input 
            v-model="voltage" 
            type="number" 
            step="0.1" 
            @input="calcFromVoltage"
            :class="{ active: lastEdited === 'voltage' }"
            placeholder="-10.0"
          >
        </div>

        <div class="arrow">⇄</div>

        <!-- Entrada GAP -->
        <div class="input-group main-input">
          <label>GAP ({{ unit }})</label>
          <input 
            v-model="gap" 
            type="number" 
            step="0.1" 
            @input="calcFromGap"
            :class="{ active: lastEdited === 'gap' }"
          >
        </div>

      </div>

      <!-- Visualización del GAP -->
      <div class="gap-visualizer">
        <div class="probe-tip"></div>
        <div class="gap-space" :style="{ height: visualGapHeight + 'px' }">
          <span class="gap-line"></span>
          <span class="gap-label">{{ gap || 0 }} {{ unit }}</span>
        </div>
        <div class="target-surface">SUPERFICIE (EJE)</div>
      </div>

      <!-- Mensaje de Diagnóstico -->
      <div v-if="diagnosticMessage" class="diagnostic-box" :style="{ borderColor: statusColor, color: statusColor }">
        {{ diagnosticMessage }}
      </div>

      <div class="divider"></div>

      <!-- Leyenda Técnica -->
      <div class="info-box">
        <h3>ℹ️ ¿Qué es esto?</h3>
        <p>
          Esta herramienta simula la curva de calibración de un sistema de <strong>Sonda de Proximidad</strong> (como Bently Nevada 3300 XL).
        </p>
        <ul>
          <li><strong>API 670:</strong> Estándar mundial para protección de maquinaria (Turbinas, Compresores).</li>
          <li><strong>TK3:</strong> Instrumento físico usado para verificar esta curva en campo.</li>
          <li><strong>Objetivo:</strong> Verificar que la sonda mida la distancia correcta (GAP) al eje basándose en el voltaje DC.</li>
        </ul>
      </div>

    </div>

    <!-- Botonera -->
    <div class="actions">
      <div class="save-group">
        <input v-model="etiqueta" placeholder="Etiqueta (Ej: VIB-201A)" class="tag-input">
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

const sensitivity = ref(200); // mV/mil standard
const unit = ref('mils');
const voltage = ref('');
const gap = ref('');
const etiqueta = ref('');
const lastEdited = ref('');

// Computed para visualización (max 100px height for visual scaling)
const visualGapHeight = computed(() => {
  const val = parseFloat(gap.value);
  if (isNaN(val)) return 5;
  // Escala visual: 1 mil = 1px (aprox), clamp entre 5 y 150
  let pixels = unit.value === 'mils' ? val * 1.5 : val * 0.06; 
  return Math.min(Math.max(pixels, 5), 150);
});

// Lógica de Diagnóstico (Rango Lineal Típico API 670: -2V a -18V)
const diagnosticMessage = computed(() => {
  const v = parseFloat(voltage.value);
  if (isNaN(v)) return '';

  // API 670 probes are usually negative voltage
  const absV = Math.abs(v); 
  
  if (absV < 2.0) return '⚠️ ALERTA: Zona Muerta / Roce (< 2V)';
  if (absV > 18.0) return '⚠️ ALERTA: Fuera de Rango Lineal (> 18V)';
  
  return '✅ Rango Lineal Óptimo';
});

const statusColor = computed(() => {
  const v = parseFloat(voltage.value);
  if (isNaN(v)) return 'var(--primary)';

  const absV = Math.abs(v);
  if (absV < 2.0 || absV > 18.0) return '#ffcc00'; // Warning Yellow
  return 'var(--accent-success)'; // Green
});

// Calcular GAP desde Voltaje
// Formula: Gap (mils) = (Voltage (V) * 1000) / Sensitivity (mV/mil)
// Nota: Usamos valor absoluto del voltaje porque la distancia es positiva
const calcFromVoltage = () => {
  lastEdited.value = 'voltage';
  const v = parseFloat(voltage.value);
  const sens = parseFloat(sensitivity.value);

  if (!isNaN(v) && !isNaN(sens) && sens !== 0) {
    const gapMils = (Math.abs(v) * 1000) / sens;
    
    if (unit.value === 'mils') {
      gap.value = gapMils.toFixed(2);
    } else {
      // Convert mils to microns (1 mil = 25.4 um)
      gap.value = (gapMils * 25.4).toFixed(1);
    }
  }
};

// Calcular Voltaje desde GAP
const calcFromGap = () => {
  lastEdited.value = 'gap';
  const g = parseFloat(gap.value);
  const sens = parseFloat(sensitivity.value);

  if (!isNaN(g) && !isNaN(sens)) {
    let gapMils = g;
    if (unit.value === 'um') {
      gapMils = g / 25.4;
    }

    // Voltage (V) = (Gap (mils) * Sensitivity) / 1000
    // Asumimos polaridad negativa por defecto (estándar API 670)
    const v = (gapMils * sens) / 1000;
    voltage.value = (-v).toFixed(2); // Mostramos negativo
  }
};

const puedeGuardar = computed(() => {
  return etiqueta.value && voltage.value && gap.value;
});

const guardar = async () => {
  try {
    const payload = {
      tipo: 'VIBRACION',
      etiqueta: etiqueta.value,
      datos_entrada: { 
        sensitivity: sensitivity.value, 
        unit: unit.value,
        input_type: lastEdited.value,
        input_value: lastEdited.value === 'voltage' ? voltage.value : gap.value
      },
      resultado: { 
        voltage: voltage.value, 
        gap: gap.value 
      }
    };
    await axios.post(`${apiBase}/api/history/`, payload);
    alert('¡Lectura guardada!');
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

.input-group input, .input-group select {
  width: 100%;
  padding: 10px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: white;
  border-radius: 5px;
  font-size: 1em;
}

.input-group input:focus, .input-group select:focus {
  border-color: var(--primary);
  box-shadow: 0 0 10px rgba(0, 242, 255, 0.2);
  outline: none;
}

/* Fix for Select Options visibility */
.input-group select option {
  background-color: var(--bg-card);
  color: white;
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

/* Visualizador de GAP */
.gap-visualizer {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 30px 0;
  background: rgba(0,0,0,0.3);
  padding: 40px 20px 20px 20px; /* More top padding for label */
  border-radius: 10px;
  border: 1px solid rgba(255,255,255,0.05);
  position: relative; /* For absolute positioning context if needed */
}

.probe-tip {
  width: 40px;
  height: 20px;
  background: #555;
  border-radius: 0 0 5px 5px;
  border: 1px solid #777;
  z-index: 2;
}

.gap-space {
  width: 2px;
  background: var(--primary);
  position: relative;
  transition: height 0.3s ease;
  box-shadow: 0 0 10px var(--primary);
}

.gap-line {
  position: absolute;
  top: 50%;
  left: -15px;
  width: 30px;
  height: 1px;
  background: rgba(255,255,255,0.5);
}

.gap-label {
  position: absolute;
  left: 25px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--primary);
  font-size: 0.9em;
  white-space: nowrap;
  background: rgba(0,0,0,0.7); /* Background for readability */
  padding: 2px 5px;
  border-radius: 3px;
}

.target-surface {
  width: 100px;
  height: 10px;
  background: linear-gradient(90deg, #333, #666, #333);
  border-radius: 2px;
  margin-top: 0;
  text-align: center;
  font-size: 0.6em;
  color: #aaa;
  line-height: 10px;
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

.reset-btn {
  cursor: pointer;
  color: var(--primary);
  margin-left: 5px;
  font-size: 1.1em;
  transition: transform 0.3s ease;
  display: inline-block;
}

.reset-btn:hover {
  transform: rotate(-180deg);
  color: white;
}

.info-box {
  background: rgba(255, 255, 255, 0.05);
  border-left: 3px solid var(--secondary);
  padding: 15px;
  margin-top: 20px;
  border-radius: 0 5px 5px 0;
  font-size: 0.9em;
  color: var(--text-muted);
}

.info-box h3 {
  color: var(--text-main);
  margin-top: 0;
  font-size: 1em;
  margin-bottom: 10px;
}

.info-box ul {
  padding-left: 20px;
  margin-bottom: 0;
}

.info-box li {
  margin-bottom: 5px;
}
</style>
