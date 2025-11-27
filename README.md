# 🏗️ Ingeniería 360

Plataforma integral de herramientas para ingeniería de instrumentación y control.

![Cyber Theme](https://img.shields.io/badge/Theme-Cyber_Dark-00f2ff)
![Stack](https://img.shields.io/badge/Stack-Nuxt_3_+_Django-green)

## 🚀 Características

### 📦 Inventario Inteligente
- **Gestión Total:** CRUD completo de equipos (Crear, Leer, Actualizar, Borrar).
- **Buscador en Tiempo Real:** Filtra por nombre, marca o modelo instantáneamente.
- **Especificaciones Dinámicas:** Agrega campos técnicos personalizados sin límites.
- **Modo Admin:** Protección de acciones críticas (Editar/Borrar) mediante contraseña local.

### 🧰 Herramientas de Cálculo
1.  **Transmisor 4-20mA:**
    - Conversión bidireccional (mA ↔ PV).
    - Diagnósticos de falla según estándar (NAMUR).
    - Tabla de calibración automática (0-100%).
2.  **Sondas de Vibración (API 670):**
    - Conversión Voltaje DC ↔ GAP (Mils/Micras).
    - Visualizador gráfico de distancia sonda-eje.
    - Curvas de sensibilidad ajustables.
3.  **Conversor Universal:**
    - Presión, Temperatura, Longitud y Peso.
    - Interfaz fluida con cálculo instantáneo.
4.  **Ley de Ohm:**
    - Calculadora interactiva con "Triángulo de Energía".

## 🛠️ Tecnologías

- **Frontend:** Nuxt 3 (Vue.js), CSS Variables (Cyber Theme).
- **Backend:** Django REST Framework.
- **Base de Datos:** MongoDB (vía PyMongo) + SQLite (Sistema Django).
- **Infraestructura:** Docker & Docker Compose.

## 🏁 Cómo Iniciar

1.  **Clonar el repositorio:**
    ```bash
    git clone <url-del-repo>
    ```
2.  **Iniciar contenedores:**
    ```bash
    docker-compose up --build
    ```
3.  **Acceder:**
    - Frontend: `http://localhost:3000`
    - Backend API: `http://localhost:8000`

---
*Desarrollado con ❤️ e Inteligencia Artificial.*
