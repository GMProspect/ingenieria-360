# Guía de Docker para "Ingeniería 360"

Como tu nueva carpeta está fuera de mi alcance, aquí tienes los archivos exactos que necesitas crear dentro de `ingenieria-360`.

## Estructura de Carpetas Recomendada
Primero, organiza tu carpeta así:
```text
ingenieria-360/
├── backend/         (Aquí irá Django)
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/        (Aquí irá Nuxt/Vue)
│   ├── Dockerfile
│   └── package.json
└── docker-compose.yml
```

---

## 1. El Archivo Maestro: `docker-compose.yml`
Crea este archivo en la raíz (`ingenieria-360/docker-compose.yml`). Este archivo conecta todo.

```yaml
version: '3.8'

services:
  # Base de Datos (MongoDB)
  mongo:
    image: mongo:latest
    container_name: ing360_mongo
    ports:
      - "27017:27017"
    volumes:
      - mongo_data:/data/db

  # Backend (Django)
  backend:
    build: ./backend
    container_name: ing360_backend
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - ./backend:/app
    ports:
      - "8000:8000"
    depends_on:
      - mongo
    environment:
      - MONGO_URI=mongodb://mongo:27017/ing360_db

  # Frontend (Nuxt/Vue)
  frontend:
    build: ./frontend
    container_name: ing360_frontend
    volumes:
      - ./frontend:/app
      - /app/node_modules
    ports:
      - "3000:3000"
    environment:
      - NUXT_HOST=0.0.0.0
      - NUXT_PORT=3000

volumes:
  mongo_data:
```

---

## 2. Dockerfile del Backend (Django)
Crea este archivo en `ingenieria-360/backend/Dockerfile`.

```dockerfile
# Usar Python ligero
FROM python:3.11-slim

# Evitar que Python genere archivos .pyc
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema (necesarias para algunos paquetes)
RUN apt-get update && apt-get install -y netcat-openbsd

# Instalar dependencias de Python
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copiar el proyecto
COPY . /app/
```

---

## 3. Dockerfile del Frontend (Nuxt)
Crea este archivo en `ingenieria-360/frontend/Dockerfile`.

```dockerfile
# Usar Node.js
FROM node:18-alpine

# Directorio de trabajo
WORKDIR /app

# Copiar archivos de dependencias
COPY package*.json ./

# Instalar dependencias
RUN npm install

# Copiar el resto del proyecto
COPY . .

# Exponer el puerto
EXPOSE 3000

# Comando para desarrollo
CMD ["npm", "run", "dev"]
```

---

## 4. Cómo Arrancar Todo
Una vez que tengas los archivos creados:

1.  Abre tu terminal en la carpeta `ingenieria-360`.
2.  Ejecuta:
    ```bash
    docker-compose up --build
    ```
3.  Docker descargará todo, instalará todo y levantará tu app.
    *   Frontend: `http://localhost:3000`
    *   Backend: `http://localhost:8000`
    *   Mongo: `localhost:27017`
